import networkx as nx
from collections import defaultdict
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


from utilityFun import parse_time_to_minutes, get_base_station_name

class Service:
    def __init__(
        self,
        service_id, 
        rake_num,
        start_station,
        start_time,
        end_station,
        end_time,
        direction,
        service_time=0,
        same_jurisdiction=None,
        step_back_rake=None,
        step_back_location=None,
        merged_rake_num1=None,
        merged_rake_num2=None
    ):
        self.service_id = str(service_id)
        self.rake_num = rake_num
        self.start_station = start_station
        self.start_time = start_time
        self.end_station = end_station
        self.end_time = end_time
        self.direction = direction
        self.service_time = int(service_time) if service_time else 0
        self.same_jurisdiction = same_jurisdiction
        self.step_back_rake = step_back_rake
        self.step_back_location = step_back_location
        self.merged_rake_num1 = merged_rake_num1
        self.merged_rake_num2 = merged_rake_num2


def load_services(csv_file):
    df = pd.read_csv(csv_file)
    services = []
    for _, row in df.iterrows():
        s = Service(
            service_id=row.get("Service"),   
            rake_num=row.get("Rake Num"),
            start_station=get_base_station_name(row.get("Start Station")),
            start_time=parse_time_to_minutes(row.get("Start Time")),
            end_station=get_base_station_name(row.get("End Station")),
            end_time=parse_time_to_minutes(row.get("End Time")),
            direction=row.get("Direction"),
            service_time=int(row["service time"]) if "service time" in row and pd.notna(row["service time"]) else 0,
            same_jurisdiction=row["Same Jurisdiction"] if "Same Jurisdiction" in row else None,
            step_back_rake=row["Step Back Rake"] if "Step Back Rake" in row else None,
            step_back_location=row["Step Back Location"] if "Step Back Location" in row else None,
            merged_rake_num1=row["mergedRakeNum1"] if "mergedRakeNum1" in row else None,
            merged_rake_num2=row["mergedRakeNum2"] if "mergedRakeNum2" in row else None,
        )
        services.append(s)
    return services





