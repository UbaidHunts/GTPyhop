import sys
sys.path.append('../')
import gtpyhop
import copy  # For deep copying states

# Step 1: Create a domain
gtpyhop.Domain('gridworld')

# Step 2: Define the initial state
grid_width = 5
grid_height = 5
state1 = gtpyhop.State('state1')
state1.agent_pos = (0, 0)  # Agent starts at (0, 0)
state1.goal_pos = (4, 4)   # Goal is at (4, 4)

# Global counter to track the number of evaluated moves
evaluated_moves_dfid = 0

# Step 3: Define the 'move' function
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
    return None  # Out of bounds

# Step 4: Implement Depth-Limited Search (DFS)
def depth_limited_search(current_pos, goal_pos, depth):
    """Performs depth-limited DFS without pruning."""
    global evaluated_moves_dfid

    if current_pos == goal_pos:
        return []  # Goal reached

    if depth == 0:
        return None  # Depth limit reached

    evaluated_moves_dfid += 1  # Increment the counter for each evaluated state

    # Explore all possible actions
    for action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        new_pos = move(current_pos, action)

        if new_pos:  # Only explore valid moves
            result = depth_limited_search(new_pos, goal_pos, depth - 1)

            if result is not None:  # If a valid path is found, return it
                return [action] + result

    return None  # No valid path found within this depth

# Step 5: Implement DFID Search
def dfid_search(start_pos, goal_pos, max_depth=20):
    """Performs DFID by incrementing the depth limit."""
    for depth in range(1, max_depth + 1):
        # Perform depth-limited DFS for the current depth
        path = depth_limited_search(start_pos, goal_pos, depth)

        if path is not None:  # If a valid path is found, return it
            return path

    return []  # No valid path found

# Step 6: Call the DFID search with the initial state
plan_dfid = dfid_search(state1.agent_pos, state1.goal_pos)

# Step 7: Calculate the number of steps in the plan
num_steps_dfid = len(plan_dfid)

# Print the plan, number of steps, and total evaluated moves
print("Generated Plan (DFID):", plan_dfid)
print("Number of Steps (DFID):", num_steps_dfid)
print("Total Evaluated Moves (DFID):", evaluated_moves_dfid)
