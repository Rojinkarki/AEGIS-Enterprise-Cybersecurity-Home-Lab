# AEGIS Final Network Routing Configuration

## Addresses

| Component | Address |
|---|---|
| Physical Kali | `192.168.12.172/24` |
| Windows Host Wi-Fi | `192.168.12.180/24` |
| Windows Host-Only | `10.60.10.254/24` |
| OPNsense ATTACK | `10.60.10.1/24` |
| OPNsense LAN | `10.50.0.1/24` |

## Persistent Routes

```text
Kali:     10.50.0.0/24 via 192.168.12.180
Windows:  10.50.0.0/24 via 10.60.10.1
OPNsense: 192.168.12.172/32 via 10.60.10.254
```

## OPNsense Firewall Scope

```text
KALI_ATTACKER = 192.168.12.172
AEGIS_TARGETS = 10.50.0.10, 10.50.0.20, 10.50.0.30, 10.50.0.40
Action        = Pass
Logging       = Enabled
```

## Validation

- ICMP Kali -> DC01
- Nmap SYN scan against DC01
- ATTACK ingress logging
- LAN egress logging
- persistence across restart
