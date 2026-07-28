# Publishing — Audit Organization Settings with Pagination

Display name: Audit Organization Settings with Pagination

Short description: Read-only audit of Meraki organization security settings (API access, SAML SSO, login security) for every organization the API key can reach. Paginated org listing (500 per page), parallel per-org API calls, partial per-org failures allowed.

## Installation instructions

### Prerequisites

- Meraki Dashboard API key with read access to the organizations to audit
- Meraki Endpoint target (for example `api.meraki.com`)

### Import and configure

1. Import the workflow from Cisco Workflow / Automation Exchange.
2. In **Targets**, confirm your Meraki Endpoint target is configured.
3. Attach your Meraki API key to the target.
4. No run-time inputs are required beyond selecting the target.

### Run

1. Open **Workflows** and select **Audit Organization Settings with Pagination**.
2. Select your Meraki Endpoint target when prompted.
3. Click **Run** and monitor the **Runs** page.
4. Review **Result**, **Status Code**, **Status Message**, and **Error Message**.

### Per-organization behavior

Each **Result** row includes `outcome`:

- **complete** — SAML and login security settings retrieved (HTTP 200 on both).
- **partial** — one of the two settings calls succeeded; the failed call adds `samlError` or `loginSecurityError` and the non-200 status code field.
- **failed** — both settings calls failed; error details are recorded on the row.

The loop continues after per-organization failures (`continue_on_failure` on **For Each Organization** and on the Meraki get-settings atomics).

### Run-level outcomes

| Status Code | Status Message | Workflow completion | Meaning |
|-------------|----------------|---------------------|---------|
| 200 | Success | Succeeded | Every organization row is `complete`. |
| 207 | Partial | Succeeded | At least one org is `complete` or `partial`; see **Error Message** for counts. |
| 500 | Failed | Failed (bulk) or Failed (empty) | All org rows `failed`, or no data collected, or organization list API not HTTP 200. |

Organization list failure sets **Result** to `[]`, **Status Message** Failed, **Status Code** from the list atomic, and **Error Message** from the atomic.

### Caveats and limitations

- **Local - Queries per Page** is **500** (Meraki pagination size).
- Pagination **while** loop **action timeout** is **900** seconds.
- Parallel SAML and login-security calls run per organization for speed.
- Read-only; no configuration changes are made.
- Does not publish with a specific automation rule or target assigned.

### External links

- [Get organizations](https://developer.cisco.com/meraki/api-v1/get-organizations/)
- [Get organization login security](https://developer.cisco.com/meraki/api-v1/get-organization-login-security/)
- [Get organization SAML](https://developer.cisco.com/meraki/api-v1/get-organization-saml/)

### Contact

snardi@cisco.com
