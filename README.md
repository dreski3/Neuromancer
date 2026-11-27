# Neuromancer

An EAE Madrid master's thesis prototype for active LAN protection in short-term rentals and small hotels. The project explores how a local gateway can identify policy violations involving property-owned devices and help staff check the network between guest stays.

## Run the first detector

From the repository root, using Python 3:

```sh
python3 prototype/check_flows.py prototype/policy.json prototype/sample-flows.jsonl
```

The three synthetic flow records should produce two events. The ordinary allowed connection is quiet, the large allowed transfer produces an informational event, and the attempt to reach the simulated lock produces an alert. The threshold is a fixture setting. This prototype reads connection summaries from a file. Live traffic collection and firewall enforcement are future pilot steps.

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
