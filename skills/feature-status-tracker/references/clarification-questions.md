# Clarification question checklist by feature type

Only ask the questions relevant to the current feature — this list is a menu, not a script to recite in full. The goal of every question is to end up with **written, testable acceptance criteria**, not just to "discuss".

## Generic questions (almost always useful)

- What is the expected end-user behavior, in one sentence?
- Is there an edge case or error that absolutely must be handled (e.g. missing data, timeout, duplicate)?
- Does this feature depend on another feature in the table that must be finished first?
- What is the criterion that lets us say "it's done" (e.g. a specific test, a manual scenario to verify)?

## If the feature touches UI/UX

- Existing screen or component to modify, or a new screen?
- Responsive/mobile behavior to handle, or out of scope?
- Loading / error states to display explicitly?

## If the feature touches an API / the backend

- New route or modification of an existing route? Which HTTP verb and expected payload?
- Authentication/permissions required on this route?
- Expected response format (JSON structure)?

## If the feature touches data / the database

- Schema migration needed? On which table?
- Impact on existing data (data migration, not just schema)?
- Uniqueness constraints, indexes, or relations to add?

## If the feature touches infra / multi-tenancy

- Same behavior for all tenants, or configurable per workspace?
- Impact on routing/custom domains if applicable?

## After the answers

Always rephrase into 2-4 concise lines and write them into the table's `Clarifications` column, as actionable acceptance criteria rather than a verbatim copy of the conversation. That text, and only that text, will serve as the spec during Phase 3 — so it must be precise enough to develop without asking the user again.
