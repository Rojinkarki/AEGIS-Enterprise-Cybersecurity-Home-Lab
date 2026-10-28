# AEGIS v1 detection artifacts

The two SPL files preserve the original lab searches. They are analyst searches, not a complete saved-search deployment export. No new detection is claimed to have been validated during the portfolio refresh.

## Splunk baseline

| Search | Telemetry / logic | Window and trigger |
|---|---|---|
| [splunk-failed-logins.spl](splunk-failed-logins.spl) | Security Event 4625; count by host; threshold >= 5 | Last 15 minutes, as described in retained configuration; results > 0 |
| [splunk-encoded-powershell.spl](splunk-encoded-powershell.spl) | WS01 Security Event 4688; raw event contains `-encodedcommand` or `-enc` | Use the known test time range; original schedule/window not retained |

Saved titles: `AEGIS - Multiple failed Login Attempts` and `AEGIS - Encoded PowerShell Execution`. Both are enabled in the [overview capture](../Screenshots/06-splunk-alerts-overview.png). The failed-logon [configuration capture](../Screenshots/10-splunk-failed-login-alert-config.png) shows a scheduled alert, threshold description and results > 0; the cron expression is not expanded and no fired events are shown.

Assumptions: extracted `EventCode`, `source="WinEventLog:Security"`, and `host=WS01` for the process search. Confirm those fields in the environment before use. Restrict `index=*` to the actual Windows index when adapting the lab.

Limitations: failed logons are aggregated per host, not per source/account. The encoded-command search matches a raw-text substring and can match unrelated process text or benign administration; it does not prove malicious execution. Audit process creation and include command lines to make 4688 useful. Preserve these baseline queries when reproducing the recorded results, then evaluate any tuning separately.

For source attribution, open underlying 4625 events in the same time range and inspect account, source address, workstation, logon type and authentication package. An aggregate host count alone does not attribute every failure to Kali. [IR-001](../Incident-Reports/IR-001-Multiple-Failed-Logins.md) records the original investigation.

## Wazuh

[Wazuh validation guidance](wazuh-validation.md) records the stock rule used and the distinction between general collection and failed-logon evidence. No custom Wazuh rule is required or claimed here.

## Suricata

[Suricata validation](suricata-validation.md) documents the existing ET Open SID 2100498 test, prior result, latest unsuccessful recapture, and reproduction checks. The third-party ruleset is managed by OPNsense and is not copied into this repository.
