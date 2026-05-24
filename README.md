# Hex AI

A tournament-grade AI for the board game **Hex**, built with **Monte
Carlo Tree Search (MCTS)** and the **RAVE** (Rapid Action Value
Estimation) enhancement. Plays the standard 11×11 game over a socket
protocol, with full support for the pie ("swap") rule.

---

## Problem

Hex is a two-player connection game on a rhombus of hexagonal cells.
**Red** wins by connecting top↔bottom with an unbroken chain; **Blue**
wins by connecting left↔right. The branching factor at 11×11 is huge
(121 → 120 → 119 …), so brute-force minimax is hopeless. We need a
search that learns *which* parts of the tree are worth expanding from
random rollouts — i.e. MCTS — and we need it to converge faster than
vanilla UCT to stay competitive within a 2-second per-move budget.

## Method

* **UCT-MCTS** baseline (`agents/GroupAgent/MCTS.py`) — the textbook
  selection / expansion / simulation / back-prop loop with the UCB1
  exploration bonus `Q/N + c · sqrt(2 ln(N_parent) / N)`.
* **RAVE-MCTS** main agent (`agents/GroupAgent/RaveMCTS.py`) — adds an
  "all-moves-as-first" side-table that updates *every* move played
  during a rollout, not just the one selected. The final node score
  is a linear blend `α · RAVE + (1 − α) · UCB1` with
  `α = max(0, (rave_const − N) / rave_const)`, so RAVE dominates early
  and UCB1 takes over as visit counts grow.
* **Opening + swap heuristics** on top of search:
  * Red turn 0 → play inside the central band `[0.25 n, 0.75 n]²`
    (strong enough to be worth playing, weak enough not to invite a
    swap).
  * Blue turn 0 → swap iff Red's stone is in that same central band.
* **Hyper-parameters tuned by self-play** (`run_hex.bat` +
  `update_meta.py`). Default landed at `EXPLORATION = 0.3`,
  `RAVE_CONST = 300`.

## Tech stack

Python 3 · only the standard library (`socket`, `math`, `random`,
`time`, `copy`, `subprocess`). No NumPy, no PyTorch — the entire
search runs on pure Python.

## Results

* Beats the bundled `NaiveAgent` reference baseline (`test.py` plays
  100 matches and reports win-rate).
* Plays competitively against the four tournament binaries shipped in
  `agents/TestAgents/` (alice, bob, jimmie, joni, rita) — the same
  fixed search budget across them all.

## Project structure

```
.
├── Hex.py                    # Convenience launcher for a single match
├── src/                      # Course-provided harness: Game, Board,
│                             # Protocol, Move, EndState, Tile, Colour
├── agents/
│   ├── DefaultAgents/        # Reference / baseline agents (Naive,
│   │                         # Timeout, Disconnecting, …)
│   ├── GroupAgent/           # ★ Our work ★
│   │   ├── CapAgent.py       # Tournament agent (uses RaveMCTS)
│   │   ├── RaveMCTS.py       # Main search
│   │   ├── MCTS.py           # Plain UCT baseline
│   │   ├── State.py          # Game-state wrapper for the search
│   │   ├── meta.py           # Tunable hyper-parameters
│   │   └── TestRave.py / TestAgent.py   # A/B variants for tuning
│   └── TestAgents/           # Compiled binaries of other groups'
│                             # tournament submissions
├── test.py                   # 100-match win-rate benchmark
├── update_meta.py            # Hyper-parameter sweep helper
└── run_hex.bat               # Windows sweep driver
```

## Run a match

```bash
# Our agent (Cap) vs the bundled NaiveAgent, verbose:
python Hex.py "a=Cap;python agents/GroupAgent/CapAgent.py" \
              "a=Naive;python agents/DefaultAgents/NaiveAgent.py" -v

# Swap colours:
python Hex.py "a=Cap;python agents/GroupAgent/CapAgent.py" \
              "a=Naive;python agents/DefaultAgents/NaiveAgent.py" -v -s
```

Useful flags:

| Flag | Meaning |
| --- | --- |
| `-v`, `-verbose` | Print the board after every move |
| `-p`, `-print_protocol` | Print the raw protocol messages |
| `-l`, `-log` | Save the match to `src/logs/*.csv` |
| `-s`, `-switch` | Swap the order of the two agents |
| `board_size=n` | Use an `n × n` board instead of 11×11 |

100-match win-rate benchmark against the reference agent:

```bash
python test.py
```

## Notes

* The team folder was renamed from `Group3` to `GroupAgent` before
  publishing this repo, so `test.py`, `run_hex.bat`, and
  `update_meta.py` still reference the old path. Either rename
  `agents/GroupAgent` → `agents/Group3` locally, or update those three
  files before running the scripts.
* `agents/TestAgents/*` were built for Linux/macOS; on Windows you may
  need to launch them through WSL or skip them.
