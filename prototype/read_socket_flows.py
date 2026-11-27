"""Read connection summaries from selected established IPv4 sockets on Linux."""

import argparse
from datetime import datetime, timezone
from ipaddress import IPv4Address
import json
import re
import subprocess


def parse_service(value):
    port, separator, label = value.partition("=")
    if not separator or not port.isascii() or not port.isdecimal() or not label.strip():
        raise argparse.ArgumentTypeError("service must be PORT=LABEL")
    port = int(port)
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("service port must be between 1 and 65535")
    return port, label


def read_flows(local_address, peer_address, source, services):
    ports = " or ".join(f"sport = :{port}" for port in services)
    scope = f"src {local_address} and dst {peer_address} and ( {ports} )"
    result = subprocess.run(
        ["ss", "-4HntiO", scope],
        check=True,
        capture_output=True,
        text=True,
        timeout=5,
    )
    timestamp = datetime.now(timezone.utc).isoformat()
    for line in result.stdout.splitlines():
        fields = line.split(maxsplit=5)
        if not fields or fields[0] != "ESTAB":
            continue
        if len(fields) < 5:
            raise ValueError("unexpected established socket output from ss")
        local_port = int(fields[3].rsplit(":", 1)[1])
        stats = fields[5] if len(fields) == 6 else ""
        received = re.search(r"\bbytes_received:(\d+)\b", stats)
        yield {
            "timestamp": timestamp,
            "source": source,
            "destination": services[local_port],
            "bytes": int(received.group(1)) if received else 0,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-address", type=IPv4Address, required=True)
    parser.add_argument("--peer-address", type=IPv4Address, required=True)
    parser.add_argument("--source", required=True, help="Peer device label from the policy")
    parser.add_argument("--service", type=parse_service, action="append", required=True,
                        help="Local test service as PORT=LABEL (repeat for multiple services)")
    args = parser.parse_args()
    services = dict(args.service)
    if len(services) != len(args.service):
        parser.error("each service port must appear only once")
    try:
        for flow in read_flows(args.local_address, args.peer_address, args.source, services):
            print(json.dumps(flow))
    except subprocess.CalledProcessError as error:
        parser.error(f"ss failed: {error.stderr.strip()}")
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
