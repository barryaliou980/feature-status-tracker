# Design — Phase 0.5: Intake of a raw feature list

Date: 2026-07-02 · Status: approved by Aliou · Version target: 1.1.0

## Goal

Let users start the feature-status-tracker pipeline from a raw list of features
(bullet points pasted in chat, or a notes file) instead of requiring a
pre-formatted Markdown table. The skill converts the list into `FEATURES.md`,
gets explicit user validation, then chains directly into the existing
clarification pipeline.

## Decisions (from brainstorming)

- **Sources:** list pasted in chat, or an existing notes file the user points to.
  (Free-form prose extraction accepted only as a side effect: actionable items
  become features, the rest is ignored and flagged.)
- **Conversion level:** light restructuring — split items that contain several
  deliverables, merge duplicates/overlaps, write a one-line description per
  feature. Keep the user's language (EN/FR) and wording when clear. All rows
  start as `todo`.
- **Validation gate:** the proposed table is shown in chat, with an explicit
  list of splits/merges, BEFORE any file is written. The user validates or
  corrects. Only then is `FEATURES.md` written.
- **Chaining:** after the file is written, Phase 1 (clarification) starts
  immediately — one end-to-end flow.
- **Architecture:** integrated as "Phase 0.5" inside the existing skill
  (option A). No separate skill, no separate plugin: one flow, no duplicated
  table-format knowledge, no extra per-session token cost.

## Routing rule

Phase 0.5 runs only when no feature table exists yet (neither in a file nor in
the conversation). If a table already exists — including a notes file that
already contains one — skip straight to Phase 1 (current behavior unchanged).

## Edge cases

- Empty or single-item list → direct conversion, no restructuring.
- More than ~20 items → suggest splitting into several runs.
- Prose mixed with the list → only actionable items become features; the
  ignored remainder is mentioned to the user.

## Files touched

- `skills/feature-status-tracker/SKILL.md` — frontmatter description trigger,
  workflow overview, new Phase 0.5 section.
- `skills/feature-status-tracker/references/table-format.md` — "From a raw
  list to the table" section with a before/after example.
- `README.md` — EN + FR: usage can start from a raw list.
- `.claude-plugin/plugin.json` + `marketplace.json` — version 1.1.0.

## Verification

`claude plugin validate . --strict`, plus a manual run on a throwaway repo with
(a) a pasted list and (b) a notes file.
