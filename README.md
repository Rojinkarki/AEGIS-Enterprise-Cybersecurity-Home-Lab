# AEGIS Enterprise Cyber Range

AEGIS is a hands-on enterprise cybersecurity home lab designed to simulate a realistic corporate environment for learning Active Directory, security monitoring, detection engineering, incident response, and controlled adversary simulation.

## Current Lab Architecture

- Physical Kali Linux laptop — Red Team / Attack Simulation
- Windows 11 Home laptop — VirtualBox host
- DC01 — Windows Server Domain Controller
- WS01 — Windows 11 Enterprise domain workstation
- SOC01 — Ubuntu Server running Splunk SIEM
- OPNsense — planned firewall and network segmentation

## Planned Internal Network

Network: AEGIS-LAN  
Subnet: 10.50.0.0/24

| IP Address | Host | Role |
|---|---|---|
| 10.50.0.1 | OPNsense | Firewall / Gateway |
| 10.50.0.10 | DC01 | Active Directory / DNS |
| 10.50.0.20 | SOC01 | Splunk SIEM |
| 10.50.0.30 | WS01 | Windows Enterprise Workstation |

## Planned Domain

corp.aegis.test

## Project Goals

- Build and manage an Active Directory environment
- Configure enterprise users, groups, OUs, and Group Policy
- Deploy Windows security telemetry using Sysmon
- Centralize logs in Splunk
- Develop custom detection rules
- Map detections to MITRE ATT&CK
- Perform controlled attack simulations
- Investigate security incidents
- Identify detection gaps
- Harden systems and retest security controls
- Add firewall and IDS-based network monitoring

## Safety

All offensive security testing will be performed only against systems owned and intentionally configured as part of this isolated lab environment.

## Status

Project currently under active development.

