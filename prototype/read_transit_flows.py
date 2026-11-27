"""Observe initial IPv4 TCP connection attempts at a Linux router interface."""

import argparse
from datetime import datetime, timezone
from ipaddress import IPv4Address
import json
import math
import socket
import struct
import sys
import time

from read_socket_flows import parse_service


def tcp_syn(header):
    if len(header) < 40 or header[0] >> 4 != 4 or header[9] != socket.IPPROTO_TCP:
        return None
    offset = (header[0] & 15) * 4
    fragment_offset = int.from_bytes(header[6:8], "big") & 0x1FFF
    if offset < 20 or len(header) < offset + 20 or fragment_offset:
        return None
    if header[offset + 13] & 0x12 != 0x02:
        return None
    destination_port, = struct.unpack_from("!H", header, offset + 2)
    return header[12:16], header[16:20], destination_port


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interface", required=True)
    parser.add_argument("--peer-address", type=IPv4Address, required=True)
    parser.add_argument("--destination-address", type=IPv4Address, required=True)
    parser.add_argument("--source", required=True, help="Peer label from the policy")
    parser.add_argument("--service", type=parse_service, action="append", required=True)
    parser.add_argument("--seconds", type=float, default=5)
    args = parser.parse_args()
    services = dict(args.service)
    if len(services) != len(args.service):
        parser.error("each service port must appear only once")
    if not math.isfinite(args.seconds) or args.seconds <= 0:
        parser.error("--seconds must be positive and finite")
    try:
        with socket.socket(socket.AF_PACKET, socket.SOCK_DGRAM, 0) as capture:
            capture.bind((args.interface, 0x0800))
            deadline = time.monotonic() + args.seconds
            print("Listening", file=sys.stderr, flush=True)
            while (remaining := deadline - time.monotonic()) > 0:
                capture.settimeout(remaining)
                try:
                    header, link = capture.recvfrom(80)
                except socket.timeout:
                    break
                connection = tcp_syn(header)
                if link[2] == socket.PACKET_OUTGOING or connection is None:
                    continue
                peer, destination, port = connection
                if peer != args.peer_address.packed or destination != args.destination_address.packed:
                    continue
                if port not in services:
                    continue
                print(json.dumps({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "source": args.source,
                    "destination": services[port],
                    # Initial SYN events do not measure transfer size.
                    "bytes": None,
                }), flush=True)
    except (AttributeError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
