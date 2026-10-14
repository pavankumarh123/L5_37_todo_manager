"""A simple task manager with saving and JSON export features."""

import json
import os
import pickle
import random
from datetime import datetime

tasks = {}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def add_task(title, priority="medium", labels=None):
    """Add a new task and return its ID."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Task title cannot be empty.")

    if priority not in PRIORITY_ORDER:
        raise ValueError("Priority must be high, medium, or low.")

    task_id = len(tasks) + 1
    task_labels = list(labels) if labels is not None else []
    task_labels.append(priority)

    tasks[task_id] = {
        "title": title.strip(),
        "priority": priority,
        "labels": task_labels,
        "done": False,
        "created": datetime.now().isoformat(),
    }
    return task_id


def complete_task(task_id):
    """Mark a task as completed."""
    if task_id in tasks:
        tasks[task_id]["done"] = True
        return True

    print(f"No task with ID {task_id}")
    return False


def pending_tasks():
    """Return pending task titles in priority order."""
    pending = [
        task for task in tasks.values()
        if not task["done"]
    ]
    pending.sort(
        key=lambda task: PRIORITY_ORDER[task["priority"]]
    )
    return [task["title"] for task in pending]


def find_task(keyword):
    """Find a task by keyword and return its ID, or None."""
    for task_id, task in tasks.items():
        if keyword.lower() in task["title"].lower():
            return task_id
    return None


def save_tasks(filename="tasks.pkl"):
    """Save tasks to a pickle file."""
    with open(filename, "wb") as file:
        pickle.dump(tasks, file)


def load_tasks(filename="tasks.pkl"):
    """Load tasks from a trusted pickle file."""
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
    except (OSError, EOFError, pickle.UnpicklingError) as error:
        print(f"Could not load tasks: {error}")
        return {}

    if not isinstance(data, dict):
        print("Invalid task data format.")
        return {}

    return data


def export_json(filename="tasks.json"):
    """Export tasks to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def remind_by_email(address):
    """Report that email reminders require a configured email service."""
    if not isinstance(address, str) or "@" not in address:
        raise ValueError("Please provide a valid email address.")

    print("Email reminders are not configured.")
    return False


def main():
    """Demonstrate the task manager features."""
    add_task("Submit lab report", "high")
    add_task("Buy groceries")
    add_task("Call plumber", "low")
    add_task("Book train tickets", "high")

    complete_task(2)
    complete_task(99)

    print("Pending tasks:", pending_tasks())
    print("Task ID for 'plumber':", find_task("plumber"))
    print("Task ID for 'gym':", find_task("gym"))

    suggestions = pending_tasks()
    if suggestions:
        print("Try this next:", random.choice(suggestions))
    else:
        print("No pending tasks.")

    save_tasks()
    restored = load_tasks()
    print("Tasks restored from file:", len(restored))

    export_json()
    print("Exported tasks to tasks.json")


if __name__ == "__main__":
    main()