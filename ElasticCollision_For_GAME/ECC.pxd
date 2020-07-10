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

cdef extern from 'elastic_collision.c':

    struct vector2d:
        float x
        float y

    struct collider_object:
        vector2d vector;
        float mass;
        vector2d centre;

    struct collision_vectors:
        vector2d v12;
        vector2d v21;

    struct v_struct:
        vector2d vector1
        vector2d vector2

    # --------------------------TRIGONOMETRY VERSION --------------------------------------

    void vecinit(vector2d *v, float x, float y)nogil
    float contact_angle(vector2d object1, vector2d object2)nogil;
    float theta_angle(vector2d vector)nogil;
    # determine object 1 vector direction and velocity after contact.
    vector2d v12_vector_components(float v1, float v2,
                                   float theta1, float theta2, float phi, float m1, float m2)nogil;

    # determine object 2 vector direction and velocity after contact.
    vector2d v21_vector_components(
            float v1, float v2, float theta1, float theta2, float phi, float m1, float m2)nogil;

    # determine object 1 and object 2 directions and velocities after contact.
    collision_vectors momentum_t(collider_object obj1, collider_object obj2)nogil;

    # --------------------------ANGLE FREE VERSION --------------------------------------

    # Determine object1 vector direction and velocity after impact.
    vector2d v1_vector_components(vector2d v1, vector2d v2, float m1, float m2,
                         vector2d x1, vector2d x2)nogil;

    # Determine object2 vector direction and velocity after impact.
    vector2d v2_vector_components(vector2d v1, vector2d v2, float m1, float m2,
                                    vector2d x1, vector2d x2)nogil;

    # Determine object1 & object2 directions and velocities after collision.
    collision_vectors momentum_angle_free(
            float v1_x, float v1_y, float v2_x, float v2_y,
            float  m1, float  m2, float  x1_x, float  x1_y, float  x2_x, float  x2_y)nogil;


    # Equivalent to momentum_angle_free method (using structural objects)
    collision_vectors momentum_angle_free1(
            collider_object obj1, collider_object obj2)nogil;


