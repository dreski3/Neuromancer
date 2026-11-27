# Cybersecurity Evidence Compendium

**EAE Madrid TFM · Active LAN protection for hospitality and short-term rentals**

Research snapshot through **25 November 2026**. Each entry identifies what the source establishes and how it informs the proposed pilot.

## Documented incidents

### E01 · XCPE backdoor in Android set-top boxes

**2 November 2026 · Google Threat Intelligence · Incident investigation and disruption**

Google and its partners reported dismantling a backdoor that enrolled more than 1.3 million set-top boxes in a botnet. Google found the software preinstalled across several models and brands and assessed with high confidence that the Android equipment manufacturer Videostrong intentionally operated it. Affiliates used compromised devices for ad fraud, residential proxying and additional malware delivery.

**Thesis relevance.** A property can install compromised equipment during routine procurement. A device's first observed traffic may already contain malicious activity. This case supports approved inventories, controlled egress and separation of entertainment devices from critical equipment. The reported figure describes botnet enrollment across affected products. The study gives no hospitality-specific prevalence estimate.

[Primary source · Google Threat Intelligence, *Shutting the Door on the XCPE Botnet*](https://cloud.google.com/blog/topics/threat-intelligence/shutting-the-door-on-the-xcpe-botnet)

### E02 · CaptiveCrunch in hospitality Wi-Fi

**31 July 2026, updated 5 October 2026 · Microsoft Threat Intelligence · Incident investigation**

Microsoft observed manipulated network traffic on captive-portal networks worldwide, including in hospitality. The campaign redirected users toward phishing and malware. Microsoft observed a resurgence on 29 September and identified shared hospitality management services as a possible factor. The initial compromise vector remained under investigation in the report.

**Thesis relevance.** Include the guest Wi-Fi router, DNS settings, captive portal and remote management in the trust model. Check known-good configurations where management access permits it. A local configuration check offers partial coverage when an upstream provider is compromised.

[Primary source · Microsoft Threat Intelligence, *CaptiveCrunch*](https://www.microsoft.com/en-us/security/blog/2026/07/31/captivecrunch-midnight-blizzard-targets-travelers-worldwide-for-malware-delivery-and-credential-theft/)

### E03 · Residential proxies and IoT botnets

**12 and 19 March 2026 · FBI and US Department of Justice · Public advisory and disruption**

The FBI identified streaming devices and routers among the equipment used as residential proxies. In a separate announcement, the Department of Justice reported disrupting infrastructure used by Aisuru, KimWolf, JackSkid and Mossad. Court documents put the combined count for the four botnets at more than three million hijacked devices as of March, mostly IoT equipment.

**Thesis relevance.** Include unexplained outbound activity from entertainment devices, even when the devices remain functional and have limited inbound exposure. The figure applies to the four botnets collectively and should be cited separately from XCPE.

[Primary source · FBI residential proxy advisory](https://www.ic3.gov/PSA/2026/PSA260312), [Primary source · DOJ IoT botnet disruption](https://www.justice.gov/usao-ak/pr/authorities-disrupt-worlds-largest-iot-ddos-botnets-responsible-record-breaking-attacks)

## Experimental evidence

### E04 · Distributed AI inference on inexpensive TV boxes

**12 October 2026 · Anthropic Frontier Red Team · Controlled experiment**

The team ran distributed inference across 15 inexpensive Android TV boxes. In a separate simplified test with the initial compromise problem largely abstracted away, a more capable model completed end-to-end replication. The paper describes a scenario that warrants further research. These experiments do not establish the prevalence of dormant AI agents on commercial hospitality networks.

**Thesis relevance.** Use the sleeper-agent scenario to test whether the same segmentation and device policies work against emerging behavior. Treat transfer volume, power draw and nearby BLE activity as indirect observations. Compare the detector with and without optional telemetry against normal updates, streaming and commissioning.

[Primary source · Anthropic Frontier Red Team, *AI models may be capable of self-replicating without access to a datacenter*](https://www.anthropic.com/research/self-replicating-ai)

## Standards and product developments

### E05 · Encrypted hostnames and DNS

**March 2026 · IETF · RFC 9849, Standards Track**

TLS Encrypted Client Hello can conceal the requested hostname from passive observers when supported and negotiated. DNS over HTTPS separately encrypts DNS queries between the client and resolver. A passive monitor may therefore lack both query names and the hostname from the handshake.

**Thesis relevance.** Measure whether firewall events and device-level flow metadata remain useful with encrypted DNS and TLS. A large encrypted download establishes volume, direction and timing. Its contents remain unknown to the gateway.

[Primary source · IETF RFC 9849](https://datatracker.ietf.org/doc/html/rfc9849), [Primary source · IETF RFC 8484](https://datatracker.ietf.org/doc/html/rfc8484)

### E06 · Matter 1.6 and local discovery

**17 June 2026 · Connectivity Standards Alliance · Specification release**

Matter 1.6 added NFC commissioning as an alternative to BLE and introduced Joint Fabric for authorized co-administration. Matter over Thread also depends on IPv6 and service discovery through a Thread border router.

**Thesis relevance.** BLE observations provide partial commissioning coverage. Test permitted discovery and control explicitly when placing controllers and devices in different network zones.

[Primary source · CSA Matter 1.6 release](https://csa-iot.org/newsroom/matter-1-6-enables-more-intuitive-setup-multi-ecosystem-experiences-and-context-driven-control/), [Technical reference · Google Matter and Thread primer](https://developers.home.google.com/matter/primer/thread-and-ipv6)

### E07 · EU Cyber Resilience Act implementation

**11 September and 18 November 2026 · European Commission · Regulatory implementation**

Reporting obligations for in-scope manufacturers began on 11 September. For qualifying cases, the early warning is due within 24 hours of awareness and the full notification within 72 hours. The first supporting European standard was published on 18 November. The main CRA provisions apply from 11 December 2027. The implementing regulation describes Class II firewalls and intrusion detection or prevention systems. Classification turns on the product's core functionality.

**Thesis relevance.** Include conformity assessment in the commercialization risk register. Scope the gateway and any cloud components supporting its functions, and account for updates, software components, vulnerability intake and incident response. The classification of the proposed kit remains to be assessed against its final design.

[Primary source · Commission reporting guidance](https://digital-strategy.ec.europa.eu/en/policies/cra-reporting), [Primary source · Commission standards announcement](https://digital-strategy.ec.europa.eu/en/news/first-european-standard-published-support-cyber-resilience-act), [Primary source · CRA summary](https://digital-strategy.ec.europa.eu/en/policies/cra-summary), [Primary source · Implementing Regulation (EU) 2025/2392](https://eur-lex.europa.eu/eli/reg_impl/2025/2392/oj/eng)

### E08 · Existing active LAN protection products

**2026 documentation · Firewalla and Ubiquiti · Vendor-described capabilities**

Firewalla documents device flow visibility, segmentation, new-device quarantine and multi-site management. Ubiquiti documents distinct controls at the gateway, switch and access point. Its documentation illustrates why an inter-VLAN firewall provides only part of the coverage for peer traffic.

**Thesis relevance.** Benchmark the proposed kit against existing network controls. Evaluate the checkout-triggered audit and property staff workflow as candidate differentiators. The sources describe capabilities. Field performance and willingness to pay require pilot evidence.

[Primary source · Firewalla visibility](https://help.firewalla.com/hc/en-us/articles/360049374514-A-Secure-and-Better-Network-with-Firewalla-Part-1-Visibility), [Primary source · Firewalla network controls](https://help.firewalla.com/hc/en-us/articles/360050334233-A-Secure-and-Better-Network-with-Firewalla-Part-2-Control), [Primary source · Ubiquiti network and client isolation](https://help.ui.com/hc/en-us/articles/18965560820247-Implementing-Network-and-Client-Isolation-in-UniFi)
