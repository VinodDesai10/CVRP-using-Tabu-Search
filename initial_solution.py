import random

def create_initial_solution(depot, customers, num_vehicles, vehicle_capacity):
    """
    Implements the Initial_Solution() algorithm from the paper.
    It randomly assigns customers to routes, respecting capacity.
    [cite_start][cite: 144-161]
    """
    
    solution = []
    unassigned_customers = list(customers)
    
    while unassigned_customers:
        solution = []
        unassigned_customers = list(customers)
        random.shuffle(unassigned_customers)
        
        # for each tour j = 1...m
        for _ in range(num_vehicles):
            tour = [depot] # T' <- (d)
            current_demand = 0
            
            for customer in list(unassigned_customers):
                
                # Check capacity constraint: sum(d_i) <= Q
                if current_demand + customer.demand <= vehicle_capacity:
                    tour.append(customer) # T' <- T' U {i}
                    current_demand += customer.demand
                    unassigned_customers.remove(customer)
            
            tour.append(depot) # T' <- T' U {d}
            solution.append(tour) # S <- S U {T'}

        if unassigned_customers:
            pass # The outer 'while' loop will handle the retry

    return solution