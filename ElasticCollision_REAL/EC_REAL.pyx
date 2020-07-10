###cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True, optimize.use_switch=True
# encoding: utf-8

"""

This code comes with a MIT license.
Copyright (c) 2018 Yoann Berenguer
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

"""

# 2D REAL ELASTIC COLLISION (EC) LIBRARY

# PROJECT FILES :
# EC_REAL.pyx
# EC_REAL.pxd
# EC_SHARED.pyx
# EC_SHARED.pxd
# setup_Project.py
# EC_REALTest.py


# DESCRIPTION:
# Cython version needs to be compile into your system.
# Please refer to the compilation section for more details.

# This library contains 2 distinct methods (trigonometry and free angle representation).
# Both techniques are using different approach:

# Angle free is by far the fastest method as it does not requires trigonometric functions
# such as (cos, sin, atan ..etc) in order to solve object's vector components at the time of contact.
# Angle free method rely on vector calculation instead.

# Trigonometry method is requiring calculation of object contact angle and angle theta at point of collision prior
# solving object's vector components.

# COMPILATION
# Building the project
# In a command prompt and under the directory containing the source files
# C:\>python setup_Project.py build_ext --inplace
#
# If the compilation fail, refers to the requirement section and make sure cython
# and a C-compiler are correctly install on your system.

#
# REQUIREMENTS:
# - Pygame 3
# - Numpy
# - Cython (C extension for python)
# - A C compiler for windows (Visual Studio, MinGW etc) install on your system
#   and linked to your windows environment.
#   Note that some adjustment might be needed once a compiler is install on your system,
#   refer to external documentation or tutorial in order to setup this process.
#   e.g https://devblogs.microsoft.com/python/unable-to-find-vcvarsall-bat/

# TIMING:
# For millions iterations
# ANGLE FREE      :  0.7796687 seconds
# TRIGONOMETRY    :  1.1638778 seconds

__author__  = "Yoann Berenguer"
__license__ = "MIT License"
__email__   = "yoyoberenguer@hotmail.com"


import cython

try:
    import pygame
    from pygame import Vector2
    from pygame import Rect
except ImportError:
    print('\nOn window, try:\nC:\>pip install pygame')
    raise SystemExit


from libc.math cimport cos, sin
from libc.stdio cimport printf
from EC_SHARED cimport get_contact_angle, get_theta_angle

cdef extern from 'vector.c':

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
    void scale_inplace(float c, vector2d *v)nogil
    float dot(vector2d *v1, vector2d *v2)nogil


DEF M_PI  = 3.14159265358979323846
DEF M_PI2 = 3.14159265358979323846 / 2.0

# **************************** PYTHON INTERFACE ***************************************

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef momentum_trigonometry_R(float obj1_cx, float obj1_cy, float obj2_cx, float obj2_cy,
                            float obj1_vx, float obj1_vy, float obj2_vx, float obj2_vy,
                            float obj1_mass, float obj2_mass):
    """
    RETURN VECTORS V1 & V2 AFTER COLLISION 
    
    This technique is using an exploded variable models instead of a compact vector model to 
    speedup calculation process (no need to convert pygame vector2 python objects into 
    equivalent cython objects). 
    
    Return python objects such as dictionary.
    e.g : 
    vec1, vec2 = momentum_trigonometry(x1x, x1y, x2x, x2y, v1x, v1y, v2x, v2y, m1, m2, invert)
    print("\nobject1 vector : (x:%s y:%s) ", (vec1['x'], vec1['y']))
    print("\nobject2 vector : (x:%s y:%s) ", (vec2['x'], vec2['y']))
    
    :param obj1_cx  : float; Object 1 centre x coordinate
    :param obj1_cy  : float; object 1 centre y coordinate
    :param obj2_cx  : float; object 2 centre x coordinate
    :param obj2_cy  : float; object 2 centre y coordinate
    :param obj1_vx  : float; object 1 vector x component
    :param obj1_vy  : float; object 1 vector y component
    :param obj2_vx  : float; object 2 vector x component
    :param obj2_vy  : float; object 2 vector y component
    :param obj1_mass: float; object 1 mass in kilogrammes
    :param obj2_mass: float; object 2 mass in kilogrammes
    :return: return a python objects
    """
    cdef vector2d vec1, vec2
    cdef v_struct collision

    vecinit(&vec1, obj1_vx, obj1_vy)
    vecinit(&vec2, obj2_vx, obj2_vy)
    # DETERMINES V1 & V2 COMPONENTS AFTER COLLISION
    collision = \
        get_momentum_trigonometry_vecR(obj1_cx, obj1_cy, obj2_cx, obj2_cy, vec1, vec2, obj1_mass, obj2_mass)

    return collision.vector1, collision.vector2


