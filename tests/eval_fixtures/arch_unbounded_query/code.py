"""Analytics dashboard — unbounded queries with no pagination or limits."""

import sqlite3
from datetime import datetime, timedelta


class AnalyticsService:
    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row

    def get_all_events(self, user_id: int) -> list[dict]:
        """Fetch all events for a user."""
        rows = self.db.execute(
            "SELECT * FROM events WHERE user_id = ?", (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_event_log(self) -> list[dict]:
        """Fetch the complete event log."""
        rows = self.db.execute("SELECT * FROM events ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]

    def search_events(self, query: str) -> list[dict]:
        """Search events by description."""
        rows = self.db.execute(
            "SELECT * FROM events WHERE description LIKE ?",
            (f"%{query}%",),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_user_activity(self, user_id: int) -> dict:
        """Build a complete activity report for a user."""
        events = self.get_all_events(user_id)
        sessions = self.db.execute(
            "SELECT * FROM sessions WHERE user_id = ?", (user_id,)
        ).fetchall()
        purchases = self.db.execute(
            "SELECT * FROM purchases WHERE user_id = ?", (user_id,)
        ).fetchall()

        return {
            "user_id": user_id,
            "total_events": len(events),
            "events": events,
            "sessions": [dict(s) for s in sessions],
            "purchases": [dict(p) for p in purchases],
        }

    def export_all_data(self) -> dict:
        """Export everything for backup."""
        events = self.db.execute("SELECT * FROM events").fetchall()
        users = self.db.execute("SELECT * FROM users").fetchall()
        sessions = self.db.execute("SELECT * FROM sessions").fetchall()
        return {
            "events": [dict(e) for e in events],
            "users": [dict(u) for u in users],
            "sessions": [dict(s) for s in sessions],
        }
