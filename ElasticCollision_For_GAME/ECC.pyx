###cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True, optimize.use_switch=True
# encoding: utf-8

from ECC cimport momentum_angle_free, momentum_t
import cython


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef collision_vectors momentum_angle_free_c(float v1_x, float v1_y, float v2_x, float v2_y,
                            float m1, float m2, float x1_x, float x1_y, float x2_x,
                                              float x2_y, bint invert=False)nogil:
    """
    
    :param v1_x: float; Object1 vector x components 
    :param v1_y: float; Object1 vector y components 
    :param v2_x: float; Object2 vector x components 
    :param v2_y: float; Object2 vector y components 
    :param m1: float; object1 mass
    :param m2: float; object2 mass
    :param x1_x: float; object 1 center x coordinate
    :param x1_y: float; object 1 center y coordinate
    :param x2_x: float; object 2 center x coordinate
    :param x2_y: float; object 2 center y coordinate 
    :param invert: boolean; 
    :return: 
    """
    if invert:
        v1_y *=-1
        v2_y *=-1
    cdef collision_vectors v = \
        momentum_angle_free(v1_x, v1_y, v2_x, v2_y, m1, m2, x1_x, x1_y, x2_x, x2_y)

    return v


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef collision_vectors momentum_angle_free_cR(float v1_x, float v1_y, float v2_x, float v2_y,
                            float m1, float m2, float x1_x, float x1_y, float x2_x,
                                              float x2_y, bint invert=False)nogil:
    """
    
    :param v1_x: float; Object1 vector x components 
    :param v1_y: float; Object1 vector y components 
    :param v2_x: float; Object2 vector x components 
    :param v2_y: float; Object2 vector y components 
    :param m1: float; object1 mass
    :param m2: float; object2 mass
    :param x1_x: float; object 1 center x coordinate
    :param x1_y: float; object 1 center y coordinate
    :param x2_x: float; object 2 center x coordinate
    :param x2_y: float; object 2 center y coordinate 
    :param invert: boolean; 
    :return: 
    """
    if invert:
        v1_y *=-1
        v2_y *=-1
    cdef collision_vectors v = \
        momentum_angle_free(v1_x, v1_y, v2_x, v2_y, m1, m2, x1_x, x1_y, x2_x, x2_y)

    return v


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef collision_vectors momentum_trigonometry_c(
        float v1x, float v1y, float m1, float x1x, float x1y, float v2x, float v2y,
        float m2, float x2x, float x2y, bint invert=False)nogil:
    """
    
    :param v1_x: float; Object1 vector x components 
    :param v1_y: float; Object1 vector y components 
    :param v2_x: float; Object2 vector x components 
    :param v2_y: float; Object2 vector y components 
    :param m1: float; object1 mass
    :param m2: float; object2 mass
    :param x1_x: float; object 1 center x coordinate
    :param x1_y: float; object 1 center y coordinate
    :param x2_x: float; object 2 center x coordinate
    :param x2_y: float; object 2 center y coordinate 
    :param invert: boolean; 
    :return: 
    """

    if invert:
        v1y *= -1
        v2y *= -1
    cdef collider_object obj1_c, obj2_c
    cdef collision_vectors obj_c
    cdef vector2d v1, v2, x1, x2
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

    obj_c = momentum_t(obj1_c, obj2_c)
    vecinit(&obj_c.v12, obj_c.v12.x, obj_c.v12.y)
    vecinit(&obj_c.v21, obj_c.v21.x, obj_c.v21.y)

    return obj_c



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef collision_vectors momentum_trigonometry_cR(
        float v1x, float v1y, float m1, float x1x, float x1y, float v2x, float v2y,
        float m2, float x2x, float x2y, bint invert=False)nogil:
    """
    
    :param v1_x: float; Object1 vector x components 
    :param v1_y: float; Object1 vector y components 
    :param v2_x: float; Object2 vector x components 
    :param v2_y: float; Object2 vector y components 
    :param m1: float; object1 mass
    :param m2: float; object2 mass
    :param x1_x: float; object 1 center x coordinate
    :param x1_y: float; object 1 center y coordinate
    :param x2_x: float; object 2 center x coordinate
    :param x2_y: float; object 2 center y coordinate 
    :param invert: boolean; 
    :return: 
    """

    if invert:
        v1y *= -1
        v2y *= -1
    cdef collider_object obj1_c, obj2_c
    cdef collision_vectors obj_c
    cdef vector2d v1, v2, x1, x2
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

    obj_c = momentum_t(obj1_c, obj2_c)
    vecinit(&obj_c.v12, obj_c.v12.x, obj_c.v12.y)
    vecinit(&obj_c.v21, obj_c.v21.x, obj_c.v21.y)

    return obj_c