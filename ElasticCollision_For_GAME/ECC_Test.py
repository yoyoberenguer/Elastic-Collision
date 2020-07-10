# IMPORT CYTHON VERSION
from ECC import momentum_angle_free_c, momentum_angle_free_cR, momentum_trigonometry_c, momentum_trigonometry_cR

import pygame
from pygame.math import Vector2

if __name__ == '__main__':

    import timeit

    v1 = Vector2(0.707, 0.707)
    x1 = Vector2(0.0, 0.0)
    v2 = Vector2(-0.707, -0.707)
    x2 = Vector2(1.4142, 1.4142)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    invert = False
    pyobject = momentum_angle_free_c(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert)
    print("\nANGLE FREE C - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nANGLE FREE C - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(-0.707, 0.707)
    x1 = Vector2(1.4142, 0.0)
    v2 = Vector2(0.707, -0.707)
    x2 = Vector2(0, 1.4142)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    pyobject = momentum_angle_free_c(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert)
    print("\nANGLE FREE C - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nANGLE FREE C - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(-0.707, -0.707)
    x1 = Vector2(1.4142, 1.4142)
    v2 = Vector2(0.707, 0.707)
    x2 = Vector2(0, 0)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    pyobject = momentum_angle_free_c(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert)
    print("\nANGLE FREE C - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nANGLE FREE C - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(0.707, -0.707)
    x1 = Vector2(0, 1.4142)
    v2 = Vector2(-0.707, 0.707)
    x2 = Vector2(1.4142, 0)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    pyobject = momentum_angle_free_c(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert)
    print("\nANGLE FREE C - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nANGLE FREE C - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    print("\nANGLE FREE : ", timeit.timeit("momentum_angle_free_c(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y)",
                                           "from __main__ import momentum_angle_free_c, v1x, "
                                           "v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y", number=1000000))

    # ----------------------------------------------------------------------------------------------
    v1 = Vector2(0.707, -0.707)
    x1 = Vector2(0.0, 0.0)
    v2 = Vector2(-0.707, 0.707)
    x2 = Vector2(1.4142, -1.4142)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    invert = False
    pyobject = momentum_angle_free_cR(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert)
    print("\nANGLE FREE C REAL - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nANGLE FREE C REAL - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(-0.707, -0.707)
    x1 = Vector2(1.4142, 0.0)
    v2 = Vector2(0.707, 0.707)
    x2 = Vector2(0, -1.4142)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    invert = False
    pyobject = momentum_angle_free_cR(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert)
    print("\nANGLE FREE C REAL - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nANGLE FREE C REAL - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(-0.707, 0.707)
    x1 = Vector2(1.4142, -1.4142)
    v2 = Vector2(0.707, -0.707)
    x2 = Vector2(0, 0)

    m1 = 1.0
    m2 = 1.0

    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y

    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    invert = False
    pyobject = momentum_angle_free_cR(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert)
    print("\nANGLE FREE C REAL - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nANGLE FREE C REAL - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(0.707, 0.707)
    x1 = Vector2(0.0, -1.4142)
    v2 = Vector2(-0.707, -0.707)
    x2 = Vector2(1.4142, 0)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    invert = False
    pyobject = momentum_angle_free_cR(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert)
    print("\nANGLE FREE C REAL - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nANGLE FREE C REAL - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    print("\nANGLE FREE C REAL : ",
          timeit.timeit("momentum_angle_free_cR(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert)",
                        "from __main__ import momentum_angle_free_cR, v1x, "
                        "v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert", number=1000000))
# # ----------------------------------------------------------------------------------------------------------------


    import timeit

    v1 = Vector2(0.707, 0.707)
    x1 = Vector2(0.0, 0.0)
    v2 = Vector2(-0.707, -0.707)
    x2 = Vector2(1.4142, 1.4142)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    invert = False
    pyobject = momentum_trigonometry_c(v1x, v1y, m1, x1x, x1y, v2x, v2y, m2, x2x, x2y, invert)
    print("\nTRIGO C - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nTRIGO C - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(-0.707, 0.707)
    x1 = Vector2(1.4142, 0.0)
    v2 = Vector2(0.707, -0.707)
    x2 = Vector2(0, 1.4142)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    pyobject = momentum_trigonometry_c(v1x, v1y, m1, x1x, x1y, v2x, v2y, m2, x2x, x2y, invert)
    print("\nTRIGO C - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nTRIGO C - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(-0.707, -0.707)
    x1 = Vector2(1.4142, 1.4142)
    v2 = Vector2(0.707, 0.707)
    x2 = Vector2(0, 0)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    pyobject = momentum_trigonometry_c(v1x, v1y, m1, x1x, x1y, v2x, v2y, m2, x2x, x2y, invert)
    print("\nTRIGO C - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nTRIGO C - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(0.707, -0.707)
    x1 = Vector2(0, 1.4142)
    v2 = Vector2(-0.707, 0.707)
    x2 = Vector2(1.4142, 0)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    pyobject = momentum_trigonometry_c(v1x, v1y, m1, x1x, x1y, v2x, v2y, m2, x2x, x2y, invert)
    print("\nTRIGO C - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nTRIGO C - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    print("\nTRIGO C : ", timeit.timeit("momentum_angle_free_c(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y)",
                                           "from __main__ import momentum_angle_free_c, v1x, "
                                           "v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y", number=1000000))

    # ----------------------------------------------------------------------------------------------
    v1 = Vector2(0.707, -0.707)
    x1 = Vector2(0.0, 0.0)
    v2 = Vector2(-0.707, 0.707)
    x2 = Vector2(1.4142, -1.4142)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    invert = False
    pyobject = momentum_trigonometry_cR(v1x, v1y, m1, x1x, x1y, v2x, v2y, m2, x2x, x2y, invert)
    print("\nTRIGO C REAL - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nTRIGO C REAL - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(-0.707, -0.707)
    x1 = Vector2(1.4142, 0.0)
    v2 = Vector2(0.707, 0.707)
    x2 = Vector2(0, -1.4142)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    invert = False
    pyobject = momentum_trigonometry_cR(v1x, v1y, m1, x1x, x1y, v2x, v2y, m2, x2x, x2y, invert)
    print("\nTRIGO C REAL - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nTRIGO C REAL - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(-0.707, 0.707)
    x1 = Vector2(1.4142, -1.4142)
    v2 = Vector2(0.707, -0.707)
    x2 = Vector2(0, 0)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    invert = False
    pyobject = momentum_trigonometry_cR(v1x, v1y, m1, x1x, x1y, v2x, v2y, m2, x2x, x2y, invert)
    print("\nTRIGO C REAL - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nTRIGO C REAL - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))

    v1 = Vector2(0.707, 0.707)
    x1 = Vector2(0.0, -1.4142)
    v2 = Vector2(-0.707, -0.707)
    x2 = Vector2(1.4142, 0)
    m1 = 1.0
    m2 = 1.0
    x1x = x1.x
    x1y = x1.y
    x2x = x2.x
    x2y = x2.y
    v1x = v1.x
    v1y = v1.y
    v2x = v2.x
    v2y = v2.y
    invert = False
    pyobject = momentum_trigonometry_cR(v1x, v1y, m1, x1x, x1y, v2x, v2y, m2, x2x, x2y, invert)
    print("\nTRIGO C REAL - object1 vector : (x:%s y:%s) ", (pyobject['v12']['x'], pyobject['v12']['y']))
    print("\nTRIGO C REAL - object2 vector : (x:%s y:%s) ", (pyobject['v21']['x'], pyobject['v21']['y']))
    print("\nTRIGO C REAL : ",
          timeit.timeit("momentum_trigonometry_cR(v1x, v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert)",
                        "from __main__ import momentum_trigonometry_cR, v1x, "
                        "v1y, v2x, v2y, m1, m2, x1x, x1y, x2x, x2y, invert", number=1000000))

