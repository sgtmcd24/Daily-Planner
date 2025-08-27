from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List
import csv
import urllib.parse


@dataclass
class Task:
    """Representation of a single planner entry."""

    title: str
    start: datetime
    end: datetime
    description: str = ""
    category: str = "general"

    def to_csv_row(self) -> List[str]:
        """Return the task as a CSV row."""
        return [
            self.title,
            self.start.isoformat(),
            self.end.isoformat(),
            self.description,
            self.category,
        ]

    def google_link(self) -> str:
        """Return a link for adding the event to Google Calendar."""
        base = "https://calendar.google.com/calendar/render"
        dates = f"{self.start.strftime('%Y%m%dT%H%M%S')}/{self.end.strftime('%Y%m%dT%H%M%S')}"
        params = {
            "action": "TEMPLATE",
            "text": self.title,
            "details": self.description,
            "dates": dates,
        }
        return f"{base}?{urllib.parse.urlencode(params)}"

    def outlook_link(self) -> str:
        """Return a link for adding the event to Outlook."""
        base = "https://outlook.live.com/owa/"
        params = {
            "path": "/calendar/action/compose",
            "subject": self.title,
            "body": self.description,
            "startdt": self.start.isoformat(),
            "enddt": self.end.isoformat(),
        }
        return f"{base}?{urllib.parse.urlencode(params)}"

    def to_ics(self) -> str:
        """Return an ICS representation of the event."""
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "BEGIN:VEVENT",
            f"SUMMARY:{self.title}",
            f"DTSTART:{self.start.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND:{self.end.strftime('%Y%m%dT%H%M%S')}",
            f"DESCRIPTION:{self.description}",
            "END:VEVENT",
            "END:VCALENDAR",
        ]
        return "\n".join(lines)


@dataclass
class DailyPlanner:
    """Simple daily planner holding a list of tasks."""

    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def export_csv(self, path: str) -> None:
        """Export all tasks to a CSV file."""
        with open(path, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["title", "start", "end", "description", "category"])
            for task in self.tasks:
                writer.writerow(task.to_csv_row())

    def fill_with_fluff(
        self, day: datetime, start_hour: int = 8, end_hour: int = 20, fluff_title: str = "Break"
    ) -> None:
        """Fill empty hours in the day with placeholder tasks.

        Parameters
        ----------
        day:
            The day to inspect.
        start_hour:
            Starting hour for planning (inclusive).
        end_hour:
            Ending hour for planning (exclusive).
        fluff_title:
            Title used for the placeholder tasks.
        """

        current = datetime(day.year, day.month, day.day, start_hour)
        last = datetime(day.year, day.month, day.day, end_hour)
        while current < last:
            overlap = any(task.start <= current < task.end for task in self.tasks)
            if not overlap:
                fluff = Task(fluff_title, current, current + timedelta(hours=1), category="fluff")
                self.tasks.append(fluff)
            current += timedelta(hours=1)
