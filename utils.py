import math

# -------------------------------------------
# --- DATA STRUCTURES
# -------------------------------------------

class Customer:
    """
    Stores data for a single customer or the depot.
    The paper mentions storing ID, X, Y, and demand.
    The depot is just a customer with ID 1 (usually) and demand 0.
    """
    def __init__(self, id, x, y, demand):
        self.id = int(id)
        self.x = float(x)
        self.y = float(y)
        self.demand = int(demand)

    def __repr__(self):
        # Helper for printing
        return f"C[{self.id}]"

# -------------------------------------------
# --- HELPER FUNCTIONS
# -------------------------------------------

def calculate_distance(cust1, cust2):
    """
    Calculates the Euclidean distance between two customers.
    """
    return math.sqrt((cust1.x - cust2.x)**2 + (cust1.y - cust2.y)**2)

def calculate_solution_cost(solution, distance_matrix):
    """
    Calculates the total cost of a solution (a list of routes).
    A solution is a list of routes, e.g., [[C[1], C[5], C[1]], [C[1], C[2], C[1]]]
    """
    total_cost = 0
    for route in solution:
        # [cite_start]Calculate cost for one route (tour) [cite: 117-118]
        for i in range(len(route) - 1):
            cust_a = route[i]
            cust_b = route[i+1]
            total_cost += distance_matrix[cust_a.id][cust_b.id]
    return total_cost

def calculate_route_demand(route):
    """
    Calculates the total demand of all customers in a single route.
    """
    total_demand = 0
    for customer in route:
        total_demand += customer.demand
    return total_demand