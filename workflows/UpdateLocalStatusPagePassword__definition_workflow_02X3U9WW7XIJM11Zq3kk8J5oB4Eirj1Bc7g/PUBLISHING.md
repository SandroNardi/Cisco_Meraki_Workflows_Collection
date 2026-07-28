# Update Meraki Local Status Page

Bulk-update local status page settings (enabled flags, username, password) on tag-filtered networks. Password complexity is checked before any API calls. Up to **500** networks per run.

## Prerequisites

- Meraki Dashboard API key (read/write) for the target organization
- Meraki Endpoint target (for example `api.meraki.com`)
- Password meeting Meraki rules (14+ characters, upper, lower, number, symbol)

## Install

1. Import from **Cisco Workflow / Automation Exchange**.
2. Configure the Meraki Endpoint **Target** and attach your API key.
3. Clear sample defaults (organization, password, tags) before production use.
4. Username defaults to `admin` (local variable); change in the designer if needed.

## Run

1. Select **Update Meraki Local Status Page** and your Meraki target.
2. On the run wizard, provide **Organization Name or ID**; set other inputs in the designer or automation payload (tags, enabled flags, password).
3. After the run, review **Result**, **Final Report**, **Status Code**, **Status Message**, and **Error Message**.

**Defaults:** Local and remote status page enabled flags default to **true**. **Local - Allow LSP Access Without Login** (designer variable, default **false**) controls Meraki authentication on the status page (inverted before API calls).

## Status codes and completion

| Code | Status message | Run completes | Meaning |
|------|----------------|---------------|---------|
| 200 | Success | Succeeded | All networks updated |
| 207 | Partial | Failed (partial bulk) | Mix of success and failure—see **Result** |
| 500 | Failed | Failed (total bulk) | No successes or nothing processed |
| 400 | Failed | Failed (early) | Invalid password, org/list errors, or >500 matches |

Early failures populate **Final Report** and **Error Message**; the per-network loop does not run.

## Per-network outcomes

- `updated` — HTTP success on standard path  
- `updated_no_remote` — success after retry with remote status page disabled  
- `apply_failed` — update failed; loop continues  

## Security and limits

- **Password** is plain text (not a platform secure string) and may appear in run history and processing details.
- Listing uses pagination; more than **500** matching networks stops the run with **400**—narrow tags and retry.

## API reference

- [Update network settings](https://developer.cisco.com/meraki/api-v1/update-network-settings/)
- [Get organization networks](https://developer.cisco.com/meraki/api-v1/get-organization-networks/)

**Contact:** snardi@cisco.com

## Disclaimer

This workflow is community-contributed and provided as-is. It is not a Cisco-supported product. Test in a non-production environment, confirm outcomes on your organizations, and use at your own discretion.
