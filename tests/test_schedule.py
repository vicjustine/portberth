"""Tests for berth allocation rules."""

from datetime import datetime, timedelta

from berthwatch.schedule import Call, conflicts, fits_berth, overlaps, unberthable


def call(vessel, berth, start_hour, hours, length_m=150):
    start = datetime(2026, 3, 2, start_hour)
    return Call(
        vessel=vessel,
        berth=berth,
        arrival=start,
        departure=start + timedelta(hours=hours),
        length_m=length_m,
    )


def test_vessel_fits_its_berth():
    assert fits_berth(call("Alder", "B2", 6, 8, length_m=300)) is True


def test_vessel_too_long_for_berth():
    assert fits_berth(call("Brindle", "A1", 6, 8, length_m=240)) is False


def test_same_berth_overlapping_calls_collide():
    first = call("Cedar", "A1", 6, 6)
    second = call("Dovetail", "A1", 10, 4)
    assert overlaps(first, second) is True


def test_buffer_is_enforced_between_calls():
    first = call("Elm", "A2", 6, 4)
    second = call("Fathom", "A2", 11, 4)
    assert overlaps(first, second) is True


def test_clear_gap_is_not_a_conflict():
    first = call("Gale", "A2", 6, 4)
    second = call("Harrier", "A2", 13, 4)
    assert overlaps(first, second) is False


def test_different_berths_never_collide():
    first = call("Ibis", "A1", 6, 12)
    second = call("Jetty", "B1", 6, 12)
    assert overlaps(first, second) is False


def test_conflicts_reports_each_pair_once():
    calls = [call("Kestrel", "A1", 6, 6), call("Lantern", "A1", 8, 6)]
    assert len(conflicts(calls)) == 1


def test_unberthable_lists_oversize_calls():
    calls = [
        call("Mistral", "A1", 6, 4, length_m=240),
        call("Nomad", "B2", 6, 4, length_m=300),
    ]
    assert [c.vessel for c in unberthable(calls)] == ["Mistral"]
