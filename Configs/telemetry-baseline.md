# Endpoint telemetry baseline

This is a sanitized description of the recorded collection path, not a complete forwarder or agent configuration export.

| Source | Collection / destination | Used by |
|---|---|---|
| DC01 Windows Security log | Splunk Universal Forwarder to SOC01; Wazuh agent to WAZUH01 | Failed-logon investigation, Event 4625 |
| WS01 Windows Security log | Splunk Universal Forwarder to SOC01 | Process creation / Event 4688 detection |
| WS01 Sysmon | Endpoint process telemetry collection in the build baseline | Endpoint investigation |
| DC01 / WS01 Wazuh agents | Wazuh manager/indexer/dashboard on WAZUH01 | Threat hunting and endpoint monitoring |
| OPNsense traffic | Firewall Live View and Suricata IDS | Network corroboration / IDS alerts |

The baseline SPL assumes `source="WinEventLog:Security"`, extracted `EventCode`, and Windows host names. XML event ingestion or different extraction settings can require equivalent source/field names. No index name is invented; the original lab searches use `index=*`.

Event 4688 matching requires process creation auditing and command-line inclusion. These prerequisites are recorded in the build, but their detailed Group Policy export and the triggering event are not retained. Sysmon deployment does not by itself make a Security-log 4688 search work.

The Wazuh screenshot demonstrates agent `dc01-aegis` collection; it does not establish that every agent/module was healthy at the same time. Splunk and Wazuh are normally exercised in separate [resource profiles](../Documentation/vm-resource-plan.md).

Keep Wazuh enrollment/agent keys, Splunk authentication files, tokens, and raw logs outside Git. See [detection assumptions](../Detection-Rules/README.md) and [validation limits](../Documentation/validation.md).
