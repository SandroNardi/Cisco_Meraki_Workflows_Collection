# Audit Organization Settings with Pagination

## Short description

Gather a read-only snapshot of login and SAML security settings for every Meraki organization your API key can reach, without changing anything in the dashboard. Organizations are listed with pagination and processed in parallel, and the workflow keeps going when an individual organization call fails so one bad row does not stop the audit. Each organization in the result includes an outcome of complete, partial, or failed along with the settings the API returned or error detail when something went wrong. Status codes summarize whether every row succeeded, some mixed results need review, or the run failed entirely. No run inputs beyond selecting your Meraki target. Requires read access via API key. Pagination is capped at five hundred organizations per page with a generous loop timeout for large estates.

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

- **200** — Status message **Success**; run completes **Succeeded**; every org row is **complete**.
- **207** — Status message **Partial**; run completes **Succeeded**; mixed org outcomes—see **Error Message**.
- **500** — Status message **Failed**; run completes **Failed**; all org rows failed, empty data, or org list API not HTTP 200.

Each **Result** row includes **outcome** **complete**, **partial**, or **failed**, plus error fields when applicable.

## Limits

- Pagination size **500**; pagination loop timeout **900** seconds.
- Read-only—no configuration changes.

## API reference

- Get organizations: https://developer.cisco.com/meraki/api-v1/get-organizations/
- Get organization login security: https://developer.cisco.com/meraki/api-v1/get-organization-login-security/
- Get organization SAML: https://developer.cisco.com/meraki/api-v1/get-organization-saml/

**Contact:** snardi@cisco.com

## Disclaimer

This workflow is community-contributed and provided as-is. It is not a Cisco-supported product. Test in a non-production environment, confirm outcomes on your organizations, and use at your own discretion.
