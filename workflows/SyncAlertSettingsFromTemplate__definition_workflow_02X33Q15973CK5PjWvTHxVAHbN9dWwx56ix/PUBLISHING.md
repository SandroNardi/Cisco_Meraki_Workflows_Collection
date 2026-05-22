# Publishing — Sync Meraki Network Alert Settings

Display name: Sync Meraki Network Alert Settings

Short description: Sync alert settings from a Meraki configuration template to tag-filtered destination networks. Validates webhooks, supports merge/replace modes and dry-run emulation, and reports per-network outcomes in Result and Formatted Report. Up to 500 networks per run.

## Installation instructions

### Prerequisites

- Meraki Dashboard API key with read/write access to the target organization
- Meraki Endpoint target (for example `api.meraki.com`)
- A configuration template network as the alert source (golden template)
- Tags applied to destination networks that should receive the sync

### Import and configure

1. Import the workflow from Git or Automation Exchange.
2. In **Targets**, confirm your Meraki Endpoint target is configured.
3. Attach your Meraki API key to the target.
4. Clear any sample defaults before production use (Organization, Source Template, Destination Tags).

### Run

1. Open **Workflows** and select **Sync Meraki Network Alert Settings**.
2. Select your Meraki Endpoint target when prompted.
3. Provide inputs:
   - **Organization** — name or ID
   - **Source Template** — template network name or ID
   - **Destination Tags** — tags used to find target networks
   - **Sync Mode** — `merge` or `replace` (case-sensitive)
   - **Emulation Mode** — `true` for dry-run (default); set `false` to apply changes
4. Click **Run** and monitor the **Runs** page.
5. Review **Result**, **Formatted Report**, **Status Code**, **Status Message**, and **Error Message**.

### Behavior

- Validates required webhook IDs exist on each destination before updating.
- Skips networks that already match the source configuration.
- Alert types present only on the destination (not on source) are kept and noted as source gaps.
- Emulation Mode `true` calculates changes without calling the update API.

### Caveats and limitations

- Maximum 500 destination networks per run. Narrow tag selection if exceeded.
- Per-network failures produce Partial status; inspect per-network outcomes in **Result**.
- Sync Mode values are case-sensitive (`merge`, `replace`).
- Re-running with Emulation Mode `true` applies no changes (expected for dry-run).
- Does not publish with a specific automation rule or target assigned.

### External links

- [Get network alerts settings](https://developer.cisco.com/meraki/api-v1/get-network-alerts-settings/)
- [Get organization networks](https://developer.cisco.com/meraki/api-v1/get-organization-networks/)

### Contact

snardi@cisco.com
