# Changelog — Update Meraki Local Status Page

Newest version first.

## v1.1

- Added local **Allow LSP Access Without Login** (default **false**, recommended); **Resolve Meraki LSP Auth Flag** maps it to Meraki `localStatusPage.authentication.enabled` (inverted).
- Set **Local - Pagination** to **500** and documented pagination vs platform loop limit; over-limit remains **Status Code** **400**.
- **For Each Network** uses `continue_on_failure: true` for partial bulk runs.
- **Organization Name or ID** shown on run wizard (`display_on_wizard: true`).
- **Status Code** workflow output is integer (**200** / **207** / **500** for bulk outcomes; **400** for validation and early failures); report and loop scripts return integers, not strings.
- Completion branches: **succeeded** on **200**; **failed-completed** on **207** (partial bulk) or **500** (total bulk failure), with distinct completion titles and **Final Report** on completion messages.
- Expanded **PUBLISHING.md** (Exchange import, password visibility, enabled-flag defaults, LSP auth flag, pagination, status codes and run outcomes).

## v1.0

- Initial publish-ready workflow: bulk local status page updates on tag-filtered networks (password complexity check, org resolve, list networks, per-network update with remote-status retry, **Result** / **Final Report** outputs).
- **PUBLISHING.md** with install, run, and per-network outcome notes.
