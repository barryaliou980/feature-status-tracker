---
name: feature-status-tracker
description: >
  Use when the user provides or references a Markdown table of features to build
  (| Feature | Description | Status | columns), mentions a feature backlog, a
  roadmap to implement, "feature status", or asks to clarify features and then
  develop them autonomously one by one. Works with English or French tables
  (Status/Statut, todo/à faire). Triggers even without the word "skill" —
  pasting a feature table with a status column is enough.
---

# Feature Status Tracker

End-to-end pilot: feature table → clarification → autonomous development branch by branch, relying on Superpowers skills for each technical step.

## Workflow overview

```
Phase 0: Prerequisites check (Superpowers, clean git repo)
Phase 1: Table parsing + Clarification (interactive, feature by feature)
Phase 2: Confirmation gate (explicit "GO" from the user)
Phase 3: Autonomous loop (1 feature = 1 branch = 1 PR = 1 row marked "done")
Phase 4: Final report
```

**Golden rule: never start coding until ALL features are clarified.** Clarification and development are two strictly separate phases.

---

## Phase 0 — Prerequisites

1. Check that we are in a clean git repository: `git status`. If uncommitted changes are lying around, flag them to the user before continuing.
2. Check for Superpowers: look for `.claude/plugins` or a skills directory containing `using-git-worktrees`, `test-driven-development`, `requesting-code-review`, `finishing-a-development-branch` (via the available skill discovery mechanism, or `find` on `~/.claude`).
   - **If Superpowers is present**: this skill explicitly delegates to those Superpowers skills during Phase 3 (see `references/superpowers-integration.md`). Do not reimplement TDD or worktree management logic in parallel — invoke the corresponding Superpowers skill.
   - **If Superpowers is absent**: mention it once to the user ("Superpowers is not detected, I'll use an equivalent manual git/TDD workflow") then continue with the fallback described in `references/superpowers-integration.md`. Do not block the workflow because of it.
3. Identify or ask for the path of the table file (e.g. `FEATURES.md`, `roadmap.md`) if it wasn't already provided in the conversation.

## Phase 1 — Parse the table and clarify

### Expected table format

See `references/table-format.md` for full details, including the bilingual (English/French) status values. In short, minimal columns:

| Feature | Description | Status | Clarifications | Branch | PR |
|---|---|---|---|---|---|

- If the provided table lacks the `Clarifications`, `Branch`, `PR` columns, add them yourself by editing the file (they serve as persistent memory across sessions).
- Possible statuses: `todo`, `clarified`, `in progress`, `done`, `blocked` — French equivalents (`à faire`, `clarifiée`, `en cours`, `bloquée`) are accepted too. **Detect which language the user's table uses and keep writing statuses in that same language.**

### Clarification loop (one feature at a time)

For each row whose status is `todo` (not yet clarified):

1. Briefly announce which feature you are handling (name + existing description).
2. Ask targeted questions to remove ambiguities — see the checklist in `references/clarification-questions.md`. Do not ask everything mechanically: only ask the questions relevant to THIS feature (a UI feature does not get the same questions as an internal API feature).
3. Use the multiple-choice question format (via the user-question tool if available in the environment, otherwise clear numbered questions) to move fast — but stay open to free-text answers.
4. Once the answers are in, summarize the retained acceptance criteria in 2-4 lines and write them into the `Clarifications` column of the corresponding row (Markdown file updated directly).
5. Set the row's status to `clarified`.
6. Move on to the next feature **without stopping for validation** — only the completion of clarification for ALL features triggers a stopping point (Phase 2).

If a feature is already marked `done` or `blocked` when entering the skill, skip it (do not re-clarify, do not re-develop).

## Phase 2 — Confirmation gate

Once all rows are `clarified` (or pre-existing `done`/`blocked`):

1. Display a compact summary of the final table (feature → one-line summary of acceptance criteria).
2. Explicitly ask for confirmation before launching autonomous development, for example: *"All features are clarified. I can start autonomous development (1 branch per feature, local PR at the end of each). I'll work alone until the table is complete — confirm to let me start."*
3. Never start Phase 3 without this explicit green light.

## Phase 3 — Autonomous development loop

Once the green light is given, **do not go back to the user between features** (except for a real blocker — see error handling). For each feature in table order whose status is `clarified`:

1. **Mark** the row `in progress` in the table file.
2. **Create the branch** dedicated to this feature. Branch name: `feature/<feature-slug>` (kebab-case, no accents). Use the Superpowers skill `using-git-worktrees` if available to isolate the workspace; otherwise `git checkout -b feature/<slug>` from the up-to-date local main branch.
3. **Develop** based on the acceptance criteria in the `Clarifications` column. Use the Superpowers skill `test-driven-development` (red-green-refactor cycle) if available; otherwise apply manually: failing test → minimal code → passing test → refactor.
4. **Have your own work reviewed** with the Superpowers skill `requesting-code-review` if available, before committing, to catch obvious problems.
5. **Commit** with a conventional message (`feat: <feature summary>`, optional body listing the covered acceptance criteria).
6. **Close out the branch**: use the Superpowers skill `finishing-a-development-branch` if available to open the PR; otherwise `git push -u origin feature/<slug>` then `gh pr create --base <local-main-branch> --fill` (if `gh` is installed) or, failing that, clearly state in the report that the branch is ready and pushed but the PR could not be opened automatically. **Never merge automatically** — the PR stays open for human review.
7. **Update the table**: status → `done`, fill in the `Branch` and `PR` columns (link or identifier).
8. **Return to the local main branch** before moving to the next feature (`git checkout <main-branch>`).
9. Automatically move on to the next feature with status `clarified`, without waiting for confirmation.

### Error / blocker handling

- If a feature cannot be completed (missing dependency, technical ambiguity discovered too late, tests impossible to pass after a reasonable number of attempts): mark the row `blocked`, write the reason in `Clarifications`, commit the partial work on its dedicated branch if relevant, then **continue with the next feature** rather than stopping the whole run.
- Never leave the repository on a feature branch at the end of a cycle — always return to the local main branch between two features.

## Phase 4 — Final report

When all rows are `done` or `blocked`, produce a text summary (no widget, simple structured format):
- Number of features completed / blocked.
- List of branches created and PRs opened (with links if available).
- List of blocked features with the reason, so the user can decide.

---

## Reference files

- `references/table-format.md` — Exact table format, full example, parsing rules, bilingual status values.
- `references/clarification-questions.md` — Clarification question checklist by feature type (UI, API, data, infra).
- `references/superpowers-integration.md` — Precise mapping between each step of this skill and the corresponding Superpowers skill, plus the fallback if Superpowers is not installed.
