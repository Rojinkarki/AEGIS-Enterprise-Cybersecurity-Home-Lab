# AEGIS Cyber Range - Build Progress

## Project Status

AEGIS is an isolated enterprise cybersecurity home lab designed for hands-on learning in:

- Active Directory
- Windows security
- Enterprise networking
- SIEM monitoring
- Detection engineering
- Endpoint telemetry
- Network intrusion detection
- Incident response
- Controlled adversary simulation

Current milestone:

**Active Directory, Splunk, Wazuh, OPNsense, and Suricata IDS are operational.**

---

# Phase 1 - Project Foundation

**Status: Complete**

Completed:

- Created structured project workspace
- Initialized Git repository
- Configured `.gitignore`
- Created network plan
- Created architecture documentation
- Created VM resource plan
- Created incident-report directory
- Created detection-rules directory
- Designed isolated VirtualBox network
- Selected internal network name: `AEGIS-LAN`
- Selected subnet: `10.50.0.0/24`

---

# Phase 2 - Domain Controller

**Status: Complete**

## DC01

Operating System:

Windows Server 2025 Standard Evaluation - Desktop Experience

Configuration:

- Hostname: `DC01`
- IPv4: `10.50.0.10`
- Subnet: `255.255.255.0`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`
- Network: `AEGIS-LAN`

Services:

- Active Directory Domain Services
- DNS
- Group Policy Management

Domain:

`corp.aegis.test`

NetBIOS:

`CORP`

Validated:

- Active Directory domain health
- DNS resolution
- SYSVOL
- NETLOGON
- Domain authentication
- Internal host resolution
- Internet connectivity through OPNsense

DNS forwarders configured:

- `1.1.1.1`
- `8.8.8.8`

---

# Phase 3 - Active Directory Enterprise Structure

**Status: Complete**

Top-level OU:

`AEGIS-CORP`

Structure:

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

Security groups:

- `GG-IT-Users`
- `GG-Engineering-Users`
- `GG-Finance-Users`
- `GG-HR-Users`

Sample users:

- Alex Carter - `acarter`
- Maya Patel - `mpatel`
- Daniel Brooks - `dbrooks`
- Sophia Reed - `sreed`

Privileged lab administrator:

`CORP\aegis-admin`

---

# Phase 4 - Group Policy Security Baseline

**Status: Complete**

Created:

`AEGIS-Workstation-Security-Baseline`

Linked to:

`AEGIS-CORP\Workstations`

Configured policies include:

- Audit Process Creation
- Include command line in process creation events
- PowerShell Script Block Logging
- PowerShell Module Logging
- Audit successful logons
- Audit failed logons
- Audit Special Logon
- Audit User Account Management
- Audit Security Group Management
- Audit Policy Change
- Advanced Audit Policy enforcement

Policy application was successfully verified on WS01.

---

# Phase 5 - Corporate Windows Workstation

**Status: Complete**

## WS01

Operating System:

Windows 11 Enterprise Evaluation

Configuration:

- Hostname: `WS01`
- IPv4: `10.50.0.30`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`
- Domain: `corp.aegis.test`
- Network: `AEGIS-LAN`

WS01 was moved into:

`AEGIS-CORP\Workstations`

Validated:

- Domain membership
- Domain authentication
- Group Policy application
- DC01 connectivity
- DNS resolution
- Internet connectivity through OPNsense

Installed monitoring software:

- Sysmon
- Splunk Universal Forwarder
- Wazuh Agent

---

# Phase 6 - Splunk Security Operations Center

**Status: Complete**

## SOC01

Operating System:

Ubuntu Server 24.04 LTS

Configuration:

