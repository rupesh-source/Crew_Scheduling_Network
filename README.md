Delhi Metro Crew Allocation – README

Project Overview
----------------
This project focuses on generating feasible crew duty schedules for the Delhi Metro Rail Corporation (DMRC).
The system is designed in compliance with the Hours of Work and Periods of Rest (HOER) rules and operational
constraints specific to Delhi Metro.

The model reads the complete set of train service data, builds a service connectivity network, and traces all
feasible crew paths (duties) using a stack-based Depth First Search (DFS) algorithm.


Key Features
-------------
- Automatic Service Loading:
  Reads all train service details from a CSV file (MainLoop file) and loads them into the Service class.

- Graph Construction:
  Builds a directed graph where each node represents a service and edges represent feasible connections based on:
    * Time feasibility (EndTime ≤ StartTime_next)
    * Location continuity (EndStation = StartStation_next)
    * Jurisdiction and rake constraints

- Feasible Path Generation:
  Uses a stack-based DFS approach to enumerate all valid crew paths while enforcing:
    * Maximum duty duration limits
    * Maximum driving time
    * Break and jurisdiction constraints
    * Rake change limitations

- Optimization Ready:
  The feasible paths generated can be used later in the optimization phase (Set Covering Model) to select an
  optimal combination of duties that covers all services with minimal crew count.


File Structure
---------------
Delhi_Metro_Crew_Allocation/
│
├── Ultimate_phase_1.ipynb       # Main notebook to run the crew path generation process
├── mainLoop.csv          # Input file containing service data
├── Crew_Allocation_Rules.txt    # Crew allocation rules and constraints
├── README.txt                   # Project documentation
└── Outputs/                     # (Optional) Folder to store generated duties or outputs


Input File Description (mainLoop_aadesh.csv)
--------------------------------------------
The MainLoop file contains all service-related data for a given day or metro line.

Typical columns include:
- Service: Unique service number
- Rake Num: Train rake number
- Start Station: Starting station of the service
- Start Time: Service start time
- End Station: Ending station of the service
- End Time: Service end time
- Direction: Direction of travel
- Service Time: Duration of the service
- Same Jurisdiction: Indicates if the service is within the same jurisdiction
- Step Back Rake: Step back rake assignment
- Step Back Location: Location of step back operation


Workflow
---------
1. Upload Input File:
   Upload 'mainLoop_aadesh.csv' in the Jupyter environment before executing the notebook.

2. Load Services:
   The notebook reads and stores each service as an instance of the Service class containing details like
   start/end stations, timings, and rake numbers.

3. Build Service Graph:
   A directed graph is created where edges are formed between feasible service pairs satisfying:
     EndStation(A) = StartStation(B)
     EndTime(A) ≤ StartTime(B)
   and all rake, jurisdiction, and time gap constraints.

4. Trace Feasible Paths:
   A stack-based DFS algorithm explores all possible paths in the graph to identify valid crew duties.
   Each path is validated against all crew allocation rules defined in Crew_Allocation_Rules.txt.

5. Output:
   Feasible duties (service combinations) are printed or stored for further optimization.


Dependencies
-------------
- pandas
- numpy
- networkx
- datetime

To install dependencies, run:
pip install pandas numpy networkx

