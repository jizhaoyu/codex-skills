#!/usr/bin/env python3
"""Update markdown task plans created from the task-planner template."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

VALID_STATUSES = {"pending", "in_progress", "completed", "blocked"}
TASK_BLOCK_RE = re.compile(
    r"^### Task (?P<task_id>\d+): (?P<title>.+?)\n(?P<body>.*?)(?=^### Task \d+: |\Z)",
    re.MULTILINE | re.DOTALL,
)


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def replace_field(block: str, field: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^- {re.escape(field)}: .*$")
    replacement = f"- {field}: {value}"
    if pattern.search(block):
        return pattern.sub(replacement, block, count=1)

    anchor = re.search(r"(?m)^- Substeps:\s*$", block)
    if anchor:
        return f"{block[:anchor.start()]}{replacement}\n{block[anchor.start():]}"
    return f"{block.rstrip()}\n{replacement}\n"


def get_field(block: str, field: str, default: str = "") -> str:
    match = re.search(rf"(?m)^- {re.escape(field)}: (?P<value>.*)$", block)
    return match.group("value").strip() if match else default


def update_substep(block: str, substep_index: int, checked: bool) -> str:
    lines = block.splitlines()
    seen = 0
    marker = "[x]" if checked else "[ ]"

    for index, line in enumerate(lines):
        if re.match(r"^\s+\d+\. \[[ xX]\] ", line):
            seen += 1
            if seen == substep_index:
                lines[index] = re.sub(r"\[[ xX]\]", marker, line, count=1)
                return "\n".join(lines) + "\n"

    raise ValueError(f"substep {substep_index} not found")


def calculate_progress(block: str) -> int:
    substeps = re.findall(r"^\s+\d+\. \[([ xX])\] ", block, re.MULTILINE)
    if not substeps:
        raw = get_field(block, "Progress", "0%").rstrip("%")
        return int(raw) if raw.isdigit() else 0

    completed = sum(1 for item in substeps if item.lower() == "x")
    return round(completed * 100 / len(substeps))


def infer_status(progress: int, current_status: str, blocker: str) -> str:
    if blocker.lower() != "none":
        return "blocked"
    if current_status == "blocked" and blocker.lower() == "none":
        current_status = "pending"
    if progress >= 100:
        return "completed"
    if progress > 0:
        return "in_progress"
    return "pending"


def add_changelog_entry(content: str, message: str) -> str:
    header = "## Changelog"
    entry = f"- {timestamp()} {message}"

    if header not in content:
        return f"{content.rstrip()}\n\n{header}\n\n{entry}\n"

    parts = content.split(header, 1)
    before = parts[0]
    after = parts[1].lstrip("\n")
    return f"{before}{header}\n\n{entry}\n{after}"


def rebuild_summary(content: str) -> str:
    counts = {status: 0 for status in VALID_STATUSES}
    total = 0
    total_progress = 0

    for match in TASK_BLOCK_RE.finditer(content):
        block = match.group(0)
        status = get_field(block, "Status", "pending")
        if status not in VALID_STATUSES:
            status = "pending"
        progress_raw = get_field(block, "Progress", "0%").rstrip("%")
        progress = int(progress_raw) if progress_raw.isdigit() else 0
        counts[status] += 1
        total += 1
        total_progress += progress

    average_progress = round(total_progress / total) if total else 0
    completed = counts["completed"]

    content = re.sub(
        r"(?m)^- Overall progress: .*$",
        f"- Overall progress: {average_progress}% ({completed}/{total} tasks completed)",
        content,
        count=1,
    )
    content = re.sub(
        r"(?m)^- Task counts: .*$",
        (
            "- Task counts: "
            f"{counts['completed']} completed, "
            f"{counts['in_progress']} in progress, "
            f"{counts['pending']} pending, "
            f"{counts['blocked']} blocked"
        ),
        content,
        count=1,
    )
    return content


def replace_task(content: str, task_id: str, updated_block: str) -> str:
    for match in TASK_BLOCK_RE.finditer(content):
        if match.group("task_id") == task_id:
            return f"{content[:match.start()]}{updated_block}{content[match.end():]}"
    raise ValueError(f"task {task_id} not found")


def get_task_block(content: str, task_id: str) -> str:
    for match in TASK_BLOCK_RE.finditer(content):
        if match.group("task_id") == task_id:
            return match.group(0)
    raise SystemExit(f"task {task_id} not found")


def update_task_block(
    block: str,
    *,
    status: str | None,
    progress: int | None,
    blocker: str | None,
    clear_blocker: bool,
    complete_substep: int | None,
    uncomplete_substep: int | None,
    auto_progress: bool,
) -> str:
    if complete_substep is not None:
        block = update_substep(block, complete_substep, True)
    if uncomplete_substep is not None:
        block = update_substep(block, uncomplete_substep, False)

    if blocker is not None:
        block = replace_field(block, "Blocker", blocker)
    elif clear_blocker:
        block = replace_field(block, "Blocker", "none")

    current_status = get_field(block, "Status", "pending")
    current_blocker = get_field(block, "Blocker", "none")

    if auto_progress:
        progress = calculate_progress(block)

    if progress is not None:
        progress = max(0, min(100, progress))
        block = replace_field(block, "Progress", f"{progress}%")
    else:
        progress_raw = get_field(block, "Progress", "0%").rstrip("%")
        progress = int(progress_raw) if progress_raw.isdigit() else 0

    if status is None:
        status = infer_status(progress, current_status, current_blocker)
    block = replace_field(block, "Status", status)
    return block


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True, help="Path to the markdown plan file")
    parser.add_argument("--task", help="Task number to update")
    parser.add_argument("--status", choices=sorted(VALID_STATUSES))
    parser.add_argument("--progress", type=int, help="Progress percentage")
    parser.add_argument("--blocker", help="Set blocker text")
    parser.add_argument("--clear-blocker", action="store_true", help="Reset blocker to none")
    parser.add_argument("--complete-substep", type=int, help="Mark a substep complete")
    parser.add_argument("--uncomplete-substep", type=int, help="Mark a substep incomplete")
    parser.add_argument("--auto-progress", action="store_true", help="Recalculate progress from substeps")
    parser.add_argument("--log", help="Custom changelog message")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plan_path = Path(args.file)
    if not plan_path.exists():
        raise SystemExit(f"plan file not found: {plan_path}")

    content = plan_path.read_text(encoding="utf-8")

    changed = False
    if args.task:
        updated_block = update_task_block(
            get_task_block(content, args.task),
            status=args.status,
            progress=args.progress,
            blocker=args.blocker,
            clear_blocker=args.clear_blocker,
            complete_substep=args.complete_substep,
            uncomplete_substep=args.uncomplete_substep,
            auto_progress=args.auto_progress,
        )
        content = replace_task(content, args.task, updated_block)
        changed = True

    if changed or args.log:
        if args.log:
            message = args.log
        elif args.task:
            task_status = get_field(updated_block, "Status", "pending")
            task_progress = get_field(updated_block, "Progress", "0%")
            message = f"Updated Task {args.task}: status={task_status}, progress={task_progress}."
        else:
            message = "Updated task plan."
        content = add_changelog_entry(content, message)

    content = rebuild_summary(content)
    plan_path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
