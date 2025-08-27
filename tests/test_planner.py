import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from planner import Task, DailyPlanner
from datetime import datetime
import csv
import urllib.parse


def test_export_csv(tmp_path):
    planner = DailyPlanner()
    task = Task("Test", datetime(2020, 1, 1, 9), datetime(2020, 1, 1, 10), "desc")
    planner.add_task(task)
    path = tmp_path / "out.csv"
    planner.export_csv(path)
    with open(path) as fh:
        rows = list(csv.reader(fh))
    assert rows[1][0] == "Test"


def test_google_link():
    task = Task("Meeting", datetime(2020, 1, 1, 9), datetime(2020, 1, 1, 10))
    link = task.google_link()
    assert "calendar.google.com" in link
    assert urllib.parse.quote("Meeting") in link


def test_fill_with_fluff():
    day = datetime(2020, 1, 1)
    planner = DailyPlanner()
    planner.fill_with_fluff(day, start_hour=9, end_hour=11, fluff_title="Rest")
    assert len(planner.tasks) == 2
    assert all(t.title == "Rest" for t in planner.tasks)
