"""Berth allocation: which vessel occupies which berth, and when."""

from dataclasses import dataclass
from datetime import datetime, timedelta

# A berth can only take a vessel up to its rated length.
BERTH_LENGTH_M = {"A1": 180, "A2": 180, "B1": 260, "B2": 310}

# Minimum gap between departures and the next arrival on the same berth.
TURNAROUND_BUFFER = timedelta(hours=0)


@dataclass(frozen=True)
class Call:
    """One vessel's scheduled call at the terminal."""

    vessel: str
    berth: str
    arrival: datetime
    departure: datetime
    length_m: int

    def duration(self) -> timedelta:
        return self.departure - self.arrival


def fits_berth(call: Call) -> bool:
    """True when the vessel is short enough for the berth it is assigned."""
    return call.length_m <= BERTH_LENGTH_M[call.berth]


def overlaps(first: Call, second: Call) -> bool:
    """True when two calls on the same berth collide, buffer included."""
    if first.berth != second.berth:
        return False
    earlier, later = sorted((first, second), key=lambda c: c.arrival)
    return later.arrival < earlier.departure + TURNAROUND_BUFFER


def conflicts(calls: list[Call]) -> list[tuple[Call, Call]]:
    """Every pair of calls that cannot both be honoured."""
    found = []
    for i, first in enumerate(calls):
        for second in calls[i + 1:]:
            if overlaps(first, second):
                found.append((first, second))
    return found


def unberthable(calls: list[Call]) -> list[Call]:
    """Calls assigned to a berth that is too short for them."""
    return [c for c in calls if not fits_berth(c)]
