"""Smoke tests for the Ops Task Board, using Flask's test client."""

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import app as app_module  # noqa: E402

# Point the app at a scratch copy of the CSV so tests never touch the sample.
shutil.copy(app_module.DATA_FILE, "/tmp/test_tasks.csv")
app_module.DATA_FILE = "/tmp/test_tasks.csv"

client = app_module.app.test_client()


def test_board_loads():
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Ops Task Board" in resp.data
    assert b"Follow up on pending invoice approvals" in resp.data


def test_owner_filter():
    resp = client.get("/?owner=Daniyal")
    assert resp.status_code == 200
    assert b"Reconcile October delivery tracker" in resp.data
    assert b"Follow up on pending invoice approvals" not in resp.data


def test_api_returns_json():
    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 12
    assert all("state" in t for t in data)


def test_add_task():
    resp = client.post(
        "/add",
        data={
            "title": "Test handover note",
            "owner": "Bassam",
            "client": "Test Client",
            "status": "To Do",
            "priority": "Low",
            "due_date": "2026-11-10",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"Test handover note" in resp.data


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"PASS {name}")
    print("All tests passed.")
