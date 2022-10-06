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

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
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


# Numpy is require
try:
    import numpy

except ImportError:
    raise ImportError("\n<numpy> library is missing on your system."
          "\nTry: \n   C:\\pip install numpy on a window command prompt.")

from libc.math cimport cos, sin, atan2, acos, sqrt

cdef extern from '../Source/vector.c':

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

__version__ = "1.0.5"

# **************************** PYTHON INTERFACE ***************************************

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef tuple momentum_trigonometry_real(
        obj1_centre : Vector2,
        obj2_centre : Vector2,
        obj1_vector : Vector2,
        obj2_vector : Vector2,
        obj1_mass   : float,
        obj2_mass   : float
    ):
    """
    RETURN VECTORS V1 & V2 AFTER OBJECT COLLISION (TRIGONOMETRY) 
    
    This method is using trigonometric equations to determine the objects final velocities
    Refer to Two-dimensional collision with two moving objects in the following link : 
    https://en.wikipedia.org/wiki/Elastic_collision 
    
    * This method can be used to resolved 2d elastic collision in a cartesian system 
    
    * obj1_vector & obj2_vector are un-normalized vectors in order to keep the total kinetic 
      energy and to redistribute the force to the final velocities (v1 & v2) 
      
    :param obj1_centre: Vector2; Centre of object 1. This vector is not normalized and the components x, y 
    correspond to the object position on the screen    
    :param obj2_centre: Vector2; Centre of object 2. This vector is not normalized and the components x, y 
    correspond to the object position on the screen 
    :param obj1_vector: Vector2; Object 1 direction vector, un-normalized 2d Vector
    If both vector direction are normalized the output will also be normalized.
    :param obj2_vector: Vector2; Object 2 direction vector, un-normalized 2d Vector
    If both vector direction are normalized the output will also be normalized. 
    :param obj1_mass: float; Mass of object 1 in kg 
    :param obj2_mass: float; Mass of object 2 in kg
    :return: Tuple containing v1 and v2 (object vectors after collision).
    """
    cdef:
        vector2d vec1, vec2
        v_struct collision
        float v1_x, v1_y, v2_x, v2_y
        float c1_x, c1_y, c2_x, c2_y

    v1_x, v1_y, v2_x, v2_y = obj1_vector.x, obj1_vector.y, obj2_vector.x, obj2_vector.y
    c1_x, c1_y, c2_x, c2_y = obj1_centre.x, obj1_centre.y, obj2_centre.x, obj2_centre.y

    with nogil:
        vecinit(&vec1, v1_x, v1_y)
        vecinit(&vec2, v2_x, v2_y)
        # DETERMINES V1 & V2 COMPONENTS AFTER COLLISION
        collision = \
            get_momentum_trigonometry_vecR(
                c1_x, c1_y, c2_x, c2_y,
                vec1, vec2, obj1_mass, obj2_mass)

    return Vector2(collision.vector1.x, collision.vector1.y), \
           Vector2(collision.vector2.x, collision.vector2.y)


# **************************** ANGLE FREE **********************************************************

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef tuple momentum_angle_free_real(
    obj1_vector  : Vector2,
    obj2_vector  : Vector2,
    obj1_mass    : float,
    obj2_mass    : float,
    obj1_centre  : Vector2,
    obj2_centre  : Vector2,
    ):
    """
    RETURN VECTORS V1 & V2 AFTER OBJECT COLLISION (ANGLE FREE METHOD)
    
    This method is using angle free equations to determine the objects final velocities
    Refer to Two-dimensional collision with two moving objects in the following link : 
    https://en.wikipedia.org/wiki/Elastic_collision 
    
    * This method can be used to resolved 2d elastic collision in cartesian system coordinates
    
    * obj1_vector & obj2_vector are un-normalized vectors in order to keep the total kinetic 
      energy and to redistribute the force to the final velocities (v1 & v2) 
    
    :param obj1_centre: Vector2; Centre of object 1. This vector is not normalized and the components x, y 
    correspond to the object position on the screen    
    :param obj2_centre: Vector2; Centre of object 2. This vector is not normalized and the components x, y 
    correspond to the object position on the screen 
    :param obj1_vector: Vector2; Object 1 direction vector, un-normalized 2d Vector
    If both vector direction are normalized the output will also be normalized.
    :param obj2_vector: Vector2; Object 2 direction vector un-normalized 2d Vector
    If both vector direction are normalized the output will also be normalized. 
    :param obj1_mass: float; Mass of object 1 in kg 
    :param obj2_mass: float; Mass of object 2 in kg
    :return: Tuple containing v1 and v2 (object vectors after collision).
    """

    cdef:
        vector2d vec1, vec2, x1_vec, x2_vec
        float v1_x, v1_y, v2_x, v2_y
        float c1_x, c1_y, c2_x, c2_y
        v_struct v

    v1_x, v1_y, v2_x, v2_y = obj1_vector.x, obj1_vector.y, obj2_vector.x, obj2_vector.y
    c1_x, c1_y, c2_x, c2_y = obj1_centre.x, obj1_centre.y, obj2_centre.x, obj2_centre.y

    with nogil:
        vecinit(&vec1, v1_x, v1_y)
        vecinit(&vec2, v2_x, v2_y)
        vecinit(&x1_vec, c1_x, c1_y)
        vecinit(&x2_vec, c2_x, c2_y)

        v = get_angle_free_vecR(vec1, vec2, obj1_mass, obj2_mass, x1_vec, x2_vec)

    return Vector2(v.vector1.x, v.vector1.y), \
           Vector2(v.vector2.x, v.vector2.y)

