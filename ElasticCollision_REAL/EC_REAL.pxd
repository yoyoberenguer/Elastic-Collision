###cython: boundscheck=False, wraparound=False, nonecheck=False, cdivision=True, optimize.use_switch=True
# encoding: utf-8

# gcc -O3 -o elastic_collision elastic_collision.c

cdef extern from 'vector.c':

    struct vector2d:
       float x
       float y

    struct v_struct:
        vector2d vector1
        vector2d vector2

# # ----------------------- TRIGONOMETRY ----------------------------------------------------

cdef vector2d get_v2R(
        float v1_, float v2_, float theta1_,
        float theta2_, float phi_, float m1_, float m2_)nogil

cdef vector2d get_v1R(
        float v1_, float v2_, float theta1_,
        float theta2_, float phi_, float m1_, float m2_)nogil

cdef v_struct get_momentum_trigonometry_vecR(
        float obj1_cx, float obj1_cy, float obj2_cx, float obj2_cy,
        vector2d obj1_vec, vector2d obj2_vec,
        float obj1_mass, float obj2_mass)nogil

# ****************************** ANGLE FREE METHOD *******************************************
# ******************************                   *******************************************
# ******************************                   *******************************************
# ******************************                   *******************************************

cdef vector2d get_v1_angle_free_vecR(
        vector2d v1, vector2d v2, float m1, float m2, vector2d x1, vector2d x2)nogil

cdef vector2d get_v2_angle_free_vecR(
        vector2d v1, vector2d v2, float m1, float m2, vector2d x1, vector2d x2)nogil

cdef v_struct get_angle_free_vecR(
        vector2d v1, vector2d v2, float m1, float m2, vector2d x1, vector2d x2)nogil


# ***************************************************************************************************

