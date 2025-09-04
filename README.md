# Minesweeper AI

An **AI-powered Minesweeper agent** capable of playing the classic game autonomously.  
This was a group project developed as part of **CS-171 at UC Irvine**, with the goal of exploring **search algorithms, inference systems, and probabilistic reasoning** in uncertain environments.  

---

## Features
- **Multiple Agents**  
  - `MyAI` → Smart agent using constraint satisfaction + probability-based reasoning  
  - `RandomAI` → Baseline random-move agent  
  - `ManualAI` → User plays manually for debugging and testing  
- **Autonomous Play**  
  - Detects safe tiles using logic-based inference  
  - Applies **subset-neighbor analysis** and **probabilistic mine estimation** when no deterministic moves are available  
- **Scalability**  
  - Handles beginner (8×8), intermediate (16×16), and expert (16×30) boards  
- **Performance**  
  - Successfully solved **973 / 1000 boards** (16×16)  
  - Average solve time: ~83s per board  
  - Ranked **Top 3** in a class-wide AI competition  

---

## Project Structure
- **`Action.py`** — Defines the `Action` object and encapsulates moves (uncover, flag, unflag, leave).  
- **`AI.py`** — Abstract base class for all agents; defines the interface.  
- **`ManualAI.py`** — Lets the user play Minesweeper interactively.  
- **`RandomAI.py`** — Simple baseline agent that chooses moves randomly.  
- **`MyAI.py`** — The main intelligent agent, implementing logic-based and probabilistic strategies.  
- **`World.py`** — Game environment that simulates Minesweeper boards and enforces rules.  
- **`Main.py`** — CLI entry point for running agents against different worlds.  

---

## Installation & Usage

### Prerequisites
- Python 3.8+  
- No external libraries required (standard library only)

### Running the Game
```bash
# Run with default MyAI
python3 Main.py

# Run with ManualAI (you play)
python3 Main.py -m

# Run with RandomAI
python3 Main.py -r

# Run on specific world file
python3 Main.py -f worlds/example.world

# Run on folder of worlds and save results
python3 Main.py -f worlds/ output.txt