# ***************************END INTERFACE *************************************



# *************************** CYTHON INTERFACE *********************************

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef v_struct get_momentum_trigonometry_vecR(
        float obj1_cx, float obj1_cy,
        float obj2_cx, float obj2_cy,
        vector2d obj1_vec, vector2d obj2_vec,
        float obj1_mass, float obj2_mass
)nogil:
    """
    RETURN VECTORS V1 & V2 OF ORIGINAL OBJECTS AFTER 
    COLLISION (TRIGONOMETRY)
    
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

    cdef:
        float phi    = get_contact_angle(obj1_cx, obj1_cy, obj2_cx, obj2_cy)
        float theta1 = get_theta_angle(obj1_vec)
        float theta2 = get_theta_angle(obj2_vec)
        float v1_length, v2_length
        vector2d v1
        vector2d v2
        v_struct collision

    v1_length         = vlength(&obj1_vec)
    v2_length         = vlength(&obj2_vec)

    v1 = get_v1R(v1_length, v2_length, theta1, theta2, phi, obj1_mass, obj2_mass)
    v2 = get_v2R(v1_length, v2_length, theta1, theta2, phi, obj1_mass, obj2_mass)

    collision.vector1 = v1
    collision.vector2 = v2

    return collision


cdef vector2d get_v1R(
        float v1_, float v2_,
        float theta1_, float theta2_,
        float phi_,
        float m1_, float m2_
)nogil:
    """
    RETURN SCALAR SIZE V1 OF THE ORIGINAL OBJECT 
    REPRESENTED BY (V1, THETA1, M1) TRIGONOMETRY
 
    Where v1_ and v2_ are the scalar sizes of the two original speeds of the objects, m1_ and m2_
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
    cdef:
        float numerator, v1x, v1y
        float r1, r2
        float m12 = m1_ + m2_
        vector2d v1_vec

    if v1_ <=0.0 or v2_ <=0.0:
        with gil:
            raise ValueError(
                '\n|v1_|, |v2_| magnitude must be >= 0.0'
                '\n|v1|=%s |v2|=%s ' % (v1_, v2_))
    if m12 <= 0.0:
        with gil:
            raise ValueError("Object's mass should be > 0.0")

    r1 = theta1_ - phi_
    r2 = phi_ + <float>M_PI2
    numerator = v1_ * <float>cos(r1) * (m1_ - m2_) + <float>(2 * m2_) * v2_ * <float>cos(theta2_ - phi_)
    v1x = numerator * <float>cos(phi_) / m12 + v1_ * <float>sin(r1) * <float>cos(r2)
    v1y = numerator * <float>sin(phi_) / m12 + v1_ * <float>sin(r1) * <float>sin(r2)

    vecinit(&v1_vec, v1x, v1y)
    return v1_vec


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef vector2d get_v2R(
        float v1_, float v2_,
        float theta1_, float theta2_,
        float phi_,
        float m1_, float m2_
)nogil:
    """
    RETURN SCALAR SIZE V2_ OF THE ORIGINAL OBJECT 
    REPRESENTED BY (V2_, THETA2_, M2_) TRIGONOMETRY

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

    r1 = (theta2_ - phi_)
    r2 = phi_ + <float>M_PI2

    if v1_ <=0.0 or v2_ <=0.0:
        with gil:
            raise ValueError(
                "\n|v1_|, |v2_| magnitude must be >= 0.0\n"
                "|v1|=%s |v2|=%s " % (v1_, v2_))
    if m21 <= 0.0:
        with gil:
            raise ValueError("Object's mass should be > 0.0")

    numerator = v2_ * <float>cos(r1) * <float>(m2_ - m1_) + <float>(2 * m1_) * v1_ * <float>cos(theta1_ - phi_)
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
        vector2d v1, vector2d v2,
        float m1, float m2,
        vector2d x1, vector2d x2
)nogil:
    """
    SCALAR SIZE V1_ OF THE ORIGINAL OBJECT SPEED REPRESENTED 
    BY (V1_, M1_, X1 ARGUMENTS).

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
        with gil:
            raise ValueError("\n|v1|, |v2| magnitude must be >= 0.0\n"
                  "|v1|=%s |v2|=%s " % (vlength(&v1), vlength(&v2)))
    if m12 <= 0.0:
        with gil:
            raise ValueError("Object's mass should be > 0.0")

    cdef float mass = <float>(2.0 * m2) / m12   # mass coefficient in the equation
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
    scale_inplace(<float>(mass * d) / <float>(x12_length * x12_length), &x12)
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
        vector2d v1, vector2d v2,
        float m1, float m2,
        vector2d x1, vector2d x2
)nogil:
    """
    SCALAR SIZE V2_ OF THE ORIGINAL OBJECT SPEED REPRESENTED 
    BY (V2_, M2_, X2 ARGUMENTS).

    :param v1: vector2d, object1 vector_
    :param v2: vector2d, object2 vector_
    :param m1: float; object1 mass_ in kilograms, must be > 0
    :param m2: float; object2 mass_ in kilograms, must be > 0
    :param x1: vector2d, object1 centre_
    :param x2: vector2d, object2 centre_
    :return: pygame.math.Vector2, resultant vector_ for object1
    """
    cdef float m12 = (m1 + m2)

    # AT LEAST ONE OBJECT MUST BE IN MOTION
    if vlength(&v1) <=0.0 or vlength(&v2) <= 0.0:
        with gil:
            raise ValueError("\n|v1|, |v2| magnitude must be >= 0.0"
                  "\n|v1|=%s |v2|=%s " % (vlength(&v1), vlength(&v2)))
    if m12 <= 0.0:
        with gil:
            raise ValueError("Object's mass should be > 0.0")

    cdef float mass = <float>(2.0 * m1) / m12   # mass coefficient in the equation
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
    scale_inplace(<float>(mass * d) / <float>(x21_length * x21_length), &x21)
    return subcomponents(v2, x21)


