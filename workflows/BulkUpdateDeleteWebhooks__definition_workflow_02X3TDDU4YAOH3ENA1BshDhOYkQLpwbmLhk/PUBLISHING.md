# Publishing — Bulk Network Update or Delete Meraki Webhooks

Display name: Bulk Network Update or Delete Meraki Webhooks

Short description: Bulk update or delete Meraki webhook HTTP servers across tag-filtered networks or configuration templates by exact URL. Reports per-target outcomes (updated, created, deleted, skipped, failed) in Result and Final Report. Up to 500 targets per run.

## Installation instructions

### Prerequisites

- Meraki Dashboard API key with read/write access to the target organization
- Meraki Endpoint target (for example `api.meraki.com`)
- Exact webhook URL string used to locate the HTTP server on each target
- For `update` operation: webhook name (required) and optional shared secret
- For `delete` operation: webhook name must be left empty (matching is by URL only)

### Import and configure

1. Import the workflow from Git or Automation Exchange.
2. In **Targets**, confirm your Meraki Endpoint target is configured.
3. Attach your Meraki API key to the target.
4. Clear any sample defaults before production use (Organization, Operation, Target Type, Webhook URL, Webhook Name).

### Run

1. Open **Workflows** and select **Bulk Network Update or Delete Meraki Webhooks**.
2. Select your Meraki Endpoint target when prompted.
3. Provide inputs:
   - **Organization Name or ID** — organization name or numeric ID
   - **Operation** — `update` or `delete` (case-sensitive)
   - **Target Type** — `networks` or `templates` (case-sensitive)
   - **Network Tag List** — tags to filter networks (networks only; empty = all networks)
   - **Webhook URL** — exact URL used to identify the webhook on each target
   - **Webhook Name** — required for `update`; must be empty for `delete`
   - **Webhook Secret** — optional shared secret for create/update (see **Security** below)
   - **Dry-Run** — set to `true` to preview expected outcomes without applying update/create/delete changes
4. Click **Run** and monitor the **Runs** page.
5. Review **Result**, **Final Report**, **Status Code**, **Status Message**, and **Error Message**.

### Operations

- **update** — If the webhook URL exists, update name and secret. If not found, create the webhook on that target.
- **delete** — If the webhook URL exists, delete it. If not found, skip the target (recorded as skipped).

### Target Type `templates`

- When **Target Type** is `templates`, the workflow lists organization configuration templates and processes each template ID in the same per-target loop used for networks.
- List, create, update, and delete steps use the Meraki **network** webhooks HTTP server APIs with each template ID as the target identifier (validated in production testing).
- **Network Tag List** is ignored for `templates`.

### Dry-Run

- Set **Dry-Run** to `true` to run organization lookup, target discovery, and webhook listing only.
- The workflow reports what **would** happen (`updated`, `created`, `deleted`, or `skipped`) without calling update/create/delete APIs.
- Per-target messages are prefixed with **Would … (dry-run — no changes applied)** and **Final Report** includes a Dry-Run banner.

### Partial success and run completion

- The run **continues** when individual targets fail (list/get or apply errors). Inspect per-target rows in **Result** and **Final Report**.
- **Status Message** is **Success** only when every processed target has an OK outcome (`updated`, `created`, `deleted`, or `skipped`).
- **Status Message** **Partial** when at least one target succeeded and at least one failed — **Status Code** **207**.
- **Status Message** **Failed** when no targets succeeded or none were processed — **Status Code** **500**.
- For **Partial** or **Failed** bulk outcomes, the workflow run still **finishes** and writes **Result** / **Final Report**, but run completion is **failed-completed** (not **succeeded**). Treat **207** + **Partial** as a completed run with mixed results, not a full success.
- Early validation or org/target discovery failures use **failed-completed** with **Status Code** **400** or **422** and do not enter the processing loop.

### Security

- **Webhook Secret** is a plain text workflow input, not a platform secure string. The secret value can appear in **in-flight processing details** and in **historic run records** for anyone with access to workflow runs. Limit run-history access and rotate secrets if exposure is a concern.

### Caveats and limitations

- Webhook URL match is exact (including scheme and query string).
- Maximum 500 targets per run (platform loop limit). Narrow tag selection if exceeded.
- Per-target API failures do not stop the run; inspect per-target outcomes in **Result**.
- Operation and Target Type values are case-sensitive.
- Does not publish with a specific automation rule or target assigned.

### External links

- [Get network webhooks HTTP servers](https://developer.cisco.com/meraki/api-v1/get-network-webhooks-http-servers/)
- [Get organization networks](https://developer.cisco.com/meraki/api-v1/get-organization-networks/)
- [Get organization config templates](https://developer.cisco.com/meraki/api-v1/get-organization-config-templates/)

### Contact

snardi@cisco.com
