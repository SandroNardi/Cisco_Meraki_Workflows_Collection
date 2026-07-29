# Changelog — Update Meraki Local Status Page

Newest version first.

## v1.1

- **Workflow Result** and **Workflow Result Code** on every exit path: **workflow-errored** on early failures; **completed-successfully**, **partially-completed**, or **completed-unsuccessfully** after bulk report (**200** / **207** / **500**).
- Human-readable output renamed to **Formatted Report** (activity title **Build Final Report** unchanged).
- Run wizard input **Autentication Enabled** (default **true**) maps to Meraki **localStatusPage.authentication.enabled**; separate inputs **Local Status Page Enabled** and **Remote Status Page Enabled** (both default **true**).
- Pagination **500** and early failure when more than 500 networks match.
- Integer **Status Code** (**200** / **207** / **500** bulk; **400** early); completion branches for full, partial, and total bulk failure.
- **Organization Name or ID** on run wizard; loop continues on per-network failures.

## v1.0

- Initial release: bulk local status page updates with password validation, org resolve, network loop, remote-status retry, **Result** and report outputs.
