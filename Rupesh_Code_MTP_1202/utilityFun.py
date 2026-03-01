from config import *


# === Utility Functions ===
def parse_time_to_minutes(t: str):
    """
    Converts a time string 'HH:MM' or 'HH:MM:SS' into minutes since midnight.
    Supports hours >= 24 (e.g., 24:05 → 1445 minutes, 25:07 → 1507 minutes)
    """
    try:
        t = t.strip()
        # Split HH:MM or HH:MM:SS
        parts = t.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        return hours * 60 + minutes
    except:
        return None


def get_base_station_name(station: str):
    """Extracts the base station name (first word) in uppercase."""
    if not station:
        return None
    return station.strip().split()[0].upper()


def rake_feasible_connection(s1, s2):
    """
    Checks if a connection between two services is feasible.
    - Must be same base station.
    - 0 <= (start - end) <= MAX_CONNECTION_GAP_MINUTES
    - If rake is same: allow directly.
    - If rake is different: allowed only at ALLOWED_RAKE_CHANGE_STATIONS 
      and gap >= MIN_RAKE_GAP_MINUTES.
    """

    # Skip if stations or times are missing
    if not s1.end_station or not s2.start_station or s1.end_time is None or s2.start_time is None:
        return False
    
    # Handle dummy start/end services
    if not s1.end_station or not s2.start_station:
        return False

    if s1.end_station != s2.start_station:
        return False

    gap = s2.start_time - s1.end_time

    # Must be non-negative and within max connection window
    if gap < 0 or gap > MAX_CONNECTION_GAP_MINUTES:
        return False

    if s1.rake_num == s2.rake_num:
        # Same rake: gap condition is already checked
        return True
    else:
        # Rake change allowed only at certain stations with min gap
        return (s1.end_station in ALLOWED_RAKE_CHANGE_STATIONS) and (gap >= MIN_RAKE_GAP_MINUTES)
