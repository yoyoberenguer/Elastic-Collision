###cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True, optimize.use_switch=True
# encoding: utf-8

cdef extern from 'vector.c':

    struct vector2d:
       float x
       float y

cdef float vector_length(float x, float y)nogil

cdef float get_contact_angle(float v1x, float v1y, float v2x, float v2y)nogil

cdef float get_theta_angle(vector2d vector_)nogil
