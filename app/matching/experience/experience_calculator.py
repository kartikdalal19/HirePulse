
import re
import calendar
from datetime import date, datetime


MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}


def parse_date(date_text: str | None, is_end_date: bool = False) -> date | None:
    """
    Parse employment dates such as:
    January 2025, Jun 2025, 01/2025, 2025, Present.
    """

    if not date_text:
        return None

    text = date_text.strip().lower()

    if text in {"present", "current", "currently", "till date", "ongoing"}:
        today = date.today()

        if is_end_date:
            return date(today.year, today.month, 1)

        return None

    # Format: January 2025 or Jan 2025
    match = re.search(
        r"\b([a-z]+)\s+(\d{4})\b",
        text
    )

    if match:
        month_text = match.group(1)
        year = int(match.group(2))

        month = MONTHS.get(month_text)

        if month is None:
            month = next(
                (
                    number
                    for name, number in MONTHS.items()
                    if name.startswith(month_text)
                ),
                None
            )

        if month:
            return date(year, month, 1)

    # Format: 01/2025 or 01-2025
    match = re.search(
        r"\b(0?[1-9]|1[0-2])[/\-](\d{4})\b",
        text
    )

    if match:
        return date(
            int(match.group(2)),
            int(match.group(1)),
            1
        )

    # Format: 2025
    match = re.search(r"\b(\d{4})\b", text)

    if match:
        year = int(match.group(1))

        if is_end_date:
            return date(year, 12, 1)

        return date(year, 1, 1)

    return None


def calculate_month_difference(start: date, end: date) -> int:
    """
    Calculate the number of calendar months between two dates.
    """

    return (
        (end.year - start.year) * 12
        + (end.month - start.month)
    ) + 1


def merge_employment_periods(periods: list[tuple[date, date]]) -> list[tuple[date, date]]:
    """
    Merge overlapping or consecutive employment periods.
    """

    if not periods:
        return []

    periods.sort(key=lambda period: period[0])

    merged = [periods[0]]

    for current_start, current_end in periods[1:]:
        previous_start, previous_end = merged[-1]

        # Merge overlapping or consecutive periods.
        if current_start <= previous_end:
            merged[-1] = (
                previous_start,
                max(previous_end, current_end)
            )
        else:
            merged.append((current_start, current_end))

    return merged


def format_duration(total_months: int) -> dict:
    """
    Convert months into years and months.
    """

    return {
        "years": total_months // 12,
        "months": total_months % 12,
        "total_months": total_months
    }


def calculate_experience(employment_records: list[dict]) -> dict:
    """
    Calculate individual and total employment experience.
    """

    today = date.today()
    current_month = date(today.year, today.month, 1)

    processed_records = []
    valid_periods = []

    for record in employment_records:

        start_date = parse_date(
            record.get("start_date")
        )

        end_date = parse_date(
            record.get("end_date"),
            is_end_date=True
        )

        if not start_date or not end_date:
            processed_records.append({
                **record,
                "duration": None,
                "date_status": "invalid_or_missing_dates"
            })
            continue

        if start_date > current_month or end_date < start_date:
            processed_records.append({
                **record,
                "duration": None,
                "date_status": "invalid_date_range"
            })
            continue

        duration_months = calculate_month_difference(
            start_date,
            end_date
        )

        processed_records.append({
            **record,
            "duration": format_duration(duration_months),
            "date_status": "valid"
        })

        valid_periods.append((start_date, end_date))

    # Merge overlapping periods to avoid double-counting.
    merged_periods = merge_employment_periods(valid_periods)

    total_months = sum(
        calculate_month_difference(start, end)
        for start, end in merged_periods
    )

    return {
        "employment_records": processed_records,
        "total_experience": format_duration(total_months),
        "valid_employment_records": len(valid_periods),
        "invalid_employment_records": (
            len(employment_records) - len(valid_periods)
        )
    }
