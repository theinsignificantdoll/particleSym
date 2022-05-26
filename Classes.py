from math import sqrt, asin, sin, cos, atan

FORCE_MULTIPLIER = 1
SPEED_LIMIT = 1
MAX_MOVE_PER_TICK = 1
DRAG = 0.01
CHARGE_STRENGTH = 0


def set_max_move_per_tick(x):
    global MAX_MOVE_PER_TICK
    MAX_MOVE_PER_TICK = x


def set_force_multiplier(x):
    global FORCE_MULTIPLIER
    FORCE_MULTIPLIER = x


def set_speed_limit(x):
    global SPEED_LIMIT
    SPEED_LIMIT = x


class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def asunit(self):
        try:
            angle = atan(abs(self.x) / abs(self.y))
        except ZeroDivisionError:
            return Vector(0, 0)

        return Vector(sin(angle) * (1 if self.x > 0 else -1), cos(angle) * (1 if self.y > 0 else -1))

    def get_length(self):
        return sqrt(self.x**2 + self.y**2)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y})"


def get_influence_add(obj, other):
    diffx = (obj.position.x - other.position.x)
    diffy = obj.position.y - other.position.y

    diff = sqrt(abs(diffx) ** 2 + abs(diffy) ** 2) / FORCE_MULTIPLIER
    try:
        strength = (1 / 2 ** diff) * (obj.mass + other.mass)
    except OverflowError:
        strength = 0
    try:
        estrength = (1 / 2 ** diff) * (obj.charge + (-1 * other.charge)) * CHARGE_STRENGTH
    except OverflowError:
        estrength = 0

    unit = Vector(diffx*-1, diffy*-1).asunit()

    return unit * strength + unit * estrength


class Neutron:
    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0):
        self.mass = 1839.0
        self.charge = 0.0

        self.position = Position(x, y)
        self.vector = Vector(vx, vy)
        self.t = 0

    def __add__(self, other):
        return get_influence_add(self, other)

    def __repr__(self):
        return f"Neutron(x={self.position.x}, y={self.position.y}, vx={self.vector.x}, vy={self.vector.y})"

    def move(self, movemultiplier):
        self.position.x += self.vector.x * movemultiplier
        self.position.y += self.vector.y * movemultiplier


class Proton:
    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0):
        self.mass = 1836.0
        self.charge = 1.0

        self.position = Position(x, y)
        self.vector = Vector(vx, vy)
        self.t = 1

    def __add__(self, other):
        return get_influence_add(self, other)

    def __repr__(self):
        return f"Proton(x={self.position.x}, y={self.position.y}, vx={self.vector.x}, vy={self.vector.y})"

    def move(self, movemultiplier):
        self.position.x += self.vector.x * movemultiplier
        self.position.y += self.vector.y * movemultiplier


class Electron:
    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0):
        self.mass = 1.0
        self.charge = -1.0

        self.position = Position(x, y)
        self.vector = Vector(vx, vy)
        self.t = 2

    def __add__(self, other):
        return get_influence_add(self, other)

    def __repr__(self):
        return f"Electron(x={self.position.x}, y={self.position.y}, vx={self.vector.x}, vy={self.vector.y})"

    def move(self, movemultiplier):
        self.position.x += self.vector.x * movemultiplier
        self.position.y += self.vector.y * movemultiplier


class Engine:
    def __init__(self):
        self.objects = []

    def dotick(self):
        dct = {}
        movemultiplier = 1
        for obj in self.objects:
            sm = Vector(0, 0)
            for other in self.objects:
                if obj == other:
                    continue
                sm += (obj + other)
            dct[obj] = sm * (1 / obj.mass)

        for n in dct:
            if (n.vector + dct[n]).get_length() > MAX_MOVE_PER_TICK:
                movemultiplier = min(movemultiplier, 1 / (n.vector + dct[n]).get_length())

        for n in dct:
            n.vector += dct[n] * movemultiplier
            n.vector -= n.vector * DRAG
            n.move(movemultiplier)

    def append(self, other):
        self.objects.append(other)

    def clear(self):
        self.objects.clear()

    def __repr__(self):
        return "\n".join([n.__repr__() for n in self.objects])

