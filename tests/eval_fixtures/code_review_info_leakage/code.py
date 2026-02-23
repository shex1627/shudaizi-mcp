"""Order processing — same date parsing logic duplicated across modules."""

from datetime import datetime


# ── orders/api.py ─────────────────────────────────────────────────

def parse_order_date(date_str: str) -> datetime:
    """Parse date from order API requests."""
    formats = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
               "%m/%d/%Y", "%d-%m-%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {date_str}")


def create_order(data: dict) -> dict:
    order_date = parse_order_date(data["date"])
    return {
        "id": 1,
        "date": order_date.isoformat(),
        "items": data["items"],
        "status": "pending",
    }


# ── reports/generator.py ─────────────────────────────────────────

def parse_report_date(date_str: str) -> datetime:
    """Parse date from report generation requests."""
    formats = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
               "%m/%d/%Y", "%d-%m-%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {date_str}")


def generate_report(start_date: str, end_date: str) -> dict:
    start = parse_report_date(start_date)
    end = parse_report_date(end_date)
    return {"start": start.isoformat(), "end": end.isoformat(), "data": []}


# ── shipping/tracker.py ──────────────────────────────────────────

def parse_shipping_date(date_str: str) -> datetime:
    """Parse date from shipping records."""
    formats = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
               "%m/%d/%Y", "%d-%m-%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {date_str}")


def track_shipment(tracking_data: dict) -> dict:
    ship_date = parse_shipping_date(tracking_data["ship_date"])
    return {"tracking_id": tracking_data["id"], "shipped": ship_date.isoformat()}
