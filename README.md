# Unstoppable Cancer #

A rewrite of a fidget spinner Scratch game using Pygame

----------------------------------------------------

# Warning #

**THIS GAME USES RAPIDLY FLASHING IMAGES!**

If this is something you are sensitive to, you can disable it by setting `FLASHING_BACKGROUND=False` in constants.py

I take no responsibility for any damage this game may cause.

# Credit #

* Scratch/Python Code: Joshua Barrass
* Concept & Sprites: Louie Woods

## Libraries ##

* pygame
* numpy
* PIL/Pillow
* colorsys

# Playing #

First install the requirements:
```pip install -r requirements.txt```

Then launch the game:
```./pycancer.py```

## Controls ##

Mash S to spin. Press Enter/Return to reset.

## Music ##

The game can be played with music, which will automatically be played when you reach a speed above 90. Simply put a .ogg file in the assets/music folder.

We recommend Max Coveri's "Running in the 90s"!

# Background #

This game was originally created by Louie and me in
[Scratch](https://scratch.mit.edu/), during the height of the fidget
spinner's popularity. Originally known as Fidget Spinner Simulator, we
later changed the name to "cancer" (or, in contexts where a
politically correct name was required, "bungus") to reflect how bad it
was. As prefects overseeing computer rooms, we introduced our game to
the masses. It was surprisingly popular, sparking competition, and our
game was upgraded over the course of a year.

Since leaving school, I got thinking about our game again. It was
surprisingly _fun_. Whilst Scratch is still around, I thought it might
be nice to port our game to a "real" language. This project is
designed to be as close as I can get to the original project using
Pygame.
