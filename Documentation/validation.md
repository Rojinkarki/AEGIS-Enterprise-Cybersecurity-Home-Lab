# AEGIS v1 validation record

AEGIS v1.0 is complete as a documented training build. This record separates retained visual evidence from historical validation in the build documentation and source conversation. The portfolio refresh did not access running lab systems.

## Retained evidence

| Capability | What the image demonstrates | Limit |
|---|---|---|
| Kali to DC01 | [Nmap](../Screenshots/02-kali-nmap-dc01.png): command, target, host up, six open ports, summary | Not AD health or a full service inventory |
| ATTACK routing | [Live View](../Screenshots/03-opnsense-attack-traffic.png): Kali source, DC01 target, ATTACK In / LAN Out, pass | Some port/label columns are clipped; no complete policy export |
| Block logging | [Default-deny rows](../Screenshots/04-opnsense-firewall-blocks.png) | General block/state-violation evidence, not a full segmentation test |
| WAN logging | [WAN rows](../Screenshots/05-opnsense-wan-traffic.png) | Firewall WAN activity, not a particular endpoint validation |
| Splunk configuration | [Overview](../Screenshots/06-splunk-alerts-overview.png): two enabled detections | Enabled state alone does not prove a trigger |
| Failed-logon threshold | [Configuration](../Screenshots/10-splunk-failed-login-alert-config.png): five failures on one host within 15 minutes; scheduled, results > 0 | Shows no fired events at capture time; exact cron is not expanded |
| Windows auditing | [DC01 Event Viewer](../Screenshots/08-dc01-windows-security-events.png): Security log, selected Event 4634 | Does not show historical 4625 or 4688 tests |
| Wazuh collection | [Threat Hunting](../Screenshots/07-wazuh-dc01-telemetry.png): `dc01-aegis`, 1,573 hits, logon/logoff | Does not show historical rule 60122 |
| Vulnerability telemetry | [DC01 event list](../Screenshots/09-wazuh-vulnerability-events.png) | Does not establish exploitability or remediation |

## Historical validation

- **Failed authentication:** IR-001 records six nonexistent usernames, DC01 Event 4625, Logon Type 3, NTLM, Kali attribution, a Splunk trigger, and Wazuh rule 60122. The original report date is October 9, 2026. Detailed trigger/event exports are not retained.
- **Encoded PowerShell:** the baseline records a harmless WS01 encoded command, Event 4688, and Splunk matching. The screenshots retain the enabled alert, not the process event or a fired-alert record.
- **Suricata:** the baseline records ET Open SID 2100498, `GPL ATTACK_RESPONSE id check returned root`, in IDS / alert-only mode. The latest conversation reports no results during recapture and then moves on. Its terminal image did not show the expected response body. No fresh successful alert is claimed.
- **Routing:** the baseline records successful reachability after host/VM restarts. Current screenshots demonstrate connectivity, not the reboot itself.
- **Snapshots:** five final snapshot names are recorded in [architecture.md](architecture.md). Snapshot listings and restore-test output are not retained here.

## Repeating checks

1. Start the relevant [VM profile](vm-resource-plan.md) and inspect the [routes](../Configs/network-routing.md).
2. From physical Kali, follow the [connectivity procedure](../Scripts/README.md).
3. Filter OPNsense Live View for source `192.168.12.172` and destination `10.50.0.10`; inspect ATTACK ingress and LAN egress.
4. For authentication triage, use the [Splunk searches and Wazuh guidance](../Detection-Rules/README.md) with the authorized exercise's time range. No password attempts are automated by this repository.
5. For IDS, follow the [Suricata procedure](../Detection-Rules/suricata-validation.md), retaining the response body and actual alert. A request alone is not a successful IDS test.

Preserve timestamps and display time zones in new evidence. Retained Kali, Windows, firewall, and SIEM captures use different clocks or display zones; no exact cross-platform incident timeline is inferred.

## Evidence handling

The [gallery](../Screenshots/README.md) captions every image. [SHA256SUMS.txt](../Screenshots/SHA256SUMS.txt) identifies published bytes; hashes check integrity, not independent proof of lab behavior. Images were visually reviewed for credentials. Raw logs, VM disks, appliance exports, passwords, and private keys are excluded.
