# Audit Organization Settings with Pagination

Read-only audit of Meraki organization security settings (SAML and login security) for every organization your API key can access. Paginated org list (**500** per page), parallel reads per org, continues when individual org calls fail.

## Prerequisites

- Meraki Dashboard API key with read access to organizations to audit
- Meraki Endpoint target

## Install

1. Import from **Cisco Workflow / Automation Exchange**.
2. Configure the Meraki Endpoint **Target** and API key.
3. No run inputs beyond selecting the target.

## Run

1. Select **Audit Organization Settings with Pagination** and your Meraki target.
2. Click **Run** and review **Result**, **Status Code**, **Status Message**, and **Error Message**.

## Status codes and completion

| Code | Status message | Run completes | Meaning |
|------|----------------|---------------|---------|
| 200 | Success | Succeeded | Every org row is `complete` |
| 207 | Partial | Succeeded | Mixed org outcomes—see **Error Message** |
| 500 | Failed | Failed | All org rows failed, empty data, or org list API not HTTP 200 |

Each **Result** row includes `outcome`: `complete`, `partial`, or `failed`, plus error fields when applicable.

## Limits

- Pagination size **500**; pagination loop timeout **900** seconds.
- Read-only—no configuration changes.

## API reference

- [Get organizations](https://developer.cisco.com/meraki/api-v1/get-organizations/)
- [Get organization login security](https://developer.cisco.com/meraki/api-v1/get-organization-login-security/)
- [Get organization SAML](https://developer.cisco.com/meraki/api-v1/get-organization-saml/)

**Contact:** snardi@cisco.com

## Disclaimer

This workflow is community-contributed and provided as-is. It is not a Cisco-supported product. Test in a non-production environment, confirm outcomes on your organizations, and use at your own discretion.
