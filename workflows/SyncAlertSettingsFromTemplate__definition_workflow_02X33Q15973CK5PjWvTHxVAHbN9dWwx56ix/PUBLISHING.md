# Sync Meraki Network Alert Settings

Copy alert settings from a configuration template network to tag-filtered destinations. Supports **merge** / **replace**, webhook validation, and **dry-run** (default **true**). Up to **500** networks per run.

## Prerequisites

- Meraki Dashboard API key (read/write)
- Meraki Endpoint target
- Source template (exact name or numeric ID) in the same organization

## Install

1. Import from **Cisco Workflow / Automation Exchange**.
2. Configure the Meraki Endpoint **Target** and API key.
3. Set **Organization**, **Source Template**, **Sync Mode**, and tags before production runs.

## Run

1. Select **Sync Meraki Network Alert Settings** and your Meraki target.
2. Provide **Organization**, **Source Template**, **Destination Tags** (empty = all org networks, still capped at 500), **Sync Mode** (`merge` or `replace`, case-sensitive), and **Dry-Run** (`false` to apply changes).
3. Review **Result**, **Formatted Report**, **Status Code**, **Status Message**, and **Error Message**.

## Status codes and completion

| Code | Status message | Run completes | Meaning |
|------|----------------|---------------|---------|
| 200 | Success | Succeeded | All destinations handled successfully |
| 207 | Partial | Failed (partial bulk) | Some per-network failures—see **Result** |
| 500 | Failed | Failed (total bulk) | No successes or nothing processed |
| 400 / 404 / 422 | Failed | Failed (early) | Validation or lookup/read failure before the loop |

## Behavior notes

- Skips destinations that already match the source; validates webhook IDs before update.
- Destination-only alert types are kept and noted as source gaps.
- **Dry-Run** is hidden at install (defaults **true**); set **false** when applying changes.

## API reference

- [Get network alerts settings](https://developer.cisco.com/meraki/api-v1/get-network-alerts-settings/)
- [Get organization networks](https://developer.cisco.com/meraki/api-v1/get-organization-networks/)

**Contact:** snardi@cisco.com

## Disclaimer

This workflow is community-contributed and provided as-is. It is not a Cisco-supported product. Test in a non-production environment, confirm outcomes on your organizations, and use at your own discretion.
