# Ops Task Board

A small Flask web app for tracking an operations team's tasks — the kind of
daily workload view an Operations Executive actually uses: what's open, who's
holding it, what's overdue, and what's due next.

## What it does

- Loads tasks from a plain CSV file (`data/tasks.csv`) — no database needed.
- Dashboard page (`/`) with counts by status (To Do / In Progress / Done)
  plus an overdue count, with overdue rows highlighted red and due-soon
  rows highlighted amber.
- Filter the board by owner or status, e.g. `/?owner=Daniyal`.
- Add a task through the form; it is appended to the CSV.
- JSON API at `/api/tasks` returning every task with its computed
  `state` (`done`, `overdue`, `due-soon`, or `on-track`).

## Skills used

Python, Flask, HTML/CSS, CSV data handling — all on the resume. No
frameworks, cloud services, or tools beyond that.

## How to run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Then open http://127.0.0.1:5000/ in a browser.

## Tests

```bash
.venv/bin/python test_app.py
```

Uses Flask's test client against a scratch copy of the CSV, so the sample
data is never modified by tests.

## Sample output

Board counts for the bundled sample data (12 tasks, as of 2026-10-31):

- Total: 12 — To Do: 5, In Progress: 4, Done: 3, Overdue: 3
- Overdue examples: "Follow up on pending invoice approvals" (Bassam, due
  2026-10-30), "Reconcile October delivery tracker" (Daniyal, due
  2026-10-29), and "Fix broken links in client dashboard export" (Bassam,
  due 2026-10-30)

Test run (2026-10-31):

```
PASS test_board_loads
PASS test_owner_filter
PASS test_api_returns_json
PASS test_add_task
All tests passed.
```

A live server check also returned HTTP 200 for both `/` and `/api/tasks`.
