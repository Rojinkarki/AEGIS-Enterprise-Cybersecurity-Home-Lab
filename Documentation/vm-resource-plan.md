# AEGIS Virtual Machine Resource Plan

## Host System

Operating System:

Windows 11 Home

Hardware:

- CPU: AMD Ryzen 7 8845HS
- Physical Cores: 8
- Logical Threads: 16
- RAM: 32 GB
- GPU: NVIDIA RTX 4060
- Storage Available at Project Start: approximately 500 GB

Virtualization Platform:

Oracle VirtualBox

---

# DC01 - Domain Controller

Operating System:

Windows Server 2025 Standard Evaluation

Resources:

- RAM: 4 GB
- vCPU: 2
- Virtual Disk: 60 GB dynamically allocated

Role:

- Active Directory Domain Services
- DNS
- Group Policy
- Domain Controller

Network:

- IP: `10.50.0.10`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`

Security Components:

- Splunk Universal Forwarder
- Wazuh Agent

---

# WS01 - Corporate Workstation

Operating System:

Windows 11 Enterprise Evaluation

Resources:

- RAM: 6 GB
- vCPU: 4
- Virtual Disk: 80 GB dynamically allocated

Role:

- Domain-joined workstation
- Sysmon telemetry source
- Security testing endpoint

Network:

- IP: `10.50.0.30`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`

Security Components:

- Sysmon
- Splunk Universal Forwarder
- Wazuh Agent

---

# SOC01 - Splunk Security Operations Server

Operating System:

Ubuntu Server 24.04 LTS

Resources:

- RAM: 8 GB
- vCPU: 4
- Virtual Disk: 100 GB dynamically allocated

Role:

- Splunk Enterprise
- Centralized log collection
- Detection engineering
- Security investigation

Network:

- IP: `10.50.0.20`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`

---

# WAZUH01 - Wazuh Security Server

Operating System:

Ubuntu Server 24.04 LTS

Resources:

- RAM: 8 GB
- vCPU: 4
- Virtual Disk: 80 GB dynamically allocated

Role:

- Wazuh Manager
- Wazuh Indexer
- Wazuh Dashboard
- Endpoint security monitoring

Network:

- IP: `10.50.0.40`
- Gateway: `10.50.0.1`
- DNS: `10.50.0.10`

---

# OPNsense-FW - Firewall

Operating System:

OPNsense 26.7

Resources:

- RAM: 4 GB
- vCPU: 2
- Virtual Disk: 25 GB dynamically allocated

Role:

- Firewall
- Default gateway
- Internet routing
- Suricata IDS
- Future Kali attack-network control

Interfaces:

```text
WAN
VirtualBox NAT

LAN
AEGIS-LAN
10.50.0.1/24
```

---

# Internal Network

Network:

`AEGIS-LAN`

Subnet:

`10.50.0.0/24`

Gateway:

`10.50.0.1`

DNS:

`10.50.0.10`

---

# Resource Strategy

The host has 32 GB of physical RAM.

Running every heavy VM at the same time would consume nearly all host memory, so AEGIS uses workload profiles.

## Splunk Profile

Recommended systems:

```text
OPNsense  4 GB
DC01      4 GB
WS01      6 GB
SOC01     8 GB
----------------
Total    22 GB
```

This leaves approximately 10 GB for Windows and VirtualBox overhead.

---

# Wazuh Profile

Recommended systems:

```text
OPNsense  4 GB
DC01      4 GB
WS01      6 GB
WAZUH01   8 GB
----------------
Total    22 GB
```

This leaves approximately 10 GB for the host operating system.

---

# Lightweight Network Profile

For firewall, Active Directory, and endpoint testing:

```text
OPNsense  4 GB
DC01      4 GB
WS01      6 GB
----------------
Total    14 GB
```

This is preferred when Splunk or Wazuh are not needed.

---

# Heavy Full-Lab Configuration

Running:

```text
OPNsense  4 GB
DC01      4 GB
WS01      6 GB
SOC01     8 GB
WAZUH01   8 GB
----------------
Total    30 GB
```

is not recommended during normal operation because it leaves too little memory for the Windows host and virtualization overhead.

SOC01 and WAZUH01 should therefore normally be operated in separate profiles.

---

# Storage Strategy

All virtual disks use dynamic allocation.

Configured disk sizes:

| VM | Disk |
|---|---:|
| DC01 | 60 GB |
| WS01 | 80 GB |
| SOC01 | 100 GB |
| WAZUH01 | 80 GB |
| OPNsense | 25 GB |

Dynamic allocation prevents the full configured capacity from being consumed immediately.

---

# Temporary Internet Access

During early installation stages, some VMs temporarily used a second VirtualBox NAT adapter.

These temporary adapters were removed after OPNsense became operational.

Permanent AEGIS systems now use:

```text
Default Gateway: 10.50.0.1
```

This ensures outbound traffic follows the firewall path.

---

# Snapshot Strategy

Snapshots are taken before or after major milestones.

Examples include:

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

# Current Recommendation

For most daily lab work, run only the systems required for that exercise.

Examples:

Splunk investigation:

```text
OPNsense + DC01 + WS01 + SOC01
```

Wazuh investigation:

```text
OPNsense + DC01 + WS01 + WAZUH01
```

Firewall / Suricata testing:

```text
OPNsense + DC01 + WS01
```

This keeps the host responsive while preserving realistic enterprise workflows.
