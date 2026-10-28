# Sanitized configuration references

These files describe the final recorded AEGIS v1 build. They are human-readable references, not complete exports or automatic deployment packages.

| Reference | Contents |
|---|---|
| [network-routing.md](network-routing.md) | Persistent route values, Kali reconstruction example, Windows inspection, OPNsense return path |
| [opnsense-attack-policy.md](opnsense-attack-policy.md) | Interface/alias policy, source retention, verification limits |
| [telemetry-baseline.md](telemetry-baseline.md) | Endpoint collection and audit prerequisites for the baseline searches |

Lab-private addresses and the reserved `.test` domain are intentional. Full OPNsense backups, NetworkManager Wi-Fi profiles, Wazuh agent keys and Splunk authentication files are excluded because they can contain credentials. Follow the [validation record](../Documentation/validation.md) for what was actually retained and tested.
