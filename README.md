# PyWeek 35

The theme for [this PyWeek](https://pyweek.org/35/) is `In The Shadows`.

# Instructions

```sh
git clone https://github.com/guidopetri/the-shady-wood
cd the-shady-wood
pip install -r requirements.txt  # or replace with your virtual env stuff
python3 src/run_game.py
```

Install the dependencies with `pip install`, then run `run_game.py` from any location!

## How to play

### Menus

Press any key to advance.

### Game

Use the arrow keys to move.

Use items with the C, F and S keys.

# Game description

To be filled.

# Lessons

Elaborate descriptions to be added.

- state as a class with property setters
- property setters to maintain consistency
- single-surface, multiple-objects blitting on it is great
- tuples for action/item combinations of spritesheets
- use placeholder images that get replaced as assets get ready
- use utils file with mixin classes, e.g. for loading spritesheet
- maybe keep track of first frame of each effect for calculating things
- separate music vs sfx folder
- music is not scary

# Build instructions

Make sure `pyinstaller` is installed:

```sh
pip install pyinstaller
```

Create the spec file:

```sh
pyi-makespec --windowed --onefile --add-data "./assets;assets" --name shady_wood src/run_game.py
```

Use a `;` for a path separator on Windows, or `:` on \*nix.

Build:

```sh
pyinstaller --clean shady_wood.spec
```

The executable will be located in `./dist/shady_wood.exe` (or no extension for \*nix).

# Credits / Attribution

Programming: Guido Petri

Art: Kendra Lemon

Sound effects: Kendra Lemon

Font: [Dogica Pixel](https://www.dafont.com/dogica.font) by Roberto Mocci.
