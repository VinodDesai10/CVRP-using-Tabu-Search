import matplotlib
matplotlib.use('Agg')   
import matplotlib.pyplot as plt
import os

def plot_solution(solution, instance_name="CVRP Solution"):
    """
    Plots the CVRP solution using Matplotlib and saves it to a file.
    Each route will be a different color.
    """
    print("Generating plot...")
    
    plt.figure(figsize=(10, 8))
    
    # A list of colors for the routes
    colors = plt.cm.jet([i / len(solution) for i in range(len(solution))])
    
    for route_idx, route in enumerate(solution):
        color = colors[route_idx]
        route_label = f"Route {route_idx + 1}"
        
        # Plot the depot (customer 0)
        depot = route[0]
        plt.plot(depot.x, depot.y, 'ks', markersize=10, label="Depot" if route_idx == 0 else "")
        
        # Plot the route lines
        for i in range(len(route) - 1):
            cust1 = route[i]
            cust2 = route[i+1]
            
            plt.plot([cust1.x, cust2.x], [cust1.y, cust2.y], color=color, 
                     linestyle='-', marker='o', label=route_label if i == 0 else "")
            
            # Plot customer nodes (only if not depot)
            if cust1.id != depot.id:
                plt.text(cust1.x, cust1.y + 0.5, str(cust1.id), fontsize=9)
        
        # Add the last customer's text (if not depot)
        last_cust = route[-2]
        if last_cust.id != depot.id:
             plt.text(last_cust.x, last_cust.y + 0.5, str(last_cust.id), fontsize=9)
            
    plt.title(f"Final Solution: {instance_name}")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid(True)
    
    # --- CHANGED LINES ---
    
    # Create an output filename based on the instance name
    # e.g., "E-n23-k3.vrp" becomes "E-n23-k3_solution.png"
    base_name = os.path.splitext(os.path.basename(instance_name))[0]
    save_path = os.path.join(os.path.dirname(__file__), 'static', f"{base_name}_solution.png")
    
    # Save the figure to a file
    plt.savefig(save_path)
    
    # Close the plot to free up memory
    plt.close()
    
    print(f"Plot saved successfully to: {save_path}")