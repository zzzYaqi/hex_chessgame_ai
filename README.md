# Hex AI

A Python implementation of the board game Hex with socket-based agents and an AI player built with Monte Carlo Tree Search (MCTS) and Rapid Action Value Estimation (RAVE).

This project was developed as an AI game-playing project. It includes the game runner, protocol handling, reference agents, test agents, and a custom `CapAgent` that searches for moves under a time limit.

## Highlights

- Implements a playable Hex engine with board, move, colour, protocol, and game state modules.
- Supports external agents through a socket protocol.
- Includes baseline agents for testing invalid moves, timeouts, disconnects, and naive play.
- Implements an MCTS agent and an enhanced RAVE-MCTS agent.
- Includes swap-rule logic and opening-move handling for competitive Hex play.

## Project Structure

```text
.
├── Hex.py                    # Convenience script for launching matches
├── src/                      # Core Hex engine and protocol code
├── agents/
│   ├── DefaultAgents/        # Baseline and error-case agents
│   ├── GroupAgent/           # Custom MCTS/RAVE-MCTS agent
│   └── TestAgents/           # Additional compiled/sample agents
├── test.py                   # Batch match script for local evaluation
└── PlayableHex.md            # Links to playable Hex apps
```

## Requirements

- Python 3.10+ recommended
- No third-party Python dependencies are required for the core project

## Run a Match

From the repository root:

```bash
python Hex.py "a=Naive;python agents/DefaultAgents/NaiveAgent.py" "a=Cap;python agents/GroupAgent/CapAgent.py" -v
```

On Windows, backslashes also work:

```bat
python Hex.py "a=Naive;python agents\DefaultAgents\NaiveAgent.py" "a=Cap;python agents\GroupAgent\CapAgent.py" -v
```

Useful flags:

- `-v` / `-verbose`: print match progress
- `-p` / `-print_protocol`: print protocol messages
- `b=n` / `board_size=n`: run on an `n x n` board
- `-s` / `-switch`: switch agent colours
- `-l` / `-log`: save match logs under `src/logs`

## AI Approach

The custom agent keeps an internal game state, updates it from protocol messages, and chooses moves using search:

- `agents/GroupAgent/MCTS.py`: baseline Monte Carlo Tree Search with UCT selection.
- `agents/GroupAgent/RaveMCTS.py`: RAVE-enhanced MCTS that blends rollout move statistics with UCT values.
- `agents/GroupAgent/State.py`: agent-side game state wrapper used during simulations.
- `agents/GroupAgent/CapAgent.py`: socket agent that connects to the game engine and sends selected moves.

The search runs with a per-move time limit and uses random rollouts to estimate winning lines.

## Notes

Some sample agents are included as compiled binaries or JAR files because they are part of the original testing set. The main project logic and custom AI agent are written in Python.
