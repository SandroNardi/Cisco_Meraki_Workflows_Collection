# Changelog — Bulk Network Update or Delete Meraki Webhooks

Newest version first.

## v1.0

- Initial publish-ready workflow: bulk Meraki webhook create/update/delete by exact HTTPS URL on tag-filtered networks or configuration templates.
- Preflight input validation (Operation, Target Type, Webhook URL, Webhook Name/Secret rules).
- Per-target loop with continue-on-failure; **Result** JSON and **Final Report** from report script (200 / 207 / 500).
- **Dry-Run** defaults to **true** for safe first runs; set **false** to apply mutations.
- Separate completion branches for full success, partial bulk failure (207), and total bulk failure (500).
- **PUBLISHING.md** with install, run, and outcome guidance for Automation Exchange.
