# IR-001 — Multiple failed Active Directory logons

| Field | Value |
|---|---|
| Status | Closed — authorized simulation |
| Classification | True positive — authorized security test |
| Triage severity | Medium (lab exercise) |
| Original report date | October 9, 2026 |
| Evidence/documentation refresh | October 28, 2026 |
| Source | Physical Kali, `192.168.12.172` |
| Target | DC01, `10.50.0.10`, `corp.aegis.test` |
| Sources examined in the recorded investigation | OPNsense, Windows Security, Splunk, Wazuh |

## Executive summary

A controlled SMB authentication exercise generated six failed domain logons against DC01 using deliberately nonexistent usernames. The recorded investigation correlated firewall traffic, Windows Event 4625, Splunk threshold detection, and Wazuh rule 60122 with the known Kali source. The activity was classified as a true positive from an authorized simulation and closed without containment.

## Scope and evidence provenance

The original report date and validation findings are retained from the completed build record. Exact per-event timestamps, raw logs and historical fired-alert exports are not available in this repository. The October 28 screenshots support network connectivity, configured detections, and general endpoint telemetry; they do not recreate the original incident timeline.

In particular, the current Splunk alert configuration image states that there are no fired events at capture time. This does not independently confirm the historical trigger reported below. See the [validation matrix](../Documentation/validation.md).

## Controlled activity

Test usernames were `CORP\AEGIS-FAIL1` through `CORP\AEGIS-FAIL6`. They were intentionally nonexistent to avoid testing real account credentials or causing legitimate account lockouts. No test password or reusable credential is published.

```text
Kali 192.168.12.172
 -> Windows 192.168.12.180 / 10.60.10.254
 -> OPNsense ATTACK 10.60.10.1
 -> OPNsense LAN 10.50.0.1
 -> DC01 10.50.0.10 (SMB authentication)
```

## Detection logic

Saved alert: `AEGIS - Multiple failed Login Attempts`.

The baseline [SPL](../Detection-Rules/splunk-failed-logins.spl) aggregates failed logons by receiving host:

```spl
index=* source="WinEventLog:Security" EventCode=4625
| stats count as Failed_Logins by host
| where Failed_Logins >= 5
```

Use a 15-minute search window, as described in the retained alert configuration. Trigger when the search returns more than zero results. The exact deployed cron expression is not visible in the screenshot.

The threshold is per host, not per source or account. Attribution requires opening underlying events; five unrelated users making errors on one host can also meet this condition. `index=*` is the exploratory lab baseline and should be narrowed to the actual Windows index in a larger deployment.

## Recorded findings

| Layer | Finding recorded in the original report |
|---|---|
| OPNsense | Kali traffic entered ATTACK and was forwarded toward AEGIS-LAN |
| Windows Security | Event 4625, Logon Type 3, account domain CORP, workstation KALI, source `192.168.12.172`, NTLM |
| Failure reason | Unknown username or bad password |
| Splunk | Six matching failed logons; threshold detection and scheduled alert reported triggered |
| Wazuh | Agent `dc01-aegis`, rule 60122: `Logon Failure - Unknown user or bad password` |

## Assessment and response

The source, target, test usernames and recorded timing matched the authorized exercise. Failed authentication alone does not demonstrate successful access, account compromise, or credential theft. The original investigation reported no production impact and no legitimate account lockout or compromise.

No containment was required for the known simulation. The analyst retained the case as a validation of routing, firewall logging, endpoint auditing, SIEM ingestion and detection. In an unplanned event, source ownership, successful logons, affected accounts, and adjacent activity would need investigation before closure.

## Published supporting evidence

- [Nmap reconnaissance](../Screenshots/02-kali-nmap-dc01.png): DC01 network exposure, not authentication failures.
- [OPNsense pass traffic](../Screenshots/03-opnsense-attack-traffic.png): source-preserving ATTACK/LAN path.
- [Splunk alert configuration](../Screenshots/10-splunk-failed-login-alert-config.png): enabled scheduled threshold; no fired events at capture time.
- [Wazuh DC01 telemetry](../Screenshots/07-wazuh-dc01-telemetry.png): collection and logon/logoff events, not the historical 60122 record.
- [Windows Security log](../Screenshots/08-dc01-windows-security-events.png): populated log with selected Event 4634, not a 4625 capture.

## Lessons learned

- Preserve source addresses across routed lab boundaries to correlate network and endpoint records.
- Pair aggregate alert results with raw account, source-IP, workstation and authentication fields.
- Retain the event time range and display time zone alongside screenshots.
- Separate enabled alert configuration from proof that an alert fired.
- Use nonexistent usernames for authorized failure simulations and keep credentials out of evidence.
