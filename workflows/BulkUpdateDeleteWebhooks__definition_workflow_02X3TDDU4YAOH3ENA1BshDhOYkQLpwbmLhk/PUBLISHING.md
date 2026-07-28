# Publishing — Bulk Network Update or Delete Meraki Webhooks

Display name: Bulk Network Update or Delete Meraki Webhooks

Short description: Bulk update or delete Meraki webhook HTTP servers across tag-filtered networks or configuration templates by exact HTTPS URL. Validates inputs before org lookup; reports per-target outcomes (`updated`, `created`, `deleted`, `skipped`, `get_failed`, `apply_failed`) in **Result** and **Final Report**. Up to 500 targets per run.

## Installation instructions

### Prerequisites

- Meraki Dashboard API key with read/write access to the target organization
- Meraki Endpoint target (for example `api.meraki.com`)
- Exact **HTTPS** webhook URL string used to locate the HTTP server on each target
- For **Operation** `update`: **Webhook Name** (required) and optional **Webhook Secret**
- For **Operation** `delete`: **Webhook Name** must be empty (matching is by URL only)

### Import and configure

1. Import the workflow from Cisco Workflow / Automation Exchange.
2. In **Targets**, confirm your Meraki Endpoint target is configured.
3. Attach your Meraki API key to the target.
4. Set required inputs before production use (**Organization Name or ID**, **Operation**, **Target Type**, **Webhook URL**, **Webhook Name** as applicable). **Operation** and **Target Type** have no default values.

### Run

1. Open **Workflows** and select **Bulk Network Update or Delete Meraki Webhooks**.
2. Select your Meraki Endpoint target when prompted.
3. Provide inputs (all case-sensitive where noted):
   - **Organization Name or ID** — organization name or numeric ID (shown on the run wizard; other inputs are set in the designer or automation payload)
   - **Operation** — `update` or `delete` (required)
   - **Target Type** — `networks` or `templates` (required)
   - **Network Tag List** — tags to filter networks when **Target Type** is `networks` (empty = all networks in scope)
   - **Webhook URL** — exact HTTPS URL used to identify the webhook on each target
   - **Webhook Name** — required when **Operation** is `update`; must be empty when **Operation** is `delete`
   - **Webhook Secret** — optional shared secret for create/update (see **Security** below)
   - **Dry-Run** — defaults to **true** (safe preview). Set to **false** to perform create, update, or delete API calls
4. Click **Run** and monitor the **Runs** page.
5. Review **Result**, **Final Report**, **Status Code**, **Status Message**, and **Error Message**.

### Input validation (preflight)

Before organization lookup, the **Input validation** group checks (first failure stops the run):

- **Operation** is `update` or `delete`
- **Target Type** is `networks` or `templates`
- **Webhook URL** is present and a valid **HTTPS** URL
- **Webhook Name** required on `update`; on `delete`, **Webhook Name** and **Webhook Secret** must be empty

If validation fails, the run stops with **Status Code** **400**, **Status Message** **Failed**, **Error Message** describing the issue, and a short **Final Report** line. **Result** stays empty; the processing loop does not run. Completion is **failed-completed** (same as organization lookup failure).

### Operations

- **update** — If the webhook URL exists on the target, update name and secret. If the URL is not found, **create** the webhook on that target.
- **delete** — If the webhook URL exists, delete it. If not found, skip the target (recorded as **skipped**).

### Target Type `templates`

- When **Target Type** is `templates`, the workflow lists organization configuration templates and processes each template ID in the same per-target loop used for **networks**.
- List, create, update, and delete steps use the Meraki **network** webhooks HTTP server APIs with each template ID as the target identifier (validated in production testing).
- **Network Tag List** is ignored when **Target Type** is `templates`.

### Dry-Run (default on)

- **Dry-Run** defaults to **true** so first imports and test runs do not mutate webhooks. Set **Dry-Run** to **false** when you intend to apply changes.
- When **Dry-Run** is **true**, the workflow runs organization lookup, target discovery, and webhook listing; apply steps are simulated, not sent to the API.
- Per-target rows report what would happen (`updated`, `created`, `deleted`, or `skipped`). Messages use **Would … (dry-run - no changes applied)** where applicable; **Final Report** includes a **Dry-Run** line.

### Partial success and run completion

- The run **continues** when individual targets fail (list/get or apply errors). Inspect per-target rows in **Result** and **Final Report**.
- OK per-target outcomes: `updated`, `created`, `deleted`, `skipped`. Failure outcomes include `get_failed` and `apply_failed`.
- **Status Message** **Success** only when every processed target has an OK outcome (**Status Code** **200**); workflow completion **succeeded**.
- **Status Message** **Partial** when at least one target succeeded and at least one failed — **Status Code** **207**. For bulk update/delete, partial completion is treated as a failed run (**failed-completed**); see **Error Message** and **Final Report**.
- **Status Message** **Failed** when no targets succeeded or none were processed — **Status Code** **500**; completion **failed-completed**.
- Input validation failures use **failed-completed** with **Status Code** **400**. Organization lookup or target-list limit failures use **422** (or related codes from those steps) and do not enter the per-target loop.

### Security

- **Webhook Secret** is a plain text workflow input, not a platform secure string. The value can appear in **in-flight processing details** and in **historic run records** for anyone with access to workflow runs. Do not use if information exposure in the dashboard is a concern.

### Caveats and limitations

- **Webhook URL** match is exact (scheme, host, path, and query string). Only **https** URLs pass preflight validation.
- Maximum **500 targets** per run (platform loop limit). Narrow **Network Tag List** or scope if exceeded.
- Per-target API failures do not stop the run; inspect **Result** for each target.
- **Operation**, **Target Type**, and keyword values are case-sensitive.
- Does not publish with a specific automation rule or target assigned.

### External links

- [Get network webhooks HTTP servers](https://developer.cisco.com/meraki/api-v1/get-network-webhooks-http-servers/)
- [Get organization networks](https://developer.cisco.com/meraki/api-v1/get-organization-networks/)
- [Get organization config templates](https://developer.cisco.com/meraki/api-v1/get-organization-config-templates/)

### Contact

snardi@cisco.com
