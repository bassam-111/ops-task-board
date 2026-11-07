"""Ops Task Board: a small Flask dashboard for operations task tracking.

Loads tasks from data/tasks.csv, shows counts by status, flags overdue
and due-soon tasks, and lets you filter by owner/status or add a task.
Everything runs locally; no database or external service is needed.
"""

import csv
import os
from datetime import date

from flask import Flask, jsonify, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "tasks.csv")

app = Flask(__name__)


def load_tasks():
    """Read tasks from CSV, returning a list of dicts (one per row)."""
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def task_state(task, today):
    """Classify a task as overdue / due-soon / on-track / done."""
    if task["status"] == "Done":
        return "done"
    due = date.fromisoformat(task["due_date"])
    if due < today:
        return "overdue"
    if (due - today).days <= 2:
        return "due-soon"
    return "on-track"


@app.route("/")
def board():
    """Dashboard page, optionally filtered by ?owner= and ?status=."""
    today = date.today()
    tasks = load_tasks()
    owner_filter = request.args.get("owner", "")
    status_filter = request.args.get("status", "")

    filtered = [
        t
        for t in tasks
        if (not owner_filter or t["owner"] == owner_filter)
        and (not status_filter or t["status"] == status_filter)
    ]
    for task in filtered:
        task["state"] = task_state(task, today)

    counts = {
        "total": len(tasks),
        "done": sum(1 for t in tasks if t["status"] == "Done"),
        "in_progress": sum(1 for t in tasks if t["status"] == "In Progress"),
        "todo": sum(1 for t in tasks if t["status"] == "To Do"),
        "overdue": sum(
            1 for t in tasks if task_state(t, today) == "overdue"
        ),
    }
    owners = sorted({t["owner"] for t in tasks})
    return render_template(
        "index.html",
        tasks=filtered,
        counts=counts,
        owners=owners,
        owner_filter=owner_filter,
        status_filter=status_filter,
        today=today.isoformat(),
    )


@app.route("/api/tasks")
def api_tasks():
    """JSON view of all tasks, with the same overdue/due-soon flags."""
    today = date.today()
    tasks = load_tasks()
    for task in tasks:
        task["state"] = task_state(task, today)
    return jsonify(tasks)


@app.route("/add", methods=["POST"])
def add_task():
    """Append a new task to the CSV and return to the board."""
    tasks = load_tasks()
    new_id = max(int(t["id"]) for t in tasks) + 1 if tasks else 1
    row = {
        "id": new_id,
        "title": request.form["title"].strip(),
        "owner": request.form["owner"].strip(),
        "status": request.form["status"],
        "priority": request.form["priority"],
        "due_date": request.form["due_date"],
        "client": request.form["client"].strip(),
    }
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        writer.writerow(row)
    return redirect(url_for("board"))


if __name__ == "__main__":
    app.run(debug=False)
