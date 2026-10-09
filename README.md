# AEGIS Enterprise Cybersecurity Home Lab

AEGIS is a hands-on enterprise cybersecurity home lab designed to simulate a small corporate environment for learning and practicing:

- Active Directory administration
- Windows security monitoring
- Network security
- SIEM operations
- Detection engineering
- Endpoint telemetry
- Firewall management
- Intrusion detection
- Incident response
- Controlled adversary simulation

The environment is built using Oracle VirtualBox and intentionally designed so offensive-security testing is performed only against systems owned and configured specifically for the lab.

---

# Lab Architecture

## Virtual Machines

| System | Operating System | Role | IP Address |
|---|---|---|---|
| OPNsense-FW | OPNsense 26.7.3_11 | Firewall / Gateway / Suricata IDS | `10.50.0.1` |
| DC01 | Windows Server 2025 | Active Directory / DNS / Group Policy | `10.50.0.10` |
| SOC01 | Ubuntu Server 24.04 LTS | Splunk Enterprise SIEM | `10.50.0.20` |
| WS01 | Windows 11 Enterprise | Domain Workstation / Sysmon Endpoint | `10.50.0.30` |
| WAZUH01 | Ubuntu Server 24.04 LTS | Wazuh SIEM / XDR | `10.50.0.40` |

## Physical Systems

### Virtualization Host

- Windows 11 Home
- AMD Ryzen 7 8845HS
- 32 GB RAM
- NVIDIA RTX 4060
- Oracle VirtualBox

### Red Team System

- Dedicated physical Kali Linux laptop
- Used only for controlled attack simulation against AEGIS systems
- Physical Kali integration through the Windows virtualization host and OPNsense ATTACK interface is operational and validated

---

# Network Design

Internal VirtualBox network:

`AEGIS-LAN`

Subnet:

`10.50.0.0/24`

Default gateway:

`10.50.0.1`

Internal DNS:

`10.50.0.10`

Active Directory domain:

`corp.aegis.test`

## Current Routing Architecture

```text
Physical Kali
192.168.12.172
      |
      | Home Wi-Fi
      v
Windows Virtualization Host
Wi-Fi: 192.168.12.180
      |
      | Persistent IPv4 forwarding
      v
VirtualBox Host-Only Adapter
10.60.10.254/24
      |
      v
OPNsense ATTACK
10.60.10.1/24
      |
      | Scoped + logged firewall access
      v
OPNsense LAN
10.50.0.1/24
      |
      v
AEGIS-LAN
10.50.0.0/24
      |
      +--> DC01    10.50.0.10
      +--> SOC01   10.50.0.20
      +--> WS01    10.50.0.30
      +--> WAZUH01 10.50.0.40
```

Persistent routing now includes:

- Kali: `10.50.0.0/24` via Windows host `192.168.12.180`
- Windows: `10.50.0.0/24` via OPNsense ATTACK `10.60.10.1`
- OPNsense: `192.168.12.172/32` via Windows Host-Only `10.60.10.254`
- Windows IPv4 forwarding enabled persistently on Wi-Fi and the VirtualBox Host-Only interface

All permanent AEGIS systems route through OPNsense.

Temporary VirtualBox NAT adapters used during installation were removed so internal systems cannot bypass the firewall.

---
# Active Directory Environment

DC01 runs:

- Active Directory Domain Services
- DNS
- Group Policy Management

Domain:

`corp.aegis.test`

NetBIOS domain:

`CORP`

## Organizational Unit Structure

```text
AEGIS-CORP
|
+-- Users
|   |
|   +-- IT
|   +-- Engineering
|   +-- Finance
|   +-- HR
|
+-- Workstations
+-- Servers
+-- Service Accounts
+-- Groups
+-- Privileged Accounts
```

## Security Groups

Created department groups:

- `GG-IT-Users`
- `GG-Engineering-Users`
- `GG-Finance-Users`
- `GG-HR-Users`

## Sample Enterprise Users

- Alex Carter
- Maya Patel
- Daniel Brooks
- Sophia Reed

A dedicated privileged administrative account was also created for lab administration.

---

# Group Policy Security Baseline

A workstation security baseline was created:

`AEGIS-Workstation-Security-Baseline`

Linked to:

`AEGIS-CORP\Workstations`

Configured telemetry and security policies include:

- Process Creation auditing
- Command-line process logging
- Successful logon auditing
- Failed logon auditing
- Special Logon auditing
- User Account Management auditing
- Security Group Management auditing
- Audit Policy Change monitoring
- PowerShell Script Block Logging
- PowerShell Module Logging
- Advanced Audit Policy enforcement

