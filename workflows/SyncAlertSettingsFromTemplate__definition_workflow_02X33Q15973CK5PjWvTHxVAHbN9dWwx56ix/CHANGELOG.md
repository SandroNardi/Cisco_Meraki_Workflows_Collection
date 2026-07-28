# Changelog — Sync Meraki Network Alert Settings

Newest version first.

## v1.0

- Initial publish-ready workflow: sync alert settings from a configuration template to tag-filtered destination networks (merge or replace).
- Webhook ID validation per destination, skip unchanged networks, source-gap reporting for destination-only alert types.
- Per-network loop with continue-on-failure; **Result** JSON and **Formatted Report** from final report script (**Status Code** **200** / **207** / **500** as integers).
- **Dry-Run** defaults to **true**; set **false** to apply API updates.
- Run completes **succeeded** on full success; **failed-completed** on partial (207) or total failure (500) and early validation/lookup failures (400, 404, 422).
- **PUBLISHING.md** with install, run, and outcome guidance for Automation Exchange.