- Hostname: `soc01`
- IPv4: `10.50.0.20`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`
- Search domain: `corp.aegis.test`

Splunk Enterprise:

`10.4.2`

Splunk receiver:

`TCP 9997`

Windows systems forwarding data:

- DC01
- WS01

Telemetry includes:

- Windows Security log
- Windows System log
- Windows Application log
- Active Directory events
- Sysmon Operational events

SOC01 Internet connectivity and internal DNS resolution were validated through OPNsense.

Temporary VirtualBox NAT access was removed after firewall routing was operational.

---

# Phase 7 - Sysmon Endpoint Monitoring

**Status: Complete**

Sysmon version:

`15.21`

Installed on:

`WS01`

Sysmon configuration path:

`C:\Tools\Sysmon\AEGIS-Sysmon.xml`

Telemetry includes:

- Process creation
- Network connections
- File creation
- DNS queries
- SHA256 hashing

Splunk Universal Forwarder permissions were adjusted so the service could read:

`Microsoft-Windows-Sysmon/Operational`

Sysmon events were successfully validated in Splunk.

---

# Phase 8 - Splunk Detection Engineering

**Status: Complete**

## Detection 1 - Multiple Failed Login Attempts

Detection:

`AEGIS - Multiple Failed Login Attempts`

Windows Event ID:

`4625`

Detection logic:

```spl
index=* source="WinEventLog:Security" EventCode=4625
| stats count as Failed_Logins by host
| where Failed_Logins >= 5
```

Configuration:

- Scheduled every minute
- 15-minute lookback
- Trigger when results are greater than zero
- Throttling enabled

Controlled failed authentication attempts were generated from WS01 against a lab Active Directory account.

The detection successfully generated an alert.

---

## Detection 2 - Encoded PowerShell Execution

Detection:

`AEGIS - Encoded PowerShell Execution`

Telemetry source:

Sysmon Process Creation

Detection searches PowerShell command lines for:

- `-EncodedCommand`
- `-enc`

A harmless Base64-encoded PowerShell test command was executed.

The Splunk detection successfully triggered.

---

# Phase 9 - Incident Response

**Status: In Progress**

First incident report created:

`Incident-Reports/IR-001-Multiple-Failed-Logins.md`

Incident:

Multiple Failed Active Directory Login Attempts

Detection source:

Splunk Enterprise

Primary event:

`Windows Event ID 4625`

Authentication type:

`Logon Type 3 - Network Logon`

Target account:

`CORP\acarter`

Classification:

`True Positive - Authorized Security Test`

Status:

`Closed - Authorized Simulation`

The report documents:

- Detection logic
- Detection flow
- Investigation fields
- Impact
- Response
- Lessons learned

Additional incident reports will be created during Kali attack simulations.

---

# Phase 10 - Wazuh SIEM / XDR

**Status: Complete**

## WAZUH01

Operating System:

Ubuntu Server 24.04 LTS

Wazuh version:

`4.14.7`

Configuration:

- Hostname: `wazuh01`
- IPv4: `10.50.0.40`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`

Components:

- Wazuh Manager
- Wazuh Indexer
- Wazuh Dashboard

Agents:

- `ws01-aegis`
- `dc01-aegis`

Both agents were successfully connected and active.

Temporary VirtualBox NAT access was removed after OPNsense routing was operational.

---

# Phase 11 - Wazuh Detection Validation

**Status: Complete**

## Failed Login Detection

Generated on:

WS01

Windows Event:

`4625`

Wazuh Rule:

`60122`

Description:

`Logon Failure - Unknown user or bad password`

Detection successfully generated.

---

## Active Directory User Creation

Generated on:

DC01

Windows Event:

`4720`

Wazuh Rule:

`60109`

A temporary Active Directory test account was created.

Wazuh successfully detected the activity.

---

## Active Directory User Deletion

Generated on:

DC01

Windows Event:

`4726`

The temporary test account was deleted after validation.

Wazuh successfully detected the deletion.

The temporary account was removed from Active Directory after testing.

---

# Phase 12 - OPNsense Firewall

**Status: Complete**

Version:

`OPNsense 26.7`

VM resources:

- RAM: 4 GB
- vCPU: 2
- Disk: 25 GB

Interfaces:

```text
WAN - le0
VirtualBox NAT
DHCP address: 10.0.2.15/24

LAN - le1
AEGIS-LAN
10.50.0.1/24
```

Internet access from OPNsense was validated.

OPNsense became the default gateway for:

- DC01
- WS01
- SOC01
- WAZUH01

All four systems successfully reached the Internet through the firewall.

Temporary individual VirtualBox NAT adapters were removed from the internal systems to eliminate firewall bypass paths.

---

# Phase 13 - Enterprise DNS and Routing

**Status: Complete**

Final architecture:

```text
Internal Systems
      |
      | DNS
      v
DC01 - 10.50.0.10
      |
      | Default route
      v
OPNsense - 10.50.0.1
      |
      v
Internet
```

Internal systems use:

```text
DNS: 10.50.0.10
Gateway: 10.50.0.1
```

DC01 handles:

