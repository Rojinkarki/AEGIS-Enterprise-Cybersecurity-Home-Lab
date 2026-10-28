# AEGIS Cyber Range - Build Progress

## Project Status

**AEGIS v1.0 is complete and validated end-to-end.**

## Major Milestones

1. Network design and VirtualBox isolation
2. Windows Server 2025 deployment
3. Active Directory, DNS, and Group Policy
4. Windows 11 enterprise workstation
5. Sysmon telemetry
6. Splunk Enterprise and detections
7. Wazuh SIEM/XDR
8. OPNsense routing and segmentation
9. Suricata IDS
10. Physical Kali integration
11. Controlled reconnaissance and authentication testing
12. Detection validation
13. Incident response documentation
14. Final recovery snapshots
15. GitHub evidence and release preparation

## Final Detection Validation

### Failed Authentication
- Source: Physical Kali
- Target: DC01
- Windows Event ID: `4625`
- Splunk detection configured and validated
- Wazuh telemetry validated

### Encoded PowerShell
- Target: WS01
- Windows Event ID: `4688`
- Splunk encoded-command detection configured and validated

### Network IDS
- Suricata in IDS / alert-only mode
- ET Open rules installed
- SID `2100498` previously validated

## Final Evidence

- `Screenshots/01-kali-nmap-dc01.png`
- `Screenshots/02-opnsense-kali-traffic.png`
- `Screenshots/03-splunk-alerts.png`
- `Screenshots/04-wazuh-dc01-telemetry.png`

## Final Recovery Snapshots

- `OPNsense-AEGIS-v1-Final`
- `DC01-AEGIS-v1-Final`
- `WS01-AEGIS-v1-Final`
- `SOC01-AEGIS-v1-Final`
- `WAZUH01-AEGIS-v1-Final`

**Current project stage: AEGIS v1.0 complete.**
