# Changelog — Audit Organization Settings with Pagination

Newest version first.

## v1.1

- Per-org **partial** outcomes; run **Status Code** **200** / **207** / **500** with finalize branches.
- Partial runs (**207**) complete as **Succeeded**; bulk failure (**500**) as **failed-completed**.
- Standardized outputs (**Result**, **Status Code**, **Status Message**, **Error Message**).
- **Workflow Result** and **Workflow Result Code** populated according to documentation

## v1.0

- Initial release: paginated organization list, parallel SAML and login-security reads, JSON **Result** array.
