# -*- UTF-8 -*-
# Yoann Berenguer "All rights reserved"

import pygame
from pygame.locals import *

import math
from random import uniform, randint
import time
import threading
from ElasticCollision import Momentum as Physics
from ElasticCollision import TestObject

SIZE = (1024, 768)
UPPER = (SIZE[0], SIZE[1])
LOWER = (0, 0)
SIDE = 1  # 0.98
FRICTION = 1  # 0.99999998
LIMIT_HIGH = 15
LIMIT_LOW = -15

DECAYLOCK = threading.Lock()


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

    def run(self):

        while True:
            DECAYLOCK.acquire()
            for name, age in Decay.particles.items():

                if name == str(self.particle.id):
                    if time.time() - age > 20:
                        Decay.particles.pop(str(self.particle.id))
                        self.particle.remove_from_inventory()
                        break

            # print (self.particle.id, Decay.particles)
            # delay to reduce overhead computer resources
            time.sleep(0.1)
            DECAYLOCK.release()
        else:
            DECAYLOCK.release()


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


def _isinstance(_obj, _type):
        return isinstance(_obj, _type)


class Momentum(object):
    """ Class momentum : Assign a momentum to a single vertex/point """

    # __slots__ = ('_Momentum__Mx', '_Momentum__My')

    # Constructor
    # Default vector components vx, vy =0
    # vx, vy corespond to the x-component, y component of the velocity vector (real numbers)
    def __init__(self, vx=0, vy=0):
        self.vx = vx if LIMIT_LOW < vx < LIMIT_HIGH else 0
        self.vy = vy if LIMIT_LOW < vx < LIMIT_HIGH else 0

    # Decorator for component x
    @property
    def vx(self):
        return self.__vx

    # component x with a range
    @vx.setter
    def vx(self, vx):
        if vx > LIMIT_HIGH:
            self.__vx = LIMIT_HIGH
        elif vx < LIMIT_LOW:
            self.__vx = LIMIT_LOW
        else:
            self.__vx = vx

    # Decorator for component y
    @property
    def vy(self):
        return self.__vy

    # component y has also a range (-10,10)
    @vy.setter
    def vy(self, vy):
        if vy > LIMIT_HIGH:
            self.__vy = LIMIT_HIGH
        elif vy < LIMIT_LOW:
            self.__vy = LIMIT_LOW
        else:
            self.__vy = vy

    def __add__(self, other):
        if isinstance(other, Momentum):
            self.vx += other.vx
            self.vy += other.vy
            return Momentum(self.vx, self.vy)
        else:
            raise Error('Argument is not a momentum instance.')

    def __sub__(self, other):
        if isinstance(other, Momentum):
            self.vx -= other.vx
            self.vy -= other.vy
            return Momentum(self.vx, self.vy)
        else:
            raise Error('Argument is not a momentum instance.')

    def __mul__(self, other):
        self.vx *= other
        self.vy *= other
        return Momentum(self.vx, self.vy)

    @staticmethod
    def inverse(momentum_):
        momentum_.vx *= -1
        momentum_.vy *= -1
        return Momentum(momentum_.vx, momentum_.vy)

    def __getitem__(self, k):
        if 0 <= k < len(self.__dict__.values()):
            if k == 0:
                return self.vx
            else:
                return self.vy
        else:
            raise Error('IndexError: list index out of range')

    def __setitem__(self, k, v):

        if 0 <= k < len(self.__dict__.values()):
            if k == 0:
                self.vx = v
            else:
                self.vy = v
        else:
            raise Error('IndexError: list index out of range')

    def __repr__(self):
        return "({0.vx!r}, {0.vy!r})".format(self)

    # Return the velocity/Motion
    def velocity(self):
        return math.hypot(self.vx, self.vy)


# Vertex or instance inventory
VERTEX_INVENTORY = []
SPLINE = []


