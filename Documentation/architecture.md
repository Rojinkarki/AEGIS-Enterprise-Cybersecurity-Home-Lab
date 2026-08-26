# AEGIS Cyber Range Architecture

## Physical Systems

### Kali Linux Laptop
Role: Red Team / Attacker
Type: Physical machine

### Windows 11 Home Laptop
Role: Virtualization Host
CPU: AMD Ryzen 7 8845HS
RAM: 32 GB
GPU: NVIDIA RTX 4060

## Planned Virtual Machines

### DC01
Operating System: Windows Server 2025
Role:
- Active Directory Domain Services
- DNS
- Domain Controller

Planned IP: 10.50.0.10

### SOC01
Operating System: Ubuntu Server
Role:
- Splunk Enterprise
- Centralized log analysis
- Detection engineering

Planned IP: 10.50.0.20

### WS01
Operating System: Windows 11 Enterprise
Role:
- Domain-joined corporate workstation
- Sysmon telemetry source
- Security testing target

Planned IP: 10.50.0.30

### OPNsense
Role:
- Firewall
- Routing
- Network segmentation

Planned IP: 10.50.0.1

## Internal Network

Name: AEGIS-LAN
Subnet: 10.50.0.0/24

Initial design:
All enterprise VMs remain isolated inside the VirtualBox Internal Network.

## Security Model

The physical Kali system will not initially have direct access to AEGIS-LAN.

Connectivity between Kali and the enterprise environment will be introduced later through a controlled firewall path.

## Detection Flow

WS01 / DC01
     |
     | Security Events
     v
Sysmon + Windows Event Logs
     |
     v
Splunk Forwarder
     |
     v
SOC01
     |
     v
Detection Rules
     |
     v
SOC Investigation
