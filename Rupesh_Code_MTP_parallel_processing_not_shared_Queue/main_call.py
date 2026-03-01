from service import load_services
import time
from graph import build_graph
from stack import stack_based_all_paths
from service import *
from config import *
from multiprocessing import Process, Queue


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



import time
from multiprocessing import Process, Queue


def worker(G, start_service, end_service,
           DRIVING_TIME_LIMIT, DUTY_TIME_LIMIT,
           allowed_services, output_csv, q):

    count = stack_based_all_paths(
        G,
        start_service=start_service,
        end_service=end_service,
        DRIVING_TIME_LIMIT=DRIVING_TIME_LIMIT,
        DUTY_TIME_LIMIT=DUTY_TIME_LIMIT,
        max_paths=10000,
        output_csv=output_csv,
        allowed_first_services=allowed_services
    )

    q.put(count)


if __name__ == "__main__":

    total_start_time = time.time()

    # ================================
    # Load services
    # ================================
    TIMETABLE_FILE = "C:/Users/srupe/Desktop/MTP/crew/mainLoop_aadesh.csv"
    services = load_services(TIMETABLE_FILE)

    # ================================
    # Build graph
    # ================================
    start_time = time.time()
    G = build_graph(services, start_service, end_service)
    end_time = time.time()
    print(f"Built graph with {len(G.nodes)} nodes and {len(G.edges)} edges in {end_time - start_time:.3f} seconds")

    # ================================
    # Dynamic Split into 4 Workers
    # ================================
    num_workers = 6

    all_services = [str(i) for i in range(1, 945)]   # 1–944
    chunk_size = len(all_services) // num_workers

    chunks = [
        all_services[i:i + chunk_size]
        for i in range(0, len(all_services), chunk_size)
    ]

    q = Queue()
    processes = []

    start_time = time.time()

    for idx, chunk in enumerate(chunks):
        p = Process(
            target=worker,
            args=(G, start_service, end_service,
                  DRIVING_TIME_LIMIT, DUTY_TIME_LIMIT,
                  chunk,
                  f"valid_paths_part{idx+1}.csv",
                  q)
        )
        processes.append(p)

    # Start all workers
    for p in processes:
        p.start()

    # Wait for completion
    for p in processes:
        p.join()

    # Collect results
    total_count = 0
    for _ in processes:
        total_count += q.get()

    end_time = time.time()

    print(f"Total valid paths: {total_count}")
    print(f"Parallel time (4 workers): {end_time - start_time:.3f} seconds")

    total_end_time = time.time()
    print(f"[Total Time] {total_end_time - total_start_time:.3f} seconds")