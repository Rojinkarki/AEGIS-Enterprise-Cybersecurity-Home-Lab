# AEGIS Cyber Range Architecture

## Overview

AEGIS is an isolated enterprise cybersecurity home lab built in Oracle VirtualBox.

The environment currently includes:

- Active Directory
- DNS
- Group Policy
- Windows endpoint telemetry
- Splunk SIEM
- Wazuh SIEM/XDR
- OPNsense firewall
- Suricata network IDS

The next phase will introduce a dedicated physical Kali Linux attacker through a controlled firewall path.

---

# Physical Systems

## Windows 11 Home Laptop

Role:

- Virtualization Host
- Primary management system

Hardware:

- CPU: AMD Ryzen 7 8845HS
- RAM: 32 GB
- GPU: NVIDIA RTX 4060

Virtualization platform:

- Oracle VirtualBox

---

## Kali Linux Laptop

Role:

- Red Team
- Controlled adversary simulation
- Network reconnaissance
- Security testing

Type:

Physical dedicated laptop

Current status:

Not yet connected directly to AEGIS-LAN.

Future connectivity will be introduced through a dedicated and restricted OPNsense interface.

---

# Virtual Machines

## OPNsense-FW

Operating System:

OPNsense 26.7

Role:

- Firewall
- Default gateway
- Internet routing
- Network control
- Suricata IDS

Resources:

- RAM: 4 GB
- vCPU: 2
- Disk: 25 GB

Interfaces:

```text
WAN
Interface: le0
Connection: VirtualBox NAT
Address: DHCP
Current example: 10.0.2.15/24

LAN
Interface: le1
Connection: Internal Network
Network: AEGIS-LAN
Address: 10.50.0.1/24
```

OPNsense is the default gateway for all permanent AEGIS systems.

---

## DC01

Operating System:

Windows Server 2025 Standard Evaluation

Role:

- Domain Controller
- Active Directory Domain Services
- DNS
- Group Policy

Network:

```text
Hostname: DC01
IP: 10.50.0.10
Subnet: 255.255.255.0
Gateway: 10.50.0.1
DNS: 10.50.0.10
```

Domain:

`corp.aegis.test`

NetBIOS:

`CORP`

Additional security components:

- Splunk Universal Forwarder
- Wazuh Agent

---

## WS01

Operating System:

Windows 11 Enterprise Evaluation

Role:

- Domain-joined corporate workstation
- Sysmon telemetry source
- Security testing target

Network:

```text
Hostname: WS01
IP: 10.50.0.30
Subnet: 255.255.255.0
Gateway: 10.50.0.1
DNS: 10.50.0.10
```

Domain:

`corp.aegis.test`

Security components:

- Sysmon
- Splunk Universal Forwarder
- Wazuh Agent

---

## SOC01

Operating System:

Ubuntu Server 24.04 LTS

Role:

- Security Operations Center
- Splunk Enterprise
- Centralized log collection
- Detection engineering
- Security investigation

Network:

```text
Hostname: soc01
IP: 10.50.0.20
Gateway: 10.50.0.1
DNS: 10.50.0.10
Search Domain: corp.aegis.test
```

Splunk receives telemetry from:

- DC01
- WS01

---

## WAZUH01

Operating System:

Ubuntu Server 24.04 LTS

Role:

- Wazuh SIEM
- Wazuh XDR
- Endpoint alerting
- Windows security monitoring

Network:

```text
Hostname: wazuh01
IP: 10.50.0.40
Gateway: 10.50.0.1
DNS: 10.50.0.10
```

Wazuh components:

- Wazuh Manager
- Wazuh Indexer
- Wazuh Dashboard

Connected agents:

- DC01
- WS01

---

# Internal Network

Network Name:

`AEGIS-LAN`

Subnet:

`10.50.0.0/24`

Gateway:

`10.50.0.1`

Internal DNS:

`10.50.0.10`

Domain:

`corp.aegis.test`

---

# IP Address Plan

| IP Address | System | Role |
|---|---|---|
| `10.50.0.1` | OPNsense-FW | Firewall / Gateway / IDS |
| `10.50.0.10` | DC01 | Active Directory / DNS |
| `10.50.0.20` | SOC01 | Splunk Enterprise |
| `10.50.0.30` | WS01 | Windows Workstation |
| `10.50.0.40` | WAZUH01 | Wazuh SIEM/XDR |

---

# Current Network Architecture

```text
                         Internet
                            |
                            v
                   VirtualBox NAT
                            |
                            v
                    OPNsense WAN
                      le0 / DHCP
                            |
                    +-------+-------+
                    |   OPNsense    |
                    |   Firewall    |
                    |  Suricata IDS |
                    +-------+-------+
                            |
                            |
                  LAN 10.50.0.1/24
                            |
                            v
                       AEGIS-LAN
                     10.50.0.0/24
                            |
          +-----------------+------------------+
          |                 |                  |
          v                 v                  v
        DC01              SOC01              WS01
     10.50.0.10        10.50.0.20         10.50.0.30
      AD / DNS            Splunk           Workstation
          |                                    |
          |                                    |
          +----------------+-------------------+
                           |
                           v
                        WAZUH01
                       10.50.0.40
                         Wazuh
```

