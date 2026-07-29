# Sync Meraki Network Alert Settings

## Short description

Align alert settings across your Meraki organization by copying from a trusted configuration template network to destinations you select with tags. Choose merge to combine template settings with what each network already has, or replace to overwrite destination alert configuration while keeping alert types that exist only on the destination. The workflow validates webhook references before updates, skips networks that already match, and defaults to dry-run so you can see what would change. Per-network outcomes roll up into JSON summary counts and a formatted report, with status codes that distinguish clean success, partial failures, and early validation or lookup errors. Up to five hundred networks per run. Requires a Meraki Endpoint target, API key, and a source template in the same organization.

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
2. Provide **Organization**, **Source Template**, **Destination Tags** (empty = all org networks, still capped at 500), **Sync Mode** (merge or replace, case-sensitive), and **Dry-Run** (set false to apply changes).
3. Review **Result**, **Formatted Report**, **Status Code**, **Status Message**, and **Error Message**.

## Result JSON summary

- **updatedNetworks** — Networks that would be updated (**Dry-Run** true, outcome dry_run) or were updated (**Dry-Run** false, outcome applied).
- **counts** — Per-outcome totals: dryRun, applied, noChange, invalid, applyFailed.
- **networks** — One row per destination; **source_gaps** lists alert types on the destination not on the template (informational; does not affect **updatedNetworks**).

## Status codes and completion

- **200** — Status message **Success**; run completes **Succeeded**; all destinations handled successfully.
- **207** — Status message **Partial**; run completes **Failed (partial bulk)**; some per-network failures—see **Result**.
- **500** — Status message **Failed**; run completes **Failed (total bulk)**; no successes or nothing processed.
- **400**, **404**, or **422** — Status message **Failed**; run completes **Failed (early)**; validation or lookup/read failure before the loop.

## Behavior notes

- Skips destinations that already match the source; validates webhook IDs before update.
- Destination-only alert types are kept; each network row may list them in **source_gaps** (separate from summary **updatedNetworks**).
- **Dry-Run** is hidden at install (defaults **true**); set **false** when applying changes.

## API reference

- Get network alerts settings: https://developer.cisco.com/meraki/api-v1/get-network-alerts-settings/
- Get organization networks: https://developer.cisco.com/meraki/api-v1/get-organization-networks/

**Contact:** snardi@cisco.com

## Disclaimer

This workflow is community-contributed and provided as-is. It is not a Cisco-supported product. Test in a non-production environment, confirm outcomes on your organizations, and use at your own discretion.
