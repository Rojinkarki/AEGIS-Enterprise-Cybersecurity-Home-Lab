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