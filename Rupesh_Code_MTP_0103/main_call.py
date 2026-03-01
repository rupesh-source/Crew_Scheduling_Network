from service import load_services
import time
from graph import build_graph
from stack import stack_based_all_paths
from service import *
from config import *


#----------------------------------# Adding Dummy Nodes
# Dummy start node
start_service = Service(
    service_id="S",
    rake_num=None,
    start_station=None,
    start_time=None,
    end_station=None,
    end_time=None,
    direction=None,
    service_time=0,
    same_jurisdiction=None,
    step_back_rake=None,
    step_back_location=None,
    merged_rake_num1=None,
    merged_rake_num2=None
)

# Dummy end node
end_service = Service(
    service_id="T",
    rake_num=None,
    start_station=None,
    start_time=None,
    end_station=None,
    end_time=None,
    direction=None,
    service_time=0,
    same_jurisdiction=None,
    step_back_rake=None,
    step_back_location=None,
    merged_rake_num1=None,
    merged_rake_num2=None
)


# Start total timer
total_start_time = time.time()

# ================================
#  Load CSV services
# ================================
start_time = time.time()
TIMETABLE_FILE = "C:/Users/srupe/Desktop/MTP/crew/mainLoop_aadesh.csv"
OUTPUT_CSV="valid_paths_using_Network_2802_test.csv"
services = load_services(TIMETABLE_FILE)
end_time = time.time()
print(f"Loaded {len(services)} services in {end_time - start_time:.3f} seconds")

# ================================
# Build graph with Service objects
# ================================
start_time = time.time()
G = build_graph(services, start_service, end_service)
end_time = time.time()
print(f"Built graph with {len(G.nodes)} nodes and {len(G.edges)} edges in {end_time - start_time:.3f} seconds")

# ================================
# Call stack-based path finder
# ================================
start_time = time.time()
valid_paths_count = stack_based_all_paths(
    G,
    start_service=start_service,
    end_service=end_service,
    DRIVING_TIME_LIMIT=DRIVING_TIME_LIMIT,
    DUTY_TIME_LIMIT=DUTY_TIME_LIMIT,
    max_paths=100000,
    output_csv=OUTPUT_CSV
)
end_time = time.time()
print(f"Found {valid_paths_count} valid paths in {end_time - start_time:.3f} seconds")

# ================================
# Total time
# ================================
total_end_time = time.time()
print(f"[Total Time] {total_end_time - total_start_time:.3f} seconds")
