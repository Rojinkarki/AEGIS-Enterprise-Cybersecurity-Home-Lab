# AEGIS Cyber Range Architecture

## Overview

AEGIS is an isolated enterprise cybersecurity lab built in Oracle VirtualBox with a dedicated physical Kali Linux attacker system.

Final components:
- Active Directory, DNS, and Group Policy
- Windows workstation telemetry
- Splunk Enterprise
- Wazuh SIEM/XDR
- OPNsense firewall and routing
- Suricata IDS
- persistent routed physical Kali integration

## Final Routing Path

```text
Physical Kali 192.168.12.172
        |
        v
Windows Wi-Fi 192.168.12.180
        |
        v
Windows Host-Only 10.60.10.254
        |
        v
OPNsense ATTACK 10.60.10.1
        |
        v
AEGIS-LAN 10.50.0.0/24
```

Persistent routes:

```text
Kali:     10.50.0.0/24 -> 192.168.12.180
Windows:  10.50.0.0/24 -> 10.60.10.1
OPNsense: 192.168.12.172/32 -> 10.60.10.254
```

## Systems

| System | Address | Role |
|---|---:|---|
| OPNsense-FW | `10.50.0.1` | Firewall / Gateway / Suricata |
| DC01 | `10.50.0.10` | AD / DNS / GPO |
| SOC01 | `10.50.0.20` | Splunk Enterprise |
| WS01 | `10.50.0.30` | Windows workstation / Sysmon |
| WAZUH01 | `10.50.0.40` | Wazuh SIEM/XDR |

## OPNsense

Version: `26.7.3_11`

Interfaces:

```text
WAN    le0   VirtualBox NAT
LAN    le1   10.50.0.1/24
ATTACK em0   10.60.10.1/24
```

Return gateway:

```text
KALI_RETURN_GW -> 10.60.10.254
```

Firewall policy:

```text
KALI_ATTACKER -> AEGIS_TARGETS
Action: Pass
Logging: Enabled
```

The earlier WireGuard integration attempt is not part of the final AEGIS v1 path and was disabled.

## Detection Architecture

```text
Physical Kali
      |
      v
OPNsense ATTACK
      |
      v
AEGIS-LAN
      |
 +----+----+
 |         |
 v         v
DC01      WS01
 |         |
 +----+----+
      |
      +------------------+
      |                  |
      v                  v
   Splunk              Wazuh
      |                  |
      v                  v
   Alerts              Alerts

AEGIS-LAN -> OPNsense -> Suricata -> Network IDS Alerts
```

## Final Recovery Points

- `OPNsense-AEGIS-v1-Final`
- `DC01-AEGIS-v1-Final`
- `WS01-AEGIS-v1-Final`
- `SOC01-AEGIS-v1-Final`
- `WAZUH01-AEGIS-v1-Final`

**AEGIS v1 architecture is complete and validated.**
