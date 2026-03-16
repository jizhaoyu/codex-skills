---
name: task-planner
description: Break down complex work into ordered phases, surface dependencies and risks, keep an execution plan current, and optionally maintain a markdown task plan file. Use when Codex needs to handle multi-step tasks such as feature delivery, refactors, migrations, debugging campaigns, research spikes, or any task where staged execution and explicit progress tracking matter.
---

# Task Planner

Use this skill when the work is large enough that execution order, checkpoints, or progress visibility matters.

## Core Workflow

1. Build context before planning.
- Inspect the repository, current changes, constraints, and acceptance criteria first.
- State assumptions that affect execution.
- Do not rely on Claude-only paths such as `~/.claude/...` or Claude-specific task tools.

2. Create a short working plan.
- For multi-step work, use the built-in planning tool to keep 3-7 outcome-oriented steps.
- Keep exactly one step `in_progress`.
- Prefer phase boundaries that can be validated independently.

3. Ask only high-impact questions.
- Ask at most 1-3 questions, and only when the answer materially changes scope, sequencing, or architecture.
- In Plan mode, prefer the structured user-input tool when it is available.
- Outside Plan mode, ask a concise plain-text question.
- Skip questions when the repository or user request already makes the decision clear.

4. Choose an execution style.
- Use `planning only` when the user only wants analysis or a written plan.
- Use `phased execution` by default for risky changes, broad refactors, or cross-cutting work.
- Use `continuous execution` only for lower-risk work where stopping between phases adds little value.

5. Keep progress synchronized.
- Update the built-in plan after each meaningful milestone.
- If the user wants a durable artifact, create a markdown plan in the current project by copying `references/plan-template.md`.
- When updating repeated status fields in that markdown plan, prefer `scripts/update_progress.py` over manual editing.

6. Validate after each phase.
- Run the narrowest useful verification after each major step.
- Record any remaining risks, skipped checks, or unresolved blockers.

## Planning Rules

- Start with the smallest amount of planning that still reduces risk.
- Prefer dependency order over category grouping.
- Separate irreversible or user-visible changes into their own phases.
- Keep optional polish work out of the critical path.
- If blocked, record the blocker, continue independent tasks, and make the stop condition explicit.

## Written Plan Artifact

Use a markdown plan file only when one of these is true:
- The task spans multiple sessions.
- The user explicitly wants a plan document.
- Several workstreams or dependencies must stay visible over time.

When you create the file:
- Store it in the repository unless the user asked for another location.
- Keep task IDs stable.
- Use the statuses `pending`, `in_progress`, `completed`, and `blocked`.
- Update the changelog when priorities or status materially change.

## Resources

- `references/plan-template.md`: Starter template for a durable task plan.
- `scripts/update_progress.py`: Helper script for updating status, progress, blockers, and changelog entries in that template.