# **************************** ANGLE FREE **********************************************************

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef momentum_angle_free_R(float v1x, float v1y, float v2x, float v2y,
                          float m1, float m2, float x1x, float x1y,
                          float x2x, float x2y):
    """
    RETURN VECTORS V1 & V2 AFTER COLLISION
    
    This technique is using an exploded variable models instead of a compact vector model to 
    speedup calculation process (no need to convert pygame vector2 python objects into 
    equivalent cython objects). 
    
    Return python objects such as dictionary.
    e.g : 
    vec1, vec2 = momentum_angle_free(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert)
    print("\nANGLE FREE - object1 vector : (x:%s y:%s) ", (vec1['x'], vec1['y']))
    print("\nANGLE FREE - object2 vector : (x:%s y:%s) ", (vec2['x'], vec2['y']))

    :param v1x: float, object1 x vector component
    :param v1y: float, object1 y vector component
    :param v2x: float, object2 x vector component
    :param v2y: float, object2 y vector component
    :param m1 : float; object1 mass in kilograms, must be > 0
    :param m2 : float; object2 mass in kilograms, must be > 0
    :param x1x: float, object1 x vector component
    :param x1y: float, object1 y vector component
    :param x2x: float, object2 x vector component
    :param x2y: float, object2 y vector component
    :return: python object tuple (v1 & v2)
    """

    cdef vector2d vec1, vec2, x1_vec, x2_vec
    vecinit(&vec1, v1x, v1y)
    vecinit(&vec2, v2x, v2y)
    vecinit(&x1_vec, x1x, x1y)
    vecinit(&x2_vec, x2x, x2y)

    cdef v_struct v = get_angle_free_vecR(vec1, vec2, m1, m2, x1_vec, x2_vec)

    return v.vector1, v.vector2

# ***************************END INTERFACE *************************************



# YOU CANNOT CALL BELOW FUNCTIONS DIRECTLY FROM PYTHON SCRIPT (USE PYTHON INTERFACE FUNCTIONS INSTEAD)
# FUNCTIONS BELOW CAN BE ACCESS FROM CYTHON CODE ONLY USING CIMPORT STATEMENT
# *************************** CYTHON INTERFACE *********************************

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef v_struct get_momentum_trigonometry_vecR(
        float obj1_cx, float obj1_cy, float obj2_cx, float obj2_cy,
        vector2d obj1_vec, vector2d obj2_vec,
        float obj1_mass, float obj2_mass)nogil:
    """
    RETURN VECTORS V1 & V2 OF ORIGINAL OBJECTS AFTER COLLISION 
    
    :param obj1_cx  : float; Object 1 centre x coordinate
    :param obj1_cy  : float; object 1 centre y coordinate
    :param obj2_cx  : float; object 2 centre x coordinate
    :param obj2_cy  : float; object 2 centre y coordinate
    :param obj1_vec : float; object 1 vector velocity/trajectory
    :param obj2_vec : float; object 2 vector velocity/trajectory
    :param obj1_mass: float; object 1 mass in kilogrammes
    :param obj2_mass: float; object 2 mass in kilogrammes
    :return: return a cython object v_struct (tuple of vector2d v1, v2)
    """

    cdef float phi    = get_contact_angle(obj1_cx, obj1_cy, obj2_cx, obj2_cy)
    cdef float theta1 = get_theta_angle(obj1_vec)
    cdef float theta2 = get_theta_angle(obj2_vec)
    cdef float v1_length, v2_length
    v1_length         = vlength(&obj1_vec)
    v2_length         = vlength(&obj2_vec)
    cdef vector2d v1  = get_v1R(
        v1_length, v2_length, theta1, theta2, phi, obj1_mass, obj2_mass)
    cdef vector2d v2  = get_v2R(
        v1_length, v2_length, theta1, theta2, phi, obj1_mass, obj2_mass)

    #scale_inplace(-1, &v1)
    #scale_inplace(-1, &v2)
    cdef v_struct collision
    collision.vector1 = v1
    collision.vector2 = v2
    return collision


