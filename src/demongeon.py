"""
This module defines various parts of the game Death Ball.

The basic idea of the game is that you have a NxNxN grid of rooms.
The base class of these rooms is a Situation.  The idea is that a
situation the hero is in could be something that's not a physical
location.  Maybe it is death, victory, interaction with a shop keeper,
or something else.  Most of the situations the hero faces are those
of being in a dungeon room.

The other class hierarchy is that based on a physical Entity.  This
is anything that exists in the game physically: the hero, monsters,
inventory items, etc.  Each thing exists in a specific situation.

Both abstractions are a bit questionable to me, but so far they are working
well enough to create the game.
"""

from random import randint
from sys import exit
from textwrap import dedent

version = (0, 0, 2) # Game version.

class Situation(object):
    """A situation the hero can be in.  Usually this is just being at a location."""
    def __init__(self):
        self.contents = []
        """ The `Entity`s in this situation. """
        self.world = None
        """ The `World` this situation is part of."""

    def add(self, entity):
        """Add an `Entity` to this `Sitaution`."""
        # An entity can only belong to one situation at a time.
        if entity.situation:
            entity.situation.remove(entity)
        self.contents.append(entity)
        # An entity knows what situation it belongs to.
        # More tightly coupled.  Might be a better way to do this.
        entity.situation = self

    def remove(self, entity):
        """Remove given `Entity` from this `Situation`."""
        ## print(self.contents)
        self.contents.remove(entity)

    def contains(self, entity):
        """Check if given `Entity` is part of this `Situation`."""
        if entity in self.contents: return True
        return False

    def containsType(self, entityType):
        """Check if the `Situation` contains some exact type of `Entity`."""
        for entity in self.contents:
            ## print(f"{entity.__class__} == {entityType}")
            if entity.__class__ == entityType: return True
        return False

    # TO DO: Really this should be the hero describing things from his point of view.
    # For example, if the hero can see invisibility, the world renders differently.
    def describe(self):
        """Describe the hero's current `Situation`."""
        print("You are in an abstract situation.")

    # This allows us to make the action parser/interpreter context-sensitive.
    def handle_hero_action(self, action):
        """Override default action handling.  Returns True if it does."""
        return False


# Inheritance here is questionable.  Maybe a situation shoud have an optional location.
class Location(Situation):
    """A `Situation` where the `Hero` is in a particular location."""
    def __init__(self):
        """Initialize the `Location` object."""
        super(Location, self).__init__()
        # Each location has a 3D coordinate.
        # x == 0 is westmost; y == 0 is northmost; z == 0 is upmost.
        self.coordinate = (-1, -1, -1)
        self.location_type = "location"

class Room(Location):
    """A generic dungeon room."""
    def __init__(self):
        super(Room, self).__init__()
        self.location_type = "dungeon room"

    def describe(self):
        """Describe this dungeon room situation."""
        print(f"You are in a {self.location_type} at {self.coordinate}.")
        self.describe_deathballs()
        self.describe_treasure()

    def get_hero(self):
        """Return the `Hero` if one is in this room."""
        for entity in self.contents:
            if isinstance(entity, Hero):
                return entity
                break
        return None

    # TO DO: Factor into hero class.
    def describe_treasure(self):
        """Describe the treasure relative to hero's current situation.

        Some entities in the game glow a certain color.  If so, that entity can be
        seen at a distance by the hero.  The range may depend on the hero's level of
        perception at the time.
        """
        hero = self.get_hero()
        x, y, z = self.coordinate
        rooms = self.world.situations
        treasure = self.world.treasure

        if self.contains(treasure):
            print("The forbidden treasure is here.")
        else:
            # TO DO: This is very repetitive.  Can it be factored down?
            # Also, it's essentially the same code as the death ball glow rendering.
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
        """Describe each death ball relative to current hero location."""
        hero = self.get_hero()
        x, y, z = self.coordinate
        rooms = self.world.situations
        treasure = self.world.treasure

        ## print(f"{globals()['DeathBall']}")

        if self.containsType(DeathBall):
            print("A deadly death ball is here to kill you!")
        else:
            adjectives = ["", "strong", "pale"]
            for d in [1, 2]:
                adjective = adjectives[d]
                try:
                    room = rooms[(x - d, y, z)]
                    if room.containsType(DeathBall) and ((x - d) >= 0):
                        print(f"A {adjective} blue glow emanates from the west.")
                except: pass
                try:
                    room = rooms[(x + d, y, z)]
                    if room.containsType(DeathBall):
                        print(f"A {adjective} blue glow emanates from the east.")
                except: pass
                try:
                    room = rooms[(x, y - d, z)]
                    if room.containsType(DeathBall) and ((y - d) >= 0):
                        print(f"A {adjective} blue glow emanates from the north.")
                except: pass
                try:
                    room = rooms[(x, y + d, z)]
                    if room.containsType(DeathBall):
                        print(f"A {adjective} blue glow emanates from the south.")
                except: pass

