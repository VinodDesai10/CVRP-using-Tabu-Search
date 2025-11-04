import copy
from utils import calculate_solution_cost, calculate_route_demand

def simple_tabu_search(solution, vehicle_capacity, dist_matrix, iters, tabu_tenure):
    """
    Implements the Simple_Tabu_Search(S, iters, tabuTenure) algorithm.
    It uses a relocation neighborhood (moving one customer) and a
    tabu list to avoid cycling.
    """
    
    # We need to deepcopy, as we'll be modifying the current solution
    # but S_best should be a separate object.
    S_cur = copy.deepcopy(solution)
    S_best = copy.deepcopy(solution)
    
    # Calculate initial costs
    current_cost = calculate_solution_cost(S_cur, dist_matrix)
    best_cost = current_cost
    
    # Tabu list 'L' [cite: 208]
    # We'll store the customer ID that was moved.
    tabu_list = []
    
    print(f"Starting Tabu Search. Initial Cost: {best_cost:.2f}")

    # Main loop: while iter < iters [cite: 230]
    for iter_num in range(iters):
        
        # Variables to store the best move found in this iteration
        # We need to find the best move, even if it's non-improving.
        best_move = None
        best_move_delta = float('inf') # M_im / C_im in paper [cite: 214-215]
        
        # --- 1. Explore the "Relocation" Neighborhood ---
        # Iterate over every route r1
        for r1_idx in range(len(S_cur)):
            # Iterate over every customer in r1 (skip depots)
            for c_idx in range(1, len(S_cur[r1_idx]) - 1):
                
                customer_to_move = S_cur[r1_idx][c_idx]
                
                # Iterate over every route r2 (can be the same as r1)
                for r2_idx in range(len(S_cur)):
                    # Iterate over every possible insertion position in r2 (skip depot 0)
                    for insert_pos in range(1, len(S_cur[r2_idx])):
                        
                        # --- 2. Check Feasibility and Calculate Cost Delta ---
                        
                        # Don't evaluate moving a customer to the same spot
                        if r1_idx == r2_idx and (c_idx == insert_pos or c_idx + 1 == insert_pos):
                            continue
                        
                        # Check Capacity Constraint [cite: 254]
                        if r1_idx != r2_idx:
                            if calculate_route_demand(S_cur[r2_idx]) + customer_to_move.demand > vehicle_capacity:
                                continue # Move is not feasible
                        
                        # Calculate cost change (delta)
                        
                        # Cost of removing customer from route 1
                        c_prev = S_cur[r1_idx][c_idx - 1]
                        c_next = S_cur[r1_idx][c_idx + 1]
                        cost_removed = (dist_matrix[c_prev.id][customer_to_move.id] + 
                                        dist_matrix[customer_to_move.id][c_next.id] - 
                                        dist_matrix[c_prev.id][c_next.id])
                        
                        # Cost of inserting customer into route 2
                        ins_prev = S_cur[r2_idx][insert_pos - 1]
                        ins_next = S_cur[r2_idx][insert_pos]
                        cost_added = (dist_matrix[ins_prev.id][customer_to_move.id] + 
                                      dist_matrix[customer_to_move.id][ins_next.id] - 
                                      dist_matrix[ins_prev.id][ins_next.id])
                        
                        delta = cost_added - cost_removed
                        
                        # --- 3. Evaluate Move (Tabu + Aspiration) ---
                        
                        is_tabu = customer_to_move.id in tabu_list
                        
                        # Aspiration Criterion: [cite: 211]
                        # If this move gives us a new *all-time* best solution
                        aspiration_met = current_cost + delta < best_cost
                        
                        if aspiration_met:
                            # This is a great move, take it
                            if delta < best_move_delta:
                                best_move = (r1_idx, c_idx, r2_idx, insert_pos)
                                best_move_delta = delta
                        elif is_tabu:
                            # It's tabu and doesn't meet aspiration, skip it
                            continue
                        else:
                            # It's not tabu, check if it's the best so far
                            if delta < best_move_delta:
                                best_move = (r1_idx, c_idx, r2_idx, insert_pos)
                                best_move_delta = delta
        
        # --- 4. Perform the Best Move Found ---
        
        if best_move is None:
            # No feasible moves found, this shouldn't happen
            print("No feasible moves found, stopping TS.")
            break

        # Unpack the best move
        (r1_idx, c_idx, r2_idx, insert_pos) = best_move
        
        # Perform the move on S_cur
        customer_to_move = S_cur[r1_idx].pop(c_idx)
        
        if r1_idx == r2_idx:
            # Handle intra-route move (indices may have shifted)
            if c_idx < insert_pos:
                S_cur[r2_idx].insert(insert_pos - 1, customer_to_move)
            else:
                S_cur[r2_idx].insert(insert_pos, customer_to_move)
        else:
            # Inter-route move
            S_cur[r2_idx].insert(insert_pos, customer_to_move)
            
        # Update current cost
        current_cost += best_move_delta
        
        # --- 5. Update Tabu List ---
        tabu_list.append(customer_to_move.id)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0) # Remove the oldest item
            
        # --- 6. Update Best Solution Found So Far (S_best) ---
        if current_cost < best_cost:
            best_cost = current_cost
            S_best = copy.deepcopy(S_cur)
            print(f"  Iter {iter_num}: New Best Cost = {best_cost:.2f}")

    print(f"Tabu Search Complete. Final Best Cost: {best_cost:.2f}")
    return S_best