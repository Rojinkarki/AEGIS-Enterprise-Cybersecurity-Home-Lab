# AEGIS Virtual Machine Resource Plan

## Host System

Operating System: Windows 11 Home
CPU: AMD Ryzen 7 8845HS
Physical Cores: 8
Logical Threads: 16
RAM: 32 GB
Available Storage at Project Start: Approximately 500 GB

## DC01 - Domain Controller

Operating System: Windows Server 2025
RAM: 4 GB
vCPUs: 2
Virtual Disk: 60 GB dynamically allocated

Services:
- Active Directory Domain Services
- DNS
- Group Policy

## WS01 - Corporate Workstation

Operating System: Windows 11 Enterprise
RAM: 6 GB
vCPUs: 4
Virtual Disk: 80 GB dynamically allocated

Services / Tools:
- Domain membership
- Sysmon
- Splunk Universal Forwarder
- Security testing endpoint

## SOC01 - Security Operations Server

Operating System: Ubuntu Server
RAM: 8 GB
vCPUs: 4
Virtual Disk: 100 GB dynamically allocated

Services:
- Splunk Enterprise
- Centralized log collection
- Detection engineering

## OPNsense - Future Firewall

RAM: 2 GB
vCPUs: 2
Virtual Disk: 20 GB dynamically allocated

Role:
- Firewall
- Routing
- Network segmentation

## Resource Strategy

Initial simultaneously running VMs:

DC01 : 4 GB
WS01 : 6 GB
SOC01: 8 GB

Total VM RAM: 18 GB

Approximately 14 GB remains available for the Windows host and virtualization overhead.

OPNsense will be introduced later.

Virtual disks will use dynamic allocation so the full configured disk capacity is not consumed immediately.
Get-Content ".\Documentation\vm-resource-plan.md"
