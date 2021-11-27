# cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True, optimize.use_switch=True
# encoding: utf-8
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

"""
This unit includes all the hook methods for the external C functions library
cpdef tuple momentum_angle_free_c
cpdef tuple momentum_trigonometry_c
"""


import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=ImportWarning)


try:
    import pygame

except ImportError:
    raise ImportError("\n<pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")

from pygame.math import Vector2


# Cython is require
try:
    cimport cython

except ImportError:
    raise ImportError("\n<cython> library is missing on your system."
          "\nTry: \n   C:\\pip install cython on a window command prompt.")


cdef extern from '../Source/elastic_collision.c':

    struct vector2d:
        float x
        float y

    struct v_struct:
        vector2d vector1
        vector2d vector2

    void vecinit(vector2d *v, float x, float y)nogil
    float vlength(vector2d *v)nogil
    void scale_inplace(float c, vector2d *v)nogil
    vector2d subcomponents(vector2d v1, vector2d v2)nogil
    float dot(vector2d *v1, vector2d *v2)nogil

    struct collision_vectors:
        vector2d v12
        vector2d v21

    collision_vectors momentum_angle_free(
            float v1_x, float v1_y,
            float v2_x, float v2_y,
            float m1, float m2,
            float x1_x, float x1_y,
            float x2_x, float x2_y
    )nogil

    struct collider_object:
        vector2d vector
        float mass
        vector2d centre

    collision_vectors momentum_t(collider_object obj1, collider_object obj2)nogil


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef tuple momentum_angle_free_c(
        v1_x: float, v1_y: float,
        v2_x: float, v2_y: float,
        m1: float, m2: float,
        x1_x: float, x1_y: float,
        x2_x: float, x2_y: float,
        invert:bint=False
):
    """
    RETURN VECTORS V1 & V2 AFTER OBJECT COLLISION (ANGLE FREE METHOD)
    
    This method is using angle free equations to determine the objects final velocities
    Refer to Two-dimensional collision with two moving objects in the following link : 
    https://en.wikipedia.org/wiki/Elastic_collision 
    
    * This method can be used to resolved 2d elastic collision in 2d space system (video game 
      space) where the Y-axis is inverted.  
    
    * v1_x & v1_y & v2_x, v2_y are un-normalized vectors (vector components) in order to 
      keep the total kinetic energy and to redistribute the force to the final velocities (v1 & v2) 
      
    NOTE : 
    If you are working in a real domain system coordinate (cartesian system), prefer to use 
    the module:
    - <real> for real domain application instead.
    This method is essentially the same than momentum_trigonometry_real but it offers the possibility
    to invert the final vectors trajectories
    
    :param v1_x: float; object 1 velocity along the x-axis
    :param v1_y: float; object 1 velocity along the y-axis
    :param v2_x: float; object 2 velocity along the x-axis
    :param v2_y: float; object 2 velocity along the y-axis
    :param m1  : float; mass for object1 in kg
    :param m2  : float; mass for object2 in kg
    :param x1_x: float; object 1 centre position x coordinate
    :param x1_y: float; object 1 centre position y coordinate
    :param x2_x: float; object 2 centre position x coordinate
    :param x2_y: float; object 2 centre position y coordinate
    :param invert: Y-axis inversion | if True convert the model 
    to a cartesian coordinate system
    :return: Return a tuple containing vectors v1 & v2 
    """

    if invert:
        v1_y *=-<float>1.0
        v2_y *=-<float>1.0
        x1_y *=-<float>1.0
        x2_y *=-<float>1.0
    cdef:
        collision_vectors v = \
            momentum_angle_free(v1_x, v1_y, v2_x, v2_y, m1, m2, x1_x, x1_y, x2_x, x2_y)
        vector2d vector1 = v.v12
        vector2d vector2 = v.v21

    return Vector2(vector1.x, vector1.y), Vector2(vector2.x, vector2.y)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef tuple momentum_trigonometry_c(
        v1x: float, v1y: float,
        m1: float,
        x1x: float, x1y: float,
        v2x: float, v2y: float,
        m2 : float,
        x2x: float, x2y : float,
        invert: bint=False
):
    """
    RETURN VECTORS V1 & V2 AFTER OBJECT COLLISION (TRIGONOMETRY) 
    
    This method is using trigonometric equations to determine the objects final velocities
    Refer to Two-dimensional collision with two moving objects in the following link : 
    https://en.wikipedia.org/wiki/Elastic_collision 
    
    * This method can be used to resolved 2d elastic collision in 2d space system (video game 
      space) where the Y-axis is inverted.  
    
    * v1_x & v1_y & v2_x, v2_y are un-normalized vectors (vector components) in order to 
      keep the total kinetic energy and to redistribute the force to the final velocities (v1 & v2) 
    
    NOTE : 
    If you are working in a real domain system coordinate (cartesian system), prefer to use 
    the module:
    - <real> for real domain application instead.
    This method is essentially the same than momentum_trigonometry_real but it offers the possibility
    to invert the final vectors trajectories
    
    :param v1x : float, object 1 velocity along the x-axis
    :param v1y : float, object 1 velocity along the y-axis
    :param m1  : float, mass for object1 in kg
    :param x1x : float, object 1 centre position x coordinate
    :param x1y : float, object 1 centre position y coordinate
    :param v2x : float, object 2 velocity along the x-axis
    :param v2y : float, object 2 velocity along the y-axis
    :param m2  : float, mass for object2 in kg
    :param x2x : float, object 2 centre position x coordinate
    :param x2y : float, object 2 centre position y coordinate
    :param invert: bool Y-axis inversion | if True convert the model 
    to a cartesian coordinate system
    :return: Return a tuple containing vectors v1 & v2
    """


    cdef:
        collider_object obj1_c, obj2_c
        vector2d v1, v2, x1, x2

    if invert:
        v1y *= -<float> 1.0
        v2y *= -<float> 1.0
        x1y *= -<float> 1.0
        x2y *= -<float> 1.0

    with nogil:
        vecinit(&v1, v1x, v1y)
        vecinit(&v2, v2x, v2y)
        vecinit(&x1, x1x, x1y)
        vecinit(&x2, x2x, x2y)

        obj1_c.vector = v1
        obj1_c.mass   = m1
        obj1_c.centre = x1

        obj2_c.vector = v2
        obj2_c.mass   = m2
        obj2_c.centre = x2

    cdef:
        collision_vectors obj_c = momentum_t(obj1_c, obj2_c)
        vector2d vector1 = obj_c.v12
        vector2d vector2 = obj_c.v21

    return Vector2(vector1.x, vector1.y), Vector2(vector2.x, vector2.y)




