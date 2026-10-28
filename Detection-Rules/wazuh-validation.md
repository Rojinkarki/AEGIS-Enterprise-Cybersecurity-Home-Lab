# Wazuh authentication validation

The original IR-001 build record reports:

- Agent: `dc01-aegis`
- Rule ID: `60122`
- Description: `Logon Failure - Unknown user or bad password`
- Windows Security Event: `4625`
- Target: DC01; source: `192.168.12.172`

This is an existing Wazuh rule result, not a custom rule authored for the project. To investigate a repeated authorized exercise, select its time range in Threat Hunting and filter `agent.name:dc01-aegis` and `rule.id:60122`; inspect the underlying event for source, account and logon fields rather than relying on the rule title alone.

The retained [telemetry screenshot](../Screenshots/07-wazuh-dc01-telemetry.png) shows collection and logon/logoff events, not a matching 60122 event. The [vulnerability-event screenshot](../Screenshots/09-wazuh-vulnerability-events.png) demonstrates a separate module's events and is not authentication or exploit evidence. See [IR-001](../Incident-Reports/IR-001-Multiple-Failed-Logins.md) for the historical finding and evidence qualifications.
