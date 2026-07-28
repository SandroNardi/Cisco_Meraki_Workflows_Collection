# Changelog — Bulk Network Update or Delete Meraki Webhooks

Newest version first.

## v1.0

- Initial release: bulk webhook create/update/delete by HTTPS URL on networks or templates.
- Preflight validation; per-target loop with continue-on-failure; **Dry-Run** default **true**.
- Integer **Status Code** with separate completion paths for **200**, **207**, and **500**.
- Exchange listing text and workflow description updated (no repository references).
