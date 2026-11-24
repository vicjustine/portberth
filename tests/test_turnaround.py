"""Tests for turnaround statistics."""

from datetime import datetime, timedelta

from berthwatch.schedule import Call
from berthwatch.turnaround import berth_utilisation, longest_stay, mean_turnaround


def call(vessel, berth, start_hour, hours):
    start = datetime(2026, 3, 2, start_hour)
    return Call(
        vessel=vessel,
        berth=berth,
        arrival=start,
        departure=start + timedelta(hours=hours),
        length_m=150,
    )


def test_mean_turnaround_of_two_calls():
    calls = [call("Alder", "A1", 6, 4), call("Brindle", "B1", 6, 8)]
    assert mean_turnaround(calls) == timedelta(hours=6)


def test_mean_turnaround_of_nothing_is_zero():
    assert mean_turnaround([]) == timedelta()


def test_berth_utilisation_is_a_fraction_of_the_window():
    calls = [call("Cedar", "A1", 0, 6), call("Dovetail", "B1", 0, 12)]
    used = berth_utilisation(calls, timedelta(hours=24))
    assert used == {"A1": 0.25, "B1": 0.5}


def test_longest_stay_picks_the_longest():
    calls = [call("Elm", "A1", 6, 4), call("Fathom", "B1", 6, 9)]
    assert longest_stay(calls).vessel == "Fathom"


def test_longest_stay_of_nothing_is_none():
    assert longest_stay([]) is None