class Vertex(object):
    """ Class Vertex (x : integer ,y: integer) """

    # Constructor
    # Initialize private instance variables self.x, self.y, coordinates of
    # a given point in a 2D projection plan.
    # self.x, self.y coordinates in the range (LOWER ,UPPER)
    # Math class methods (+,//,-,*) will also return values beetween LOWER and UPPER.
    # self.id private instance variable represents the unique identification number
    # for the instance created.

    def __init__(self, x=0, y=0):
        # Private variables
        # self.x = x if LOWER[0] < x < UPPER[0] else 0
        # self.y = y if LOWER[1] < y < UPPER[1] else 0
        self.x = x
        self.y = y
        self.id = id(self)
        self.momentum = Momentum(0, 0)
        self.add_to_inventory()

    # Decorator for x properties
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        try:
            self.__x = x
            if x <= LOWER[0] or x >= UPPER[0]:
                if x <= LOWER[0]:
                    self.__x = LOWER[0]
                else:
                    self.__x = UPPER[0]
                self.momentum[0] *= -SIDE
                # sound1.play()
            return self.__x
        except Exception as e:
            print(e)

    # Decorator for y properties
    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        try:
            self.__y = y
            if y <= LOWER[1] or y >= UPPER[1]:
                if y <= LOWER[1]:
                    self.__y = LOWER[1]
                else:
                    self.__y = UPPER[1]
                self.momentum[1] *= -SIDE
                # sound1.play()
            return self.__y

        except Exception as e:
            print(e)

    def __add__(self, point):
        if isinstance(point, Vertex):
            self.x += point.x
            self.y += point.y
            return Vertex(self.x, self.y)
        else:
            raise Error('Argument is not a Vertex')

    def __sub__(self, point):
        if isinstance(point, Vertex):
            self.x -= point.x
            self.y -= point.y
            return Vertex(self.x, self.y)
        else:
            raise Error('Argument is not a Vertex')

    def __invert__(self):
        self.x = -self.x
        self.y = -self.y
        return Vertex(self.x, self.y)

    def __abs__(self):
        self.x = abs(self.x)
        self.y = abs(self.y)
        return Vertex(self.x, self.y)

    def __mul__(self, point):
        if isinstance(point, Vertex):
            self.x *= point.x
            self.y *= point.y
            return Vertex(self.x, self.y)
        else:
            raise Error('Argument is not a Vertex')

    def __floordiv__(self, point):
        if isinstance(point, Vertex):
            self.x /= point.x
            self.y /= point.y
            return Vertex(self.x, self.y)
        else:
            raise Error('Argument is not a Vertex')

    def __lt__(self, point):
        if isinstance(point, Vertex):
            return self.hypo() < math.hypot(point.x, point.y)
        else:
            raise Error('Argument is not a Vertex')

    def __eq__(self, point):
        if isinstance(point, Vertex):
            return self.x == point.x and self.y == point.y
        else:
            raise Error('Argument is not a Vertex')

    def __repr__(self):
        return "Vertex {0._id!r}(x={0._x!r}, y={0._y!r})".format(self)

    # Show the Vertex position (x,y)
    def position(self):
        return self.x, self.y

    # my_list all instances/vertexes from the inventory
    @staticmethod
    def show_inventory():
        for r_ in VERTEX_INVENTORY:
            print('Vertex : %s' % r_)

    # Add instance/vertex to the inventory
    def add_to_inventory(self):
        if self not in VERTEX_INVENTORY:
            VERTEX_INVENTORY.append(self)

    # Remove a specific vertex from the inventory
    @staticmethod
    def v_remove_from_inventory(vertex):
        try:
            if vertex in VERTEX_INVENTORY:
                VERTEX_INVENTORY.remove(vertex)
                print('Vertex id %s removed from inventory.' % vertex.id)
        except Exception as Err:
            print(Err)
            raise Error('Vertex with id %s cannot be remove from inventory.' % vertex.id)

    def add_to_spline(self):
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
    def __init__(self, p1, p2, mass_, name_, x_deformation=1, y_deformation=1):
        if not isinstance(p1, Vertex) or not isinstance(p2, Vertex):
            raise Error('Arguments are not a Vertex type.')
        self.p1 = p1
        self.p2 = p2
        # (x,y) deformation factors
        # (x_deformation or y_deformation=1, no deformation)
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
    def x_deformation(self):
        return self.__Xdeformation

    @x_deformation.setter
    def x_deformation(self, x):
        self.__Xdeformation = x
        if x < 1 or x > 0:
            self.__Xdeformation = x
        return self.__Xdeformation

    # momentum = mass x velocity
    def Momentum(self, velocity_vector):
        return self.mass * velocity_vector

        # Add Rectangle to the inventory

    def add_to_inventory(self):
        if self not in _RECTANGLE_INVENTORY:
            _RECTANGLE_INVENTORY.append(self)
            return

    # my_list all Rectangle/Instance from the inventory
    @staticmethod
    def show_inventory():
        for rect in _RECTANGLE_INVENTORY:
            print('Rectangle : %s' % rect)

    # Remove a specific Rectangle from the inventory
    def remove_from_inventory(self):
        if isinstance(self, Rectangle):
            try:

                if self in _RECTANGLE_INVENTORY:
                    _RECTANGLE_INVENTORY.remove(self)
                    print('Rectangle id %s removed from inventory.' % self.id)
                    Vertex.v_remove_from_inventory(self.p1)
                    Vertex.v_remove_from_inventory(self.p2)

            except Exception as Err:
                print(Err)
                raise Error('Rectangle id %s cannot be remove from inventory.' % self.id)

            finally:
                pass
        else:
            raise Error('Argument is not a Rectangle.')

    @staticmethod
    def function(*args):
        for x, y in args:
            if x is None:
                x = 0
            elif y is None:
                y = 0
            return x, y

    def __add__(self, *args):
        if isinstance(args[0], tuple):

            if len(*args) > 2:
                raise Error('Argument list is too long')

            x, y = self.function(*args)
            self.p1.x += x if LOWER[0] <= x <= UPPER[0] else 0
            self.p1.y += y if LOWER[0] <= y <= UPPER[1] else 0
            return self.p1
        else:
            raise Error('Argument must be a tuple (x,y)')

    def __sub__(self, *args):
        if isinstance(args[0], tuple):

            if len(*args) > 2:
                raise Error('my_list of argument incorrect')

            x, y = self.function(*args)
            self.p1.x -= x if LOWER[0] <= x <= UPPER[0] else 0
            self.p1.y -= y if LOWER[0] <= y <= UPPER[1] else 0
            return self.p1
        else:
            raise Error('Argument must be a tuple (x,y)')

    def intersection(self, object_):
        """ detect collision between objects """
        if isinstance(self, type(object_)):
            if Rectangle.center_distance(self, object_) <= 2 * (self.p2.x / 2):
                return True
        else:
            raise Error('object_ is not a Rectangle class.')

    def __repr__(self):

        return "{0.name}({0.p1.x!r},{0.p1.y!r})-" \
               "({0.p2.x!r},{0.p2.y!r})".format(self)

    # Returns a dictionary with rectangle's coordinates
    # This dict can be use during the construction of a PyGame
    # rectangle by passing the whole dict as an argument
    def my_list(self):
        return [self.p1.x, self.p1.y, self.p2.x, self.p2.y]

    @staticmethod
    # Distance between two vertexes of rectangles
    def vertex_distance(point1, point2):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    @staticmethod
    # Distance between two rectangles (from center of mass)
    def center_distance(rect1, rect2):
        c1 = list(rect1.center())
        c2 = list(rect2.center())
        return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)

    # center of mass is the mean position of the mass in an object
    def center(self):
        return self.p1.x + self.p2.x / 2, self.p1.y + self.p2.y / 2


