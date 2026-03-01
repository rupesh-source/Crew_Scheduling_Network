from utilityFun import rake_feasible_connection
import networkx as nx


def build_graph(services_list, start_service, end_service):
    """
    Build a directed graph from Service objects.
    All nodes are Service objects (including start and end dummies).
    """

    services_list = [s for s in services_list if s.start_time is not None and s.end_time is not None]

    G = nx.DiGraph()

    # Add nodes (store Service object directly as key)
    for s in services_list:
        G.add_node(s.service_id, data=s)

    # Add start/end dummy nodes
    G.add_node(start_service.service_id, data=start_service)
    G.add_node(end_service.service_id, data=end_service)

    # Connect source to all services
    for s in services_list:
        G.add_edge(start_service.service_id, s.service_id, color="black")

    # Feasible service_id-to-service_id connections
    for i, s1 in enumerate(services_list):
        for j, s2 in enumerate(services_list):
            if i == j:
                continue
            if rake_feasible_connection(s1, s2):
                #edge_color = "red" if s1.rake_num != s2.rake_num else "gray"
                G.add_edge(s1.service_id, s2.service_id)

    # Connect all services to sink
    for s in services_list:
        G.add_edge(s.service_id, end_service.service_id, color="black")

    return G
