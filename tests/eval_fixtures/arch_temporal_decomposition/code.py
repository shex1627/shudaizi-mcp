"""ETL pipeline for processing daily sales reports.

Reads CSV sales data, converts currencies, aggregates by region and date,
and writes formatted reports.
"""

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


# ── Step 1: Read raw files ───────────────────────────────────────


def read_csv_file(filepath: str) -> list[dict]:
    """Read a CSV file and return rows as dicts."""
    rows = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def read_json_file(filepath: str) -> dict:
    """Read a JSON config file."""
    with open(filepath) as f:
        return json.load(f)


def read_exchange_rates(filepath: str) -> dict[str, float]:
    """Read currency exchange rates from a text file."""
    rates = {}
    with open(filepath) as f:
        for line in f:
            currency, rate = line.strip().split("=")
            rates[currency.strip()] = float(rate.strip())
    return rates


# ── Step 2: Parse and validate ───────────────────────────────────


def parse_date(raw: str) -> datetime:
    """Try multiple date formats."""
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {raw}")


def parse_amount(raw: str) -> float:
    """Remove currency symbols and parse as float."""
    cleaned = raw.replace("$", "").replace(",", "").replace("€", "").replace("£", "")
    return float(cleaned)


def validate_row(row: dict) -> bool:
    """Check that required fields are present and non-empty."""
    required = ["date", "amount", "currency", "region"]
    return all(row.get(field) for field in required)


def parse_sales_rows(raw_rows: list[dict]) -> list[dict]:
    """Parse and validate all rows."""
    parsed = []
    for row in raw_rows:
        if not validate_row(row):
            continue
        parsed.append({
            "date": parse_date(row["date"]),
            "amount": parse_amount(row["amount"]),
            "currency": row["currency"],
            "region": row["region"],
        })
    return parsed


# ── Step 3: Transform ────────────────────────────────────────────


def convert_currencies(rows: list[dict], rates: dict[str, float], target: str = "USD") -> list[dict]:
    """Convert all amounts to the target currency."""
    converted = []
    for row in rows:
        if row["currency"] == target:
            converted.append(row)
        else:
            rate = rates.get(row["currency"], 1.0)
            converted.append({
                **row,
                "amount": row["amount"] * rate,
                "currency": target,
            })
    return converted


def aggregate_by_region(rows: list[dict]) -> dict[str, float]:
    """Sum amounts by region."""
    totals = {}
    for row in rows:
        region = row["region"]
        totals[region] = totals.get(region, 0) + row["amount"]
    return totals


def aggregate_by_date(rows: list[dict]) -> dict[str, float]:
    """Sum amounts by date."""
    totals = {}
    for row in rows:
        key = row["date"].strftime("%Y-%m-%d")
        totals[key] = totals.get(key, 0) + row["amount"]
    return totals


def compute_summary_stats(totals: dict[str, float]) -> dict:
    """Compute min, max, mean for a totals dict."""
    values = list(totals.values())
    return {
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / len(values),
        "count": len(values),
    }


# ── Step 4: Format output ───────────────────────────────────────


def format_currency(amount: float) -> str:
    """Format as USD string."""
    return f"${amount:,.2f}"


def format_region_report(region_totals: dict[str, float]) -> str:
    """Build a text report of region totals."""
    lines = ["Region Sales Report", "=" * 40]
    for region, total in sorted(region_totals.items()):
        lines.append(f"  {region:<20} {format_currency(total)}")
    return "\n".join(lines)


def format_date_report(date_totals: dict[str, float]) -> str:
    """Build a text report of daily totals."""
    lines = ["Daily Sales Report", "=" * 40]
    for date, total in sorted(date_totals.items()):
        lines.append(f"  {date:<20} {format_currency(total)}")
    return "\n".join(lines)


def format_summary(stats: dict) -> str:
    """Format summary statistics."""
    return (
        f"Summary: min={format_currency(stats['min'])}, "
        f"max={format_currency(stats['max'])}, "
        f"mean={format_currency(stats['mean'])}, "
        f"n={stats['count']}"
    )


# ── Step 5: Write output ────────────────────────────────────────


def write_text_report(report: str, filepath: str) -> None:
    """Write a report string to a file."""
    with open(filepath, "w") as f:
        f.write(report)


def write_json_output(data: dict, filepath: str) -> None:
    """Write aggregated data as JSON."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)


def write_csv_output(region_totals: dict[str, float], filepath: str) -> None:
    """Write region totals as CSV."""
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["region", "total"])
        for region, total in sorted(region_totals.items()):
            writer.writerow([region, f"{total:.2f}"])


# ── Pipeline entry point ─────────────────────────────────────────


def run_pipeline(
    sales_csv: str,
    config_json: str,
    rates_file: str,
    output_dir: str,
) -> None:
    """Run the full ETL pipeline."""
    # Step 1: Read
    raw_rows = read_csv_file(sales_csv)
    config = read_json_file(config_json)
    rates = read_exchange_rates(rates_file)

    # Step 2: Parse
    parsed = parse_sales_rows(raw_rows)

    # Step 3: Transform
    converted = convert_currencies(parsed, rates, config.get("target_currency", "USD"))
    by_region = aggregate_by_region(converted)
    by_date = aggregate_by_date(converted)
    region_stats = compute_summary_stats(by_region)

    # Step 4: Format
    region_report = format_region_report(by_region)
    date_report = format_date_report(by_date)
    summary = format_summary(region_stats)

    # Step 5: Write
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_text_report(region_report + "\n\n" + summary, str(out / "region_report.txt"))
    write_text_report(date_report, str(out / "daily_report.txt"))
    write_json_output({"by_region": by_region, "by_date": by_date, "stats": region_stats}, str(out / "data.json"))
    write_csv_output(by_region, str(out / "region_totals.csv"))
