from utils import Customer, calculate_distance
import re

def load_cvrp_instance(filepath):
    """
    Loads a CVRP instance from a file in the CVRPLIB format.
    """
    print(f"Loading instance from {filepath}...")
    
    customers = []
    
    # We will read the file line by line and switch modes
    # as we encounter different sections.
    mode = 'HEADER' 
    dimension = 0
    vehicle_capacity = 0
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            
            if not line or line == "EOF":
                continue
                
            if "NODE_COORD_SECTION" in line:
                mode = 'COORDS'
                continue
            elif "DEMAND_SECTION" in line:
                mode = 'DEMANDS'
                continue
            elif "DEPOT_SECTION" in line:
                mode = 'DEPOT'
                continue
            
            # --- Parse Header ---
            if mode == 'HEADER':
                if "DIMENSION" in line:
                    dimension = int(re.search(r'\d+', line).group())
                    # Initialize our customer list with placeholders
                    customers = [None] * (dimension + 1)
                elif "CAPACITY" in line:
                    vehicle_capacity = int(re.search(r'\d+', line).group())
                elif "NAME" in line:
                    print(f"Loading instance: {line.split(':')[-1].strip()}")
            
            # --- Parse Coords ---
            elif mode == 'COORDS':
                parts = line.split()
                if len(parts) == 3:
                    node_id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    customers[node_id] = Customer(node_id, x, y, 0) # Demand set later
            
            # --- Parse Demands ---
            elif mode == 'DEMANDS':
                parts = line.split()
                if len(parts) == 2:
                    node_id = int(parts[0])
                    demand = int(parts[1])
                    if customers[node_id]:
                        customers[node_id].demand = demand
            
            # --- Parse Depot ---
            elif mode == 'DEPOT':
                node_id = int(line)
                if node_id == -1:
                    mode = 'EOF' # We are done
                    continue
                # The depot is already in our list, just identify it
                depot = customers[node_id]

    # Post-processing:
    # Separate depot from the main customer list
    # The paper's P-n19-k2 has 18 customers + 1 depot
    depot = customers[1] # By convention, depot is usually 1
    customer_nodes = [c for c in customers[2:] if c is not None] # All others
    
    # HACK: The num_vehicles is often not in the file, but in the filename
    # e.g., P-n19-k2 means 2 vehicles. We'll parse it.
    num_vehicles = 0
    k_match = re.search(r'-k(\d+)', filepath)
    if k_match:
        num_vehicles = int(k_match.group(1))
    else:
        print("Warning: Could not parse number of vehicles from filename. Defaulting to 1.")
        num_vehicles = 1
        
    # Pre-calculate distance matrix
    n = len(customers) -1 # Since we are 1-indexed
    distance_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if customers[i] and customers[j]:
                dist = calculate_distance(customers[i], customers[j])
                distance_matrix[i][j] = dist
            
    print(f"Loaded {len(customer_nodes)} customers, {num_vehicles} vehicles, capacity {vehicle_capacity}.")
    return depot, customer_nodes, num_vehicles, vehicle_capacity, distance_matrix