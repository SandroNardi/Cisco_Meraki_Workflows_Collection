# Changelog — Sync Meraki Network Alert Settings

Newest version first.

## v1.1

- **Result** summary field renamed to `updatedNetworks` (count of `dry_run` + `applied` networks); replaces misleading `sourceGapNetworks`. Per-network `source_gaps` unchanged.
- Completion branches on integer **status_code** from **Format Final Report** (**200** succeeded, **207** partial bulk, **500** total bulk).

## v1.0

- Initial release: template-to-network alert sync (merge/replace), webhook validation, dry-run default **true**, per-network **Result** and **Formatted Report**, integer status codes.
