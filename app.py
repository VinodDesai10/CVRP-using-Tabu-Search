from flask_cors import CORS
import contextlib
import os
import io
from flask import Flask, request, jsonify, send_from_directory

# Import your existing solver functions
from data_loader import load_cvrp_instance
from initial_solution import create_initial_solution
from local_search import local_search_by_swapping
from tabu_search import simple_tabu_search
from utils import calculate_solution_cost, calculate_route_demand
from visualizer import plot_solution

# --- Configuration ---
# Make 'static' folder in this 'backend' directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Tell Flask where to serve images from
app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app) # Allow browser to access this server

# --- Main Solver Route ---
@app.route('/solve', methods=['POST'])
def solve_cvrp():
    try:
        # --- 1. Get Data from Frontend ---
        data = request.json
        file_content = data.get('fileContent')
        file_name = data.get('fileName', 'instance.vrp')
        
        # Get parameters
        iterations = int(data.get('iterations', 200))
        tenure = int(data.get('tenure', 10))

        if not file_content:
            return jsonify({"error": "No file content provided."}), 400

        # --- 2. Save Temp File to Feed to Your functions ---
        # Your data_loader expects a filepath, so we give it one.
        temp_filepath = os.path.join(os.path.dirname(__file__), file_name)
        with open(temp_filepath, 'w') as f:
            f.write(file_content)

        # --- 3. Run Your Solver ---
        # We capture all 'print()' statements to send to the frontend log
        log_stream = io.StringIO()
        with contextlib.redirect_stdout(log_stream):
            
            print(f"Loading instance from {file_name}...")
            depot, customers, m, Q, dist_matrix = load_cvrp_instance(temp_filepath)
            print(f"Loaded {len(customers)} customers, {m} vehicles, capacity {Q}.")

            print("\nCreating initial solution...")
            initial_solution = create_initial_solution(depot, customers, m, Q)
            initial_cost = calculate_solution_cost(initial_solution, dist_matrix)
            print(f"Initial Cost: {initial_cost:.2f}")

            print("\nApplying Local Search (Swap)...")
            ls_solution = local_search_by_swapping(initial_solution, Q, dist_matrix)
            ls_cost = calculate_solution_cost(ls_solution, dist_matrix)
            print(f"Local Search Cost: {ls_cost:.2f}")

            print("\nApplying Tabu Search (Relocation)...")
            ts_solution = simple_tabu_search(ls_solution, Q, dist_matrix, 
                                             iterations, tenure)
            ts_cost = calculate_solution_cost(ts_solution, dist_matrix)
            print("Tabu Search Complete.")

            print("\n--- COST SUMMARY ---")
            print(f"Initial Cost:     {initial_cost:.2f}")
            print(f"Local Search Cost: {ls_cost:.2f}")
            print(f"Tabu Search Cost:  {ts_cost:.2f}")
            print(f"\nTotal Improvement: {initial_cost - ts_cost:.2f}")
            
            # --- 4. Generate Plot ---
            # This will save the image to the 'backend/static' folder
            print("\nGenerating plot...")
            plot_solution(ts_solution, instance_name=file_name)

        # Get the captured log text
        log_output = log_stream.getvalue()
        
        # --- 5. Clean up temp file and prepare response ---
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
            
        # Create the URL for the image
        base_name = os.path.splitext(file_name)[0]
        image_name = f"{base_name}_solution.png"
        # The URL will be like: http://127.0.0.1:5000/static/E-n23-k3_solution.png
        image_url = f"/static/{image_name}"

        return jsonify({
            "log": log_output,
            "image_url": image_url
        })

    except Exception as e:
        # Send any Python errors back to the browser
        return jsonify({"error": str(e)}), 500

# This lets you serve the images (e.g., /static/solution.png)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# --- Run the Server ---
if __name__ == "__main__":
    print("Starting Flask server at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)