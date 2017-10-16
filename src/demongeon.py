# This module defines various parts of the game Death Ball.

from random import randint
from sys import exit
from textwrap import dedent

class Situation(object):
    """A situation the hero can be in.  Usually this is just being at a location."""
    def __init__(self):
        self.contents = [] # The things present in this situation.
        self.world = None # The world this situation belongs to.

    def add(self, entity):
        """Adds an entity to this situation."""
        # An entity can only belong to one situation at a time.
        if entity.situation:
            entity.situation.remove(entity)
        self.contents.append(entity)
        # An entity knows what situation it belongs to.
        # More tightly coupled.  Might be a better way to do this.
        entity.situation = self

    def remove(self, entity):
        """Removes given entity from this situation."""
        ## print(self.contents)
        self.contents.remove(entity)

    def contains(self, entity):
        """Checks if given entity is part of this situation."""
        if entity in self.contents: return True
        return False

    def containsType(self, entityType):
        """Checks if the situation contains some type of entity."""
        for entity in self.contents:
            if isinstance(entity, entityType): return True
        return False

    # TO DO: Really this should be the hero describing things from his point of view.
    # For example, if the hero can see invisibility, the world renders differently.
    def describe(self):
        """Describes the hero's current situation."""
        print("You are in an abstract situation.")


# Inheritance here is questionable.  Maybe a situation shoud have an optional location.
class Location(Situation):
    """A situation where the hero is in a particular location."""
    def __init__(self):
        super(Location, self).__init__()
        # Each location has a 3D coordinate.
        # x == 0 is westmost; y == 0 is northmost; z == 0 is upmost.
        self.coordinate = (-1, -1, -1)

class Room(Location):
    """A generic dungeon room."""
    def __init__(self):
        super(Room, self).__init__()

    def describe(self):
        """Describes this dungeon room situation."""
        print(f"You are in dungeon room {self.coordinate}.")
        self.describe_deathballs()
        self.describe_treasure()

    def get_hero(self):
        """Returns hero if one is in this room."""
        for entity in self.contents:
            if isinstance(entity, Hero):
                return entity
                break
        return None

    # TO DO: Factor into hero class.
    def describe_treasure(self):
        """Describes the treasure relative to hero's current situation."""
        hero = self.get_hero()
        x, y, z = self.coordinate
        rooms = self.world.situations
        treasure = self.world.treasure

        if self.contains(treasure):
            print("The forbidden treasure is here.")
        else:
            adjectives = ["", "bright", "faint"]
            for d in [1, 2]:
                adjective = adjectives[d]
                try:
                    room = rooms[(x - d, y, z)]
                    if room.contains(treasure) and ((x - d) >= 0):
                        print(f"A {adjective} yellow glow emanates from the west.")
                except: pass
                try:
                    room = rooms[(x + d, y, z)]
                    if room.contains(treasure):
                        print(f"A {adjective} yellow glow emanates from the east.")
                except: pass
                try:
                    room = rooms[(x, y - d, z)]
                    if room.contains(treasure) and ((y - d) >= 0):
                        print(f"A {adjective} yellow glow emanates from the north.")
                except: pass
                try:
                    room = rooms[(x, y + d, z)]
                    if room.contains(treasure):
                        print(f"A {adjective} yellow glow emanates from the south.")
                except: pass
                try:
                    room = rooms[(x, y, z - d)]
                    if room.contains(treasure) and ((z - d) >= 0):
                        print(f"A {adjective} yellow glow emanates from above.")
                except: pass
                try:
                    room = rooms[(x, y, z + d)]
                    if room.contains(treasure):
                        print(f"A {adjective} yellow glow emanates from below.")
                except: pass

    # TO DO: Extend entity percepts to z-axis.
    # TO DO: Factor into hero class.
    def describe_deathballs(self):
        """Describes each death ball relative to current hero location."""
        hero = self.get_hero()
        x, y, z = self.coordinate
        rooms = self.world.situations
        treasure = self.world.treasure

        if self.containsType(DeathBall.__class__):
            print("A deadly death ball is here to kill you!")
        else:
            adjectives = ["", "strong", "pale"]
            for d in [1, 2]:
                adjective = adjectives[d]
                try:
                    room = rooms[(x - d, y, z)]
                    if room.containsType(DeathBall.__class__) and ((x - d) >= 0):
                        print(f"A {adjective} blue glow emanates from the west.")
                except: pass
                try:
                    room = rooms[(x + d, y, z)]
                    if room.containsType(DeathBall.__class__):
                        print(f"A {adjective} blue glow emanates from the east.")
                except: pass
                try:
                    room = rooms[(x, y - d, z)]
                    if room.containsType(DeathBall.__class__) and ((y - d) >= 0):
                        print(f"A {adjective} blue glow emanates from the north.")
                except: pass
                try:
                    room = rooms[(x, y + d, z)]
                    if room.containsType(DeathBall.__class__):
                        print(f"A {adjective} blue glow emanates from the south.")
                except: pass


