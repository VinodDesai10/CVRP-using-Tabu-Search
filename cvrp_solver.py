# Import the functions from our new files
from data_loader import load_cvrp_instance
from initial_solution import create_initial_solution
from local_search import local_search_by_swapping
from tabu_search import simple_tabu_search # <-- IMPORT THIS
from utils import calculate_solution_cost, calculate_route_demand
from visualizer import plot_solution

def main():
    
    
    # <-- CHANGE THIS LINE
    filepath = 'E-n23-k3.vrp'
    depot, customers, m, Q, dist_matrix = load_cvrp_instance(filepath)
    
    print(f"Loaded {len(customers)} customers, {m} vehicles, capacity {Q}.")
    
    # --- 2. Create Initial Solution ---
    print("\nCreating initial solution...")
    initial_solution = create_initial_solution(depot, customers, m, Q)
    initial_cost = calculate_solution_cost(initial_solution, dist_matrix)
    
    print("Initial Solution Found:")
    for i, route in enumerate(initial_solution):
        route_demand = calculate_route_demand(route)
        print(f"  Route #{i+1} (Demand: {route_demand}/{Q}): {route}")
    print(f"\nTotal Cost (Initial): {initial_cost:.2f}")
    
    # --- 3. Run Local Search ---
    print("\nApplying Local Search (Swap)...")
    ls_solution = local_search_by_swapping(initial_solution, Q, dist_matrix)
    ls_cost = calculate_solution_cost(ls_solution, dist_matrix)
    
    print("Local Search Complete:")
    for i, route in enumerate(ls_solution):
        route_demand = calculate_route_demand(route)
        print(f"  Route #{i+1} (Demand: {route_demand}/{Q}): {route}")
    print(f"\nTotal Cost (Local Search): {ls_cost:.2f}")

    # --- 4. Run Tabu Search ---
    # This implements the "Tabu Search Algorithm" block [cite: 134]
    print("\nApplying Tabu Search (Relocation)...")
    
    # Set algorithm parameters
    # We can tune these later
    NUM_ITERATIONS = 1000
    TABU_TENURE = 15 # Size of the tabu list
    
    ts_solution = simple_tabu_search(ls_solution, Q, dist_matrix, 
                                     NUM_ITERATIONS, TABU_TENURE)
    
    ts_cost = calculate_solution_cost(ts_solution, dist_matrix)
    
    print("\n--- FINAL RESULTS ---")
    
    print("Final Solution:")
    for i, route in enumerate(ts_solution):
        route_demand = calculate_route_demand(route)
        print(f"  Route #{i+1} (Demand: {route_demand}/{Q}): {route}")

    print("\n--- COST SUMMARY ---")
    print(f"Initial Cost:     {initial_cost:.2f}")
    print(f"Local Search Cost: {ls_cost:.2f}")
    print(f"Tabu Search Cost:  {ts_cost:.2f}")
    print(f"\nTotal Improvement: {initial_cost - ts_cost:.2f}")
    
    # --- 5. Visualize Solution ---  <-- ADD THIS BLOCK
    plot_solution(ts_solution, instance_name=filepath)

if __name__ == "__main__":
    main()