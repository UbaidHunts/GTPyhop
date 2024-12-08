# Pyperplan with Lookahead Strategies and Manhattan Distance Heuristic

This project extends the functionality of the official GTPyHOP repository by implementing several lookahead strategies and integrating the Manhattan Distance heuristic for use in planning tasks.

## Project Directory Structure
- **Lookahead Strategies:** Implemented in `/lookahead`.

In this directory, the following lookahead strategies have been implemented:
- **A-star:** `astar.py`
- **Run-Lazy Lookahead (RLL):** `rll.py`
- **Run-Lookahead (RL):** `rl.py`
- **Depth-First Iterative Deepening (DFID):** `dfid.py`
- **Monte Carlo Tree Search (MCTS):** `mcts.py`

I also implemented the `Manhattan Distance Heuristic` which can be find in each lookahead strategy code. 


## Run

If you have GTPyHOP installed on you machine, to run the project for DFID copy the `dfid.py` file from `/lookahead` and paste it in `GTPyHOP/Examples`. After doing simply fun the file using:
```bash
python3 dfid.py
```

## Experiments 
The results of experiments can be find in `/results` directory.

