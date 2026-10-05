# Flying Fish

A 2D arcade mini-game built with Python and Pygame where players catch falling fish using a bucket.

## Overview

In Flying Fish, your objective is to catch as many falling fish as possible in your bucket while keeping track of your score and elapsed time. The game features retro-style visuals and sound effects.

This game was inspired by the indie game "The Walking Fish 2".

Please note that this application is completely harmless and safe to run. It does not perform any malicious activities, make unauthorized system changes, or damage your computer in any way. It is purely a lightweight, entertaining arcade game.

## Requirements

- Python 3.8 or higher
- Pygame

## Installation

1. Clone the repository:
```bash
git clone https://github.com/theStxve/flyingFish.git
cd flyingFish
```

2. (Optional) Set up a virtual environment:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

Start the game by executing:
```bash
python main.py
```

## Controls

- Any key / Left click: Start the game
- Left Arrow: Move bucket left
- Right Arrow: Move bucket right
- Ctrl + Q: Exit game

## Building from Source

To package the game as a standalone Windows executable:

```bash
pip install pyinstaller
build.bat
```
