# NullPointer - The OG Game - Dark Cyberpunk 3D RPG

**A 3D Dark Cyberpunk RPG coded in Python + Ursina Engine**
*Optimized for Linux (tested on Intel i3 / HD 520, 4GB RAM)*

---

## 📖 Game Overview

You play as **Alex**, a developer pulled into a digital server realm known as **The Codebase**. The system is collapsing under corruption from **The NullPointer King** and his horde of **Syntax Glitches** and **Memory Leaks**. To escape and restore the server, you must explore 3D sectors, solve terminal puzzles, upgrade abilities, and defeat the core bugs.

The game features:
- Dark cyberpunk aesthetic with neon glow accents
- First-person exploration with smooth 3D movement
- Interactive dialogue and terminal puzzles
- Developer-themed abilities (`sudo kill -9`, `git stash`, `refactor()`, `ping`)
- Save system at `git commit` checkpoints
- Low-poly stylized geometry for performance on integrated graphics

---

## ⬇️ How to Download & Run (Linux)

### Method 1: One-Click Script (Recommended)

1. **Clone the repository** (or download the ZIP):
   ```bash
   git clone https://github.com/your-username/The-Codebase-Legacy-of-the-Root.git
   cd The-Codebase-Legacy-of-the-Root
   ```

2. **Make the launch script executable**:
   ```bash
   chmod +x run.sh
   ```

3. **Run the game**:
   ```bash
   ./run.sh
   ```

### Method 2: Manual Installation

1. **Ensure Python 3.14+ is installed**:
   ```bash
   python3 --version
   # Should output something like: Python 3.14.x
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # This installs Ursina Engine and required packages
   ```

4. **Start the game**:
   ```bash
   python3 main.py
   ```

---

## 🎮 How to Play

| Control | Action |
|---------|--------|
| **WASD** | Move forward/backward / left/right |
| **Space** | Jump |
| **Left Click** | Debug Staff attack (destroy nearby entities) |
| **1-5** | Select abilities: `sudo kill -9`, `git stash`, `ping`, `refactor()`, `git commit` (save) |
| **F** | Interact with terminals / NPCs / save points |
| **Esc** | Pause / exit game |
| **Mouse** | Look around / aim |

### Game Objective (Early Build)
- Navigate the 3D cybernetic world
- Avoid / defeat **Syntax Glitch** enemies (neon cyan / purple cubes)
- Touch **`git commit`** save points to persist progress
- Use abilities strategically: `git stash` grants brief invulnerability, `refactor()` restores health (RAM)
- Reach the **Root Citadel** to face the final boss

### Tips for Smooth Performance (Intel HD 520)
- The game is capped at **60 FPS** to prevent CPU/GPU overload
- Graphics are **low-poly stylized** — close background apps to free RAM
- If lag occurs, reduce window size or run in windowed mode
- Audio and particle effects are minimal to conserve resources

---

## 🛠️ Technical Details

- **Engine**: [Ursina Engine](https:// ursinaengine.org/) (built on Panda3D)
- **Language**: Python 3.14+
- **Graphics Style**: Dark cyberpunk, neon glow, low-poly models, atmospheric fog
- **Performance Target**: 60 FPS on Intel HD 520 / 4GB RAM
- **Save Format**: JSON checkpoints at `git commit` nodes
- **License**: MIT (free for personal & public use)

---

## 📂 Project Structure

```
NullPointer/
├── main.py              # Entry point & game loop
├── run.sh               # One-click Linux launch script
├── requirements.txt     # Python dependencies (Ursina)
├── README.md            # This file
├── .venv/               # Auto-generated virtual environment
└── assets/              # (Future: models, sounds, levels)
```

---

## 🛡️ Contributing & Feedback

This is an open-source project! If you'd like to:
- Report bugs or suggest features
- Add new abilities, levels, or NPCs
- Optimize graphics or performance
- Translate the README

Please fork the repo, create a branch, and submit a pull request. For issues, use the **Issues** tab on GitHub.

---

## ⚠️ Known Issues (Early Build)

- Fullscreen mode may not work on all Intel integrated graphics configurations — use windowed mode (`python3 main.py` starts windowed).
- Save/load system is functional but limited to the current session; persistent saves will be added in later updates.
- Enemy AI is basic — later versions will include pathfinding and varied behaviors.

---

**Enjoy the game, and may your code compile on the first try!**

---
*Built with ❤️ by Theogabhishek — 3 cups of coffee + AI assistance · GitHub: [https://github.com/Theogabhishek/NullPointer] (https://github.com/Theogabhishek/Null-Pointer)*
