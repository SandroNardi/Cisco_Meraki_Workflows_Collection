# Bulk Network Update or Delete Meraki Webhooks

## Short description

Create, update, or delete Meraki webhook HTTP servers across many networks or configuration templates in one run. You point the workflow at an organization, choose whether to work on tag-filtered networks or templates, and identify webhooks by an exact HTTPS URL so matching stays predictable. Preflight checks run before any organization lookup, and dry-run defaults to on so you can preview creates, updates, skips, and deletes before committing changes. Each target is processed individually with continue-on-failure behavior, and you get structured results plus a readable report with clear status codes for full success, partial bulk outcomes, or total failure. Up to five hundred targets per run. Requires a Meraki Endpoint target and an API key with appropriate write access. Webhook secrets are supplied as plain text and may appear in run history.

## Prerequisites

- Meraki Dashboard API key (read/write)
- Meraki Endpoint target
- Exact webhook URL (HTTPS) on each target

For **update**: **Webhook Name** required; **Webhook Secret** optional. For **delete**: **Webhook Name** and **Webhook Secret** must be empty.

## Install

1. Import from **Cisco Workflow / Automation Exchange**.
2. Configure the Meraki Endpoint **Target** and API key.
3. Set **Operation**, **Target Type**, **Webhook URL**, and related fields—no defaults on operation or target type.

## Run

1. Select **Bulk Network Update or Delete Meraki Webhooks** and your Meraki target.
2. Provide **Organization Name or ID** (run wizard) and remaining inputs in the designer or payload: **Operation** (update or delete), **Target Type** (networks or templates), **Network Tag List**, **Webhook URL**, **Webhook Name**, **Webhook Secret**, **Dry-Run**.
3. Review **Result**, **Final Report**, **Status Code**, **Status Message**, and **Error Message**.

## Status codes and completion

- **200** — Status message **Success**; run completes **Succeeded**; every processed target OK.
- **207** — Status message **Partial**; run completes **Failed (partial bulk)**; mix of OK and failed targets.
- **500** — Status message **Failed**; run completes **Failed (total bulk)**; no OK targets or none processed.
- **400** — Status message **Failed**; run completes **Failed (early)**; input validation failed.
- **422** (typical) — Status message **Failed**; run completes **Failed (early)**; org lookup or list limit failure.

Per-target OK outcomes: **updated**, **created**, **deleted**, **skipped**. Failures: **get_failed**, **apply_failed**.

## Operations

- **update** — Update matching URL; create if missing.  
- **delete** — Delete matching URL; skip if absent.  
- **templates** — Uses template IDs in the network webhooks APIs; **Network Tag List** is ignored.

## Security and limits

- **Webhook Secret** is plain text and may appear in run history.
- URL match is exact (scheme, host, path, query). Only **https** passes validation.

## API reference

- Get network webhooks HTTP servers: https://developer.cisco.com/meraki/api-v1/get-network-webhooks-http-servers/
- Get organization networks: https://developer.cisco.com/meraki/api-v1/get-organization-networks/
- Get organization config templates: https://developer.cisco.com/meraki/api-v1/get-organization-config-templates/

**Contact:** snardi@cisco.com

## Disclaimer

This workflow is community-contributed and provided as-is. It is not a Cisco-supported product. Test in a non-production environment, confirm outcomes on your organizations, and use at your own discretion.
