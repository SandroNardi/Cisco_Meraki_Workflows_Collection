# Changelog — Update Meraki Local Status Page

Newest version first.

## v1.1

- Local **Allow LSP Access Without Login** (default **false**); maps to Meraki `localStatusPage.authentication.enabled` (inverted).
- Pagination **500** and early failure when more than 500 networks match.
- Integer **Status Code** (**200** / **207** / **500** bulk; **400** early); completion branches for full, partial, and total bulk failure.
- **Organization Name or ID** on run wizard; loop continues on per-network failures.
- Exchange listing text and workflow description updated (no repository references).

## v1.0

- Initial release: bulk local status page updates with password validation, org resolve, network loop, remote-status retry, **Result** and **Final Report** outputs.