class Tuple2Vertex(Vertex):
    """ Class Tuple2Vertex """

    # Constructor
    # Transform a tuple with coordinates (x,y) into a Vertex object
    # This class inherit from Parent class Vertex
    # Vertex self.id is automatically initialized when calling super()
    def __init__(self, *args):
        if len(tuple(*args)) > 0:
            (self.x, self.y) = (tuple(*args))
        self = super().__init__(self.x, self.y)


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

    def add_object(self, object_):
        """ Method for adding objects to 2D Engine """
        if object_ not in self.objects:
            self.objects.append(object_)

    def remove_object(self, object_):
        if object_ in self.objects:
            self.objects.pop(object_)

    @staticmethod
    def list_processing(my_list, object_, color_=None):
        """ Iter every objects from a list and determines position of a given obj."""
        n = 0
        # Iter all object_ from a list
        for item in my_list:
            if item.Name == object_.Name:
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
    def un_stick(obj1, obj2, v1, v2):
        """ Class method to un-stick objects after collision """

        d_ = obj1.p2.x + obj2.p2.x
        N_ = 0
        # un-stick objects by adding momentum increments to objects
        while Rectangle.center_distance(obj1, obj2) <= 40:
                # print(Rectangle.center_distance(obj1, obj2))
                obj1.p1.x += min(v1.x, d_ * v1.normalize().x)
                obj1.p1.y += min(v1.y, d_ * v1.normalize().y)

                obj2.p1.x += min(v2.x, d_ * v2.normalize().x)
                obj2.p1.y += min(v2.y, d_ * v2.normalize().y)
                if N_ > 5:
                    break
                N_ += 1

    @staticmethod
    def explode(obj1):

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
            mass = uniform(0.1, 0.9)

            rect = Rectangle(Vertex(x, y), Vertex(size, size), mass, str(len(BALL) + r_), 1, 1)

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
    def detect(cls, Engine):

        ind = 0

        for Obj in Engine.objects:
            self = Obj
            ind += 1

            for obj in Engine.objects[ind:]:

                # objects are colliding
                if self.intersection(obj):

                    self.ColidingObjects = [self, obj]

                    # ------------
                    #  ANGLE FREE
                    # ------------
                    v1 = pygame.math.Vector2(self.p1.momentum[0], self.p1.momentum[1])
                    v2 = pygame.math.Vector2(obj.p1.momentum[0], obj.p1.momentum[1])
                    x1 = pygame.math.Vector2(self.center())
                    x2 = pygame.math.Vector2(obj.center())
                    m1 = self.mass
                    m2 = obj.mass
                    mass1 = 2 * m2 / (m1 + m2)
                    mass2 = 2 * m1 / (m1 + m2)
                    if x1 == x2:
                        x1 += pygame.math.Vector2(0.1, 0.1)
                    V11x, V11y = v1 - (mass1 * (v1 - v2).dot(x1 - x2) / pow((x1 - x2).length(), 2)) * (x1 - x2)
                    V12x, V12y = v2 - (mass2 * (v2 - v1).dot(x2 - x1) / pow((x2 - x1).length(), 2)) * (x2 - x1)

                    V11 = pygame.math.Vector2(V11x, V11y)
                    V12 = pygame.math.Vector2(V12x, V12y)

                    # ------------
                    # Trigonometry
                    # ------------
                    v1 = pygame.math.Vector2(self.p1.momentum[0], self.p1.momentum[1])
                    v2 = pygame.math.Vector2(obj.p1.momentum[0], obj.p1.momentum[1])
                    v1.y *= -1
                    v2.y *= -1
                    mass1, mass2 = self.mass, obj.mass
                    obj1 = TestObject(v1.x, v1.y, mass1, self.center())
                    obj2 = TestObject(v2.x, v2.y, mass2, obj.center())
                    V1x, V1y = Physics.process_v1(obj1, obj2)
                    V2x, V2y = Physics.process_v2(obj1, obj2)
                    V1 = pygame.math.Vector2(V1x, V1y)
                    V2 = pygame.math.Vector2(V2x, V2y)

                    # Add components x,y to vertex momentum
                    self.p1.momentum[0] = V1x
                    self.p1.momentum[1] = V1y
                    obj.p1.momentum[0] = V2x
                    obj.p1.momentum[1] = V2y

                    self.p1.x += V1x
                    self.p1.y += V1y
                    obj.p1.x += V2x
                    obj.p1.y += V2y

                    # still colliding?
                    if Rectangle.center_distance(self, obj) <= self.p1.x + obj.p2.x:
                        Collision.un_stick(self, obj, V1, V2)

                    # if self in Engine.objects:
                    #    Deformation(self).start()

                    # if obj in Engine.objects:
                    #    Deformation(obj).start()


