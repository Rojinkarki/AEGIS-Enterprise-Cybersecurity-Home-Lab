# AEGIS Cyber Range - Build Progress

## Project Status

AEGIS is an isolated enterprise cybersecurity home lab designed for hands-on learning in Active Directory, Windows security, Group Policy, SIEM monitoring, detection engineering, incident response, and controlled adversary simulation.

---

## Phase 1 - Project Foundation

Status: Complete

- Created structured project workspace
- Initialized Git repository
- Configured .gitignore
- Created network plan
- Created architecture documentation
- Created VM resource plan
- Designed isolated VirtualBox network: AEGIS-LAN
- Selected subnet: 10.50.0.0/24

---

## Phase 2 - Domain Controller

Status: Complete

### DC01

Operating System:
Windows Server 2025 Standard Evaluation - Desktop Experience

Configuration:

- Hostname: DC01
- IPv4: 10.50.0.10
- Subnet: 255.255.255.0
- DNS: 10.50.0.10
- Network: AEGIS-LAN
- Default gateway intentionally left blank during isolated build stage

Services deployed:

- Active Directory Domain Services
- DNS
- Group Policy Management

Domain created:

corp.aegis.test

NetBIOS domain:

CORP

Validation completed:

- Active Directory domain resolution
- DNS resolution
- SYSVOL availability
- NETLOGON availability
- Domain Controller health checks

---

## Phase 3 - Active Directory Enterprise Structure

Status: Complete

Created top-level OU:

AEGIS-CORP

Organizational structure:

- Users
  - IT
  - Engineering
  - Finance
  - HR
- Workstations
- Servers
- Service Accounts
- Groups
- Privileged Accounts

Security groups created:

- GG-IT-Users
- GG-Engineering-Users
- GG-Finance-Users
- GG-HR-Users

Sample enterprise users created:

- Alex Carter - carter
- Maya Patel - mpatel
- Daniel Brooks - dbrooks
- Sophia Reed - sreed

Each user was assigned to the appropriate department security group.

Privileged administrative account created:

CORP\aegis-admin

The account was added to the Domain Admins security group.

---

## Phase 4 - Group Policy Security Baseline

Status: Complete

Created:

AEGIS-Workstation-Security-Baseline

Linked to:

AEGIS-CORP\Workstations

Security telemetry policies configured include:

- Process Creation auditing
- Command-line process logging
- Successful and failed logon auditing
- Special logon auditing
- User account management auditing
- Security group management auditing
- Audit policy change monitoring
- PowerShell Script Block Logging
- PowerShell Module Logging
- Advanced Audit Policy enforcement

---

## Phase 5 - Corporate Windows Workstation

Status: Complete

### WS01

Operating System:
Windows 11 Enterprise Evaluation

Configuration:

- Hostname: WS01
- IPv4: 10.50.0.30
- Subnet: 255.255.255.0
- DNS: 10.50.0.10
- Network: AEGIS-LAN

Domain membership:

corp.aegis.test

WS01 was moved into:

AEGIS-CORP\Workstations

Group Policy validation:

- AEGIS-Workstation-Security-Baseline applied successfully
- Default Domain Policy applied successfully
- Process Creation auditing verified
- PowerShell Script Block Logging verified
- PowerShell Module Logging verified

---

## VirtualBox Recovery Points

DC01 snapshots:

1. DC01-Baseline-AD-Healthy
2. DC01-AD-Structure-Complete
3. DC01-GPO-Security-Baseline

These snapshots provide recovery points before major configuration stages.

---

## Current Architecture

Physical Kali Linux Laptop
        |
        | Future controlled attack path
        |
        v

AEGIS Cyber Range

DC01
Windows Server 2025
10.50.0.10
Active Directory + DNS
        |
        | AEGIS-LAN
        |
        +-------------------+
                            |
                           WS01
                    Windows 11 Enterprise
                        10.50.0.30
                  Domain-Joined Workstation

Future:

SOC01
Ubuntu Server + Splunk
10.50.0.20

OPNsense
Firewall / segmentation
10.50.0.1

---

## Next Phase

Phase 6 - Security Operations Center

Planned work:

- Build SOC01
- Install Ubuntu Server
- Deploy Splunk Enterprise
- Configure Windows log forwarding
- Deploy Sysmon
- Ingest DC01 and WS01 telemetry
- Build detection rules
- Create SOC dashboards
- Map detections to MITRE ATT&CK
- Perform controlled attack simulations
- Investigate generated alerts
- Document detection gaps and remediation
