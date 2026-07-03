# Feature table format

## From a raw list to the table (Phase 0.5 intake)

When the input is a raw list (bullets in chat, notes file) instead of a table, convert it with these rules, then get the user's explicit OK before writing the file:

- **One feature = one deliverable unit.** An item that bundles several deliverables is split into several rows.
- **Merge duplicates and overlapping items** into a single row.
- **Write a one-line description** for each feature; reuse the user's own wording when it is already clear.
- **Keep the user's language** (English or French) for feature names, descriptions and statuses.
- Every row starts as `todo`; the `Clarifications`, `Branch`, `PR` columns are added empty.

### Example

Raw input:

```
- oauth login (google + github)
- export the dashboard as pdf and csv
- pdf export of the dashboard
- make search faster
```

Proposed table (announce: "merged the two PDF export items, split PDF/CSV export into 2 features"):

| Feature | Description | Status | Clarifications | Branch | PR |
|---|---|---|---|---|---|
| OAuth login | Sign in with Google and GitHub | todo | | | |
| Dashboard PDF export | Export the dashboard as PDF | todo | | | |
| Dashboard CSV export | Export the dashboard as CSV | todo | | | |
| Faster search | Improve search performance | todo | | | |

## Minimal columns expected as input

| Feature | Description | Status |
|---|---|---|
| Multi-account OAuth | Allow connecting several social accounts per workspace | todo |
| Dashboard PDF export | Export the KPI dashboard as PDF | todo |

If the user provides a table with only these 3 columns (or even just `Feature` + `Status`), the skill must **enrich the file itself** by adding the missing columns below, editing the Markdown file directly (do not just keep them in memory — they must survive a session interruption/resume).

## Full columns after enrichment

| Feature | Description | Status | Clarifications | Branch | PR |
|---|---|---|---|---|---|
| Multi-account OAuth | Allow connecting several social accounts per workspace | done | Scope: TikTok+Instagram only for v1. One account = one token, auto refresh. Expired token → in-app notification. | feature/multi-account-oauth | #42 |
| Dashboard PDF export | Export the KPI dashboard as PDF | clarified | A4 portrait, workspace logo in header, last 30 days of data only | | |

## Valid statuses (bilingual)

The skill accepts both English and French status values. **Detect which language the user's table uses and keep writing statuses in that same language** — never mix the two in one file.

| English | French | Meaning |
|---|---|---|
| `todo` | `à faire` | Not yet clarified, not yet developed. |
| `clarified` | `clarifiée` | Questions answered, acceptance criteria written, ready for Phase 3. |
| `in progress` | `en cours` | Being developed (transient state during Phase 3; should never remain at the end of a run except after an interruption). |
| `done` | `done` / `terminée` | Branch created, code written and tested, branch closed out per the integration mode chosen in Phase 2 (PR opened, merged locally, or left as-is). |
| `blocked` | `bloquée` | Development hit a real obstacle; see the `Clarifications` column for the reason. |

Matching is case-insensitive and tolerant of close variants (`to do`, `TODO`, `in-progress`, `WIP`, `fait`, `terminé`). When rewriting a status, use the canonical spelling of the table's language from the table above.

## Parsing rules

- Column names may vary slightly (`Status`/`Statut`, `Feature`/`Fonctionnalité`, `Branch`/`Branche`) — match tolerantly on position/meaning rather than exact name, but **keep the user's original column names** when rewriting the file.
- A row with no value in `Status` is treated as `todo`.
- The branch slug (`Branch` column) must be derived from the feature name: lowercase, no accents, spaces → hyphens, no special characters. Example: "Dashboard PDF export" → `feature/dashboard-pdf-export`.
- Always rewrite the complete table file at each status update (no appending outside the table) so it remains the single source of truth, readable at a glance.