cdef vector2d get_v1R(
        float v1_, float v2_, float theta1_,
        float theta2_, float phi_, float m1_, float m2_)nogil:
    """
    RETURN SCALAR SIZE V1 OF THE ORIGINAL OBJECT REPRESENTED BY (V1, THETA1, M1)
 
    where v1_ and v2_ are the scalar sizes of the two original speeds of the objects, m1_ and m2_
    are their masses, θ1 and θ2 are their movement angles, that is,v1x = v1_.cos(θ1) , v1y = v1_.sin(θ1)
    (meaning moving directly down to the right is either a -45° angle, or a 315°angle), and lowercase phi_ (φ)
    is the contact angle.

    :param v1_     : float; object1 vector_ length
    :param v2_     : float; object2 vector_ length
    :param theta1_ : float; Θ1 angle in radians (object1)
    :param theta2_ : float; Θ2 angle in radians (object2)
    :param phi_    : float; φ contact angle in radians
    :param m1_     : float; Mass in kilograms, must be > 0 (object1)
    :param m2_     : float; Mass in kilograms, must be > 0(object2)
    :return        : Returns a vector2d cython object, vector v1
    :rtype         : vector2d 
    """
    cdef float numerator, v1x, v1y
    cdef float r1, r2
    cdef float m12 = m1_ + m2_

    if v1_ <=0.0 or v2_ <=0.0:
        printf('|v1_|, |v2_| magnitude must be >= 0.0')
        with gil:
            print("\n|v1|=%s |v2|=%s " % (v1_, v2_))
            raise SystemExit
    if m12 <= 0.0:
        printf("Object's mass should be > 0.0")
        with gil:
            raise SystemExit

    r1 = theta1_ - phi_
    r2 = phi_ + M_PI2
    numerator = v1_ * <float>cos(r1) * (m1_ - m2_) + 2 * m2_ * v2_ * <float>cos(theta2_ - phi_)
    v1x = numerator * <float>cos(phi_) / m12 + v1_ * <float>sin(r1) * <float>cos(r2)
    v1y = numerator * <float>sin(phi_) / m12 + v1_ * <float>sin(r1) * <float>sin(r2)

    cdef vector2d v1_vec
    vecinit(&v1_vec, v1x, v1y)
    return v1_vec


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef vector2d get_v2R(
        float v1_, float v2_, float theta1_,
        float theta2_, float phi_, float m1_, float m2_)nogil:
    """
    RETURN SCALAR SIZE V2_ OF THE ORIGINAL OBJECT REPRESENTED BY (V2_, THETA2_, M2_)

    where v1_ and v2_ are the scalar sizes of the two original speeds of the objects, m1_ and m2_
    are their masses, θ1 and θ2 are their movement angles, that is,v1x = v1_.cos(θ1) , v1y = v1_.sin(θ1)
    (meaning moving directly down to the right is either a -45° angle, or a 315°angle), and lowercase phi_ (φ)
    is the contact angle.

    :param v1_    : float; object1 vector_ length
    :param v2_    : float; object2 vector_ length
    :param theta1_: float; Θ1 angle in radians (object1)
    :param theta2_: float; Θ2 angle in radians (object2)
    :param phi_   : float; φ contact angle in radians
    :param m1_    : float; Mass in kilograms, must be > 0 (object1)
    :param m2_    : float; Mass in kilograms, must be > 0(object2)
    :return       : float; Returns a direction vector_
    :return       : float; Return a cython object, vector v2
    """
    cdef:
        float numerator, v2x, v2y
        float r1, r2
        float m21 = m2_ + m1_
        vector2d v2_vec

    r1 = theta2_ - phi_
    r2 = phi_ + M_PI2

    if v1_ <=0.0 or v2_ <=0.0:
        printf('|v1_|, |v2_| magnitude must be >= 0.0')
        with gil:
            print("\n|v1|=%s |v2|=%s " % (v1_, v2_))
            raise SystemExit
    if m21 <= 0.0:
        printf("Object's mass should be > 0.0")
        with gil:
            raise SystemExit
    numerator = v2_ * <float>cos(r1) * (m2_ - m1_) + 2 * m1_ * v1_ * <float>cos(theta1_ - phi_)
    v2x = numerator * <float>cos(phi_) / m21 + v2_ * <float>sin(r1) * <float>cos(r2)
    v2y = numerator * <float>sin(phi_) / m21 + v2_ * <float>sin(r1) * <float>sin(r2)

    vecinit(&v2_vec, v2x, v2y)
    return v2_vec



# ****************************** ANGLE FREE METHOD *******************************************

