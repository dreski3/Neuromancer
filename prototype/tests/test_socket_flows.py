"""Smoke test the detector against real TCP sockets on Linux."""

from contextlib import ExitStack
import json
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import unittest


PROTOTYPE = Path(__file__).resolve().parents[1]


@unittest.skipUnless(sys.platform.startswith("linux") and shutil.which("ss"),
                     "requires Linux with iproute2 ss")
class SocketFlowsTest(unittest.TestCase):
    def test_live_connections(self):
        address = "127.0.0.1"
        with ExitStack() as sockets:
            def connect(payload):
                listener = sockets.enter_context(socket.socket())
                listener.bind((address, 0))
                listener.listen(1)
                client = sockets.enter_context(socket.create_connection(listener.getsockname()))
                server, _ = listener.accept()
                sockets.enter_context(server)
                client.sendall(payload)
                self.assertEqual(server.recv(len(payload), socket.MSG_WAITALL), payload)
                return listener.getsockname()[1]

            allowed_port = connect(b"hello")
            restricted_port = connect(b"test")
            flows = subprocess.check_output([
                sys.executable, str(PROTOTYPE / "read_socket_flows.py"),
                "--local-address", address, "--peer-address", address,
                "--source", "media-device",
                "--service", f"{allowed_port}=approved-media-service",
                "--service", f"{restricted_port}=test-lock",
            ], text=True, timeout=10)

        records = {flow["destination"]: flow["bytes"]
                   for flow in map(json.loads, flows.splitlines())}
        self.assertEqual(records, {"approved-media-service": 5, "test-lock": 4})

        events = subprocess.check_output([
            sys.executable, str(PROTOTYPE / "check_flows.py"),
            str(PROTOTYPE / "policy.json"), "-",
        ], input=flows, text=True, timeout=10)
        alert = json.loads(events)
        self.assertEqual(alert["severity"], "alert")
        self.assertEqual(alert["destination"], "test-lock")
        self.assertEqual(alert["reason"], "destination_not_allowed")