# ************************************************************************
# Angle free calculation, return V1 and V2
# ************************************************************************
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef v_struct get_angle_free_vecR(
        vector2d v1, vector2d v2,
        float m1, float m2,
        vector2d x1, vector2d x2
)nogil:
    """
    RETURN BOTH FINAL VELOCITIES VECTORS V1 & V2 
    
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
    cdef v_struct collision
    collision.vector1 = v11
    collision.vector2 = v22
    return collision


# # ***************************************************************************************************

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef float vector_length(float x, float y)nogil:
    """
    CALCULATE A VECTOR LENGTH GIVEN ITS COMPONENTS (SCALAR VALUES)

    :param x: float; x coordinate
    :param y: float; y coordinate
    :return: float; vector length  
    """
    return <float>sqrt(x * x + y * y)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef float get_contact_angle(
        float v1x, float v1y,
        float v2x, float v2y
)nogil:
    """
    RETURN THE CONTACT ANGLE Φ [0, -2Π] IN RADIANS BETWEEN OBJ1 AND 
    OBJ2 OR [0 ... -360 degrees].

    The distance dx & dy between both objects is determine by 
    dx = v2x - v1x & dy = v2y - v1y. 
    
    * Angle φ between the two objects at the point of collision
      This function returns the angle φ at the time of the contact.
        
    * atan2(y, x) returns value of atan(y/x) in radians. The atan2() method returns
      a numeric value between –pi and pi representing the angle theta of a (x, y) 
      point and positive x-axis.   
    
    :param v1x : object 1 centre value (x component) at time of contact.
    :param v1y : object 1 centre value (y component) at time of contact.
    :param v2x : object 2 centre value (x component) at time of contact.
    :param v2y : object 2 centre value (y component) at time of contact. 
    :return    : float; contact angle in radians [0, -2π]
    :rtype     : float (angle φ radians)
    """
    cdef:
        float dx, dy
        float phi

    dx = v2x - v1x
    dy = v2y - v1y

    phi = <float> atan2(dy, dx)
    if phi > 0.0:
        phi -= <float>(2.0 * M_PI)
    # phi *= -1.0
    return <float> phi

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef float get_theta_angle(vector2d vector_)nogil:
    """
    RETURN THETA ANGLE Θ IN RADIANS [Π, -Π]

    Angle theta at point of collision.
    
    * vector_ correspond to the initial angle for an object, similar 
      to the object direction at time of contact. The vector must be normalized range [-1.0 ... 1.0] 
      vector_ contains the vector components (x, y) describing the object velocity and direction 
      (angle) at time of contact.  
      when the vector component (vector_.y) is > 0, the acos value is in range [0 ... pi]
      When the vector component (vector_.y) is < 0, the acos value is multiply by -1 to 
      get an angle in range [0 ... -pi]
      
    * acos (angle domain) is be definition in range y [0 ... +pi] and x values [-1 ... +1] 
      y [0 ... 180] degrees

    :param vector_: vector2d
    :return       : float (angle Θ in radians)
    """
    cdef:
        float theta
        float vl = vlength(&vector_)

    if vl != <float>0.0:
        theta = <float> acos(vector_.x / vl)
    else:
        # AT CONTACT TIME, OBJECT SHOULD BE MOVING.
        # IDEALLY PROGRAM SHOULD RAISE AN ERROR MSG.
        return <float>0.0
    if vector_.y < 0.0:
        theta *= -<float>1.0

    theta = <float> min(theta, M_PI)
    theta = <float> max(theta, -M_PI)
    return <float> theta