#!/usr/bin/env python3

import sys
from demongeon import *

# PRE: Due to use of f strings, this only works on Python 3.6 or later.
try:
    assert sys.version_info >= (3, 6)
except:
    print("ERROR: You are not running Python 3.6 or later.")
    sys.exit(1)

# You're in a 10x10 grid.  Room (0,0).
# There are n death balls that move randomly.
# If you enter a room with a death ball you die.
# You see a strong glow adjacent.  Faint 2 rooms away.
# Yellow glow for treasure.

#==============================================================================
# Main
#==============================================================================

init_world(10, 3)
# print(world)

print("Welcome to Demongeon!")
print("Try to find the treasure and escape without being killed.")

while True:
    location = get_hero_location()
    describe_room(location)
    action = input(f"{location}> ")
    action = action.strip()
    if action == "":
        print("You wait for a while.")
    elif action == "help":
        help() # Looks like we're overriding a builtin.
    elif action in "nN":
        go_north()
    elif action in "eE":
        go_east()
    elif action in "sS":
        go_south()
    elif action in "wW":
        go_west()
    elif "treasure" in action:
        take_treasure()
    elif action == "cheat":
        print(world)
    elif action == "exit" or action == "quit":
        break
    else:
        print(f"I don't know how to '{action}'.")
    update_world()




