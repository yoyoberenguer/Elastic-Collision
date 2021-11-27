# -*- UTF-8 -*-
"""
MIT License

Copyright (c) 2019 Yoann Berenguer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import random

import pygame
from pygame.locals import *

from math import hypot, sqrt
from random import uniform, randint
import time
import threading
from ElasticCollision.ec_game import momentum_trigonometry, momentum_angle_free
from ElasticCollision.c_game import momentum_trigonometry_c, momentum_angle_free_c
from pygame.math import Vector2

# Screen size
SIZE = (1024, 1024)

# Screen bottom right corner
UPPER = (SIZE[0], SIZE[1])
# Screen top left corner
LOWER = (0, 0)

FRICTION = 1.0  # 0.998

# Maximum Velocity
LIMIT_HIGH = 15
LIMIT_LOW = -15

DECAY_LOCK = threading.Lock()


class Error(BaseException):
    pass


class Decay(threading.Thread):
    """ Class particle decay """

    particles = {}

    def __init__(self, particle):
        threading.Thread.__init__(self)

        # particle instance variable
        self.particle = particle
        Decay.particles[str(particle.id)] = time.time()
        self.ThreadId = id(self)
        self.breakup = False

    def run(self):
        global DECAY_LOCK
        while not self.breakup:
            DECAY_LOCK.acquire()
            for name, age in Decay.particles.items():

                if name == str(self.particle.id):
                    if time.time() - age > 20:
                        Decay.particles.pop(str(self.particle.id))
                        self.particle.remove_from_inventory()
                        self.breakup = False

            # print (self.particle.id, Decay.particles)
            # delay to reduce overhead computer resources
            time.sleep(0.1)
            DECAY_LOCK.release()

        DECAY_LOCK.release()


class Deformation(threading.Thread):
    """ Thread class object deformation """

    # my_list of object(rectangle class) being deformed
    # with x and y axis variations
    DeformationInventory = []

    # Constructor
    def __init__(self, object_):

        threading.Thread.__init__(self)

        self.object = object_

        # object_ deformation along the x axis
        self.data = [0.98, 0.95, 0.92, 0.90, 0.87,
                     0.85, 0.86, 0.88, .85, 0.82, 0.80, 0.77,
                     0.75, 0.73, 0.71, 0.67, 0.65, 0.60, 0.62,
                     0.64, 0.66, 0.68, 0.72, 0.75, 0.78, 0.81,
                     0.84, 0.87, 0.90, 0.92,
                     0.93, 0.95, 0.98, 1.1, 1.2, 1.1,
                     1.0, 0.98, 0.95, 0.92, 0.90, 0.87,
                     0.85, 0.86, 0.88, 0.90, 0.92,
                     0.93, 0.95, 0.98, 1.1, 1.2, 1.1,
                     1.0]
        # object_ deformation along the y axis
        self.data_r = [1.0, 1.1, 1.2, 1.1, 0.98, 0.95,
                       0.93, 0.92, 0.9, 0.88, 0.86, 0.85,
                       0.87, 0.9, 0.92, 0.95, 0.98, 1.0,
                       1.1, 1.2, 1.1, 0.98, 0.95, 0.93,
                       0.92, 0.9, 0.87, 0.84, 0.81, 0.78,
                       0.75, 0.72, 0.68, 0.66, 0.64, 0.62,
                       0.6, 0.65, 0.67, 0.71, 0.73, 0.75,
                       0.77, 0.8, 0.82, 0.85, 0.88, 0.86,
                       0.85, 0.87, 0.9, 0.92, 0.95, 0.98]

        # Thread identification
        self.id = id(self)

    def cancel_deformation(self):
        """Function used to cancel an object deformation """

        i = 0
        for r_ in Deformation.DeformationInventory:
            if r_.name == self.object.name:
                Deformation.DeformationInventory.pop(i)
            else:
                i += 1

    def run(self):

        # Return if a deformation is already active
        if self.object in Deformation.DeformationInventory:
            return
        else:
            Deformation.DeformationInventory.append(self.object)

        j_ = 0
        for r_ in self.data:

            # Check if the ball has not been deleted/exploded after a collision
            if self.object in Engine.objects:
                # Apply deformation to x,y
                self.object.x_deformation = r_
                self.object.y_deformation = self.data_r[j_]

                # Adjust the delay below for the deformation duration.
                # default 0.01
                time.sleep(0.01)
                j_ += 1

            else:
                # Removing object from the active deformation list 'DeformationInventory'
                self.cancel_deformation()
                # The ball has been destroyed.
                # object deformation is stopped.
                break

        # End of transformation, object returns with normal
        # shape (no transformation).
        self.object.x_deformation = 1
        self.object.y_deformation = 1

        self.cancel_deformation()


class Momentum(object):
    """
    CLASS MOMENTUM : ASSIGN A MOMENTUM TO A SINGLE VERTEX/POINT
    """
    # Constructor
    # Default vector components vx, vy =0
    # vx, vy correspond to the x-component, y component of the velocity vector (real numbers)
    def __init__(self, vx : float = 1.0, vy : float = 1.0) -> None:

        self.vx = vx if LIMIT_LOW < vx < LIMIT_HIGH else 0.0
        self.vy = vy if LIMIT_LOW < vx < LIMIT_HIGH else 0.0

    # Decorator for component x
    @property
    def vx(self) -> float:
        return self.__vx

    # component x with a range (-LIMIT_LOW,LIMIT_HIGH)
    @vx.setter
    def vx(self, vx: float) -> None:
        if vx > LIMIT_HIGH:
            self.__vx = LIMIT_HIGH

        elif vx < LIMIT_LOW:
            self.__vx = LIMIT_LOW
        else:
            self.__vx = vx

    # Decorator for component y
    @property
    def vy(self) -> float:
        return self.__vy

    # component y has also a range (-LIMIT_LOW,LIMIT_HIGH)
    @vy.setter
    def vy(self, vy: float) -> None:
        if vy > LIMIT_HIGH:
            self.__vy = LIMIT_HIGH
        elif vy < LIMIT_LOW:
            self.__vy = LIMIT_LOW
        else:
            self.__vy = vy

    def __add__(self, other: object) -> object:
        if isinstance(other, Momentum):
            self.vx += other.vx
            self.vy += other.vy
            return Momentum(self.vx, self.vy)
        else:
            raise TypeError(
                '\nArgument other is not a '
                'momentum type, got %s ' % type(other))

    def __sub__(self, other : object) -> object:
        if isinstance(other, Momentum):
            self.vx -= other.vx
            self.vy -= other.vy
            return Momentum(self.vx, self.vy)
        else:
            raise TypeError(
                '\nArgument other is not a '
                'momentum type, got %s ' % type(other))

    def __mul__(self, other: object) -> object:
        if isinstance(other, Momentum):
            self.vx *= other
            self.vy *= other
            return Momentum(self.vx, self.vy)
        else:
            raise TypeError(
                '\nArgument other is not a '
                'momentum type, got %s ' % type(other))

    @staticmethod
    def inverse(momentum_: object) -> None:
        if hasattr(momentum_, "vx"):
            momentum_.vx *= -1.0
            momentum_.vy *= -1.0
        else:
            raise TypeError(
                '\nArgument momentum_ is not a '
                'momentum type, got %s ' % type(momentum_))

    def __getitem__(self, k: float) -> float:
        if 0 <= k < len(self.__dict__.values()):
            if k == 0:
                return self.vx
            else:
                return self.vy
        else:
            raise IndexError('IndexError: list index out of range')

    def __setitem__(self, k : int, v : float) -> None:

        if 0 <= k < len(self.__dict__.values()):
            if k == 0:
                self.vx = v
            else:
                self.vy = v
        else:
            raise IndexError('IndexError: list index out of range')

    def __repr__(self) -> str:
        return "({0.vx!r}, {0.vy!r})".format(self)

    # Return the velocity/Motion
    def velocity(self) -> float:
        return hypot(self.vx, self.vy)


# Vertex or instance inventory
VERTEX_INVENTORY = []
SPLINE = []


class Vertex(object):
    """ Class Vertex (x : integer ,y: integer) """

    # Constructor
    # Initialize private instance variables self.x, self.y, coordinates of
    # a given point in a 2D projection plan.
    # self.x, self.y coordinates in the range (LOWER ,UPPER)
    # Math class methods (+,//,-,*) will also return values between LOWER and UPPER.
    # self.id private instance variable represents the unique identification number
    # for the instance created.

    def __init__(self, x: float = 0, y: float = 0) -> None:
        # Private variables
        self.id = id(self)

        # Set the momentum to zero (vector length zero)
        self.momentum = Momentum(0.0, 0.0)

        self.x = x
        self.y = y

        # Add the object vertex into the inventory
        self.add_to_inventory()

    # Decorator for x properties
    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, x: float) -> None:
        self.__x = x
        if x < LOWER[0] or x > (UPPER[0] - 50):
            if x < LOWER[0]:
                self.__x = LOWER[0]
            else:
                self.__x = (UPPER[0] - 50)

            # goes to the opposite direction
            self.momentum[0] *= -1

    @property
    def y(self: float) -> float:
        return self.__y

    @y.setter
    def y(self, y: float) -> None:

        self.__y = y
        if (y < LOWER[1]) or (y > UPPER[1] - 50):
            if y <= LOWER[1]:
                self.__y = LOWER[1]
            else:
                self.__y = (UPPER[1] - 50)

            # go in the opposite direction
            self.momentum[1] *= -1

    def __add__(self, point: object) -> object:
        if isinstance(point, Vertex):
            self.x += point.x
            self.y += point.y
            return Vertex(self.x, self.y)
        else:
            raise TypeError(
                'Argument point is not a '
                'Vertex instance got %s ' % type(point))

    def __sub__(self, point : object) -> object:
        if isinstance(point, Vertex):
            self.x -= point.x
            self.y -= point.y
            return Vertex(self.x, self.y)
        raise TypeError(
            'Argument point is not a '
            'Vertex instance got %s ' % type(point))

    def __invert__(self) -> object:
        self.x = -self.x
        self.y = -self.y
        return Vertex(self.x, self.y)

    def __abs__(self) -> object:
        self.x = abs(self.x)
        self.y = abs(self.y)
        return Vertex(self.x, self.y)

    def __mul__(self, point : object) -> object:
        if isinstance(point, Vertex):
            self.x *= point.x
            self.y *= point.y
            return Vertex(self.x, self.y)
        else:
            raise TypeError(
                'Argument point is not a '
                'Vertex instance got %s ' % type(point))

    def __floordiv__(self, point: object) -> object:
        if isinstance(point, Vertex):
            self.x /= point.x
            self.y /= point.y
            return Vertex(self.x, self.y)
        else:
            raise TypeError(
                'Argument point is not a '
                'Vertex instance got %s ' % type(point))

    def __lt__(self, point: object) -> bool:
        if isinstance(point, Vertex):
            return hypot(self.x, self.y) < hypot(point.x, point.y)
        else:
            raise TypeError(
                'Argument point is not a '
                'Vertex instance got %s ' % type(point))

    def __eq__(self, point: object) -> bool:
        if isinstance(point, Vertex):
            return self.x == point.x and self.y == point.y
        else:
            raise TypeError(
                'Argument point is not a '
                'Vertex instance got %s ' % type(point))

    def __repr__(self) -> str:
        return "Vertex {0._id!r}(x={0._x!r}, y={0._y!r})".format(self)

    # Show the Vertex position (x,y)
    def position(self) -> tuple:
        return self.x, self.y

    # my_list all instances/vertexes from the inventory
    @staticmethod
    def show_inventory() -> None:
        for r_ in VERTEX_INVENTORY:
            print('Vertex : %s' % r_)

    # Add and object (instance/vertex) into the inventory
    def add_to_inventory(self) -> None:
        if self not in VERTEX_INVENTORY:
            VERTEX_INVENTORY.append(self)

    # Remove a specific vertex from the inventory
    @staticmethod
    def v_remove_from_inventory(vertex : object) -> None:
        try:
            if vertex in VERTEX_INVENTORY:
                VERTEX_INVENTORY.remove(vertex)
                print('Vertex id %s removed from inventory.' % vertex.id)
        except Exception as Err:
            print(Err)
            raise Error('Vertex with id %s cannot be remove from inventory.' % vertex.id)

    def add_to_spline(self) -> None:
        SPLINE.append(self)

    @staticmethod
    def remove_from_spline():
        return NotImplemented

    @staticmethod
    def show_spline():
        return NotImplemented


_RECTANGLE_INVENTORY = []


class Rectangle(object):
    """ Class Rectangle (Point1 : Vertex, Point2 : Vertex) """

    # Constructor:
    # self.id is the unique ID instance number
    def __init__(self,
                 p1: Vertex,
                 p2: Vertex,
                 mass_: float,
                 name_: str,
                 x_deformation: float = 1.0,
                 y_deformation: float = 1.0):
        """

        :param p1: Vertex; random position onto the display (x, y)
        :param p2: Vertex; size of the rectangle tuple (size_x, size_y)
        :param mass_: float in kg
        :param name_: str; name of the object (int value converted into string)
        :param x_deformation: float; default 1.0 represent the x deformation value
        :param y_deformation: float; default 1.0 represent the y deformation value
        """

        if not isinstance(p1, Vertex):
            raise TypeError('\nArgument p1 is not a Vertex type got %s ' % type(p1))

        if not isinstance(p2, Vertex):
            raise TypeError('\nArgument p2 is not a Vertex type got %s ' % type(p2))

        self.p1 = p1
        self.p2 = p2

        self.x_deformation = x_deformation
        self.y_deformation = y_deformation

        self.id = id(self)
        # object mass_ in kg
        self.mass = mass_
        # object name_ (Integer)
        self.name = name_

        # Add object automatically to inventory <_RECTANGLE_INVENTORY>
        self.add_to_inventory()
        # print ('object id : %s created.' % (self.name_) )

    @property
    def x_deformation(self) -> float:
        return self.__Xdeformation

    @x_deformation.setter
    def x_deformation(self, x: float) -> None:
        self.__Xdeformation = x
        if 0 < x < 1:
            self.__Xdeformation = x

    # momentum = mass x velocity
    def Momentum(self, velocity_vector) -> float:
        return self.mass * velocity_vector

        # Add Rectangle to the inventory

    def add_to_inventory(self) -> None:
        if self not in _RECTANGLE_INVENTORY:
            _RECTANGLE_INVENTORY.append(self)

    # my_list all Rectangle/Instance from the inventory
    @staticmethod
    def show_inventory() -> None:
        for rect in _RECTANGLE_INVENTORY:
            print('Rectangle : %s' % rect)

    # Remove a specific Rectangle from the inventory
    def remove_from_inventory(self) -> None:

        if isinstance(self, Rectangle):
            try:

                if self in _RECTANGLE_INVENTORY:
                    _RECTANGLE_INVENTORY.remove(self)
                    print('Rectangle id %s removed from inventory.' % self.id)
                    Vertex.v_remove_from_inventory(self.p1)
                    Vertex.v_remove_from_inventory(self.p2)

            except Exception as Err:
                raise ValueError('Rectangle id %s cannot be remove from inventory.\n%s' % (self.id, Err))

        else:
            raise TypeError('\nIncorrect type for object Rectangle got %s ' % type(Rectangle))

    @staticmethod
    def function(*args) -> tuple:
        for x, y in args:
            if x is None:
                x = 0
            elif y is None:
                y = 0
            return x, y

    def __add__(self, *args) -> object:
        if isinstance(args[0], tuple):

            if len(*args) != 2:
                raise Error('\nInvalid argument')

            x, y = self.function(*args)
            self.p1.x += x if LOWER[0] <= x <= UPPER[0] else 0
            self.p1.y += y if LOWER[0] <= y <= UPPER[1] else 0
            return self.p1
        else:
            raise TypeError('\nArgument must be a tuple (x,y) got %s ' % type(args[0]))

    def __sub__(self, *args) -> object:
        if isinstance(args[0], tuple):

            if len(*args) > 2:
                raise Error('\nInvalid argument')

            x, y = self.function(*args)
            self.p1.x -= x if LOWER[0] <= x <= UPPER[0] else 0
            self.p1.y -= y if LOWER[0] <= y <= UPPER[1] else 0
            return self.p1

        else:
            raise TypeError('\nArgument must be a tuple (x,y) got %s ' % type(args[0]))

    @staticmethod
    def intersection(rect1: object, rect2: object) -> bool:
        """ detect collision between objects """
        ctr_to_ctr = Rectangle.center_distance(rect1, rect2)
        if ctr_to_ctr <= (rect1.p2.x / 2.0 + rect2.p2.x / 2.0):
            return True
        else:
            return False

    def __repr__(self) -> str:

        return "{0.name}({0.p1.x!r},{0.p1.y!r})-" \
               "({0.p2.x!r},{0.p2.y!r})".format(self)

    # Returns a dictionary with rectangle's coordinates
    # This dict can be use during the construction of a PyGame
    # rectangle by passing the whole dict as an argument
    def my_list(self) -> list:
        return [self.p1.x, self.p1.y, self.p2.x, self.p2.y]

    @staticmethod
    # Distance between two vertexes of rectangles
    def vertex_distance(point1 : Vertex, point2: Vertex) -> float:
        return sqrt((point1.x - point2.x) * (point1.x - point2.x)
                    + (point1.y - point2.y) * (point1.y - point2.y))

    @staticmethod
    # Distance between two rectangles (from center of mass)
    def center_distance(rect1: object, rect2: object) -> float:
        c1 : list = rect1.center()
        c2 : list = rect2.center()
        return sqrt((c1[0] - c2[0]) * (c1[0] - c2[0]) +
                    (c1[1] - c2[1]) * (c1[1] - c2[1]))

    # center of mass is the mean position of the mass in an object
    def center(self) -> list:
        m1 = self.p1.x + (self.p2.x / 2.0)
        m2 = self.p1.y + (self.p2.y / 2.0)
        return [m1, m2]


class Tuple2Vertex(Vertex):
    """ Class Tuple2Vertex """

    # Constructor
    # Transform a tuple with coordinates (x,y) into a Vertex object
    # This class inherit from Parent class Vertex
    # Vertex self.id is automatically initialized when calling super()
    def __init__(self, *args):
        if len(tuple(*args)) > 0:
            (self.x, self.y) = (tuple(*args))
        else:
            raise ValueError(
                "\nTuple2Vertex constructor required a tuple (x, y) ")

        super().__init__(self.x, self.y)


class Collision:
    """ Class 2D Engine collision detection """

    # Constructor
    def __init__(self):

        # 2D Engine collision identification
        self.collision_item_id = id(self)

        # my_list of objects to be process by the 2D Engine collision
        self.objects = []

        # my_list returning colliding objects
        self.colliding_objects = []

        print('Collision object engine id : %s initialized' % self.collision_item_id)

    def add_object(self, object_: object) -> None:
        """ Method for adding objects to 2D Engine """
        if object_ not in self.objects:
            self.objects.append(object_)

    def remove_object(self, object_) -> None:
        if object_ in self.objects:
            self.objects.pop(object_)

    @staticmethod
    def list_processing(my_list: list, object_: Rectangle, color_=None) -> None:
        """ Iter every objects from a list and determines position of a given obj."""
        n = 0
        # Iter all object_ from a list
        for item in my_list:
            if item.name == object_.name:
                # object_ found into the list at position n
                break
            else:
                # object_ not found, increment counter
                n += 1

        # Remove object_ (position n) from the list
        my_list.pop(n)

        # if color_ argument is non null
        if color_ is not None:
            # Remove object_ color_ from the <color_> list
            color_.pop(n)

    @staticmethod
    def un_stick(rect1: Rectangle, rect2: Rectangle, v1: Vector2, v2: Vector2) -> None:
        """ Class method to un-stick objects after collision """

        diff = Rectangle.center_distance(rect1, rect2)
        while Rectangle.intersection(rect1, rect2):
            rect1.p1.x += v1.x
            rect1.p1.y += v1.y
            rect2.p1.x += v2.x
            rect2.p1.y += v2.y
            # Check the distance after applying opposite force
            diff_ = Rectangle.center_distance(rect1, rect2)
            # If the distance diff_ is smaller than the original distance diff
            # then something is going wrong; breaking the loop to avoid infinity loop
            if diff_ < diff:
                # print(v1, v2)
                break

    @staticmethod
    def explode(obj1: Rectangle) -> None:

        global BALL
        global COLOR

        # Checking if object is existing into the 2D Engine
        if obj1 not in Engine.objects:
            return

        # Remove object from the collision engine detection
        Collision.list_processing(Engine.objects, obj1)

        # object removed from the list of drawable objects
        Collision.list_processing(BALL, obj1, COLOR)

        # Remove object (rectangle) from the rectangle inventory <_RECTANGLE_INVENTORY>
        obj1.remove_from_inventory()

        # object center
        x, y = obj1.center()

        # object size particles
        size = 4

        # Particles to be created after object disintegration
        particles = 1

        # Particles are indivisible
        if obj1.mass < 1:
            return

        for r_ in range(particles):
            # particle with random mass
            obj_mass = uniform(0.1, 0.9)

            rect = Rectangle(Vertex(x, y), Vertex(size, size), obj_mass, str(len(BALL) + r_), 0, 0)

            # Add the particle to the drawable list
            BALL.append(rect)

            # Add the particle color to the list
            COLOR.append((randint(100, 255), randint(10, 255), randint(20, 255)))

            # To add the particle the the collision engine, uncomment the line below
            Engine.add_object(rect)

            Decay(rect).start()

        # Add a momentum for every new particles
        for r_ in BALL[len(BALL) - particles:]:
            r_.p1.Momentum[0] = randint(-10, 10)
            r_.p1.Momentum[1] = randint(-10, 10)

    @classmethod
    def detect(cls, engine_: object) -> None:

        ind = 0

        for rect1 in engine_.objects:
            ind += 1

            for rect2 in engine_.objects[ind:]:

                # objects are colliding
                if Rectangle.intersection(rect1, rect2):

                    # todo try normalization ?
                    v1 = Vector2(rect1.p1.momentum[0], rect1.p1.momentum[1])
                    v2 = Vector2(rect2.p1.momentum[0], rect2.p1.momentum[1])
                    x1 = Vector2(rect1.center())
                    x2 = Vector2(rect2.center())
                    m1 = rect1.mass
                    m2 = rect2.mass
                    v11_angle_free, v12_angle_free = momentum_trigonometry(
                        x1, x2, v1, v2, float(m1), float(m2), invert=False)

                    v1 = Vector2(rect1.p1.momentum[0], rect1.p1.momentum[1])
                    v2 = Vector2(rect2.p1.momentum[0], rect2.p1.momentum[1])
                    x1 = Vector2(rect1.center())
                    x2 = Vector2(rect2.center())
                    m1 = rect1.mass
                    m2 = rect2.mass
                    v11_trigonometry, v12_trigonometry = momentum_trigonometry_c(
                        v1.x, v1.y, m1, x1.x, x1.y, v2.x, v2.y, m2, x2.x, x2.y, invert=False)

                    # v1 = pygame.math.Vector2(rect1.p1.momentum[0], rect1.p1.momentum[1])
                    # v2 = pygame.math.Vector2(rect2.p1.momentum[0], rect2.p1.momentum[1])
                    # x1 = pygame.math.Vector2(rect1.center())
                    # x2 = pygame.math.Vector2(rect2.center())
                    # m1 = rect1.mass
                    # m2 = rect2.mass
                    # v11_angle_free, v12_angle_free = momentum_angle_free(
                    #     v1, v2, m1, m2, x1, x2, invert=True)
                    #
                    # v1 = Vector2(rect1.p1.momentum[0], rect1.p1.momentum[1])
                    # v2 = Vector2(rect2.p1.momentum[0], rect2.p1.momentum[1])
                    # x1 = Vector2(rect1.center())
                    # x2 = Vector2(rect2.center())
                    # m1, m2 = rect1.mass, rect2.mass
                    #
                    # v11_trigonometry, v12_trigonometry = momentum_angle_free_c(
                    #     v1.x, v1.y, v2.x, v2.y, m1, m2, x1.x, x1.y, x2.x, x2.y, invert=True)

                    # p = 1e-5
                    # diff1 = v11_angle_free.x - v11_trigonometry.x
                    # diff2 = v11_angle_free.y - v11_trigonometry.y
                    # diff3 = v12_angle_free.x - v12_trigonometry.x
                    # diff4 = v12_angle_free.y - v12_trigonometry.y
                    # assert diff1 < p, "diff1 %s %s %s" % (v11_angle_free.x, v11_trigonometry.x, diff1)
                    # assert diff2 < p, "diff2 %s %s %s" % (v11_angle_free.y, v11_trigonometry.y, diff2)
                    # assert diff3 < p, "diff3 %s %s %s" % (v12_angle_free.x, v12_trigonometry.x, diff3)
                    # assert diff3 < p, "diff4 %s %s %s" % (v12_angle_free.y, v12_trigonometry.y, diff4)

                    # Add components x,y to the vertex momentum
                    rect1.p1.momentum[0] = v11_angle_free.x
                    rect1.p1.momentum[1] = v11_angle_free.y
                    rect2.p1.momentum[0] = v12_angle_free.x
                    rect2.p1.momentum[1] = v12_angle_free.y

                    # rect1.p1.x += v11_angle_free.x
                    # rect1.p1.y += v11_angle_free.y
                    # rect2.p1.x += v12_angle_free.x
                    # rect2.p1.y += v12_angle_free.y

                    # still colliding?
                    if Rectangle.center_distance(rect1, rect2) <= rect1.p1.x + rect2.p2.x:
                        Collision.un_stick(rect1, rect2, v11_angle_free, v12_angle_free)

                    # if Obj in engine_.objects:
                    #     Deformation(Obj).start()
                    #
                    # if obj in engine_.objects:
                    #     Deformation(obj).start()


class GL(object):
    def __init_(self):
        self.screen = None


if __name__ == '__main__':

    # BackGroundCollection = ['..//Assets//ph-10046.jpg']
    pygame.display.set_caption("Elastic-collision demo")
    GL.screen = pygame.display.set_mode((UPPER[0], UPPER[1]), vsync=1)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (106, 195, 61)
    RED = (224, 32, 64)
    BLUE = (49, 136, 207)
    ORANGE = (201, 100, 55)

    balls = 50

    while True:

        BALL = []
        COLOR = []

        for ball in range(balls):
            mass = 10      # random.randint(10 , 50)
            diameter = 50  # size of the ball
            BALL.append(
                Rectangle(
                    Vertex(randint(LOWER[0], UPPER[0]),
                           randint(LOWER[1], UPPER[1])),
                    Vertex(diameter, diameter), mass, str(ball), 1.0, 1.0))
            COLOR.append((randint(10, 255), randint(10, 255), randint(20, 255)))

        for ball in BALL:
            x_ = uniform(-4.0, 4.0)
            y_ = uniform(-4.0, 4.0)
            while x_ == 0:
                x_ = uniform(-4.0, 4.0)
            while y_ == 0:
                y_ = uniform(-4.0, 4.0)
            ball.p1.momentum[0] = x_
            ball.p1.momentum[1] = y_

        # Initialized 2D Engine collision detection
        Engine = Collision()

        # Add balls to the Engine
        for ball in BALL:
            Engine.add_object(ball)

        if not Collision.detect(Engine):
            # Breaking the loop
            break
        else:
            Engine.objects = []

    print('\nStarting Engine')

    Poster = 0
    N = -400

    pygame.mixer.pre_init(44100, 16, 2, 4095)
    pygame.init()

    # background = pygame.image.load(BackGroundCollection[0]).convert()

    Font = pygame.font.SysFont("arial", 10)

    pygame.mouse.set_visible(True)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    pos1, pos2 = (0, 0), (0, 0)
    Vector = False

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():  # User did something

            keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                Vector = True
                pos1 = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP:
                pos2 = pygame.mouse.get_pos()
                Vector = False
                for r in BALL:
                    r.p1.momentum[0] = pos2[0] - pos1[0]
                    r.p1.momentum[1] = pos2[1] - pos1[1]

            elif event.type == pygame.MOUSEMOTION:
                pos2 = pygame.mouse.get_pos()

            if keys[K_ESCAPE]:
                done = True

        pressed_mouse = pygame.mouse.get_pressed()

        GL.screen.fill(BLACK)
        # GL.screen.blit(background, (N, 0))

        I_ = 0
        for r in BALL:

            pygame.draw.ellipse(
                GL.screen, COLOR[I_],
                [int(r.center()[0]), int(r.center()[1]), int(r.p2.x / 2) * 2 * r.x_deformation,
                 int(r.p2.x / 2) * 2 * r.y_deformation
                 ])
            I_ += 1

        Collision.detect(Engine)

        if Vector:
            pygame.draw.line(GL.screen, RED, list(pos1), list(pos2), 1)

        j = 1
        for r in BALL:
            r.p1.x += r.p1.momentum[0] * FRICTION
            r.p1.y += r.p1.momentum[1] * FRICTION

        j = 0

        N += 0.5

        if N > UPPER[0]:
            N = -1000

        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(100)

    pygame.quit()