import sys
sys.path.append('../')
import gtpyhop
import random
import copy  # For deep copying states
from collections import defaultdict

# Step 1: Create a domain
gtpyhop.Domain('gridworld')

# Step 2: Define the Grid Dimensions
grid_width = 5
grid_height = 5

# Step 3: Define the initial state
state1 = gtpyhop.State('state1')
state1.agent_pos = (0, 0)  # Agent starts at (0, 0)
state1.goal_pos = (4, 4)   # Goal is at (4, 4)

# Global counter to track the number of evaluated moves
evaluated_moves_mcts = 0

# MCTS Parameters
num_simulations = 50  # Number of simulations per move
exploration_constant = 1.41  # Exploration-exploitation tradeoff
rollout_depth_limit = 100  # Limit the depth of rollouts

# Step 4: Define the 'move' function
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
    if 0 <= new_pos[0] < grid_width and 0 <= new_pos[1] < grid_height:
        new_state = copy.deepcopy(state)
        new_state.agent_pos = new_pos
        return new_state  # Return the new state after the move
    return None  # Out of bounds move

# Step 5: MCTS Node to store statistics
class MCTSNode:
    def __init__(self):
        self.visits = 0  # How many times this state has been visited
        self.wins = 0  # How many times this state led to the goal

# Step 6: MCTS Rollout (Simulation) with Depth Limit
def rollout(state):
    """Simulate a random path from the current state until the goal or depth limit."""
    global evaluated_moves_mcts

    depth = 0  # Track the depth of the rollout

    while state.agent_pos != state1.goal_pos and depth < rollout_depth_limit:
        evaluated_moves_mcts += 1  # Increment the counter
        action = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        new_state = move(state, action)

        if new_state:  # If the move is valid, update the state
            state = new_state
        depth += 1  # Increment the depth

    # If the goal was reached, return success (1), otherwise failure (0)
    return 1 if state.agent_pos == state1.goal_pos else 0

# Step 7: MCTS Selection and Expansion
def select_and_expand(state, node_stats):
    """Select the most promising node to explore further."""
    best_action = None
    best_score = -float('inf')

    for action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        new_state = move(state, action)
        if not new_state:
            continue

        stats = node_stats[action]
        score = (stats.wins / (stats.visits + 1)) + exploration_constant * (
            (2 * evaluated_moves_mcts) ** 0.5 / (stats.visits + 1)
        )

        if score > best_score:
            best_score = score
            best_action = action

    if best_action:
        return best_action, move(state, best_action)

    return None, None  # No valid moves available

# Step 8: MCTS Search
def mcts(state, max_iterations=100):
    """Perform MCTS search from the given state."""
    node_stats = defaultdict(MCTSNode)

    for _ in range(max_iterations):
        simulated_state = copy.deepcopy(state)
        action, new_state = select_and_expand(simulated_state, node_stats)

        if not new_state:
            continue

        # Perform a rollout from the new state
        result = rollout(new_state)

        # Update statistics
        node_stats[action].visits += 1
        node_stats[action].wins += result

    # Choose the action with the most visits
    best_action = max(node_stats.items(), key=lambda x: x[1].visits)[0]
    return best_action

# Step 9: Generate a Plan using MCTS
def generate_mcts_plan(state):
    """Generate a complete plan using MCTS lookahead."""
    plan = []

    while state.agent_pos != state1.goal_pos:
        action = mcts(state)
        new_state = move(state, action)

        if not new_state:  # If no valid move, break
            break

        plan.append((action,))
        state = new_state

    return plan

# Step 10: Run the MCTS Lookahead Strategy
plan_mcts = generate_mcts_plan(state1)

# Calculate the number of steps in the plan
num_steps_mcts = len(plan_mcts)

# Print the plan, number of steps, and total evaluated moves
print("Generated Plan (MCTS):", plan_mcts)
print("Number of Steps (MCTS):", num_steps_mcts)
print("Total Evaluated Moves (MCTS):", evaluated_moves_mcts)