class TeleporterRoom(Room):
    """This is a special teleporter room.  You can teleport to another random location."""
    def __init__(self):
        super(TeleporterRoom, self).__init__()
        self.location_type = "teleporter"

    def describe(self):
        super(TeleporterRoom, self).describe()
        print("This is a teleporter room.  Try teleporting.")

    # TO DO: Extend this handler extension idea to entities as well.
    # For example, if hero has a wand, this opens up more context-specific actions.
    def handle_hero_action(self, action):
        """Interpret hero action in the context of this room.

        In this case, the room gives the hero the special ability to teleport somewhere else
        in the dungeon randomly.
        """
        size = self.world.size
        if action == "teleport":
            print("You magically teleport to another location.")
            loc = (randint(0, size - 1), randint(0, size - 1), randint(0, size - 1))
            self.world.situations[loc].add(self.world.hero)
            return True
        else:
            return False

class TreasureRoom(Room):
    """Special room where the forbidden treasure is initially located."""
    def __init__(self):
        super(TreasureRoom, self).__init__()
        self.location_type = "treasure room"

    # TO DO: Make this more of a template method so everything gets described in the right order.
    # That is, I think there needs to be an ordering to the rendering of a room.  Perhaps it goes
    # general situation description, distant entities, entities in the room, hero invertory,
    # hero wearables, stuff the hero has eaten, feelings of the hero.  Kind of ordering most of it
    # by percept distance.
    def describe(self):
        super(TreasureRoom, self).describe()
        print("The walls, floor, and ceiling of this room all sparkle.")


class World(object):
    """The game world consists of all the situations the hero can find himself in."""
    def __init__(self):
        """Initialize the game world."""
        # Mostly the situations are dungeon rooms forming an NxNxN cube.
        self.situations = {}
        self.size = 10
        self.initial_death_balls = 100 # TO DO: Generalize this more.
        self.treasure = None
        self.hero = None

        # Populate the world with dungeon rooms.
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    room = None
                    coordinate = (x, y, z)
                    if (x == y == z != 0):
                        room = TeleporterRoom()
                    else:
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
        """Populate the game world with enemies."""
        # We start with some number of death balls in random rooms.
        for i in range(self.initial_death_balls):
            while True:
                x = randint(0, self.size - 1)
                y = randint(0, self.size - 1)
                z = randint(0, self.size - 1)
                c = (x, y, z)
                ## print(f"x = {x}; y = {y}; z = {z}")
                # Don't start with a death ball in the starting room.
                situation = self.situations[c]
                if situation.contains(self.hero):
                    continue
                else:
                    deathball = DeathBall()
                    situation.add(deathball)
                    break

    def _init_items(self):
        """Populate the game world with items."""
        # PRE: Hero has been created and placed in game world.
        # Now place the treasure.
        while True:
            x = randint(0, self.size - 1)
            y = randint(0, self.size - 1)
            z = randint(0, self.size - 1)
            c = (x, y, z)
            ## print(f"Placing treasure at ({x},{y},{z}).")
            # Don't start with the treasure in the starting room.
            situation = self.situations[c]
            if situation.contains(self.hero):
                continue
            else:
                # Replace normal dungeon room with special treasure room.
                self.treasure = Treasure()
                self.situations[c] = TreasureRoom()
                situation = self.situations[c]
                situation.add(self.treasure)
                situation.coordinate = c
                situation.world = self
                break

    def update(self):
        """Update the game world after hero acts in response to current situation."""
        loc = self.hero.situation.coordinate
        situation = self.situations[loc]
        # TO DO: Use a Death situation.
        if situation.containsType(DeathBall):
            print("A blazing blue death ball hurls itself toward you, killing you on impact.")
            print("YOU LOSE!")
            exit(0)
        else:
            pass

        self.move_deathballs()

        # Make sure items know when they have been moved.
        for item in self.hero.inventory:
            item.situation = self.hero.situation

        # TO DO: Use a Victory situation.
        if loc == (0, 0, 0) and (self.treasure in self.hero.inventory):
            print("You escaped with the treasure.")
            print("YOU WIN!")
            exit(0)

        # Reset the action flag so entities will be able to do something next turn.
        for entity in Entity.entities:
            entity.acted = False

    # TO DO: Just iterate thru list of entities rather than all rooms/situations.
    def move_deathballs(self):
        """Move each death ball."""
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
        """Start the game world in action."""
        while True:
            hero = self.hero
            situation = self.hero.situation
            print()
            situation.describe()
            action = input(f"{situation.coordinate}> ")
            action = action.strip()

            # TO DO: Model the idea of turns, time, activations more explicitly.
            # This would allow modeling of creatures more like the mechanics of Zombicide
            # where a monster can move a long distance in a single activation or have
            # multiple activations in a single unit of turn time.
            # Would be interesting if you could actually model a Zombicide level in the game
            # engine.
            if situation.handle_hero_action(action):
                pass
            else: # Default action handling.
                if action == "":
                    print("You wait for a while.")
                elif action == "help":
                    help() # Looks like we're overriding a builtin.
                    continue
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
                    continue
                elif action == "exit" or action == "quit":
                    break
                else:
                    print(f"I don't know how to '{action}'.")
            self.update()


