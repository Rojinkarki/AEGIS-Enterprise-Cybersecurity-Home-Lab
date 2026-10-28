# AEGIS Cyber Range - Build Progress

## Project Status

AEGIS is an isolated enterprise cybersecurity home lab for hands-on practice in Active Directory, enterprise networking, SIEM monitoring, detection engineering, endpoint telemetry, network IDS, incident response, and controlled adversary simulation.

**Current milestone: Core AEGIS v1 build complete and validated end-to-end.**

---

# Core Infrastructure

## DC01

- Windows Server 2025 Standard Evaluation
- IPv4: `10.50.0.10`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`
- Domain: `corp.aegis.test`
- Roles: AD DS, DNS, Group Policy

Validated:

- Active Directory health
- DNS resolution
- SYSVOL / NETLOGON
- Domain authentication
- Internet routing through OPNsense

## WS01

- Windows 11 Enterprise Evaluation
- IPv4: `10.50.0.30`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`
- Domain joined
- Sysmon installed
- Splunk Universal Forwarder installed
- Wazuh Agent installed

## SOC01

- Ubuntu Server 24.04 LTS
- IPv4: `10.50.0.20`
- Splunk Enterprise `10.4.2`
- Receiver: TCP `9997`
- Receives telemetry from DC01 and WS01

## WAZUH01

- Ubuntu Server 24.04 LTS
- IPv4: `10.50.0.40`
- Wazuh `4.14.7`
- Agents: `dc01-aegis`, `ws01-aegis`

## OPNsense

- Version: `26.7.3_11`
- WAN: VirtualBox NAT
- LAN: `10.50.0.1/24`
- ATTACK: `10.60.10.1/24`
- Suricata IDS enabled
- ET Open rules installed

---

# Physical Kali Red Team Integration

**Status: Complete**

Physical Kali:

`192.168.12.172/24`

Validated path:

```text
Physical Kali
192.168.12.172
      |
      | Home Wi-Fi
      v
Windows Host Wi-Fi
192.168.12.180
      |
      | Persistent IPv4 forwarding
      v
Windows VirtualBox Host-Only
10.60.10.254/24
      |
      v
OPNsense ATTACK
10.60.10.1/24
      |
      | Scoped + logged firewall rule
      v
AEGIS-LAN
10.50.0.0/24
```

Persistent routing:

- Kali: `10.50.0.0/24` via `192.168.12.180`
- Windows: `10.50.0.0/24` via `10.60.10.1`
- OPNsense: `192.168.12.172/32` via `10.60.10.254`
- Windows IPv4 forwarding enabled persistently on Wi-Fi and Host-Only adapter

OPNsense ATTACK policy:

```text
Source      â†’ KALI_ATTACKER
Destination â†’ AEGIS_TARGETS
Action      â†’ Pass
Logging     â†’ Enabled
```

The old WireGuard integration was disabled after confirming the routed physical-Kali path remained reachable.

---

# Detection Validation

## Suricata

Validated signature:

`SID 2100498`

`GPL ATTACK_RESPONSE id check returned root`

Result:

Suricata successfully inspected traffic and generated an IDS alert.

## Splunk - Multiple Failed Login Attempts

Detection:

`AEGIS - Multiple failed Login Attempts`

Windows Event ID:

`4625`

Controlled SMB authentication failures were generated from physical Kali against DC01 using nonexistent usernames:

- `AEGIS-FAIL1`
- `AEGIS-FAIL2`
- `AEGIS-FAIL3`
- `AEGIS-FAIL4`
- `AEGIS-FAIL5`
- `AEGIS-FAIL6`

DC01 recorded:

- Logon Type `3`
- Account Domain `CORP`
- Workstation `KALI`
- Source Network Address `192.168.12.172`
- NTLM failures

Splunk correlated six matching failures and the scheduled alert triggered successfully.

## Wazuh - Failed Login

Wazuh detected the same activity on:

`dc01-aegis`

Rule ID:

`60122`

Description:

`Logon Failure - Unknown user or bad password`

## Splunk - Encoded PowerShell

Detection:

`AEGIS - Encoded PowerShell Execution`

Validated Windows Event ID:

`4688`

Validated search:

```spl
index=* host=WS01 source="WinEventLog:Security" EventCode=4688
| where match(lower(_raw), "(-encodedcommand|-enc)")
| table _time host EventCode Account_Name _raw
```

A harmless Base64-encoded PowerShell command was executed on WS01.

The original Sysmon-only alert query was corrected to use Windows Security Event ID `4688`, and a fresh alert trigger was successfully generated.

---

# Controlled Red Team Validation

Validated actions:

- Kali â†’ DC01 ICMP reachability
- Nmap SYN reconnaissance against DC01
- OPNsense ATTACK ingress logging
- OPNsense LAN egress logging
- Controlled SMB authentication failures
- Windows Event ID `4625`
- Splunk failed-login alert
- Wazuh Rule `60122`
- Encoded PowerShell on WS01
- Windows Event ID `4688`
- Splunk encoded-PowerShell alert

End-to-end defensive lifecycle demonstrated:

```text
Attack
  |
  v
Telemetry
  |
  v
Detection
  |
  v
Alert
  |
  v
Investigation
  |
  v
Response
```

---

# Incident Response

**Status: Complete**

Primary report:

`Incident-Reports/IR-001-Multiple-Failed-Logins.md`

Classification:

`True Positive - Authorized Security Test`

Status:

`Closed - Authorized Simulation`

---

# Recovery Points

Existing snapshots include:

## DC01
- `DC01-Baseline-AD-Healthy`
- `DC01-AD-Structure-Complete`
- `DC01-GPO-Security-Baseline`
- `DC01-Splunk-Forwarder-Integrated`

## WS01
- `WS01-Splunk-Sysmon-Integrated`

## SOC01
- `SOC01-Splunk-Detection-Engine-Operational`

## WAZUH01
- `WAZUH01-Baseline-Ubuntu-Healthy`
- `WAZUH01-Agents-and-AD-Detection-Operational`
- `WAZUH01-OPNsense-Routing-Integrated`

## OPNsense
- `OPNsense-Baseline-WAN-LAN-Healthy`
- `OPNsense-Suricata-IDS-Operational`

Final validated snapshots should be added after the final Git commit.

---

# Overall Status

AEGIS v1 now contains operational:

- Active Directory
- DNS
- Group Policy
- Windows enterprise endpoint
- Sysmon
- Splunk SIEM
- Splunk detections
- Wazuh SIEM/XDR
- Wazuh agents
- OPNsense firewall
- Persistent physical-Kali routing
- Scoped ATTACK firewall policy
- Suricata IDS
- Incident response documentation
- Controlled Red Team validation

**Current project stage: Core AEGIS v1 build complete.**