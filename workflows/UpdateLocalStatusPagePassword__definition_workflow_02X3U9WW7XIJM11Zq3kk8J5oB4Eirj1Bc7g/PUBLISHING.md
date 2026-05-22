# Publishing — Update Meraki Local Status Page

Display name: Update Meraki Local Status Page

Short description: Bulk-update Meraki local status page settings on tag-filtered networks. Sets local and remote enabled flags, username, and password after upfront complexity validation. Retries without remote status page when unsupported. Up to 500 networks per run.

## Installation instructions

### Prerequisites

- Meraki Dashboard API key with read/write access to the target organization
- Meraki Endpoint target (for example `api.meraki.com`)
- Password meeting Meraki complexity rules (minimum 14 characters, uppercase, lowercase, number, symbol)
- Optional network tags to filter destinations

### Import and configure

1. Import the workflow from Git or Automation Exchange.
2. In **Targets**, confirm your Meraki Endpoint target is configured.
3. Attach your Meraki API key to the target.
4. Clear any sample defaults before production use (Organization, Password, Network Tags, enabled flags).
5. Username defaults to `admin` via a local workflow variable; edit in the designer if a different username is required.

### Run

1. Open **Workflows** and select **Update Meraki Local Status Page**.
2. Select your Meraki Endpoint target when prompted.
3. Provide inputs:
   - **Organization Name or ID** — organization name or numeric ID
   - **Network Tags** — tags to filter networks (empty = all networks)
   - **Local Status Page Enabled** — `true` or `false`
   - **Remote Status Page Enabled** — `true` or `false`
   - **Password** — local status page password (validated before org lookup)
4. Click **Run** and monitor the **Runs** page.
5. Review **Result**, **Final Report**, **Status Code**, **Status Message**, and **Error Message**.

### Per-network behavior

- **Update succeeds (HTTP 200)** — recorded as `updated`
- **Remote status page unsupported** — retries with remote disabled; success → `updated_no_remote`, failure → `apply_failed`
- **Other API failure** — recorded as `apply_failed`; loop continues

### Caveats and limitations

- Password complexity is validated before any API calls.
- Maximum 500 networks per run. Narrow tag selection if exceeded.
- Per-network API failures do not stop the run; inspect per-network outcomes in **Result**.
- Zero matching networks produces Failed status.
- Does not publish with a specific automation rule or target assigned.

### External links

- [Update network settings](https://developer.cisco.com/meraki/api-v1/update-network-settings/)
- [Get organization networks](https://developer.cisco.com/meraki/api-v1/get-organization-networks/)

### Contact

snardi@cisco.com
