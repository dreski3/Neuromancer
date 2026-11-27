# Neuromancer

Neuromancer is an EAE Madrid master's thesis (TFM) project for **active LAN protection in short-term rentals and small hotels**. It proposes a local gateway that separates guest Wi-Fi, entertainment devices, and critical equipment such as locks and thermostats. The gateway would block prohibited connections, flag unusual device activity using network metadata, and give staff a checkout report showing what needs attention before the next guest arrives.

The pilot will measure whether a suspicious media device can be contained while guest Wi-Fi and normal lock operation continue. Detection time, false alerts, and service continuity are the main measures. Compromised streaming devices are a documented use case. Dormant on-device AI is an emerging threat scenario for later testing.

The current prototype is an offline policy checker. It reads synthetic connection summaries and emits JSON events. Live traffic collection, firewall enforcement, and turnover reporting are planned pilot work.

## Repository layout

| Path | Purpose |
| --- | --- |
| [`prototype/check_flows.py`](prototype/check_flows.py) | Python CLI and policy evaluation logic. |
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
