import csv
from is_path_acceptable import is_path_acceptable
from is_final_path_valid import is_final_path_valid
from config import *


def stack_based_all_paths(
    G, start_service, end_service,
    DRIVING_TIME_LIMIT, DUTY_TIME_LIMIT,
    max_paths=int,
    output_csv=str
):
    """
    Enumerates all feasible paths using stack-based DFS.
    Saves valid paths (formatted) into a CSV file.
    """
    stack = [(start_service, [start_service], 0)]  # node, path_so_far, driving time
    n = 0

    with open(output_csv, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        while stack:
            if n >= max_paths:
                break

            current_service, path, total_driving_time = stack.pop()

            for neighbor_id in G.successors(current_service.service_id):
                neighbor = G.nodes[neighbor_id]["data"]
                service_time = neighbor.service_time or 0

                # Calculate gap 
                last_service = path[-1]
                if neighbor.start_time is not None and last_service.end_time is not None:
                    gap = neighbor.start_time - last_service.end_time
                else:
                    gap = 0

                new_total_driving_time = total_driving_time + service_time
                if gap < SHORT_BREAK:                                             # changed here <=
                    new_total_driving_time += gap

                new_path = path + [neighbor]

                if is_path_acceptable(
                    new_path, end_service,
                    new_total_driving_time, DRIVING_TIME_LIMIT,
                    DUTY_TIME_LIMIT
                ):
                    if neighbor.service_id == end_service.service_id:
                        if is_final_path_valid(new_path):
                            n += 1

                            # Extract middle services (exclude S and T)
                            middle_services = [s.service_id for s in new_path[1:-1]]

                            # Write as separate columns (no quotes)
                            writer.writerow(middle_services)

                            #print(",".join(map(str, middle_services)))

                    else:
                        stack.append((neighbor, new_path, new_total_driving_time))

    print(f"Total valid paths found: {n}")
    return n
