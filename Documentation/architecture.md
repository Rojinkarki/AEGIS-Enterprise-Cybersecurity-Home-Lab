# \# AEGIS Cyber Range Architecture

# 

# \## Overview

# 

# AEGIS is an isolated enterprise cybersecurity home lab built in Oracle VirtualBox.

# 

# The environment currently includes:

# 

# \- Active Directory

# \- DNS

# \- Group Policy

# \- Windows endpoint telemetry

# \- Splunk SIEM

# \- Wazuh SIEM/XDR

# \- OPNsense firewall

# \- Suricata network IDS

# 

# The next phase will introduce a dedicated physical Kali Linux attacker through a controlled firewall path.

# 

# \---

# 

# \# Physical Systems

# 

# \## Windows 11 Home Laptop

# 

# Role:

# 

# \- Virtualization Host

# \- Primary management system

# 

# Hardware:

# 

# \- CPU: AMD Ryzen 7 8845HS

# \- RAM: 32 GB

# \- GPU: NVIDIA RTX 4060

# 

# Virtualization platform:

# 

# \- Oracle VirtualBox

# 

# \---

# 

# \## Kali Linux Laptop

# 

# Role:

# 

# \- Red Team

# \- Controlled adversary simulation

# \- Network reconnaissance

# \- Security testing

# 

# Type:

# 

# Physical dedicated laptop

# 

# Current status:

# 

# Not yet connected directly to AEGIS-LAN.

# 

# Future connectivity will be introduced through a dedicated and restricted OPNsense interface.

# 

# \---

# 

# \# Virtual Machines

# 

# \## OPNsense-FW

# 

# Operating System:

# 

# OPNsense 26.7

# 

# Role:

# 

# \- Firewall

# \- Default gateway

# \- Internet routing

# \- Network control

# \- Suricata IDS

# 

# Resources:

# 

# \- RAM: 4 GB

# \- vCPU: 2

# \- Disk: 25 GB

# 

# Interfaces:

# 

# ```text

# WAN

# Interface: le0

# Connection: VirtualBox NAT

# Address: DHCP

# Current example: 10.0.2.15/24

# 

# LAN

# Interface: le1

# Connection: Internal Network

# Network: AEGIS-LAN

# Address: 10.50.0.1/24