# ***************************************************************
# Angle free representation, the changed velocities are computed
# using centers x1 and x2 at the time of contact.
# ***************************************************************
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef vector2d get_v1_angle_free_vecR(
        vector2d v1, vector2d v2, float m1, float m2, vector2d x1, vector2d x2)nogil:
    """
    SCALAR SIZE V1_ OF THE ORIGINAL OBJECT SPEED REPRESENTED BY (V1_, M1_, X1 ARGUMENTS).

    :param v1: vector2d, object1 vector_
    :param v2: vector2d, object2 vector_
    :param m1: float; object1 mass_ in kilograms, must be > 0
    :param m2: float; object2 mass_ in kilograms, must be > 0
    :param x1: vector2d, object1 centre_
    :param x2: vector2d, object2 centre_
    :return: vector2d, resultant vector_ for object1
    """
    cdef float m12 = m1 + m2

    if vlength(&v1) <=0.0 or vlength(&v2) <= 0.0:
        printf('|v1|, |v2| magnitude must be >= 0.0')
        with gil:
            print("\n|v1|=%s |v2|=%s " % (vlength(&v1), vlength(&v2)))
            raise SystemExit

    if m12 <= 0.0:
        printf("Object's mass should be > 0.0")
        with gil:
            raise SystemExit

    cdef float mass = 2.0 * m2 / (m1 + m2)      # mass coefficient in the equation
    cdef vector2d v12, x12		                # 2d vector declaration v12 & x12

    v12 = subcomponents(v1, v2)     	        # subtract v1 and v2 (v1 - v2).
                                                # subcomponents return a new vector v12,
                                                # original vector v1 & v2 components remain unchanged.
    x12 = subcomponents(x1, x2)             	# Objects centre difference (x1 - x2).
                                                # subcomponents return a new vector x12
                                                # x1 & x2 vector components remain unchanged.
    cdef float x12_length = vlength(&x12)       # x12 vector length (scalar)
    cdef float d = dot(&v12, &x12)	            # vector dot product v12 & x12, return a scalar value (float)
    # rescale vector x12
    scale_inplace((mass * d) / (x12_length * x12_length), &x12)
    return subcomponents(v1, x12)



# ***************************************************************
# Angle free representation, the changed velocities are computed
# using centers x1 and x2 at the time of contact.
# ***************************************************************
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef vector2d get_v2_angle_free_vecR(
        vector2d v1, vector2d v2, float m1, float m2, vector2d x1, vector2d x2)nogil:
    """
    scalar size v2_ of the original object speed represented by (v2_, m2_, x2 arguments).

    :param v1: vector2d, object1 vector_
    :param v2: vector2d, object2 vector_
    :param m1: float; object1 mass_ in kilograms, must be > 0
    :param m2: float; object2 mass_ in kilograms, must be > 0
    :param x1: vector2d, object1 centre_
    :param x2: vector2d, object2 centre_
    :return: pygame.math.Vector2, resultant vector_ for object1
    """
    cdef float m12 = m1 + m2

    # AT LEAST ONE OBJECT MUST BE IN MOTION
    if vlength(&v1) <=0.0 or vlength(&v2) <= 0.0:
        printf('|v1|, |v2| magnitude must be >= 0.0')
        with gil:
            print("\n|v1|=%s |v2|=%s " % (vlength(&v1), vlength(&v2)))
            raise SystemExit
    if m12 <= 0.0:
        printf("Object's mass should be > 0.0")
        with gil:
            raise SystemExit

    cdef float mass = 2.0 * m1 / (m1 + m2)   	# mass coefficient in the equation
    cdef vector2d v21, x21		                # 2d vector declaration v21 & x21

    v21 = subcomponents(v2, v1)		            # subtract v2 and v1 (v2 - v1).
                                                # subcomponents return a new vector v21,
                                                # original vector v2 & v1 components remain unchanged.
    x21 = subcomponents(x2, x1)             	# Objects centre difference (x2 - x1).
                                                # subcomponents return a new vector x21
                                                # x2 & x1 vector components remain unchanged.
    cdef float x21_length = vlength(&x21)	    # x21 vector length (scalar)
    cdef float d = dot(&v21, &x21)	            # vector dot product v21 & x21, return a scalar value (float)
    # rescale vector x21
    scale_inplace((mass * d) / (x21_length * x21_length), &x21)
    return subcomponents(v2, x21)


# ************************************************************************
# Angle free calculation, return V1 and V2
# ************************************************************************
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef v_struct get_angle_free_vecR(
        vector2d v1, vector2d v2, float m1, float m2, vector2d x1, vector2d x2)nogil:
    """
    :param v1: vector2d, object1 vector_
    :param v2: vector2d, object2 vector_
    :param m1: float; object1 mass_ in kilograms, must be > 0
    :param m2: float; object2 mass_ in kilograms, must be > 0
    :param x1: vector2d, object1 centre_
    :param x2: vector2d, object2 centre_
    :return: tuple, (object1 resultant vector_, object2 resultant vector_)
    """
    cdef vector2d v11, v22
    v11 = get_v1_angle_free_vecR(v1, v2, m1, m2, x1, x2)
    v22 = get_v2_angle_free_vecR(v1, v2, m1, m2, x1, x2)
    #scale_inplace(-1, &v11)
    #scale_inplace(-1, &v22)
    cdef v_struct collision
    collision.vector1 = v11
    collision.vector2 = v22
    return collision


# # ***************************************************************************************************
#
