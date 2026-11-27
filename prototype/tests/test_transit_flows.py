"""Exercise routed traffic inside isolated Linux network namespaces as root."""

from contextlib import ExitStack
import json
import os
from pathlib import Path
import select
import shutil
import subprocess
import sys
import unittest
from uuid import uuid4


PROTOTYPE = Path(__file__).resolve().parents[1]

SERVER = """
from contextlib import ExitStack
import socket

with ExitStack() as listeners:
    endpoints = []
    for port in (8080, 8081):
        server = listeners.enter_context(socket.socket())
        server.bind(("198.51.100.2", port))
        server.listen(1)
        server.settimeout(5)
        endpoints.append(server)
    print("Listening", flush=True)
    for server in endpoints:
        connection, _ = server.accept()
        with connection:
            connection.sendall(b"ok")
"""

CLIENT = """
import socket
for port in (8080, 8081):
    with socket.create_connection(("198.51.100.2", port), timeout=2) as connection:
        if connection.recv(2, socket.MSG_WAITALL) != b"ok":
            raise RuntimeError(f"missing reply from test service on port {port}")
"""


def ip(*args):
    subprocess.run(["ip", *args], check=True, timeout=5)


def launch(stack, command, **options):
    process = stack.enter_context(subprocess.Popen(command, text=True, **options))
    stack.callback(process.terminate)
    return process


@unittest.skipUnless(
    sys.platform.startswith("linux") and os.geteuid() == 0 and shutil.which("ip"),
    "requires root on Linux with iproute2",
)
class TransitFlowsTest(unittest.TestCase):
    def test_routed_connections(self):
        media, router, services = [f"nm-{uuid4().hex[:10]}" for _ in range(3)]
        with ExitStack() as lab:
            for namespace in (media, router, services):
                ip("netns", "add", namespace)
                lab.callback(ip, "netns", "delete", namespace)
            ip("-n", router, "link", "add", "media0", "type", "veth",
               "peer", "name", "eth0", "netns", media)
            ip("-n", router, "link", "add", "services0", "type", "veth",
               "peer", "name", "eth0", "netns", services)

            for namespace, interface, address in (
                (media, "eth0", "192.0.2.2/24"),
                (router, "media0", "192.0.2.1/24"),
                (router, "services0", "198.51.100.1/24"),
                (services, "eth0", "198.51.100.2/24"),
            ):
                ip("-n", namespace, "address", "add", address, "dev", interface)
                ip("-n", namespace, "link", "set", interface, "up")
            ip("-n", media, "route", "add", "198.51.100.0/24", "via", "192.0.2.1")
            ip("-n", services, "route", "add", "192.0.2.0/24", "via", "198.51.100.1")
            ip("netns", "exec", router, "sysctl", "-qw", "net.ipv4.ip_forward=1")

            server = launch(lab, ["ip", "netns", "exec", services, sys.executable,
                                  "-c", SERVER], stdout=subprocess.PIPE)
            self.assertTrue(select.select([server.stdout], [], [], 5)[0])
            self.assertEqual(server.stdout.readline().strip(), "Listening")
            reader = launch(lab, [
                "ip", "netns", "exec", router, sys.executable, "-B",
                str(PROTOTYPE / "read_transit_flows.py"),
                "--interface", "media0", "--peer-address", "192.0.2.2",
                "--destination-address", "198.51.100.2", "--source", "media-device",
                "--service", "8080=approved-media-service", "--service", "8081=test-lock",
                "--seconds", "3",
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertTrue(select.select([reader.stderr], [], [], 5)[0])
            self.assertEqual(reader.stderr.readline().strip(), "Listening")
            ip("netns", "exec", media, sys.executable, "-c", CLIENT)
            self.assertEqual(server.wait(timeout=5), 0)
            records, errors = reader.communicate(timeout=5)
            self.assertEqual(reader.returncode, 0, errors)

        self.assertEqual([json.loads(line)["destination"] for line in records.splitlines()],
                         ["approved-media-service", "test-lock"])
        alerts = subprocess.check_output([
            sys.executable, str(PROTOTYPE / "check_flows.py"),
            str(PROTOTYPE / "policy.json"), "-",
        ], input=records, text=True, timeout=5)
        alert = json.loads(alerts)
        self.assertEqual(alert["reason"], "destination_not_allowed")
        self.assertEqual(alert["destination"], "test-lock")
        self.assertIsNone(alert["bytes"])