class World(object):
    """The game world consists of all the situations the hero can find himself in."""
    def __init__(self):
        """Initialize the game world."""
        # Mostly the situations are dungeon rooms forming an NxNxN cube.
        self.situations = {}
        self.size = 10
        self.initial_death_balls = 3 # TO DO: Generalize this more.
        self.treasure = None
        self.hero = None

        # Populate the world with dungeon rooms.
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    coordinate = (x, y, z)
                    room = Room()
                    room.coordinate = coordinate
                    self.situations[coordinate] = room
                    room.world = self

        # Start the hero at (0, 0, 0)
        c = (0, 0, 0)
        starting_situation = self.situations[c]
        self.hero = Hero()
        starting_situation.add(self.hero)
        self._init_enemies()
        self._init_items()

    def _init_enemies(self):
        """Populates the game world with enemies."""
        # We start with some number of death balls in random rooms.
        for i in range(self.initial_death_balls):
            while True:
                x = randint(0, self.size - 1)
                y = randint(0, self.size - 1)
                z = randint(0, self.size - 1)
                c = (x, y, z)
                print(f"x = {x}; y = {y}; z = {z}")
                # Don't start with a death ball in the starting room.
                situation = self.situations[c]
                if situation.contains(self.hero):
                    continue
                else:
                    deathball = DeathBall()
                    situation.add(deathball)
                    break

    def _init_items(self):
        """Populates the game world with items."""
        # PRE: Hero has been created and placed in game world.
        # Now place the treasure.
        while True:
            x = randint(0, self.size - 1)
            y = randint(0, self.size - 1)
            z = randint(0, self.size - 1)
            c = (x, y, z)
            print(f"Placing treasure at ({x},{y},{z}).")
            # Don't start with the treasure in the starting room.
            situation = self.situations[c]
            if situation.contains(self.hero):
                continue
            else:
                self.treasure = Treasure()
                situation.add(self.treasure)
                break

    def update(self):
        """Updates the game world after hero acts in response to current situation."""
        loc = self.hero.situation.coordinate
        situation = self.situations[loc]
        if situation.containsType(DeathBall.__class__):
            print("A blazing blue death ball hurls itself toward you, killing you on impact.")
            print("YOU LOSE!")
            exit(0)
        else:
            pass

        self.move_deathballs()

        # Make sure items know when they have been moved.
        for item in self.hero.inventory:
            item.situation = hero.situation

        if loc == (0, 0, 0) and (self.treasure in self.hero.inventory):
            print("You escaped with the treasure.")
            print("YOU WIN!")
            exit(0)

    # TO DO: Just iterate thru list of entities rather than all rooms/situations.
    def move_deathballs(self):
        """Moves each death ball."""
        size = self.size
        rooms = self.situations
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    room = rooms[(x, y, z)]
                    for entity in room.contents:
                        if isinstance(entity, Enemy):
                            entity.act()

    def start(self):
        """Starts the game world in action."""
        while True:
            hero = self.hero
            situation = self.hero.situation
            situation.describe()
            action = input(f"{situation.coordinate}> ")
            action = action.strip()
            if action == "":
                print("You wait for a while.")
            elif action == "help":
                help() # Looks like we're overriding a builtin.
            elif action in "nN":
                hero.go_north()
            elif action in "eE":
                hero.go_east()
            elif action in "sS":
                hero.go_south()
            elif action in "wW":
                hero.go_west()
            elif action in "uU":
                hero.go_up()
            elif action in "dD":
                hero.go_down()
            elif "treasure" in action:
                hero.take(self.treasure)
            elif action == "cheat":
                for e in Entity.entities:
                    e.debug()
            elif action == "exit" or action == "quit":
                break
            else:
                print(f"I don't know how to '{action}'.")
            self.update()


class Entity(object):
    """Something that has physical manifestation in the game."""
    entities = []

    def __init__(self):
        print("Creating Entity.")
        self.weight = 0 # In pounds.
        self.situation = None
        self.acted = False # Has this entity taken its action this turn?
        Entity.entities.append(self)

    def get_world(self):
        return self.situation.world

    def get_location(self):
        """Returns the location of the entity in the game world as an (x, y, z) tuple."""
        if isinstance(self.situation, Location):
            return self.situation.coordinate
        else:
            return (-1, -1, -1)

    def debug(self):
        print(f"I am a {self.__class__.__name__} at {self.situation.coordinate}.")


