from utils import calculate_route_demand

def local_search_by_swapping(solution, vehicle_capacity, dist_matrix):
    """
    Implements the Local_Search_By_Swapping(S) algorithm[cite: 176].
    It performs one full pass, checking all possible pairs of customers
    for a cost-reducing and feasible swap.
    """
    # A simple flag to track if we made any improvements in this pass
    improved = True
    
    # We'll use a 'while' loop to repeat the process until no more 
    # improvements can be found in a full pass. This is a common
    # "local search descent" strategy.
    while improved:
        improved = False
        
        # Iterate over all routes (r1)
        for r1_idx in range(len(solution)):
            route1 = solution[r1_idx]
            
            # Iterate over all customers in route1 (skip depot at start/end)
            # The pseudocode's 'l' loop [cite: 180]
            for c1_idx in range(1, len(route1) - 1):
                
                # Iterate over all routes (r2), starting from the current route (r1)
                # The pseudocode's 'j'' loop [cite: 183, 186]
                for r2_idx in range(r1_idx, len(solution)):
                    route2 = solution[r2_idx]
                    
                    # Determine start index for c2_idx
                    # If same route, start at next customer to avoid redundant pairs
                    # [cite: 184]
                    start_c2_idx = 1
                    if r1_idx == r2_idx:
                        start_c2_idx = c1_idx + 1
                    
                    # Iterate over all customers in route2 (skip depot)
                    # The pseudocode's 'l'' loop [cite: 192]
                    for c2_idx in range(start_c2_idx, len(route2) - 1):
                        
                        # --- 1. Get customers and their neighbors ---
                        cust1 = route1[c1_idx]
                        cust2 = route2[c2_idx]
                        
                        c1_prev = route1[c1_idx - 1]
                        c1_next = route1[c1_idx + 1]
                        
                        c2_prev = route2[c2_idx - 1]
                        c2_next = route2[c2_idx + 1]
                        
                        # --- 2. Check Capacity Constraint  ---
                        # This check is slightly different if it's an intra-route swap
                        if r1_idx == r2_idx:
                            # Intra-route swap: demands don't change, always feasible
                            pass # Always feasible
                        else:
                            # Inter-route swap: check new demands
                            r1_new_demand = calculate_route_demand(route1) - cust1.demand + cust2.demand
                            r2_new_demand = calculate_route_demand(route2) - cust2.demand + cust1.demand
                            
                            if (r1_new_demand > vehicle_capacity or 
                                r2_new_demand > vehicle_capacity):
                                continue # Swap is not feasible, skip
                        
                        # --- 3. Calculate Cost Change (Delta) [cite: 194-195] ---
                        cost_removed = 0
                        cost_added = 0
                        
                        if r1_idx == r2_idx:
                            # Intra-route swap (handling adjacent vs. non-adjacent)
                            if c1_idx + 1 == c2_idx:
                                # Case A: Adjacent swap (c1, c2)
                                cost_removed = (dist_matrix[c1_prev.id][cust1.id] + 
                                                dist_matrix[cust1.id][cust2.id] + 
                                                dist_matrix[cust2.id][c2_next.id])
                                cost_added = (dist_matrix[c1_prev.id][cust2.id] + 
                                              dist_matrix[cust2.id][cust1.id] + 
                                              dist_matrix[cust1.id][c2_next.id])
                            else:
                                # Case B: Non-adjacent swap
                                cost_removed = (dist_matrix[c1_prev.id][cust1.id] + 
                                                dist_matrix[cust1.id][c1_next.id] +
                                                dist_matrix[c2_prev.id][cust2.id] + 
                                                dist_matrix[cust2.id][c2_next.id])
                                cost_added = (dist_matrix[c1_prev.id][cust2.id] + 
                                              dist_matrix[cust2.id][c1_next.id] +
                                              dist_matrix[c2_prev.id][cust1.id] + 
                                              dist_matrix[cust1.id][c2_next.id])
                        else:
                            # Case C: Inter-route swap
                            cost_removed = (dist_matrix[c1_prev.id][cust1.id] + 
                                            dist_matrix[cust1.id][c1_next.id] +
                                            dist_matrix[c2_prev.id][cust2.id] + 
                                            dist_matrix[cust2.id][c2_next.id])
                            cost_added = (dist_matrix[c1_prev.id][cust2.id] + 
                                          dist_matrix[cust2.id][c1_next.id] +
                                          dist_matrix[c2_prev.id][cust1.id] + 
                                          dist_matrix[cust1.id][c2_next.id])
                        
                        delta = cost_added - cost_removed
                        
                        # --- 4. Perform Swap if Profitable  ---
                        if delta < -0.0001: # Use a small tolerance for floating point
                            # Swap is feasible and reduces cost, perform it
                            # [cite: 198-200]
                            route1[c1_idx] = cust2
                            route2[c2_idx] = cust1
                            
                            improved = True
                            
                            # Since we made a swap, we break the inner loops
                            # and restart the 'while' loop to do a fresh pass
                            # on the new solution.
                            break
                    if improved:
                        break
            if improved:
                break

    return solution