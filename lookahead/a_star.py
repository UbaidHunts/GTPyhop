import sys
sys.path.append('../')
import gtpyhop
import copy  # For deep copying states
import heapq  # Priority queue for A* search

# Step 1: Create a domain
gtpyhop.Domain('gridworld')

# Step 2: Define the initial state
grid_width = 5
grid_height = 5
state1 = gtpyhop.State('state1')
state1.agent_pos = (0, 0)  # Agent starts at (0, 0)
state1.goal_pos = (4, 4)   # Goal is at (4, 4)

# Global counter to track the number of evaluated moves
evaluated_moves_astar = 0

# Step 3: Define the heuristic function (Manhattan Distance)
def heuristic(pos):
    """Estimate the Manhattan distance to the goal."""
    x1, y1 = pos
    x2, y2 = state1.goal_pos
    return abs(x1 - x2) + abs(y1 - y2)

# Step 4: Define the 'move' function
def move(pos, direction):
    """Update the agent's position based on the direction."""
    x, y = pos
    if direction == 'UP':
        new_pos = (x, y + 1)
    elif direction == 'DOWN':
        new_pos = (x, y - 1)
    elif direction == 'LEFT':
        new_pos = (x - 1, y)
    elif direction == 'RIGHT':
        new_pos = (x + 1, y)
    else:
        return None  # Invalid move

    # Ensure the move is within grid boundaries
    if 0 <= new_pos[0] <= grid_width and 0 <= new_pos[1] <= grid_width:
        return new_pos  # Valid move
    return None  # Out of bounds move

# Step 5: Implement A* Search
def a_star_search(start_pos, goal_pos):
    """A* search algorithm using a priority queue."""
    global evaluated_moves_astar  # Access the global counter

    # Priority queue: (priority, path_cost, unique_id, current_pos, plan)
    frontier = []
    counter = 0  # Unique identifier for tiebreaking
    heapq.heappush(frontier, (heuristic(start_pos), 0, counter, start_pos, []))

    visited = set()  # Track visited positions

    while frontier:
        _, path_cost, _, current_pos, plan = heapq.heappop(frontier)

        # If we reach the goal, return the plan
        if current_pos == goal_pos:
            return plan

        # Mark this position as visited
        visited.add(current_pos)

        # Explore all possible actions
        for action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            new_pos = move(current_pos, action)

            if new_pos and new_pos not in visited:  # Only explore unvisited states
                evaluated_moves_astar += 1  # Increment the counter
                new_cost = path_cost + 1  # Increment the path cost (g(n))
                priority = new_cost + heuristic(new_pos)  # f(n) = g(n) + h(n)
                counter += 1  # Ensure unique entries in the priority queue

                # Add the new state to the priority queue
                heapq.heappush(
                    frontier, (priority, new_cost, counter, new_pos, plan + [(action,)])
                )

    return []  # Return an empty plan if no path found

# Step 6: Call the A* planner with the initial state
plan_astar = a_star_search(state1.agent_pos, state1.goal_pos)

# Step 7: Calculate the number of steps in the plan
num_steps_astar = len(plan_astar)

# Print the plan, number of steps, and total evaluated moves
print("Generated Plan (A*):", plan_astar)
print("Number of Steps (A*):", num_steps_astar)
print("Total Evaluated Moves (A*):", evaluated_moves_astar)
