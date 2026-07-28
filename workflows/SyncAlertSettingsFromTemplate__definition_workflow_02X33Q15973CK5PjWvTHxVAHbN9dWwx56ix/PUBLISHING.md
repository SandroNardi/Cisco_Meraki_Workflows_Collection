# Publishing — Sync Meraki Network Alert Settings

Display name: Sync Meraki Network Alert Settings

Short description: Sync alert settings from a Meraki configuration template to tag-filtered destination networks. Validates webhooks, supports merge/replace modes and dry-run, and reports per-network outcomes in Result and Formatted Report. Up to 500 networks per run.

## Installation instructions

### Prerequisites

- Meraki Dashboard API key with read/write access to the target organization
- Meraki Endpoint target (for example `api.meraki.com`)
- A configuration template network as the alert source (golden template)
- Tags on destination networks when scoping the sync (optional—empty tag list processes all org networks, up to the per-run limit)

### Import and configure

1. Import the workflow from Cisco Workflow / Automation Exchange.
2. In **Targets**, confirm your Meraki Endpoint target is configured.
3. Attach your Meraki API key to the target.
4. Set required inputs before production use (**Organization**, **Source Template**, **Destination Tags**, **Sync Mode**). Clear sample defaults where present.

### Run

1. Open **Workflows** and select **Sync Meraki Network Alert Settings**.
2. Select your Meraki Endpoint target when prompted.
3. Provide inputs:
   - **Organization** — name or ID
   - **Source Template** — exact template name (case-sensitive) or numeric template ID
   - **Destination Tags** — tags to filter targets; leave empty to sync all organization networks (500 per-run cap still applies)
   - **Sync Mode** — `merge` or `replace` (case-sensitive; required, no default)
   - **Dry-Run** — `true` to calculate only (default); set `false` to apply changes
4. Click **Run** and monitor the **Runs** page.
5. Review **Result**, **Formatted Report**, **Status Code**, **Status Message**, and **Error Message**.

### Input validation and early failures

- Invalid **Sync Mode** stops with **Status Code** **400** (integer), **Status Message** **Failed**, and **Error Message** describing the issue. **Result** includes a minimal failed summary JSON.
- Organization lookup, source template resolution, destination list, and source alert read failures set **Status Code** from the failing step (for example **404** or **422**) and do not enter the per-network loop.
- Completion is **failed-completed** for these paths; use **Formatted Report** and **Error Message** on the run.

### Run outcome and Status Code

- **Status Code** is an integer HTTP-style outcome: **200** (all networks OK), **207** (partial per-network failures), **500** (total failure or no networks processed).
- **Status Message** **Success** with **200** completes the run as **succeeded**.
- **Partial** (**207**) or **Failed** (**500**) complete as **failed-completed** so operators investigate **Result** and **Formatted Report**.

### Behavior

- Validates required webhook IDs exist on each destination before updating.
- Skips networks that already match the source configuration.
- Alert types present only on the destination (not on source) are kept and noted as source gaps.
- **Dry-Run** `true` calculates changes without calling the update API.

### Caveats and limitations

- Maximum 500 destination networks per run. Narrow tag selection if exceeded.
- Per-network failures set **Status Message** to **Partial** and **Status Code** to **207**, but the workflow run still **fails** on purpose so operators see that something went wrong. Use **Result** and **Formatted Report** for per-network detail.
- **Dry-Run** is not shown at install (default `true` for safety). Change it on each run when you intend to apply updates.
- Sync Mode values are case-sensitive (`merge`, `replace`).
- Re-running with **Dry-Run** `true` applies no changes (expected).
- Does not publish with a specific automation rule or target assigned.

### External links

- [Get network alerts settings](https://developer.cisco.com/meraki/api-v1/get-network-alerts-settings/)
- [Get organization networks](https://developer.cisco.com/meraki/api-v1/get-organization-networks/)

### Contact

snardi@cisco.com
