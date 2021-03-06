#!/usr/bin/env python3

import sys
from demongeon import *

# PRE: Due to use of f strings, this only works on Python 3.6 or later.
try:
    assert sys.version_info >= (3, 6)
except:
    print("ERROR: You are not running Python 3.6 or later.")
    sys.exit(1)

# Play the game.
major, minor, patch = version
while True:
    print(f"Welcome to Demongeon v{major}.{minor}.{patch}!")
    print("Try to find the treasure and escape without being killed.")
    world = World()
    should_restart = world.start()
    if not should_restart: break