---

# DNS Architecture

Internal systems do not use public DNS directly.

They use:

`DC01 - 10.50.0.10`

DNS flow:

```text
WS01 / SOC01 / WAZUH01
          |
          v
        DC01
     10.50.0.10
          |
          | External DNS forwarding
          v
       OPNsense
     10.50.0.1
          |
          v
       Internet
```

Configured DC01 forwarders:

- `1.1.1.1`
- `8.8.8.8`

This allows Active Directory DNS to remain authoritative for:

`corp.aegis.test`

while still resolving Internet domains.

---

# Firewall Architecture

All permanent AEGIS systems route through:

`10.50.0.1`

Traffic flow:

```text
Internal System
      |
      v
OPNsense LAN
10.50.0.1
      |
      v
OPNsense WAN
      |
      v
VirtualBox NAT
      |
      v
Internet
```

Temporary VirtualBox NAT adapters previously used during installation were removed from:

- DC01
- WS01
- SOC01
- WAZUH01

This prevents systems from bypassing the OPNsense firewall.

---

# Splunk Detection Architecture

```text
                 DC01
           Windows Security Logs
                    |
                    |
          Splunk Universal Forwarder
                    |
                    |
                    v
                 SOC01
          Splunk Enterprise
                    ^
                    |
          Splunk Universal Forwarder
                    |
                    |
                  WS01
             Windows Logs
               + Sysmon
```

Validated Splunk detections include:

- Multiple Failed Login Attempts
- Encoded PowerShell Execution

---

# Wazuh Detection Architecture

```text
              DC01
                |
          Wazuh Agent
                |
                |
                v
             WAZUH01
        Wazuh Manager
        Wazuh Indexer
        Wazuh Dashboard
                ^
                |
          Wazuh Agent
                |
              WS01
```

Validated Windows events include:

- Event ID `4625` - Failed Login
- Event ID `4720` - User Account Creation
- Event ID `4726` - User Account Deletion

---

# Suricata IDS Architecture

Suricata runs inside OPNsense.

Configuration:

```text
Mode: IDS / Alert Only
Capture: PCAP Live Mode
Interface: LAN
Rules: Emerging Threats Open
```

Traffic inspection flow:

```text
WS01 / DC01 / SOC01 / WAZUH01
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
             Alert
```

Detection testing successfully triggered:

`SID 2100498`

Signature:

`GPL ATTACK_RESPONSE id check returned root`

---

# Layered Detection Model

AEGIS currently provides three primary security-monitoring layers.

## Endpoint / Windows Telemetry

```text
Windows Event Logs
        +
      Sysmon
```

## SIEM / Endpoint Detection

```text
Splunk
Wazuh
```

## Network Detection

```text
OPNsense
   |
Suricata IDS
```

This allows the same security activity to eventually be investigated across multiple telemetry sources.

---

# Security Model

The AEGIS internal enterprise network remains isolated behind OPNsense.

The physical Kali laptop does not currently have unrestricted access to AEGIS-LAN.

The planned attacker architecture is:

```text
Physical Kali Linux Laptop
          |
          |
          v
Dedicated OPNsense Attack Interface
          |
          | Restrictive Firewall Rules
          |
          v
       OPNsense
          |
          v
      AEGIS-LAN
          |
      +---+---+
      |       |
      v       v
    DC01     WS01
```

This design will allow controlled adversary simulations without directly exposing the entire enterprise lab to the normal home network.

---

# Resource Strategy

The virtualization host contains 32 GB RAM.

Because Splunk and Wazuh are resource-intensive, different operating profiles are used when appropriate.

## Splunk Profile

```text
DC01   - 4 GB
WS01   - 6 GB
SOC01  - 8 GB
```

## Wazuh Profile

```text
DC01     - 4 GB
WS01     - 6 GB
WAZUH01  - 8 GB
```

## Firewall

```text
OPNsense
RAM: 4 GB
vCPU: 2
```

Not every heavy VM needs to run simultaneously.

---

# Current Architecture Status

Operational:

- OPNsense Firewall
- OPNsense Routing
- Active Directory
- DNS
- Group Policy
- Windows Domain Workstation
- Sysmon
- Splunk Enterprise
- Splunk Universal Forwarders
- Splunk Detection Rules
- Wazuh SIEM/XDR
- Wazuh Agents
- Suricata IDS
- Emerging Threats Open Rules
- Incident Response Workflow

Pending:

- Physical Kali integration
- Dedicated attack interface
- Controlled reconnaissance
- Multi-layer attack detection
- Detection correlation
- Additional incident reports
- Security hardening and retesting
