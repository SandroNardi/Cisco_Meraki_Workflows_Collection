# Update Meraki Local Status Page

## Short description

Roll out consistent local status page settings across tag-filtered Meraki networks in bulk, including whether local and remote status pages are enabled, the local username, and a new password. Password rules are checked up front against Meraki complexity requirements so invalid secrets fail fast before any network is touched. The workflow handles devices that cannot enable a remote status page by retrying with remote disabled when needed, and it continues across per-network failures so you still get a full picture in the result and formatted report. Up to five hundred matching networks per run; narrow tags if your organization exceeds that limit. Requires a Meraki Endpoint target and API key. Passwords are plain text inputs and may appear in run history.

## Prerequisites

- Meraki Dashboard API key (read/write) for the target organization
- Meraki Endpoint target (for example api.meraki.com)
- Password meeting Meraki rules (14+ characters, upper, lower, number, symbol)

## Install

1. Import from **Cisco Workflow / Automation Exchange**.
2. Configure the Meraki Endpoint **Target** and attach your API key.
3. Clear sample defaults (organization, password, tags) before production use.
4. Username defaults to **admin** (local variable); change in the designer if needed.

## Run

1. Select **Update Meraki Local Status Page** and your Meraki target.
2. On the run wizard, provide **Organization Name or ID** and **Autentication Enabled**; set other inputs in the designer or automation payload (**Network Tags**, **Local Status Page Enabled**, **Remote Status Page Enabled**, **Password**, and related fields).
3. After the run, review **Result**, **Formatted Report**, **Status Code**, **Status Message**, **Error Message**, **Workflow Result**, and **Workflow Result Code**.

**Defaults:** **Local Status Page Enabled** and **Remote Status Page Enabled** default to **true**. **Autentication Enabled** defaults to **true** on the run wizard and is written to Meraki **localStatusPage.authentication.enabled** before updates. Username defaults to **admin** (local variable); change in the designer if needed.

## Workflow Result Code

- Early validation or lookup failures: **workflow-errored** (**Workflow Result** mirrors **Status Message**).
- After a bulk run: **completed-successfully** (**200**), **partially-completed** (**207**), or **completed-unsuccessfully** (**500**).

## Status codes and completion

- **200** — Status message **Success**; run completes **Succeeded**; all networks updated.
- **207** — Status message **Partial**; run completes **Failed (partial bulk)**; mix of success and failure—see **Result**.
- **500** — Status message **Failed**; run completes **Failed (total bulk)**; no successes or nothing processed.
- **400** — Status message **Failed**; run completes **Failed (early)**; invalid password, org/list errors, or more than 500 matches.

Early failures populate **Formatted Report** and **Error Message**; the per-network loop does not run.

## Per-network outcomes

- **updated** — HTTP success on standard path.
- **updated_no_remote** — success after retry with remote status page disabled.
- **apply_failed** — update failed; loop continues.

## Security and limits

- **Password** is plain text (not a platform secure string) and may appear in run history and processing details.
- Listing uses pagination; more than **500** matching networks stops the run with **400**—narrow tags and retry.

## API reference

- Update network settings: https://developer.cisco.com/meraki/api-v1/update-network-settings/
- Get organization networks: https://developer.cisco.com/meraki/api-v1/get-organization-networks/

**Contact:** snardi@cisco.com

## Disclaimer

This workflow is community-contributed and provided as-is. It is not a Cisco-supported product. Test in a non-production environment, confirm outcomes on your organizations, and use at your own discretion.