The policy was successfully applied and verified on WS01.

---

# Windows Workstation

## WS01

Operating System:

Windows 11 Enterprise Evaluation

Configuration:

- Hostname: `WS01`
- IPv4: `10.50.0.30`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`
- Domain: `corp.aegis.test`

WS01 is located inside:

`AEGIS-CORP\Workstations`

Installed monitoring components include:

- Sysmon
- Splunk Universal Forwarder
- Wazuh Agent

---

# Sysmon Endpoint Telemetry

Sysmon is deployed on WS01 to provide enhanced Windows endpoint visibility.

Telemetry collected includes:

- Process creation
- Command-line execution
- Network connections
- File creation
- DNS queries
- SHA256 process hashes

Sysmon Operational events are forwarded to Splunk for search, detection engineering, and investigation.

---

# Splunk SIEM

SOC01 runs Splunk Enterprise.

Configuration:

- Hostname: `soc01`
- IPv4: `10.50.0.20`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`

Splunk Universal Forwarders are installed on:

- DC01
- WS01

Telemetry ingested includes:

- Windows Security logs
- Windows System logs
- Windows Application logs
- Active Directory security events
- Sysmon Operational logs

---

# Splunk Detection Engineering

## Detection 1 - Multiple Failed Login Attempts

Detection name:

`AEGIS - Multiple Failed Login Attempts`

Primary Windows Event ID:

`4625`

Detection logic:

```spl
index=* source="WinEventLog:Security" EventCode=4625
| stats count as Failed_Logins by host
| where Failed_Logins >= 5
```

The detection identifies hosts generating five or more failed authentication events during the configured detection window.

A controlled authentication simulation successfully triggered the alert.

### Test Scenario

Controlled SMB authentication failures were generated from the dedicated physical Kali Linux laptop against DC01.

Attack source:

`192.168.12.172`

Nonexistent test accounts `AEGIS-FAIL1` through `AEGIS-FAIL6` were used so no legitimate domain account could be locked out.

DC01 recorded:

- Windows Event ID `4625`
- Logon Type `3`
- Account Domain `CORP`
- Workstation `KALI`
- Source Network Address `192.168.12.172`
- NTLM authentication failures

Splunk ingested the Security events from DC01 and correlated six failed logons from the Kali source.

The saved alert:

`AEGIS - Multiple failed Login Attempts`

successfully triggered.

---
# Detection 2 - Encoded PowerShell Execution

The validated detection uses Windows Security Process Creation auditing.

Primary Windows Event ID:

`4688`

Validated Splunk search:

```spl
index=* host=WS01 source="WinEventLog:Security" EventCode=4688
| where match(lower(_raw), "(-encodedcommand|-enc)")
| table _time host EventCode Account_Name _raw
```

A harmless Base64-encoded PowerShell command was executed on WS01.

Test marker:

`AEGIS_ENCODED_TEST_2`

Splunk ingested the Event ID `4688` process-creation event containing the `-EncodedCommand` argument.

The saved alert:

`AEGIS - Encoded PowerShell Execution`

was corrected from the original Sysmon-only query to Windows Security Event ID `4688` and successfully generated a fresh trigger after the update.

Sysmon remains installed on WS01 for additional endpoint telemetry.

---
# Wazuh SIEM / XDR

WAZUH01 runs Wazuh 4.14.7 using an all-in-one deployment.

Components include:

- Wazuh Manager
- Wazuh Indexer
- Wazuh Dashboard

Configuration:

- Hostname: `wazuh01`
- IPv4: `10.50.0.40`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`

Wazuh agents are installed on:

- DC01
- WS01

---

# Wazuh Detection Validation

Several Windows and Active Directory security events were generated and successfully detected.

## Failed Windows Login

Windows Event ID:

`4625`

Wazuh Rule ID:

`60122`

Description:

`Logon Failure - Unknown user or bad password`

The event was generated by controlled failed SMB authentication attempts from the physical Kali laptop (192.168.12.172) against DC01. Wazuh displayed matching events for agent dc01-aegis using rule ID 60122.

---

## Active Directory User Creation

Windows Event ID:

`4720`

Wazuh Rule ID:

`60109`

A temporary Active Directory test account was created on DC01.

Wazuh successfully detected the account creation event.

---

## Active Directory User Deletion

Windows Event ID:

`4726`

The same temporary account was deleted after testing.

Wazuh successfully detected the deletion event.

The test account was removed after validation.

---

# OPNsense Firewall

OPNsense 26.7.3_11 is deployed as the main AEGIS firewall, gateway, and network-security control point.

Configuration:

```text
WAN          â†’ VirtualBox NAT
LAN          â†’ AEGIS-LAN
LAN IP       â†’ 10.50.0.1/24
ATTACK       â†’ VirtualBox Host-Only
ATTACK IP    â†’ 10.60.10.1/24
Windows Host â†’ 10.60.10.254/24
```

Physical Kali uses:

`192.168.12.172`

The ATTACK interface restricts offensive traffic with aliases and a logged firewall rule:

```text
Source      â†’ KALI_ATTACKER
Destination â†’ AEGIS_TARGETS
Action      â†’ Pass
Logging     â†’ Enabled
```

A persistent OPNsense gateway and static route send return traffic for `192.168.12.172/32` through the Windows Host-Only router at `10.60.10.254`.

Validated attack path:

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
AEGIS-LAN
10.50.0.0/24
```