class Entity(object):
    """Something that has physical manifestation in the game."""
    entities = []
    """The set of all `Entity` instances ever created."""

    def __init__(self):
        ## print("Creating Entity.")
        self.weight = 0 # In pounds.
        self.situation = None
        self.acted = False # Has this entity taken its action this turn?
        Entity.entities.append(self)

    def get_world(self):
        return self.situation.world

    def get_location(self):
        """Return the location of the entity in the game world as an (x, y, z) tuple."""
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
        ## print("Creating Lifeform.")
        self.strength = 1

    def carrying_capacity(self):
        """Report the carrying capacity of this lifeform."""
        return self.strength * 20

    def weight_carried(self):
        """Tell how much weight this lifeform is carrying."""
        carried = 0
        for item in self.inventory:
            carried += item.weight
        return carried

class Enemy(Lifeform):
    """A lifeform that is trying to kill or otherwise thwart our hero."""
    def __init__(self):
        super(Enemy, self).__init__()


class DeathBall(Enemy):
    """A slow, randomly-moving, glowing ball of death."""
    def __init__(self):
        super(DeathBall, self).__init__()
        self.weight = 0
        self.color = "blue"

    def act(self):
        """Cause a death ball to act."""
        if not self.acted:
            self.move()
            self.acted = True

    def move(self):
        """Cause a death ball to move.

        Death balls are not very smart.  They just move one step in a random direction
        each turn.
        """
        room = self.situation
        world = self.get_world()
        size = world.size
        rooms = world.situations

        # If the hero is at our location, kill him.
        # TO DO: Create Death situation.
        if room.contains(world.hero):
            print("A blazing blue death ball hurls itself toward you, killing you on impact.")
            print("YOU LOSE!")
            exit(0)

        # Randomly move the death ball.
        loc = self.get_location()
        x, y, z = loc
        ## print(f"Moving death ball from ({x}, {y}, {z})", end=' ')
        direction = randint(0, 5)
        if direction == 0: # N
            if (y >= 1):
                y -= 1
                rooms[(x, y, z)].add(self)
        elif direction == 1: # E
            if (x < (size - 1)):
                x += 1
                rooms[(x, y, z)].add(self)
        elif direction == 2: # S
            if (y < (size - 1)):
                y += 1
                rooms[(x, y, z)].add(self)
        elif direction == 3: # W
            if (x >= 1):
                x -= 1
                rooms[(x, y, z)].add(self)
        elif direction == 4: # D
            if (z < (size - 1)):
                z += 1
                rooms[(x, y, z)].add(self)
        elif direction == 5: # U
            if (z >= 1):
                z -= 1
                rooms[(x, y, z)].add(self)
        else:
            print(f"ERROR: Unexpected direction: {direction}.")

        ## print(f"to ({x}, {y}, {z}).")


class Hero(Lifeform):
    """The protagonist of this story."""
    def __init__(self):
        super(Hero, self).__init__()
        ## print("Creating Hero.")
        self.inventory = []

    def get_world(self):
        """Return the world this hero is part of."""
        return self.situation.world

    def go_north(self):
        """ Move the hero one room north if possible. """
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        y -= 1
        if (y >= 0):
            world.situations[(x, y, z)].add(self)
        else:
            print("I can't go any farther north.")

    def go_east(self):
        """ Move the hero one room east if possible. """
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        x += 1
        if (x < world.size):
            world.situations[(x, y, z)].add(self)
        else:
            print("I can't go any farther east.")

    def go_south(self):
        """Move the hero one room south if possible."""
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        y += 1
        if (y < world.size):
            world.situations[(x, y, z)].add(self)
        else:
            # TO DO: Game time should not pass for illegal move attempts.
            print("I can't go any farther south.")

    def go_west(self):
        """Move the hero one room west if possible."""
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        x -= 1
        if (x >= 0):
            world.situations[(x, y, z)].add(self)
        else:
            print("I can't go any farther west.")

    def go_down(self):
        """Move the hero one room down if possible."""
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        z += 1
        if (z < world.size):
            world.situations[(x, y, z)].add(self)
        else:
            print("I can't go any farther down.")

    def go_up(self):
        """Move the hero one room up if possible."""
        loc = self.get_location()
        world = self.get_world()
        x, y, z = loc
        z -= 1
        if (z >= 0):
            world.situations[(x, y, z)].add(self)
        else:
            print("I can't go any farther up.")


    def take(self, item):
        """Attempt to take an item for the hero."""
        s = self.situation
        if s.contains(item):
            print(f"You take the {item.name}.")
            s.remove(item)
            self.inventory.append(item)
        else:
            # TO DO: Game time should not pass for illegal actions.
            print(f"The {item.name} is not here.")

# end class Hero


def help():
    """Print out the help message."""
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



