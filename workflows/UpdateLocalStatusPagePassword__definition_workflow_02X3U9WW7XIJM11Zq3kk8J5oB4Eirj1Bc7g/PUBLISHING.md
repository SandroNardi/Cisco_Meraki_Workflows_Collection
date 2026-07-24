# Publishing — Update Meraki Local Status Page

Display name: Update Meraki Local Status Page

Short description: Bulk-update Meraki local status page settings on tag-filtered networks. Sets local and remote enabled flags, username, and password (with local status page authentication enabled) after upfront complexity validation. Retries without remote status page when unsupported. Up to 500 networks per run.

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
4. Clear any sample defaults before production use (Organization, Password, Network Tags). Review enabled-flag defaults (see **Run** below).
5. Username defaults to `admin` via a local workflow variable; edit in the designer if a different username is required.

### Run

1. Open **Workflows** and select **Update Meraki Local Status Page**.
2. Select your Meraki Endpoint target when prompted.
3. Provide inputs (only **Organization Name or ID** is shown on the run wizard by default; set other inputs in the designer or automation payload):
   - **Organization Name or ID** — organization name or numeric ID (run wizard)
   - **Network Tags** — tags to filter networks (empty = all networks)
   - **Local Status Page Enabled** — defaults to **true** if not overridden
   - **Remote Status Page Enabled** — defaults to **true** if not overridden
   - **Password** — local status page password (validated before org lookup; see **Security** below)
4. Click **Run** and monitor the **Runs** page.
5. Review **Result**, **Final Report**, **Status Code**, **Status Message**, and **Error Message**.

### Per-network behavior

- **Update succeeds (HTTP 200)** — recorded as `updated`
- **Remote status page unsupported** — retries with remote disabled; success → `updated_no_remote`, failure → `apply_failed`
- **Other API failure** — recorded as `apply_failed`; loop continues

### Security

- **Password** is a plain text workflow input, not a platform secure string. The value can appear in **in-flight processing details** and in **historic run records** for anyone with access to workflow runs. Restrict run visibility and rotate passwords after use if exposure is a concern.

### Caveats and limitations

- Password complexity is validated before any API calls.
- Maximum **500 networks** per run (platform loop limit). Listing uses Meraki pagination (`perPage` / starting-after) so the **For Each Network** loop stays within the approved workflow range; if a pagination token is returned, more than 500 networks matched and the run fails early with **Status Code** **400** — narrow tag selection and retry.
- **Local Status Page Enabled** and **Remote Status Page Enabled** default to **true** in the workflow definition. Set them explicitly to **false** when you need those pages disabled.
- Local status page **authentication** is set to **enabled** when username and password are applied via the Meraki API payload.
- Per-network API failures do not stop the run; inspect per-network outcomes in **Result**.
- Zero matching networks produces Failed status.
- Does not publish with a specific automation rule or target assigned.

### External links

- [Update network settings](https://developer.cisco.com/meraki/api-v1/update-network-settings/)
- [Get organization networks](https://developer.cisco.com/meraki/api-v1/get-organization-networks/)

### Contact

snardi@cisco.com
