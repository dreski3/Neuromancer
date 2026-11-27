"""Evaluate synthetic connection summaries for a managed media device."""

import argparse
import json
from pathlib import Path


def evaluate(flow, policy):
    source = flow["source"]
    allowed = policy["allowed_destinations"].get(source)
    if allowed is None:
        return None

    destination = flow["destination"]
    if destination not in allowed:
        severity, reason = "alert", "destination_not_allowed"
    elif flow["bytes"] >= policy["large_transfer_bytes"]:
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
    parser.add_argument("flows", type=Path, help="Connection summaries in JSON Lines format")
    args = parser.parse_args()

    try:
        policy = json.loads(args.policy.read_text(encoding="utf-8"))
        with args.flows.open(encoding="utf-8") as flows:
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
