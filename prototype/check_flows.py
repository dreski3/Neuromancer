"""Evaluate connection summaries for managed devices."""

import argparse
from contextlib import nullcontext
import json
from pathlib import Path
import sys


def evaluate(flow, policy):
    source = flow["source"]
    allowed = policy["allowed_destinations"].get(source)
    if allowed is None:
        return None

    destination = flow["destination"]
    if destination not in allowed:
        severity, reason = "alert", "destination_not_allowed"
    elif flow["bytes"] is not None and flow["bytes"] >= policy["large_transfer_bytes"]:
        severity, reason = "info", "large_allowed_transfer"
    else:
        return None

    return {
        "timestamp": flow["timestamp"],
        "source": source,
        "destination": destination,
        "bytes": flow["bytes"],
        "severity": severity,
        "reason": reason,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    parser.add_argument("flows", help="JSON Lines connection summaries, or - for standard input")
    args = parser.parse_args()

    try:
        policy = json.loads(args.policy.read_text(encoding="utf-8"))
        input_stream = nullcontext(sys.stdin) if args.flows == "-" else Path(args.flows).open(encoding="utf-8")
        with input_stream as flows:
            for number, line in enumerate(flows, 1):
                if not line.strip():
                    continue
                try:
                    event = evaluate(json.loads(line), policy)
                except (ValueError, KeyError, TypeError, AttributeError) as error:
                    parser.error(f"{args.flows}:{number}: {error}")
                if event is not None:
                    print(json.dumps(event))
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
