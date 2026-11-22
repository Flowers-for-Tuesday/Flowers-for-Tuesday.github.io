"""Locale-independent display dates; source dates remain Gregorian and sortable."""
from datetime import date
import re


MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def display_date(value):
    """Format an ISO or slash-separated date as Oct 12,2026."""
    match = re.fullmatch(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", str(value).strip())
    if not match:
        raise ValueError(f"Expected a Gregorian date: {value!r}")
    parsed = date(*(int(part) for part in match.groups()))
    return f"{MONTHS[parsed.month - 1]} {parsed.day},{parsed.year}"
