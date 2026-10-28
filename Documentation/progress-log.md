# AEGIS v1 milestone log

**Current status: AEGIS v1.0 complete.** Future capabilities belong to v2. This log consolidates the recorded build; dates are used only where the retained record provides them.

## Completed milestones

| Milestone | Final recorded outcome |
|---|---|
| Network foundation | VirtualBox internal AEGIS-LAN, static addressing, `corp.aegis.test` |
| Identity | DC01: AD DS, DNS, Group Policy, Windows security auditing |
| Workstation | Domain-joined WS01, Sysmon and process telemetry |
| Splunk | SOC01 ingestion, failed-logon and encoded-PowerShell detections |
| Wazuh | Manager/indexer/dashboard, agents and DC01 telemetry |
| Perimeter | OPNsense WAN/LAN/ATTACK, scoped and logged Kali policy |
| IDS | Suricata alert-only with ET Open; prior SID 2100498 validation |
| Kali | Physical laptop routed through Windows and ATTACK; persistent routes |
| Exercises | Reconnaissance, failed SMB logons using nonexistent usernames, harmless encoded command |
| Investigation | IR-001 closed as an authorized security test |
| Recovery | Five final snapshots recorded; routing reported persistent after restart |

## Authentication simulation — original report date 2026-10-09

IR-001 records six failed logons from `192.168.12.172` against DC01, Event 4625 / Logon Type 3 / NTLM, a Splunk match and triggered alert, and Wazuh rule 60122. The original report date is retained as historical metadata; October 28 screenshots do not reconstruct the simulation's exact timestamps.

## Portfolio evidence refresh — 2026-10-28

- Recovered the original uploaded Nmap image unchanged as `02-kali-nmap-dc01.png`.
- Reviewed local and repository screenshots, consolidated duplicates, and replaced generic and double-extension filenames.
- Confirmed visually: six DC01 open ports; logged ATTACK/LAN passes; enabled Splunk detections; general DC01 Windows/Wazuh telemetry; Wazuh vulnerability events.
- Documented that the failed-logon alert screenshot shows no fired events at capture time. It demonstrates configuration, not the historical trigger.
- Retained the prior Suricata validation record. The latest recapture returned no matching alert and was skipped in the source conversation; no fresh IDS success is claimed.
- Added sanitized configuration references, detection explanations, scoped scripts, evidence checksums, and repository hygiene checks.
- Updated the resource plan to include the completed ATTACK network.

## Final recovery snapshots

| VM | Recorded snapshot |
|---|---|
| OPNsense-FW | `OPNsense-AEGIS-v1-Final` |
| DC01 | `DC01-AEGIS-v1-Final` |
| WS01 | `WS01-AEGIS-v1-Final` |
| SOC01 | `SOC01-AEGIS-v1-Final` |
| WAZUH01 | `WAZUH01-AEGIS-v1-Final` |

Names and reboot validation come from the completed build baseline. Snapshot inventory and restores were not repeated during this refresh. Snapshot files and disks are excluded from Git.

## Releases

- `v1.0.0`: existing original v1 milestone tag, retained unchanged.
- `v1.0.1`: documentation, evidence, and reusable artifact refresh; no infrastructure change.

See [validation.md](validation.md) and [release-notes.md](release-notes.md).
