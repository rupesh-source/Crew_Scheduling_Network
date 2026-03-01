from functools import lru_cache
from config import *

@lru_cache(maxsize=None)
def get_jurisdiction_groups(station):
    """
    Return the set of jurisdiction groups a station belongs to.

    Add caching (lru_cache) so repeated calls with the same station
    are very cheap. We return a frozenset (immutable) so the cached object is
    stable and safe to use with set operations like isdisjoint.
    """
    # build frozenset from global jurisdiction_dict 
    return frozenset(
        Jurisdiction_group_id
        for Jurisdiction_group_id, stations in jurisdiction_dict.items()
        if station in stations
    )


def is_final_path_valid(path):
    """
    Check if a completed path ending at end_service is valid based on:
    1. Jurisdiction overlap between first and last duty.
    2. Required break conditions.
    """

    # === Jurisdiction check ===
    start_station_first_duty = path[1].start_station
    end_station_last_duty = path[-2].end_station

    start_groups = get_jurisdiction_groups(start_station_first_duty)
    end_groups = get_jurisdiction_groups(end_station_last_duty)

    # Short-circuit early: if no overlap in jurisdiction groups => invalid path.
    # This avoids running the more expensive break logic when jurisdiction fails.
    if start_groups.isdisjoint(end_groups):
        return False

    # Pass computed start_groups into has_required_breaks to
    # avoid recomputing the same group inside that function.
    if not has_required_breaks(path, start_jurisdictions=start_groups):
        return False

    return True


def has_required_breaks(path, start_jurisdictions=None):
    """
    Check break conditions:
    Case 1: Only one break >=50min (and total < CUMULATIVE_BREAKS_DURATION).
    Case 2: Multiple breaks:
        - If there a 30min break, at least one >=50min break must also exist.
        - Two or more >=50min breaks are allowed.
        - In all cases, total < CUMULATIVE_BREAKS_DURATION.
    Additional:
    - At least one break must lie within the jurisdiction of the first duty's start station.
    """

    if len(path) < 6:
        return False  # skip very short paths

    # Use passed-in start_jurisdictions if available (avoids recomputation).
    if start_jurisdictions is None:
        start_station_first_duty = path[1].start_station
        start_jurisdictions = get_jurisdiction_groups(start_station_first_duty)

    # Extract times
    start_times = [s.start_time for s in path[1:-1]]
    end_times = [s.end_time for s in path[1:-1]]

    gaps = [
        start_times[i + 1] - end_times[i]
        for i in range(len(start_times) - 1)
    ]

    breaks = []
    has_break_in_same_jurisdiction = False

    for i, break_gap in enumerate(gaps):
        station = path[1 + i].end_station  # station where break occurs

        # Only consider allowed break stations and minimal break_gap
        if station in BREAK_STATIONS and break_gap >= SHORT_BREAK:
            breaks.append(break_gap)

            break_jurisdictions = get_jurisdiction_groups(station)
            if not start_jurisdictions.isdisjoint(break_jurisdictions):
                has_break_in_same_jurisdiction = True

    if not breaks:
        return False

    # Ensure at least one break is in same jurisdiction
    if not has_break_in_same_jurisdiction:
        return False

    total_break = sum(breaks)
    if total_break > CUMULATIVE_BREAKS_DURATION:                       # changed here
        return False

    has_SHORT_BREAK = any(SHORT_BREAK <= b < LONG_BREAK for b in breaks)
    has_LONG_BREAK = any(b >= LONG_BREAK for b in breaks)

    # Case 1: single break
    if len(breaks) == 1:
        return has_LONG_BREAK

    # Case 2: multiple breaks
    if has_SHORT_BREAK and not has_LONG_BREAK:
        return False  # shorts without a long break not allowed

    # Valid if (short + long) OR (multiple longs)
    return True
