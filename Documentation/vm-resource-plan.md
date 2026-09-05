# \# AEGIS Virtual Machine Resource Plan

# 

# \## Host System

# 

# Operating System:

# 

# Windows 11 Home

# 

# Hardware:

# 

# \- CPU: AMD Ryzen 7 8845HS

# \- Physical Cores: 8

# \- Logical Threads: 16

# \- RAM: 32 GB

# \- GPU: NVIDIA RTX 4060

# \- Storage Available at Project Start: approximately 500 GB

# 

# Virtualization Platform:

# 

# Oracle VirtualBox

# 

# \---

# 

# \# DC01 - Domain Controller

# 

# Operating System:

# 

# Windows Server 2025 Standard Evaluation

# 

# Resources:

# 

# \- RAM: 4 GB

# \- vCPU: 2

# \- Virtual Disk: 60 GB dynamically allocated

# 

# Role:

# 

# \- Active Directory Domain Services

# \- DNS

# \- Group Policy

# \- Domain Controller

# 

# Network:

# 

# \- IP: `10.50.0.10`

# \- Gateway: `10.50.0.1`

# \- DNS: `10.50.0.10`

# 

# Security Components:

# 

# \- Splunk Universal Forwarder

# \- Wazuh Agent

# 

# \---

# 

# \# WS01 - Corporate Workstation

# 

# Operating System:

# 

# Windows 11 Enterprise Evaluation

# 

# Resources:

# 

# \- RAM: 6 GB

# \- vCPU: 4

# \- Virtual Disk: 80 GB dynamically allocated

# 

# Role:

# 

# \- Domain-joined workstation

# \- Sysmon telemetry source

# \- Security testing endpoint

# 

# Network:

# 

# \- IP: `10.50.0.30`

# \- Gateway: `10.50.0.1`

# \- DNS: `10.50.0.10`

# 

# Security Components:

# 

# \- Sysmon

# \- Splunk Universal Forwarder

# \- Wazuh Agent

# 

# \---

# 

# \# SOC01 - Splunk Security Operations Server

# 

# Operating System:

# 

# Ubuntu Server 24.04 LTS

# 

# Resources:

# 

# \- RAM: 8 GB

# \- vCPU: 4

# \- Virtual Disk: 100 GB dynamically allocated

# 

# Role:

# 

# \- Splunk Enterprise

# \- Centralized log collection

# \- Detection engineering

# \- Security investigation

# 

# Network:

# 

# \- IP: `10.50.0.20`

# \- Gateway: `10.50.0.1`

# \- DNS: `10.50.0.10`

# 

# \---

# 

# \# WAZUH01 - Wazuh Security Server

# 

# Operating System:

# 

# Ubuntu Server 24.04 LTS

# 

# Resources:

# 

# \- RAM: 8 GB

# \- vCPU: 4

# \- Virtual Disk: 80 GB dynamically allocated

# 

# Role:

# 

# \- Wazuh Manager

# \- Wazuh Indexer

# \- Wazuh Dashboard

# \- Endpoint security monitoring

# 

# Network:

# 

# \- IP: `10.50.0.40`

# \- Gateway: `10.50.0.1`

# \- DNS: `10.50.0.10`

# 

# \---

# 

# \# OPNsense-FW - Firewall

# 

# Operating System:

# 

# OPNsense 26.7

# 

# Resources:

# 

# \- RAM: 4 GB

# \- vCPU: 2

# \- Virtual Disk: 25 GB dynamically allocated

# 

# Role:

# 

# \- Firewall

# \- Default gateway

# \- Internet routing

# \- Suricata IDS

# \- Future Kali attack-network control

# 

# Interfaces:

# 

# ```text

# WAN

# VirtualBox NAT

# 

# LAN

# AEGIS-LAN

# 10.50.0.1/24