A controlled Nmap SYN reconnaissance scan from physical Kali successfully reached DC01.

OPNsense Live View confirmed the traffic entering on ATTACK and leaving on LAN:

```text
ATTACK In â†’ 192.168.12.172 â†’ 10.50.0.10
LAN Out   â†’ 192.168.12.172 â†’ 10.50.0.10
```

Internal systems continue using DC01 for DNS:

`10.50.0.10`

DC01 forwards Internet DNS queries upstream while maintaining DNS resolution for:

`corp.aegis.test`

---
# Suricata Network IDS

Suricata is enabled within OPNsense.

Configuration:

- Interface: LAN
- Capture Mode: PCAP live mode
- Operating Mode: IDS / Alert Only
- Promiscuous Mode: Disabled
- Emerging Threats Open rules installed

IDS mode was intentionally selected before enabling IPS blocking so detections could be validated without accidentally disrupting lab traffic.

---

# Suricata Detection Validation

Suricata detection was validated using Emerging Threats rule:

`SID 2100498`

Alert:

`GPL ATTACK_RESPONSE id check returned root`

A controlled HTTP test was generated from WS01.

Traffic path:

```text
WS01
 |
 v
OPNsense
 |
 v
Suricata IDS
 |
 v
ET Open Rule Match
 |
 v
Alert Generated
```

The alert confirmed that Suricata was successfully inspecting internal network traffic.

---

# Incident Response

The project includes documented incident investigations.

## IR-001 - Multiple Failed Login Attempts

File:

`Incident-Reports/IR-001-Multiple-Failed-Logins.md`

Scenario:

Multiple failed Active Directory authentication attempts generated from WS01 against a domain account.

Detection source:

Splunk Enterprise

Primary Windows Event:

`4625`

Classification:

`True Positive - Authorized Security Test`

The report documents:

- Detection logic
- Affected systems
- Authentication type
- Investigation process
- Important event fields
- Impact assessment
- Response
- Lessons learned

---

# Detection Architecture

```text
                    Windows Environment
                           |
                 +---------+---------+
                 |                   |
                 v                   v
               DC01                WS01
                 |                   |
                 |                   +---- Sysmon
                 |                          |
                 +------------+-------------+
                              |
                              v
                   Splunk Universal Forwarder
                              |
                              v
                           SOC01
                       Splunk Enterprise
                              |
                              v
                     Detection Engineering
                              |
                              v
                           Alerts
                              |
                              v
                       Investigation
```

Wazuh provides a second detection path:

```text
DC01 / WS01
     |
     v
Wazuh Agent
     |
     v
WAZUH01
     |
     +-- Manager
     +-- Indexer
     +-- Dashboard
     |
     v
Built-in Security Rules
     |
     v
Alerts
```

Network traffic is also monitored through:

```text
AEGIS-LAN
    |
    v
OPNsense
    |
    v
Suricata
    |
    v
ET Open Rules
    |
    v
Network IDS Alerts
```

---

# VirtualBox Recovery Strategy

Snapshots are taken before major configuration changes.

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

---

# Resource Strategy

The VirtualBox host contains 32 GB of physical RAM.

Heavy SIEM systems are therefore operated in different profiles when necessary.

Example Splunk profile:

```text
DC01   → 4 GB
WS01   → 6 GB
SOC01  → 8 GB
```

Example Wazuh profile:

```text
DC01     → 4 GB
WS01     → 6 GB
WAZUH01  → 8 GB
```

OPNsense runs with:

```text
RAM  → 4 GB
vCPU → 2
Disk → 25 GB
```

