# AEGIS Incident Report IR-001

## Incident Title

Multiple Failed Active Directory Login Attempts from Physical Kali

## Severity

Medium

## Detection Sources

- Splunk Enterprise
- Wazuh
- Windows Security Log
- OPNsense firewall logging

## Detection Rule

`AEGIS - Multiple failed Login Attempts`

## Validation Date

October 9, 2026

## Affected System

- DC01 - `10.50.0.10`

## Source System

- Physical Kali Linux laptop - `192.168.12.172`

## Test Accounts

- `CORP\AEGIS-FAIL1`
- `CORP\AEGIS-FAIL2`
- `CORP\AEGIS-FAIL3`
- `CORP\AEGIS-FAIL4`
- `CORP\AEGIS-FAIL5`
- `CORP\AEGIS-FAIL6`

These usernames were intentionally nonexistent so no legitimate domain account could be locked out.

## Detection Logic

The Splunk alert detects five or more Windows failed logon events (`Event ID 4625`) within the configured detection window.

Validated SPL:

```spl
index=* source="WinEventLog:Security" EventCode=4625
| stats count as Failed_Logins by host
| where Failed_Logins >= 5
```

## Relevant Windows Event

Event ID:

`4625`

Observed fields:

- Logon Type: `3`
- Account Domain: `CORP`
- Workstation Name: `KALI`
- Source Network Address: `192.168.12.172`
- Authentication Package: `NTLM`
- Failure Reason: unknown username or bad password

## Observed Activity

Physical Kali generated controlled SMB authentication failures against DC01.

Traffic path:

```text
Physical Kali
192.168.12.172
      |
      v
Windows Host
192.168.12.180 / 10.60.10.254
      |
      v
OPNsense ATTACK
10.60.10.1
      |
      v
DC01
10.50.0.10
```

OPNsense Live View confirmed the Kali source entering on the ATTACK interface and being forwarded toward AEGIS-LAN.

DC01 generated Windows Security Event ID `4625`.

## Splunk Validation

Splunk ingested the DC01 Security events.

A validation search identified six matching failed logons from source IP:

`192.168.12.172`

The scheduled alert:

`AEGIS - Multiple failed Login Attempts`

successfully triggered.

## Wazuh Validation

Wazuh displayed matching failed-logon events for agent:

`dc01-aegis`

Rule ID:

`60122`

Description:

`Logon Failure - Unknown user or bad password`

## Investigation

The activity was correlated across:

- OPNsense firewall logs
- DC01 Windows Security events
- Splunk
- Wazuh

The source IP, timing, target, and test usernames matched the authorized AEGIS simulation.

## Classification

`True Positive - Authorized Security Test`

## Impact

No production impact.

No legitimate account was locked or compromised.

No unauthorized system was targeted.

## Response

No containment was required because the activity was intentionally generated inside the isolated AEGIS cyber range.

The event was retained as evidence that these controls were operating correctly:

- network routing
- firewall logging
- Windows authentication auditing
- Splunk ingestion
- Splunk threshold detection
- Wazuh endpoint detection

## Lessons Learned

- Windows Event ID `4625` provides useful authentication-failure telemetry.
- Source IP and workstation fields are critical for attribution.
- Threshold-based detections reduce noise from isolated mistakes.
- SIEM detections should be tested using controlled, repeatable simulations.
- Correlating network, endpoint, and SIEM evidence provides stronger confidence than relying on a single source.
- Nonexistent test usernames prevent accidental account lockouts during authentication testing.

## Status

`Closed - Authorized Simulation`