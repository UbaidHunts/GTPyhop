import sys
sys.path.append('../')
import gtpyhop
import copy  # Use Python's copy module to deep copy the state

# Step 1: Create a domain
gtpyhop.Domain('gridworld')

# Step 2: Define the initial state
grid_width = 5
grid_height = 5
state1 = gtpyhop.State('state1')
state1.agent_pos = (0, 0)  # Agent starts at (0, 0)
state1.goal_pos = (4, 4)   # Goal is at (4, 4)

# Step 3: Define a heuristic function (Manhattan Distance)
def heuristic(state):
    """Estimate the Manhattan distance to the goal."""
    x1, y1 = state.agent_pos
    x2, y2 = state.goal_pos
    return abs(x1 - x2) + abs(y1 - y2)

# Step 4: Define the action 'move'
def move(state, direction):
    """Update the agent's position based on the direction."""
    x, y = state.agent_pos
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
        new_state = copy.deepcopy(state)
        new_state.agent_pos = new_pos
        return new_state  # Return the new state after the move
    return None  # If the move is out of bounds

# Register the action with GTPyHOP
gtpyhop.declare_actions(move)

# Global counter to track the number of evaluated moves
evaluated_moves_lazy = 0

# Step 5: Define the Run Lazy Lookahead strategy
def lazy_lookahead(state):
    """Evaluate the next best move based on one-step lookahead."""
    global evaluated_moves_lazy  # Access the global counter
    best_score = float('inf')
    best_action = None

    # Explore all possible actions (one-step lookahead)
    for action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        new_state = move(state, action)
        if new_state:  # If the move is valid
            evaluated_moves_lazy += 1  # Increment the counter
            score = heuristic(new_state)  # Evaluate the state using heuristic

            # Keep the best action based on the heuristic score
            if score < best_score:
                best_score = score
                best_action = action

    return best_action  # Return the best action found

# Step 6: Define the 'lazy_navigate' task
def lazy_navigate(state, goal_pos):
    """Incrementally plan and execute one step at a time."""
    if state.agent_pos == goal_pos:
        return []  # Goal reached

    # Use one-step lookahead to decide the next action
    best_action = lazy_lookahead(state)

    if best_action:
        # Update the state with the selected move
        new_state = move(state, best_action)
        if new_state:  # If the move was valid, continue planning
            return [('move', best_action)] + lazy_navigate(new_state, goal_pos)
    return []  # No valid move found

# Register the task with GTPyHOP
gtpyhop.declare_task_methods('lazy_navigate', lazy_navigate)

# Step 7: Call the lazy lookahead planner with the initial state and task
plan_lazy = gtpyhop.find_plan(state1, [('lazy_navigate', state1.goal_pos)])

# Step 8: Calculate the number of steps in the plan
num_steps_lazy = len(plan_lazy)  # Number of steps in the generated plan

# Print the plan, number of steps, and total evaluated moves
print("Generated Plan (Lazy):", plan_lazy)
print("Number of Steps (Lazy):", num_steps_lazy)
print("Total Evaluated Moves (Lazy):", evaluated_moves_lazy)