This approach prevents unnecessary resource exhaustion while keeping the environment realistic.

---

# Current Project Status

## Completed

- Project repository structure
- Network architecture planning
- VirtualBox isolated network
- Windows Server 2025 deployment
- Active Directory Domain Services
- DNS
- Enterprise Organizational Units
- Security Groups
- Enterprise test users
- Privileged administrative account
- Group Policy security baseline
- Windows 11 Enterprise workstation
- Domain join
- Sysmon deployment
- Splunk Enterprise deployment
- Splunk Universal Forwarders
- Windows Event Log ingestion
- Sysmon ingestion
- Splunk detection engineering
- Failed-login detection
- Encoded PowerShell detection
- Splunk scheduled alerts
- Incident Report IR-001
- Wazuh 4.14.7 deployment
- Wazuh Windows agents
- Wazuh failed-login detection
- Active Directory account creation detection
- Active Directory account deletion detection
- OPNsense 26.7.3_11 installation
- OPNsense LAN/WAN configuration
- OPNsense Internet routing
- Removal of temporary VM NAT bypass adapters
- DC01 DNS forwarding
- SOC01 routing through OPNsense
- WAZUH01 routing through OPNsense
- Suricata IDS deployment
- Emerging Threats Open rules
- Suricata test alert validation
- Physical Kali Red Team integration
- Persistent Kali-to-AEGIS routing
- Persistent Windows IPv4 forwarding
- Persistent OPNsense return route to physical Kali
- Scoped and logged ATTACK-interface firewall policy
- Physical Kali Nmap reconnaissance against DC01
- OPNsense firewall logging of Kali reconnaissance
- Physical Kali SMB failed-login simulation
- DC01 Event ID 4625 validation from Kali
- Splunk failed-login scheduled alert triggered
- Wazuh Rule 60122 failed-login validation
- Windows Security Event ID 4688 encoded-PowerShell validation
- Corrected encoded-PowerShell Splunk alert triggered

---

# Controlled Red Team Integration

Physical Kali Red Team integration is now operational.

Validated capabilities include:

- Persistent routed access from physical Kali into the isolated AEGIS network
- Scoped OPNsense ATTACK-interface firewall policy
- Logged Nmap reconnaissance against DC01
- Controlled SMB authentication failures
- Windows Event ID `4625` generation on DC01
- Splunk ingestion and scheduled threshold alerting
- Wazuh detection using rule `60122`
- Encoded PowerShell execution on WS01
- Windows Security Event ID `4688` ingestion
- Splunk encoded-command alerting

The validated defensive workflow is:

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
  |
  v
Hardening
  |
  v
Retest
```

---

# Remaining Finalization Work

- Remove or disable abandoned WireGuard configuration from the earlier integration attempt
- Capture and organize final evidence screenshots
- Update detailed progress and incident-response documentation
- Take final clean-state VirtualBox snapshots
- Perform one final end-to-end validation
- Complete final repository cleanup and documentation polish

---
# Project Goals

AEGIS is designed to build practical skills in:

- Active Directory administration
- Windows security
- Enterprise networking
- Firewall configuration
- SIEM operations
- Detection engineering
- Threat hunting
- Endpoint monitoring
- Network intrusion detection
- Incident response
- Security investigation
- Red Team / Blue Team collaboration
- Security architecture
- Technical documentation

---

# Repository Structure

```text
AEGIS-Cyber-Range/
|
+-- Configs/
|
+-- Detection-Rules/
|
+-- Documentation/
|   +-- architecture.md
|   +-- network-plan.txt
|   +-- progress-log.md
|   +-- vm-resource-plan.md
|
+-- Incident-Reports/
|   +-- IR-001-Multiple-Failed-Logins.md
|
+-- Screenshots/
|
+-- Scripts/
|
+-- ISOs/
|
+-- .gitignore
|
+-- README.md
```

Installation media, virtual disks, packet captures, credentials, secrets, and generated SIEM data are intentionally excluded from Git.

---

# Safety and Authorization

All offensive-security testing performed as part of AEGIS is restricted to systems owned and intentionally configured for this isolated cybersecurity lab.

No testing is performed against unauthorized systems, networks, accounts, or services.

The objective of AEGIS is defensive cybersecurity education, detection engineering, incident response practice, and controlled adversary simulation.

---

# Project Status

**Active Development**

Current milestone:

**Enterprise network, Active Directory, Splunk, Wazuh, OPNsense, and Suricata IDS operational.**

Next milestone:

**Controlled Kali Linux Red Team integration and multi-layer detection testing.**