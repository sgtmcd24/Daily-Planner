# Daily-Planner

A lightweight daily planner aimed at users who benefit from structured days. It can
export entries to CSV and provides links for adding events to popular calendars.
A small cyberpunk-themed web interface is included for inspiration.

## Features

- Add tasks with a title, description and time range.
- Export tasks to a CSV file for record keeping.
- Generate links for Google Calendar and Outlook.
- Generate ICS data that can be imported into iOS or Samsung calendars.
- Fill empty hours with "fluff" entries to avoid overwhelming schedules.

## Usage

```python
from datetime import datetime
from planner import Task, DailyPlanner

planner = DailyPlanner()
planner.add_task(Task("Therapy", datetime(2024, 1, 1, 9), datetime(2024, 1, 1, 10)))
planner.fill_with_fluff(datetime(2024, 1, 1))
planner.export_csv("out.csv")
```

Run the tests with:

```bash
pytest
```

A static web prototype with a cyberpunk style lives in `web/index.html`.
