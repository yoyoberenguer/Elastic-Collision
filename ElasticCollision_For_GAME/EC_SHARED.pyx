###cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True, optimize.use_switch=True
# encoding: utf-8

import cython

try:
    import pygame
    from pygame import Vector2
    from pygame import Rect
except ImportError:
    print('\nOn window, try:\nC:\>pip install pygame')
    raise SystemExit


try:
    from cpython.dict cimport PyDict_DelItem, PyDict_Clear, PyDict_GetItem, PyDict_SetItem, \
        PyDict_Values, PyDict_Keys, PyDict_Items, PyDict_SetItemString
    from cpython cimport PyObject, PyObject_HasAttr, PyObject_IsInstance
    from cpython.list cimport PyList_Append, PyList_GetItem, PyList_Size
except ImportError:
    raise ImportError("\n<cython> library is missing on your system."
          "\nTry: \n   C:\\pip install cython on a window command prompt.")


from libc.math cimport sqrt, atan2, acos, cos, sin
from libc.stdio cimport printf

cdef extern from 'vector.c':

    struct vector2d:
       float x
       float y

    struct rect_p:
        int x
        int y

    struct v_struct:
        vector2d vector1
        vector2d vector2

    cdef float RAD_TO_DEG
    cdef float DEG_TO_RAD
    void vecinit(vector2d *v, float x, float y)nogil
    float vlength(vector2d *v)nogil
    void mulv_inplace(vector2d *v1, vector2d v2)nogil
    void scale_inplace(float c, vector2d *v)nogil
    vector2d addcomponents(vector2d v1, vector2d v2)nogil
    vector2d subcomponents(vector2d v1, vector2d v2)nogil
    vector2d scalevector2d(float c, vector2d *v)nogil
    void scale_inplace(float c, vector2d *v)nogil
    float distance_to(vector2d v1, vector2d v2)nogil
    float dot(vector2d *v1, vector2d *v2)nogil


DEF M_PI  = 3.14159265358979323846
DEF M_PI2 = 3.14159265358979323846 / 2.0



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
    return sqrt(x * x + y * y)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef float get_contact_angle(float v1x, float v1y, float v2x, float v2y)nogil:
        """
        RETURN THE CONTACT ANGLE Φ [Π, -Π] IN RADIANS BETWEEN OBJ1 AND OBJ2.
        
        Angle phi between the two objects at the point of collision
        This function returns the angle Phi at the time of the contact.
        v1x and v1y are object 1 centre values at time of contact.
        v2x and v2y are object 2 centre values at time of contact. 
        
        :return   : contact angle in radians [π, -π]
        :rtype    : float (angle φ radians)
        """
        cdef:
            float dx, dy
            float phi

        dx = v2x - v1x
        dy = v2y - v1y

        phi = <float>atan2(dy, dx)
        if phi > 0.0:
            phi -= 2.0 * M_PI
        # phi *= -1.0
        return <float>phi


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef float get_theta_angle(vector2d vector_)nogil:
    """
    RETURN THETA ANGLE Θ IN RADIANS [Π, -Π]

    Angle theta at point of collision.
    vector_ correspond to the initial angle for an object, similar 
    to the object direction at time of contact.
    vector_ contains the vector components describing the object velocity 
    and direction (angle) at time of contact.
 
    :param vector_: vector2d
    :return       : float (angle Θ in radians)
    """
    cdef:
        float theta
        float vl = vlength(&vector_)

    if vl!=0.0:
        theta = <float>acos(vector_.x / vl)
    else:
        # AT CONTACT TIME, OBJECT SHOULD BE MOVING.
        # IDEALLY PROGRAM SHOULD RAISE AN ERROR MSG.
        return 0.0
    if vector_.y < 0.0:
        theta *= -1.0
    return <float>theta