# AEGIS v1 evidence gallery

Nine unique images are published. The Nmap file is the original uploaded image, copied unchanged. Other images are reviewed copies from the local AEGIS screenshot collection and match the existing repository captures where available. Generic names, duplicate copies, and double extensions were consolidated.

## Evidence index

| Image | What is visible | Qualification |
|---|---|---|
| [02 — Kali Nmap](02-kali-nmap-dc01.png) | Command, DC01 address, host up, open 53/88/135/139/389/445, summary | Original full capture; repeated scans visible; no password value displayed |
| [03 — OPNsense ATTACK traffic](03-opnsense-attack-traffic.png) | Kali-source ATTACK In / LAN Out passes to DC01 | Some columns clipped; not a full firewall-rule export |
| [04 — OPNsense blocks](04-opnsense-firewall-blocks.png) | Default-deny/state-violation rows | General block logging, not proof of every ATTACK restriction |
| [05 — OPNsense WAN](05-opnsense-wan-traffic.png) | WAN traffic log rows | Separate egress context, not a specific endpoint test |
| [06 — Splunk detections](06-splunk-alerts-overview.png) | Encoded PowerShell and failed-logon detections enabled | Configuration, not triggered-alert evidence |
| [07 — Wazuh DC01](07-wazuh-dc01-telemetry.png) | Agent dc01-aegis, 1,573 hits, logon/logoff rows | General telemetry; historical rule 60122 is not shown |
| [08 — DC01 Security log](08-dc01-windows-security-events.png) | Populated Windows Security log; selected Event 4634 | Does not show the historical 4625 or 4688 exercise |
| [09 — Wazuh vulnerability events](09-wazuh-vulnerability-events.png) | DC01 vulnerability-related event rows | Not exploit or remediation evidence |
| [10 — Failed-logon configuration](10-splunk-failed-login-alert-config.png) | Five failures / host / 15 minutes, scheduled, results > 0 | No fired events at capture time; cron expression not expanded |

## Integrity and provenance

[SHA256SUMS.txt](SHA256SUMS.txt) records the exact published bytes. Verify with `python Scripts/check-repository.py` from the repository root. Files were copied without altering image contents. Checksums provide integrity checks, not independent validation of behavior.

The source captures are dated October 28, 2026 in their displayed clocks; preserve their native clocks/time zones rather than inferring a single shared incident timestamp. No fresh Suricata alert image was available, and the unsuccessful terminal-only recapture was not included as success evidence. The full [validation record](../Documentation/validation.md) explains historical results and evidence limits.

Images were visually reviewed for passwords, private keys and tokens before publication. The visible lab-private addresses, reserved test domain and administrative UI account names describe the training environment; no reusable credential values are displayed.
