# Publishing — Bulk Network Update or Delete Meraki Webhooks

Display name: Bulk Network Update or Delete Meraki Webhooks

Short description: Bulk update or delete Meraki webhook HTTP servers across tag-filtered networks or configuration templates by exact URL. Reports per-target outcomes (updated, created, deleted, skipped, failed) in Result and Final Report. Up to 500 targets per run.

## Installation instructions

### Prerequisites

- Meraki Dashboard API key with read/write access to the target organization
- Meraki Endpoint target (for example `api.meraki.com`)
- Exact webhook URL string used to locate the HTTP server on each target
- For update mode: webhook name (required) and optional shared secret
- For delete mode: webhook name must be left empty (matching is by URL only)

### Import and configure

1. Import the workflow from Git or Automation Exchange.
2. In **Targets**, confirm your Meraki Endpoint target is configured.
3. Attach your Meraki API key to the target.
4. Clear any sample defaults before production use (Organization, Mode, Target Type, Webhook URL, Webhook Name).

### Run

1. Open **Workflows** and select **Bulk Network Update or Delete Meraki Webhooks**.
2. Select your Meraki Endpoint target when prompted.
3. Provide inputs:
   - **Organization Name or ID** — organization name or numeric ID
   - **Mode** — `update` or `delete` (case-sensitive)
   - **Target Type** — `networks` or `templates` (case-sensitive)
   - **Network Tag List** — tags to filter networks (networks mode only; empty = all networks)
   - **Webhook URL** — exact URL used to identify the webhook on each target
   - **Webhook Name** — required for `update` mode; must be empty for `delete` mode
   - **Webhook Secret** — optional shared secret for create/update
4. Click **Run** and monitor the **Runs** page.
5. Review **Result**, **Final Report**, **Status Code**, **Status Message**, and **Error Message**.

### Modes

- **update** — If the webhook URL exists, update name and secret. If not found, create the webhook.
- **delete** — If the webhook URL exists, delete it. If not found, skip the target (recorded as skipped).

### Caveats and limitations

- Webhook URL match is exact (including scheme and query string).
- Maximum 500 targets per run (platform loop limit). Narrow tag selection if exceeded.
- Per-target API failures do not stop the run; inspect per-target outcomes in **Result**.
- Mode and Target Type values are case-sensitive.
- Does not publish with a specific automation rule or target assigned.

### External links

- [Get network webhooks HTTP servers](https://developer.cisco.com/meraki/api-v1/get-network-webhooks-http-servers/)
- [Get organization networks](https://developer.cisco.com/meraki/api-v1/get-organization-networks/)
- [Get organization config templates](https://developer.cisco.com/meraki/api-v1/get-organization-config-templates/)

### Contact

snardi@cisco.com
