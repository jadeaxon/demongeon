# This module defines various parts of the game Death Ball.

from random import randint
from sys import exit
from textwrap import dedent

world = [] # The game world.  An NxN grid of rooms.
size = 10 # Size in rooms of one side of the world grid.
death_balls = 3 # Number of death balls in the world.
inventory = [] # Hero's inventory.

# Populates the initial game world model.
def init_world(size, death_balls):
    for x in range(size):
        row = [] 
        for y in range(size):
            row.append([])
        world.append(row)
    world[0][0].append("hero")

    # We start with some number of death balls in random rooms.
    for i in range(death_balls):
        while True:
            x = randint(0, size - 1)
            y = randint(0, size - 1)
            # print(f"x = {x}; y = {y}") 
            # Don't start with a death ball in the starting room.
            room = world[x][y]
            # print(room)
            if "hero" in room: 
                continue
            else:
                world[x][y].append("death ball")
                break

    # Now place the treasure.
    while True:
        x = randint(0, size - 1)
        y = randint(0, size - 1)
        # print(f"x = {x}; y = {y}") 
        # Don't start with a death ball in the starting room.
        room = world[x][y]
        # print(room)
        if "hero" in room: 
            continue
        else:
            world[x][y].append("treasure")
            break

# Returns the location of the hero in the dungeon as an (x, y) tuple.
def get_hero_location():
    for x in range(size):
        for y in range(size):
            room = world[x][y]
            if "hero" in room:
                return (x, y)
    # Should throw some kind of exception.
    return (-1, -1)


# Moves the hero one room north if possible.
def go_north():
    loc = get_hero_location()
    x = loc[0]
    y = loc[1]
    y -= 1
    if (y >= 0):
        world[x][y + 1].remove("hero")
        world[x][y].append("hero")
    else:
        print("I can't go any farther north.")

# Moves the hero one room east if possible.
def go_east():
    loc = get_hero_location()
    x = loc[0]
    y = loc[1]
    x += 1
    if (x < size):
        world[x - 1][y].remove("hero")
        world[x][y].append("hero")
    else:
        print("I can't go any farther east.")

# Moves the hero one room south if possible.
def go_south():
    loc = get_hero_location()
    x = loc[0]
    y = loc[1]
    y += 1
    if (y < size):
        world[x][y - 1].remove("hero")
        world[x][y].append("hero")
    else:
        print("I can't go any farther south.")

# Moves the hero one room west if possible.
def go_west():
    loc = get_hero_location()
    x = loc[0]
    y = loc[1]
    x -= 1
    if (x >= 0):
        world[x + 1][y].remove("hero")
        world[x][y].append("hero")
    else:
        print("I can't go any farther west.")

# Describes room at given location.  Assumes the hero is in that room.
def describe_room(location):
    print(f"You are in room {location}.")
    describe_deathballs() 
    describe_treasure()

# Takes the treasure.
def take_treasure():
    loc = get_hero_location()
    x, y = loc
    room = world[x][y]
    if "treasure" in room:
        print("You take the treasure.")
        world[x][y].remove("treasure")
        inventory.append("treasure")
    else:
        print("The treasure is not here.")

# Describes the treasure relative to current hero location.
def describe_treasure():
    loc = get_hero_location()
    x, y = loc
    room = world[x][y]
    if "treasure" in room:
        print("The forbidden treasure is here.")
    else:
        adjectives = ["", "bright", "faint"]
        for d in [1, 2]:
            adjective = adjectives[d]
            try:
                room = world[x - d][y]
                if "treasure" in room and ((x - d) >= 0):
                    print(f"A {adjective} yellow glow emanates from the west.")
            except: pass
            try:
                room = world[x + d][y]
                if "treasure" in room:
                    print(f"A {adjective} yellow glow emanates from the east.")
            except: pass
            try:
                room = world[x][y - d]
                if "treasure" in room and ((y - d) >= 0):
                    print(f"A {adjective} yellow glow emanates from the north.")
            except: pass
            try:
                room = world[x][y + d]
                if "treasure" in room:
                    print(f"A {adjective} yellow glow emanates from the south.")
            except: pass


# Describes each death ball relative to current hero location.
def describe_deathballs():
    loc = get_hero_location()
    x, y = loc
    room = world[x][y]
    if "death ball" in room:
        print("A deadly death ball is here to kill you!")
    else:
        adjectives = ["", "strong", "pale"]
        for d in [1, 2]:
            adjective = adjectives[d]
            try:
                room = world[x - d][y]
                if "death ball" in room and ((x - d) >= 0):
                    print(f"A {adjective} blue glow emanates from the west.")
            except: pass
            try:
                room = world[x + d][y]
                if "death ball" in room:
                    print(f"A {adjective} blue glow emanates from the east.")
            except: pass
            try:
                room = world[x][y - d]
                if "death ball" in room and ((y - d) >= 0):
                    print(f"A {adjective} blue glow emanates from the north.")
            except: pass
            try:
                room = world[x][y + d]
                if "death ball" in room:
                    print(f"A {adjective} blue glow emanates from the south.")
            except: pass


# Updates the game world.
def update_world():
    loc = get_hero_location()
    x, y = loc
    room = world[x][y]
    if "death ball" in room:
        print("A blazing blue death ball hurls itself toward you, killing you on impact.")
        print("YOU LOSE!")
        exit(0)
    else:
        pass

    move_deathballs()
    if (x == 0) and (y == 0) and ("treasure" in inventory):
        print("You escaped with the treasure.")
        print("YOU WIN!")
        exit(0)

# Moves each death ball.
def move_deathballs():
    for x in range(size):
        for y in range(size):
            room = world[x][y]
            if "death ball" in room:
                move_deathball(x, y)

    for x in range(size):
        for y in range(size):
            room = world[x][y]
            if "death ball (moved)" in room:
                world[x][y].remove("death ball (moved)")
                world[x][y].append("death ball")


# Moves a particular death ball.
def move_deathball(x, y):
    room = world[x][y]
    if "hero" in room:
        print("A blazing blue death ball hurls itself toward you, killing you on impact.")
        print("YOU LOSE!")
        exit(0)

    ## print(f"Moving death ball from ({x}, {y})", end=' ')
    direction = randint(0, 3)
    if direction == 0: # N
        if (y >= 1):
            world[x][y].remove("death ball")
            y -= 1
            world[x][y].append("death ball (moved)")
    elif direction == 1: # E
        if (x < (size - 1)):
            world[x][y].remove("death ball")
            x += 1
            world[x][y].append("death ball (moved)")
    elif direction == 2: # S
        if (y < (size - 1)):
            world[x][y].remove("death ball")
            y += 1
            world[x][y].append("death ball (moved)")
    elif direction == 3: # W
        if (x >= 1):
            world[x][y].remove("death ball")
            x -= 1
            world[x][y].append("death ball (moved)")
    else:
        print(f"ERROR: Unexpected direction: {direction}.")

    ## print(f"to ({x}, {y}).")


def help():
    """Prints out the help message."""
    msg = """
    Your goal is to get the treasure and leave the dungeon without dying.
    The treasure is put in a random location in the dungeon at the start of each game. 
    When you find the treasure, type 'take treasure' to take it.
    Once you have the treasure, make your way back to location (0, 0).
    If you do that without dying, you win the game!

    Other commands:
    help - print this help message
    exit - exit the game
    cheat - show the game world state
    n - go north
    e - go east
    s - go south
    w - go west
    <Enter> - wait a turn
    """
    msg = dedent(msg).strip()

    print(msg)



