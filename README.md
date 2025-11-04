Hybrid Tabu Search Algorithm for the Capacitated Vehicle Routing Problem (CVRP)
This project is a Python implementation of the hybrid algorithm described in the paper: "Implementation of a Hybrid Tabu Search Algorithm with Local Search for Solving the Capacitated Vehicle Routing Problem"  by Hernández-Aguilar et al. (2025).

The algorithm is designed to solve the CVRP, a well-known combinatorial optimization problem. The primary objective is to find the optimal set of routes for a fleet of vehicles to serve a set of customers with known demands, minimizing the total travel distance while respecting the capacity of each vehicle.



Methodology
This implementation follows the three-stage methodology proposed in the paper :


Stage 1: Initial Solution

A feasible initial solution is generated using a Randomized Algorithm.


Customers are randomly assigned to routes, ensuring that the total demand on any route does not exceed the vehicle's capacity.

This is implemented in initial_solution.py.

Stage 2: Local Search (Swap)

The initial solution is then improved using the Swap Local Search Algorithm.

This algorithm iteratively swaps pairs of customers (both within the same route and between different routes) if the swap reduces the total cost and remains feasible .

This is implemented in local_search.py.

Stage 3: Tabu Search (Relocation)

The solution from Stage 2 is fed into a Simple Tabu Search (TS) algorithm for final optimization.

The TS algorithm explores a "relocation neighborhood" by moving individual customers to different routes.

It uses a "tabu list" (a short-term memory) to avoid reverting to previous solutions and to escape local optima.

An Aspiration Criterion is used to override the tabu list if a move leads to a new best-known solution.


This is implemented in tabu_search.py.

Project Structure
.
├── cvrp_solver.py       # Main execution file
├── data_loader.py       # Parses CVRPLIB .vrp files
├── initial_solution.py  # Implements Stage 1
├── local_search.py      # Implements Stage 2
├── tabu_search.py       # Implements Stage 3
├── visualizer.py        # Plots the final solution and saves it
├── utils.py             # Customer class and helper functions (distance, cost)
├── P-n19-k2.vrp         # Sample data file
├── E-n23-k3.vrp         # Sample data file
└── README.md            # This file


Getting Started
Prerequisites

Python 3.x (The paper used 3.9 )

matplotlib library for visualization

Installation

Clone or download this repository.

Install the only dependency, matplotlib:

Bash
pip3 install matplotlib
Download CVRPLIB instance files (e.g., E-n23-k3.vrp, A-n32-k5.vrp) and place them in the project's root directory.

The algorithm from the paper was tested on instances from CVRPLIB.

How to Run

Open the main file, cvrp_solver.py, in a text editor.

Change the filepath variable to the instance file you want to solve:

Python
# Set the problem file to run
filepath = 'E-n23-k3.vrp'
You can also tune the Tabu Search parameters in cvrp_solver.py:

Python
NUM_ITERATIONS = 1000
TABU_TENURE = 15
Run the solver from your terminal:

Bash
python3 cvrp_solver.py

Output
The script will produce two forms of output:

Console Output:

Shows the progress of loading the instance and the cost improvement at each stage of the algorithm.

Loading instance from E-n23-k3.vrp...
Loaded 22 customers, 3 vehicles, capacity 4500.

Creating initial solution...
Total Cost (Initial): 1278.09

Applying Local Search (Swap)...
Total Cost (Local Search): 702.51

Applying Tabu Search (Relocation)...
Starting Tabu Search. Initial Cost: 702.51
  Iter 0: New Best Cost = 658.88
  Iter 1: New Best Cost = 630.97
  Iter 2: New Best Cost = 622.17
Tabu Search Complete. Final Best Cost: 622.17

--- COST SUMMARY ---
Initial Cost:     1278.09
Local Search Cost: 702.51
Tabu Search Cost:  622.17
Saved Plot Image:

A .png image visualizing the final, optimized routes will be saved to the project directory (e.g., E-n23-k3_solution.png).



Citation
This project is a direct implementation of the work described in the following paper:

Hernández-Aguilar, J. A., Pacheco-Valencia, V., Cruz-Rosales, M. H., Ponce-Gallegos, J. C., & Condado-Huerta, C. (2025). Implementation of a Hybrid Tabu Search Algorithm with Local Search for Solving the Capacitated Vehicle Routing Problem. International Journal of Combinatorial Optimization Problems and Informatics, 16(3), 82-91.
