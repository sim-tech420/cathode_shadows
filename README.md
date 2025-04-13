# Cathode Shadows

*Cathode Shadows* is an interactive text-based adventure game set in a gritty 1983 world, inspired by retro CRT aesthetics. Players make choices that shape the story, manage stats (*Psyche*, *Suspicion*, *Skill*), and experience a nostalgic terminal-like interface with glitch effects, scanlines, and typewriter sounds. Built with Python and Pygame, the game offers a modular structure for easy expansion.

## Features

- **Dynamic Story**: JSON-driven narrative with branching choices that affect the story and stats.
- **Retro CRT Effects**: Scanlines, screen curvature, random glitches, and static bursts for an authentic 1980s terminal feel.
- **Typewriter Effect**: Text appears character-by-character with sound effects (`type.wav`).
- **Stats System**: Tracks *Psyche* (mental stability), *Suspicion* (how much attention you draw), and *Skill* (your competence), influencing story events.
- **Input Options**: Choose actions via typing commands or selecting menu options (1–3 keys or mouse clicks).
- **Error Handling**: Invalid commands display helpful feedback (e.g., "Command not recognized. Try: sleep ('Go to sleep'), plan ('Plan next steps')").

## Getting Started

### Prerequisites

- **Python**: Version 3.6 or higher (tested with 3.13.2).
- **Pygame**: Install via pip:
  ```bash
  pip install pygame

- Ensure the sounds/ and fonts/ directories contain:
  - sounds/type.wav (typewriter sound).
  - fonts/vcr_osd_mono.ttf (retro font).

### Installation

- Clone the repository:
  - git clone https://github.com/sim-tech420/cathode_shadows.git
  - cd cathode_shadows

- Install dependencies:
  - See above

- Run the game:
  python3 main.py

### File Structure

cathode_shadows/
├── main.py               # Entry point and main game loop
├── game.py               # Game state, stats, and command processing
├── story.py              # JSON story loading and scene management
├── ui.py                 # Rendering, input handling, and CRT effects
├── story.json            # Story scenes, choices, and stat changes
├── sounds/
│   └── type.wav          # Typewriter sound effect
├── fonts/
│   └── vcr_osd_mono.ttf  # Retro font
└── README.md             # Project documentation

### Gameplay

- Objective: Navigate a noir-inspired story set in 1983, making choices
  that shape your path as a lawyer entangled in a mystery.

- Controls:
  - Type commands (e.g., "burn", "go to sleep") or a number ("1", "2", "3")
    to select a menu option, then press Enter.
  - Select menu options by pressing the 1, 2, or 3 keys directly (e.g., "1" for "Burn").
  - Click a menu option to select it (e.g., click "1. Burn").
  - Press Escape or close the window to exit.

- Stats:
  - Psyche: Your mental stability (0–100). Low Psyche triggers glitches and story variations.
  - Suspicion: How much attention you draw (0–100). High Suspicion adds tension.
  - Skill: Your competence (0–100). Affects your ability to handle challenges.

- Effects:
  - CRT scanlines and curvature for a retro monitor look.
  - Random glitches (increased at low Psyche).
  - Static burst when Psyche drops significantly.
