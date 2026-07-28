# Changelog — Audit Organization Settings with Pagination

Newest version first.

## v1.1

- Per-organization **partial** handling: SAML and login-security calls use `continue_on_failure`; **Accumulate organization audit row** records `outcome` (`complete`, `partial`, `failed`), HTTP status codes, and branch error text without stopping the org loop.
- **Compute run status from audit table** sets run **Status Code** **200** / **207** / **500** with matching **Status Message** and **Error Message** for finalize branches (full success, partial success, bulk failed).
- Partial runs complete as **Succeeded** with **Status Code** **207**; bulk failure uses **failed-completed**.
- Standardized output variable names (**Result**, **Status Message**, **Error Message**, **Status Code**) and consistent **Apply finalize outputs** / org-list failure output steps.
- Workflow description updated (plain-text lead, no markdown in first 130 characters); activity display names clarified.
- **PUBLISHING.md** added for Exchange install and run guidance.

## v1.0

- Initial export: paginated organization list, parallel SAML and login-security reads, JSON **Result** array.
