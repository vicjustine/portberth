# berthwatch

Berth allocation and turnaround tracking for port terminals.

A berth has a rated length and can take one vessel at a time, with a two-hour
turnaround buffer between a departure and the next arrival. `berthwatch` checks a
draft schedule for vessels assigned to berths that are too short for them, and for
calls that collide on the same berth.

## Berths

| Berth | Rated length |
|-------|--------------|
| A1    | 180 m        |
| A2    | 180 m        |
| B1    | 260 m        |
| B2    | 310 m        |

## Use

    from berthwatch.schedule import conflicts, unberthable

    conflicts(draft)     # pairs of calls that cannot both be honoured
    unberthable(draft)   # calls on a berth that is too short

All vessel names and schedules in the tests are synthetic.

## Operations

Schedules are reviewed by the duty berth planner.
