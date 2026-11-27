# Neuromancer

Neuromancer is an EAE Madrid master's thesis (TFM) project for **active LAN protection in short-term rentals and small hotels**. It proposes a local gateway that separates guest Wi-Fi, entertainment devices, and critical equipment such as locks and thermostats. The gateway would block prohibited connections, flag unusual device activity using network metadata, and give staff a checkout report showing what needs attention before the next guest arrives.

The pilot will measure whether a suspicious media device can be contained while guest Wi-Fi and normal lock operation continue. Detection time, false alerts, and service continuity are the main measures. Compromised streaming devices are a documented use case. Dormant on-device AI is an emerging threat scenario for later testing.

The current prototype checks connection summaries and emits JSON events. It accepts synthetic records and can collect a snapshot of selected TCP connections on the Raspberry Pi. It can also flag routed connection attempts in an isolated Raspberry Pi lab. Physical LAN deployment, firewall enforcement, and turnover reporting are planned pilot work.

## Repository layout

| Path | Purpose |
| --- | --- |
| [`prototype/check_flows.py`](prototype/check_flows.py) | Python CLI and policy evaluation logic. |
| [`prototype/read_socket_flows.py`](prototype/read_socket_flows.py) | Linux collector for selected established IPv4 TCP sockets on the local machine. |
| [`prototype/read_transit_flows.py`](prototype/read_transit_flows.py) | Observes initial IPv4 TCP connections at a Linux router interface. |
| [`prototype/tests/test_transit_flows.py`](prototype/tests/test_transit_flows.py) | End-to-end test with a sender, router and service host in separate Linux network namespaces. |
| [`prototype/tests/test_socket_flows.py`](prototype/tests/test_socket_flows.py) | Linux smoke test using real loopback connections. |
| [`prototype/policy.json`](prototype/policy.json) | Allowed destinations by device and the large-transfer threshold. |
| [`prototype/sample-flows.jsonl`](prototype/sample-flows.jsonl) | Three synthetic connection records used for the smoke test. |
| [`apartment-kit-simulation.html`](apartment-kit-simulation.html) | Standalone browser demo of the proposed workflow. |
| [`scripts/build_overview_pdf.py`](scripts/build_overview_pdf.py) | Generates the thesis overview PDF using the floor plan in [`figures/`](figures/). |

## Test the detector

Run from the repository root on the Mac or Raspberry Pi. Python 3 is the only requirement for the detector.

```sh
python3 prototype/check_flows.py prototype/policy.json prototype/sample-flows.jsonl
```

The command should print **two JSON lines**, in fixture order:

| Fixture | Expected result |
| --- | --- |
| Ordinary connection to the approved media service | No event |
| Large transfer to the approved media service | `info` with reason `large_allowed_transfer` |
| Connection from the media device to the simulated lock | `alert` with reason `destination_not_allowed` |

To exercise the same policy with your own synthetic data, pass a different JSON Lines file as the second argument. Each line is a connection summary with `timestamp`, `source`, `destination`, and `bytes`. Device and destination labels must match the policy for the intended test.

To try the visual simulation, open `apartment-kit-simulation.html` in a browser and step through the incident to the quarantine prompt. The simulation illustrates the workflow independently of the Python checker.

## Test live detection on the Pi

From the repository root on the Pi, run the Linux smoke test. It uses the installed `ss` command from iproute2 and creates two temporary loopback connections. The test checks the byte counts and verifies that only the simulated lock produces an alert.

```sh
python3 -m unittest discover -s prototype/tests -v
```

For a manual test, run a benign client against test services you control on the Pi and keep the connections open while you take a snapshot. Replace the example addresses and ports below with the Pi's local IPv4 address, the test client's IPv4 address, and your two test service ports.

```sh
python3 prototype/read_socket_flows.py \
  --local-address 192.0.2.10 --peer-address 192.0.2.20 \
  --source media-device \
  --service 8080=approved-media-service --service 8081=test-lock |
  python3 prototype/check_flows.py prototype/policy.json -
```

The collector reads kernel socket metadata, including bytes received by the Pi. It takes a single snapshot, so it can miss connections that have already closed. Its coverage is limited to TCP connections terminating on the Pi at the specified ports. Observing traffic between other LAN devices will require a router log feed or a capture point with access to that traffic.

## Test traffic forwarded through the Pi

On the Pi, run the routed lab with Python 3 and iproute2. The test uses root to create three temporary network namespaces connected by virtual Ethernet. It enables forwarding inside the router namespace. The physical LAN interfaces and host routing remain outside the lab.

```sh
sudo python3 -B -m unittest discover -s prototype/tests -p test_transit_flows.py -v
```

The media endpoint connects to two listening test services across the router. Both return a reply. The collector sees both TCP connection attempts on the ingress interface, and the policy checker emits one alert for the simulated lock. This is a passive test. It checks IPv4 TCP SYN metadata on one interface. Transfer size is reported as unknown and records contain no packet payload. The test removes its virtual network after it finishes.

## Thesis materials

- [Project overview and implementation plan (PDF)](IoT-Security-Kit-Against-Sleeper-AI-Agents.pdf)
- [Cybersecurity evidence compendium](cybersecurity-evidence-compendium.md)
- [Editable project overview](iot-security-kit-ai-sleeper-agents-overview.md)
- [Apartment simulation](apartment-kit-simulation.html), which can be opened locally in a browser

To rebuild the PDF on macOS, install the dependencies in a virtual environment and run the generator from the repository root. The builder uses system Avenir and Charter fonts and the checked-in floor plan.

```sh
python3 -m venv .venv-pdf
.venv-pdf/bin/python -m pip install matplotlib fonttools pillow reportlab
.venv-pdf/bin/python scripts/build_overview_pdf.py
```