class GL:
    def __init_(self):
        screen = None


if __name__ == '__main__':

    BackGroundCollection = ['Assets\\Graphics\\ph-10046.jpg']
    pygame.display.set_caption("2D Collision detection engine")
    GL.screen = pygame.display.set_mode((UPPER[0], UPPER[1]), HWSURFACE | DOUBLEBUF, 16)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (106, 195, 61)
    RED = (224, 32, 64)
    BLUE = (49, 136, 207)
    ORANGE = (201, 100, 55)

    balls = 20

    while True:

        BALL = []
        COLOR = []

        for r in range(balls):
            mass = 1
            diameter = 0
            BALL.append(Rectangle(Vertex(randint(LOWER[0], UPPER[0]), randint(LOWER[1], UPPER[1])),
                                  Vertex(40 + diameter, 40 + diameter), mass, str(r), 1, 1))
            COLOR.append((randint(10, 255), randint(10, 255), randint(20, 255)))

        for r in BALL:
            r.p1.momentum[0] = randint(-4, 4)
            r.p1.momentum[1] = randint(-4, 4)

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
    N = -1000

    pygame.mixer.pre_init(44100, 16, 2, 4095)
    pygame.init()

    background = pygame.image.load(BackGroundCollection[0])

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
                    r.p1.momentum[1] = (pos2[1] - pos1[1]) * -1

            elif event.type == pygame.MOUSEMOTION:
                pos2 = pygame.mouse.get_pos()

        pressed_mouse = pygame.mouse.get_pressed()

        # --- Game logic should go here

        # --- Drawing code should go here

        GL.screen.fill(BLACK)
        GL.screen.blit(background, (N, 0))

        I_ = 0
        for r in BALL:
            pygame.draw.ellipse(GL.screen, COLOR[I_],
                                [int(r.center()[0]), int(r.center()[1]), int(r.p2.x / 2) * 2 * r.x_deformation,
                                 int(r.p2.x / 2) * 2 * r.y_deformation])
            I_ += 1

        Collision.detect(Engine)

        if Vector:
            pygame.draw.line(GL.screen, RED, list(pos1), list(pos2), 1)

        time_passed = clock.tick() / 1000
        # print (time_passed)

        j = 1
        for r in BALL:
            r.p1.x += r.p1.momentum[0]
            r.p1.y += r.p1.momentum[1]

        for r in BALL:
            r.p1.momentum[0] *= FRICTION
            r.p1.momentum[1] *= FRICTION

        j = 0

        N += 0.5

        if N > UPPER[0]:
            N = -1000

        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    pygame.quit()





