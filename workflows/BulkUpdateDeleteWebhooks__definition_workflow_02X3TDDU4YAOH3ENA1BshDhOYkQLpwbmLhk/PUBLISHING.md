# Bulk Network Update or Delete Meraki Webhooks

Create, update, or delete Meraki webhook HTTP servers by exact **HTTPS URL** across tag-filtered **networks** or **configuration templates**. Preflight validation runs before org lookup. Up to **500** targets per run; **Dry-Run** defaults to **true**.

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
2. Provide **Organization Name or ID** (run wizard) and remaining inputs in the designer or payload: **Operation** (`update` / `delete`), **Target Type** (`networks` / `templates`), **Network Tag List**, **Webhook URL**, **Webhook Name**, **Webhook Secret**, **Dry-Run**.
3. Review **Result**, **Final Report**, **Status Code**, **Status Message**, and **Error Message**.

## Status codes and completion

| Code | Status message | Run completes | Meaning |
|------|----------------|---------------|---------|
| 200 | Success | Succeeded | Every processed target OK |
| 207 | Partial | Failed (partial bulk) | Mix of OK and failed targets |
| 500 | Failed | Failed (total bulk) | No OK targets or none processed |
| 400 | Failed | Failed (early) | Input validation failed |
| 422 (typical) | Failed | Failed (early) | Org lookup or list limit failure |

Per-target OK outcomes: `updated`, `created`, `deleted`, `skipped`. Failures: `get_failed`, `apply_failed`.

## Operations

- **update** — Update matching URL; create if missing.  
- **delete** — Delete matching URL; skip if absent.  
- **templates** — Uses template IDs in the network webhooks APIs; **Network Tag List** is ignored.

## Security and limits

- **Webhook Secret** is plain text and may appear in run history.
- URL match is exact (scheme, host, path, query). Only **https** passes validation.

## API reference

- [Get network webhooks HTTP servers](https://developer.cisco.com/meraki/api-v1/get-network-webhooks-http-servers/)
- [Get organization networks](https://developer.cisco.com/meraki/api-v1/get-organization-networks/)
- [Get organization config templates](https://developer.cisco.com/meraki/api-v1/get-organization-config-templates/)

**Contact:** snardi@cisco.com

## Disclaimer

This workflow is community-contributed and provided as-is. It is not a Cisco-supported product. Test in a non-production environment, confirm outcomes on your organizations, and use at your own discretion.