class Item(Entity):
    """An inanimate item."""
    def __init__(self):
        super(Item, self).__init__()

class Treasure(Item):
    """The forbidden treasure."""
    def __init__(self):
        super(Treasure, self).__init__()
        self.weight = 25
        self.color = "golden"
        self.name = "treasure"

class Lifeform(Entity):
    """A living entity in the game."""
    def __init__(self):
        super(Lifeform, self).__init__()
        print("Creating Lifeform.")
        self.strength = 1

    def carrying_capacity(self):
        """Reports the carrying capacity of this lifeform."""
        return self.strength * 20

    def weight_carried(self):
        """Tells how much weight this lifeform is carrying."""
        carried = 0
        for item in self.inventory:
            carried += item.weight
        return carried

class Enemy(Lifeform):
    def __init__(self):
        super(Enemy, self).__init__()

    """A lifeform that is trying to kill or otherwise thwart our hero."""

class DeathBall(Enemy):
    """A slow, randomly-moving, glowing ball of death."""
    def __init__(self):
        super(DeathBall, self).__init__()
        self.weight = 0
        self.color = "blue"

    def act(self):
        """Causes a death ball to act."""
        if not self.acted:
            self.move()
            self.acted = True

    def move(self):
        """Causes a death ball to move."""
        room = self.situation
        world = self.get_world()
        size = world.size
        rooms = world.situations

        # If the hero is at our location, kill him.
        if room.contains(world.hero):
            print("A blazing blue death ball hurls itself toward you, killing you on impact.")
            print("YOU LOSE!")
            exit(0)

        # Randomly move the death ball.
        loc = self.get_location()
        x, y, z = loc
        ## print(f"Moving death ball from ({x}, {y}, {z})", end=' ')
        direction = randint(0, 3) # TO DO: Add z axis.
        if direction == 0: # N
            if (y >= 1):
                rooms[(x, y - 1, z)].add(self)
        elif direction == 1: # E
            if (x < (size - 1)):
                rooms[(x + 1, y, z)].add(self)
        elif direction == 2: # S
            if (y < (size - 1)):
                rooms[(x, y + 1, z)].add(self)
        elif direction == 3: # W
            if (x >= 1):
                rooms[(x - 1, y, z)].add(self)
        else:
            print(f"ERROR: Unexpected direction: {direction}.")

        ## print(f"to ({x}, {y}, {z}).")


class Hero(Lifeform):
    """The protagonist of this story."""
    def __init__(self):
        super(Hero, self).__init__()
        print("Creating Hero.")
        self.inventory = []

    def get_world(self):
        """Returns the world this hero is part of."""
        return self.situation.world

    def go_north(self):
        """ Moves the hero one room north if possible. """
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        y -= 1
        if (y >= 0):
            world.situations[(x, y, z)].add(self)
        else:
            print("I can't go any farther north.")

    def go_east(self):
        """ Moves the hero one room east if possible. """
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        x += 1
        if (x < world.size):
            world.situations[(x, y, z)].add(self)
        else:
            print("I can't go any farther east.")

    def go_south(self):
        """Moves the hero one room south if possible."""
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        y += 1
        if (y < world.size):
            world.situations[(x, y, z)].add(self)
        else:
            print("I can't go any farther south.")

    def go_west(self):
        """Moves the hero one room west if possible."""
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        x -= 1
        if (x >= 0):
            world.situations[(x, y, z)].add(self)
        else:
            print("I can't go any farther west.")

    def go_down(self):
        """Moves the hero one room down if possible."""
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        z += 1
        if (z < world.size):
            world.situations[(x, y, z)].add(self)
        else:
            print("I can't go any farther down.")

    def go_up(self):
        """Moves the hero one room up if possible."""
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        z -= 1
        if (z >= 0):
            world.situations[(x, y, z)].add(self)
        else:
            print("I can't go any farther up.")


    def take(self, item):
        """Attempts to take an item for the hero."""
        s = self.situation
        if s.contains(item):
            print(f"You take the {item.name}.")
            s.remove(item)
            self.inventory.append(item)
        else:
            print(f"The {item.name} is not here.")

# end class Hero


def help():
    """Prints out the help message."""
    msg = """
    Your goal is to get the treasure and leave the dungeon without dying.
    The treasure is put in a random location in the dungeon at the start of each game.
    When you find the treasure, type 'take treasure' to take it.
    Once you have the treasure, make your way back to location (0, 0, 0).
    If you do that without dying, you win the game!

    Other commands:
    help - print this help message
    exit - exit the game
    cheat - show useful game world state info
    n - go north
    e - go east
    s - go south
    w - go west
    d - go down
    u - go up
    <Enter> - wait a turn
    """
    msg = dedent(msg).strip()

    print(msg)



