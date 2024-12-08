import sys
sys.path.append('../')
sys.setrecursionlimit(10000) 
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

    # Ensure the move is within the grid boundaries
    if 0 <= new_pos[0] <= grid_width and 0 <= new_pos[1] <= grid_width:
        new_state = copy.deepcopy(state)
        new_state.agent_pos = new_pos
        return new_state  # Return the new state after the move
    return None  # If the move is out of bounds

# Register the action with GTPyHOP
gtpyhop.declare_actions(move)
evaluated_moves = 0

# Step 5: Define the lookahead strategy
def lookahead(state, steps, visited=None):
    """Simulate several steps ahead and return the best sequence of actions."""
    global evaluated_moves  # Access the global counter

    if visited is None:
        visited = set()  # Initialize the visited set only once at the top level

    if steps == 0 or state.agent_pos == state.goal_pos:
        return [], heuristic(state)  # Base case: No more steps or goal reached

    best_score = float('inf')
    best_plan = []
    visited.add(state.agent_pos)  # Mark this state as visited

    # Explore all possible actions
    for action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        new_state = move(state, action)

        if new_state and new_state.agent_pos not in visited:  # Avoid revisiting states
            evaluated_moves += 1  # Increment the counter
            plan, score = lookahead(new_state, steps - 1, visited)  # Pass the same visited set

            # Only update if the new path is better
            if score < best_score:
                best_score = score
                best_plan = [(action,)] + plan  # Accumulate actions

    visited.remove(state.agent_pos)  # Backtrack by removing the state
    return best_plan, best_score



def navigate(state, goal_pos):
    """High-level task to navigate to the goal using lookahead strategy."""

    if state.agent_pos == goal_pos:
        return []  # Goal reached, no further actions

    # Use the lookahead function to determine the best sequence of actions
    plan, _ = lookahead(state, steps=20)  # Look 5 steps ahead for better accuracy

    # Return the entire plan, not just the first action
    if plan:
        return [('move', action) for action, in plan]
    else:
        return []  # No valid plan found

def dynamic_depth(state):
    """Adjust depth based on the Manhattan distance to the goal."""
    return heuristic(state)  # Use the distance to dynamically limit depth



# Register the task with GTPyHOP
gtpyhop.declare_task_methods('navigate', navigate)

# Step 7: Call the planner with the initial state and task
# plan = gtpyhop.find_plan(state1, [('navigate', state1.goal_pos)])
plan, _ = lookahead(state1, steps=dynamic_depth(state1))

# Step 8: Calculate the number of steps
num_steps = len(plan)  # Number of steps in the generated plan

# Print the plan and the number of steps
print("Generated Plan:", plan)
print("Number of Steps:", num_steps)
print("Total Evaluated Moves:", evaluated_moves)