- Active Directory DNS
- `corp.aegis.test` resolution
- External DNS forwarding

Validated on:

- DC01
- WS01
- SOC01
- WAZUH01

---

# Phase 14 - Suricata Network IDS

**Status: Complete**

Suricata was enabled inside OPNsense.

Configuration:

- Interface: LAN
- Capture Mode: PCAP live mode
- IDS / alert-only mode
- Promiscuous mode disabled
- Emerging Threats Open rules installed

IDS-only mode was selected so suspicious traffic could be detected without automatically blocking lab traffic.

Suricata service operation was verified.

---

# Phase 15 - Suricata Detection Validation

**Status: Complete**

Test rule:

`SID 2100498`

Signature:

`GPL ATTACK_RESPONSE id check returned root`

A controlled HTTP request was generated from WS01.

Traffic path:

```text
WS01
  |
  v
OPNsense
  |
  v
Suricata
  |
  v
ET Open Rule
  |
  v
Alert
```

The Suricata alert appeared successfully in OPNsense.

This validated:

- Packet inspection
- ET Open rule loading
- IDS processing
- Alert generation
- LAN traffic monitoring

---

# Current Detection Stack

```text
                 +------------------+
                 |      WS01        |
                 | Windows Endpoint |
                 +--------+---------+
                          |
          +---------------+---------------+
          |                               |
          v                               v
       Sysmon                         Wazuh Agent
          |                               |
          v                               v
Splunk Universal Forwarder            WAZUH01
          |                               |
          v                               v
        SOC01                         Wazuh Rules
   Splunk Enterprise                     |
          |                               v
          v                            Alerts
    SPL Detections
          |
          v
       Alerts
```

Network detection:

```text
AEGIS-LAN
    |
    v
OPNsense
    |
    v
Suricata IDS
    |
    v
ET Open Rules
    |
    v
Network Alerts
```

---

# VirtualBox Recovery Points

## DC01

1. `DC01-Baseline-AD-Healthy`
2. `DC01-AD-Structure-Complete`
3. `DC01-GPO-Security-Baseline`
4. `DC01-Splunk-Forwarder-Integrated`

## WS01

1. `WS01-Splunk-Sysmon-Integrated`

## SOC01

1. `SOC01-Splunk-Detection-Engine-Operational`

## WAZUH01

1. `WAZUH01-Baseline-Ubuntu-Healthy`
2. `WAZUH01-Agents-and-AD-Detection-Operational`
3. `WAZUH01-OPNsense-Routing-Integrated`

## OPNsense

1. `OPNsense-Baseline-WAN-LAN-Healthy`
2. `OPNsense-Suricata-IDS-Operational`

---

# Current Network

```text
                     Internet
                        |
                        v
                  OPNsense WAN
                 VirtualBox NAT
                        |
                        v
               OPNsense Firewall
                  10.50.0.1
                        |
                        v
                   AEGIS-LAN
                 10.50.0.0/24
                        |
       +----------------+----------------+
       |                |                |
       v                v                v
     DC01             SOC01            WS01
  10.50.0.10       10.50.0.20       10.50.0.30
   AD / DNS           Splunk         Workstation
       |
       +--------------------------------+
                                        |
                                        v
                                     WAZUH01
                                    10.50.0.40
                                      Wazuh
```

---

# Next Phase - Physical Kali Integration

**Status: Pending**

Planned work:

- Add controlled attacker-facing interface to OPNsense
- Integrate physical Kali Linux laptop
- Restrict Kali access with firewall rules
- Keep the enterprise network protected from unnecessary external exposure
- Perform controlled reconnaissance
- Perform port scanning
- Generate Windows security events
- Generate Suricata network alerts
- Observe Splunk detections
- Observe Wazuh detections
- Correlate network and endpoint telemetry
- Create additional incident reports
- Document detection gaps
- Apply hardening
- Retest detections

The next objective is to demonstrate the full defensive lifecycle:

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

# Overall Status

AEGIS currently contains operational:

- Active Directory
- DNS
- Group Policy
- Windows enterprise endpoint
- Sysmon
- Splunk SIEM
- Custom Splunk detections
- Wazuh SIEM/XDR
- Wazuh endpoint agents
- OPNsense firewall
- Centralized routing
- Suricata IDS
- Emerging Threats rules
- Incident response documentation

**Current project stage: Controlled Red Team integration pending.**
