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

Anne was going for a picnic at her usual favorite spot, but when she
arrived, she accidentally angered a fairy! The angry fairy cast a spell on
her and transported her to the middle of the cursed forest known as the Shady
Wood.

Help Anne find her way out of the Shady Wood. If she becomes too scared,
she'll be turned to stone and be lost forever!

Some helpful items can be found around the forest, but be sure to use them
carefully... people say the forest changes every time you enter it!

# Lessons

## state as a class with property setters

Keeping track of state is hard. In this game, we used a config module that
contained a lot of different state-related defaults, and managed state by
changing the values in a variable that was passed around. This was incredibly
inconvenient: making sure that the game state was consistent had to be done
in several different parts of the code, and it was easy to create bugs by
forgetting to keep a consistent game state.

One alternative idea is to use a class or an object with property setters/
getters to manage state. This way, consistent state can be kept by ensuring
the class implements correctness, and the object can be called forth in any
module without having to worry about bugs creeping up if something is
forgotten.

## property setters to maintain consistency

Hand-in-hand with the above point, maintaining consistency is hard. Some
variables can only have certain values, and using an enum is too much for
how simple that variable is; and sometimes, variables are parts of objects
and it's difficult to use an enum. Property setters can ensure consistency
and enforce rules for setting variables.

## single-surface, multiple-objects blitting on it is great

Previously, we had tried using multiple surfaces and blitting different
things on them to then switch which surface was being displayed. This is
probably a pretty natural idea to start with, but a much better idea is to
use a single surface that is being displayed, and to blit things on it
depending on what's required. By blitting things in the correct order, we can
ensure that the image looks as it should to the player.

## tuples for action/item combinations of spritesheets

Spritesheets can come in many different flavors, and keeping track of all the
spritesheets as individual variables is annoying. One potential improvement
is to use tuples or dictionaries instead to select the correct spritesheet
as required. One even better idea is to use a spreadsheet class that can
keep track of its own fps and looping, and exposes a stable API that makes
interacting with a spritesheet much easier than keeping track of which frame
you're on!

## use placeholder images that get replaced as assets get ready

This one should have been obvious, but as the artist takes time to create
art, it's useful to use placeholder images instead so that the coder doesn't
have to wait for the artist before implementing anything image-related.

## use utils file with mixin classes, e.g. for loading spritesheets

Mixin classes can implement specific methods on "child" classes that can
help with reducing code duplication. For example, loading a spritesheet is
pretty standard; we don't really need to have that code everywhere in each
object, we can just use a mixin instead.

## maybe keep track of first frame of each effect for calculating things

Calculating how long an effect is, or side effects of an action, means
that it's easy to calculate things as an offset of the first instance
instead of just having a counter that counts down.

## separate music vs sfx folder

Also in the obvious territory, but having separate folders for music vs sound
effects is very useful so that you don't have to keep track of what kind of
file a file is!

## music is not scary

Pygame makes it super easy to add music, and it's really not that bad, even
though I was totally anxious about it.

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

Music and sound effects: Kendra Lemon

Font: [Dogica Pixel](https://www.dafont.com/dogica.font) by Roberto Mocci.
