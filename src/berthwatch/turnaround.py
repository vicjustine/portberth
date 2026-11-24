"""Turnaround statistics across a window of vessel calls."""

from datetime import timedelta

from .schedule import Call


def mean_turnaround(calls: list[Call]) -> timedelta:
    """Average time alongside across the given calls."""
    if not calls:
        return timedelta()
    total = sum((c.duration() for c in calls), timedelta())
    return total / len(calls)


def berth_utilisation(calls: list[Call], window: timedelta) -> dict[str, float]:
    """Fraction of the window each berth is occupied, 0.0 to 1.0."""
    occupied: dict[str, timedelta] = {}
    for call in calls:
        occupied[call.berth] = occupied.get(call.berth, timedelta()) + call.duration()
    return {
        berth: round(taken / window, 3)
        for berth, taken in sorted(occupied.items())
    }


def longest_stay(calls: list[Call]) -> Call | None:
    """The call that spent the most time alongside."""
    return max(calls, key=lambda c: c.duration(), default=None)
