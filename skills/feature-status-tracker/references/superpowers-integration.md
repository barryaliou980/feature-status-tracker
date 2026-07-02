# Superpowers integration (obra/superpowers)

This skill is designed to run in Claude Code with the Superpowers plugin installed. Superpowers provides specialized skills for each technical step of development — this skill orchestrates, Superpowers executes.

## Checking for Superpowers

At the start of Phase 0, look for the available Superpowers skills (e.g. list accessible skills, or search for a plugins directory containing their names). The Superpowers skills relevant to this workflow:

- `using-git-worktrees`
- `test-driven-development`
- `requesting-code-review`
- `finishing-a-development-branch`
- `brainstorming` (optional, see note below)

## Step-by-step mapping

| Step in this skill | Superpowers skill to invoke | What it does |
|---|---|---|
| Branch creation (Phase 3, step 2) | `using-git-worktrees` | Creates an isolated workspace on a new branch, runs project setup, verifies a clean test baseline before starting to code. |
| Development (Phase 3, step 3) | `test-driven-development` | Enforces the red-green-refactor cycle: write a failing test, minimal code to make it pass, refactor. |
| Self-review before commit (Phase 3, step 4) | `requesting-code-review` | Has the work reviewed against the acceptance criteria and code quality, before considering the feature done. |
| Branch close-out + PR (Phase 3, step 6) | `finishing-a-development-branch` | Verifies tests, offers merge / create a PR / continue / abandon. **Always choose the "create a PR" option and never "merge"**, per the user's rule (local PR against the main branch, no automatic merge). |

### Note on `brainstorming`

Superpowers includes a `brainstorming` skill that refines a vague idea through questions before any code — conceptually close to Phase 1 of this skill. Do not invoke both on the same feature: Phase 1 of `feature-status-tracker` replaces `brainstorming` for this specific workflow, since clarification already starts from a structured table. If `brainstorming` activates spontaneously during Phase 3 (e.g. an ambiguity rediscovered mid-development), let it run that one time rather than blocking it — but it must remain the exception, not the norm, otherwise the autonomous loop loses its autonomy.

## Fallback if Superpowers is not installed

Never block the workflow if Superpowers is absent — apply the equivalent manually:

1. **Branch**: `git checkout -b feature/<slug>` from the up-to-date local main branch (`git pull` first if a remote exists).
2. **Manual TDD**: write a failing test, code the minimum to make it pass, refactor, then move to the next acceptance criterion.
3. **Self-review**: before committing, re-read your own diff (`git diff`) against the `Clarifications` column and explicitly flag any uncovered point rather than committing silently.
4. **Close-out**: `git push -u origin feature/<slug>`, then `gh pr create --base <main-branch> --fill` if the `gh` CLI is available and authenticated. If `gh` is not available, do not try to guess a URL — clearly state in the final report that the branch is pushed but the PR must be opened manually, with the exact command to run.

In both cases (with or without Superpowers), the user's business rule stays fixed: **never merge automatically**, always an open PR against the local main branch, awaiting human review.
