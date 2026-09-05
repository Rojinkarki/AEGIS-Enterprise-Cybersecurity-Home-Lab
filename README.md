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
| OPNsense-FW | OPNsense 26.7 | Firewall / Gateway / Suricata IDS | `10.50.0.1` |
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
- Controlled firewall integration is the next project phase

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
                        Internet
                           |
                           |
                 VirtualBox NAT / WAN
                           |
                           v
                    +---------------+
                    |   OPNsense    |
                    |   Firewall    |
                    |               |
                    | LAN 10.50.0.1 |
                    +-------+-------+
                            |
                            |
                     AEGIS-LAN
                    10.50.0.0/24
                            |
          +-----------------+-----------------+
          |                 |                 |
          v                 v                 v
       DC01              SOC01             WS01
    10.50.0.10        10.50.0.20        10.50.0.30
    AD / DNS           Splunk SIEM       Workstation
          |
          |
          +-------------------------------+
                                          |
                                          v
                                      WAZUH01
                                     10.50.0.40
                                      Wazuh XDR
```

All permanent AEGIS systems now route outbound traffic through OPNsense.

Temporary VirtualBox NAT adapters used during software installation were removed so internal systems cannot bypass the firewall.

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

Multiple failed network authentication attempts were generated from WS01 against a lab Active Directory user account.

The activity generated:

- Windows Event ID `4625`
- Network Logon Type `3`
- Failed-password authentication telemetry

Splunk successfully aggregated the events and generated an alert.

---

# Detection 2 - Encoded PowerShell Execution

Sysmon Process Creation telemetry was used to detect suspicious PowerShell execution involving encoded commands.

Detection logic extracts fields from Sysmon XML telemetry and searches for:

- `-EncodedCommand`
- `-enc`

A harmless Base64-encoded PowerShell command was executed on WS01.

The detection successfully generated an alert in Splunk.

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

The event was generated using a controlled failed login attempt on WS01.

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

OPNsense 26.7 is deployed as the main AEGIS firewall and gateway.

Configuration:

```text
WAN → VirtualBox NAT
LAN → AEGIS-LAN
LAN IP → 10.50.0.1/24
```

Validated routing:

```text
DC01     → OPNsense → Internet
WS01     → OPNsense → Internet
SOC01    → OPNsense → Internet
WAZUH01  → OPNsense → Internet
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
- OPNsense 26.7 installation
- OPNsense LAN/WAN configuration
- OPNsense Internet routing
- Removal of temporary VM NAT bypass adapters
- DC01 DNS forwarding
- SOC01 routing through OPNsense
- WAZUH01 routing through OPNsense
- Suricata IDS deployment
- Emerging Threats Open rules
- Suricata test alert validation

---

# Next Phase - Controlled Red Team Integration

The next phase will introduce the physical Kali Linux laptop through a controlled firewall path.

Planned architecture:

```text
Physical Kali Laptop
        |
        | Controlled Attack Network
        v
     OPNsense
        |
        | Firewall Rules
        v
    AEGIS-LAN
        |
   +----+----+
   |         |
   v         v
 DC01       WS01
```

Planned testing includes:

- Host discovery
- Network reconnaissance
- Port scanning
- Authentication testing
- Windows security-event generation
- Network IDS detection
- Endpoint detection
- SIEM investigation
- Detection correlation
- Incident response documentation

The goal is not simply to execute attacks, but to understand the complete defensive workflow:

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