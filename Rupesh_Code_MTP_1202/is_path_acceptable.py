from config import *

def is_path_acceptable(
    path, end_service,
    total_driving_time, DRIVING_TIME_LIMIT,
    DUTY_TIME_LIMIT
):
    """
    Checks whether a partial path is acceptable:
    - Driving time limit
    - Duty time limit
    - Continuous driving CONTINUOUS_DRIVE_LIMIT-min rule
    """

    
    # -----------------------------
    # Condition 1: Driving time limit
    # -----------------------------
    if total_driving_time > DRIVING_TIME_LIMIT:
        return False

    # -----------------------------
    # Condition 2: Duty time limit
    # -----------------------------
    first_service_start_time = path[1].start_time  # skip dummy SOURCE

    if path[-1] == end_service:
        last_service = path[-2]  # path ended with sink dummy
    else:
        last_service = path[-1]

    last_service_end_time = last_service.end_time
    total_duty_time = last_service_end_time - first_service_start_time

    # Morning/evening tighter limit
    if first_service_start_time < MORNING_SHIFT_CUTOFF or first_service_start_time > EVENING_SHIFT_CUTOFF:
        effective_duty_limit = MORN_EVEN_DUTY_TIME_LIMIT
    else:
        effective_duty_limit = DUTY_TIME_LIMIT      # usually 445

    if total_duty_time > effective_duty_limit:
        return False

    # -----------------------------
    # Condition 3: Continuous driving CONTINUOUS_DRIVE_LIMIT rule
    # -----------------------------
    continuous_drive = 0
    long_break_required = False   # NEW: becomes True once continuous driving > 120

    # skip dummy SOURCE and SINK
    end_index = len(path) - 1 if path[-1] == end_service else len(path)


    for i in range(1, end_index):
        current_service = path[i]
        service_time = current_service.service_time or 0
        continuous_drive += service_time

        # NEW: once 120 mins crossed, next break must be LONG
        if continuous_drive > 120:
            long_break_required = True
    
        # Add gap to next service if it exists
        if i < end_index - 1:
            next_service = path[i + 1]
            gap_btw_service = next_service.start_time - current_service.end_time
    
            if gap_btw_service < SHORT_BREAK:
                continuous_drive += gap_btw_service
            elif gap_btw_service >= SHORT_BREAK:
                  # NEW: short break not allowed after crossing 120 mins
                if long_break_required and gap_btw_service < LONG_BREAK:
                 return False
                
                # valid break → reset
                continuous_drive = 0
                long_break_required = False
    
        # Rule: cannot exceed continuous drive limit
        if continuous_drive > CONTINUOUS_DRIVE_LIMIT:
            return False

    # -----------------------------
    # All conditions passed
    # -----------------------------
    return True
