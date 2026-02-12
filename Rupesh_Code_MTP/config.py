# === Configuration ===
TIMETABLE_FILE = "C:/Users/srupe/Downloads/crew/mainLoop_aadesh.csv"
MIN_RAKE_GAP_MINUTES = 30   # Minimum required gap between different rakes
ALLOWED_RAKE_CHANGE_STATIONS = {"KKDA", "PVGW"}  # Allowed rake-change stations
MAX_CONNECTION_GAP_MINUTES = 120   # Maximum allowed gap between services
BREAK_STATIONS = {"KKDA", "PVGW"}  # Breaks allowed only here
CUMULATIVE_BREAKS_DURATION = 120    # cumulative breaks should be less than CUMULATIVE_BREAKS_DURATIONS min
SHORT_BREAK = 30     # short break duration
LONG_BREAK =  50     # Long break duration
DUTY_TIME_LIMIT = 445 # Noraml duty duration
MORN_EVEN_DUTY_TIME_LIMIT = 405  # morning and evening duty time duration
MORNING_SHIFT_CUTOFF = 360     # 360 -> 6:00 AM
EVENING_SHIFT_CUTOFF = 1410     # 1410 -> 23:30 PM
CONTINUOUS_DRIVE_LIMIT = 180   # continuous driving without a break greater than 30 mins in it.
DRIVING_TIME_LIMIT =360        # Actual driving time(Mins) it have gaps< SHORT_BREAKS also counted in it


# === Jurisdiction Buckets ===
jurisdiction_dict = {
    1: {'MKPR','MKPR UP','MKPR DN','SAKP','DDSC','DDSC DN PF','DDSC SDG','DDSC SDG STABLE (DAY)','DDSC DN',
        'DDSC SDG','PVGW','PVGW UP','PVGW DN','MKPD','MKPD','SAKP 3RD','SAKP 3RD PF','MKPR DN SDG','MKPR DN PF','DDSC DN SDG'},
        
    2: {'MUPR DN SDG STABLE (DAY)','MUPR 4TH SDG STABLE (DAY)','MUPR 3RD SDG STABLE','SVVR','SVVR DN','MUPR',
        'MUPR DN','MUPR 4TH','MUPR 3RD SDG','KKDA DN','KKDA UP','IPE','IPE 3RD PF','IPE 3RD','VND','VND (M)',
        'MVPO','MVPO DN','NZM','NIZM','KKDA','MUPR DN SDG','MVPO DN PF','SVVR DN PF','MUPR 3RD SDG','MUPR 4TH PF',
        'MUPR 4TH SDG','MUPR DN PF','MUPR DN SDG','MUPR DN SDG'}
}



