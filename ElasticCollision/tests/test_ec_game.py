""""
TEST LIBRARY C_GAME, EC_GAME
"""

import unittest
import math

try:
    import pygame

except ImportError:
    raise ImportError("\n<pygame> library is missing on your system."
                      "\nTry: \n   C:\\pip install pygame on a window command prompt.")

from pygame.math import Vector2

from ElasticCollision.c_game import momentum_angle_free_c, momentum_trigonometry_c
from ElasticCollision.ec_game import momentum_trigonometry, momentum_angle_free, get_momentum_trigonometry_v1v2, \
     get_v11, get_v12, get_v1_angle_free_v1, get_v2_angle_free_v2, get_angle_free_v1v2, \
     get_theta_angle_, get_contact_angle_


class TestMomentumTrigonometry(unittest.TestCase):
    """
    Test Momentum Trigonometry momentum_trigonometry
    """

    def runTest(self) -> None:
        """

        :return:  void
        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0
        v11, v12 = momentum_trigonometry(centre1, centre2, vector1, vector2, mass1, mass2, False)
        self.assertIsInstance(v11, Vector2)
        self.assertIsInstance(v12, Vector2)
        self.assertTrue(hasattr(v11, 'x'))
        self.assertTrue(hasattr(v11, 'y'))
        self.assertTrue(hasattr(v12, 'x'))
        self.assertTrue(hasattr(v12, 'y'))
        self.assertIsInstance(v11.x, float)
        self.assertIsInstance(v11.y, float)
        self.assertIsInstance(v12.x, float)
        self.assertIsInstance(v12.y, float)
        print("Momentum trigonometry - object1 vector : (x:%s y:%s) ", (v11.x, v11.y))
        print("Momentum trigonometry - object2 vector : (x:%s y:%s) ", (v12.x , v12.y))
        self.assertAlmostEqual(round(v11.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v11.y, 3), -round(math.sin(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.y, 3), round(math.sin(math.pi / 4.0), 3))

        # Invert is True both object are not colliding (object with opposite direction)
        v11, v12 = momentum_trigonometry(centre1, centre2, vector1, vector2, mass1, mass2, invert=True)

        self.assertAlmostEqual(round(v11.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v11.y, 3), round(math.sin(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.y, 3), -round(math.sin(math.pi / 4.0), 3))

        # Verification with angle free method
        v11, v12 = momentum_trigonometry(centre1, centre2, vector1, vector2, mass1, mass2)
        v11_, v12_ = momentum_angle_free(vector1, vector2, mass1, mass2, centre1, centre2)
        self.assertAlmostEqual(round(v11.x, 5), round(v11_.x, 5), places=4)
        self.assertAlmostEqual(round(v11.y, 5), round(v11_.y, 5), places=4)
        self.assertAlmostEqual(round(v12.x, 5), round(v12_.x, 5), places=4)
        self.assertAlmostEqual(round(v12.y, 5), round(v12_.y, 5), places=4)

        # horizontal object 2 on the right of object 1
        vector1 = Vector2(0.707, 0)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, 0)
        centre2 = Vector2(1.4142, 0)
        mass1 = 1.0
        mass2 = 1.0
        v11, v12 = momentum_trigonometry(centre1, centre2, vector1, vector2, mass1, mass2, invert=False)
        self.assertTrue(round(v11.x, 3) == -0.707)
        self.assertTrue(round(v11.y, 3) == 0.000)
        self.assertTrue(round(v12.x, 3) == 0.707)
        self.assertTrue(round(v12.y, 3) == 0.000)

        # vertical object 2 below object 1
        vector1 = Vector2(0.0, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(0, -0.707)
        centre2 = Vector2(0, 1.4142)
        mass1 = 1.0
        mass2 = 1.0
        v11, v12 = momentum_trigonometry(centre1, centre2, vector1, vector2, mass1, mass2, invert=False)
        self.assertTrue(round(v11.x, 3) == 0.000)
        self.assertTrue(round(v11.y, 3) == -0.707)
        self.assertTrue(round(v12.x, 3) == 0.000)
        self.assertTrue(round(v12.y, 3) == 0.707)

        # object 2 on the left of object 1
        vector1 = Vector2(-0.707, 0)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(0.707, 0)
        centre2 = Vector2(-1.4142, 0)
        mass1 = 1.0
        mass2 = 1.0
        v11, v12 = momentum_trigonometry(centre1, centre2, vector1, vector2, mass1, mass2, invert=False)
        self.assertTrue(round(v11.x, 3) == 0.707)
        self.assertTrue(round(v11.y, 3) == 0.000)
        self.assertTrue(round(v12.x, 3) == -0.707)
        self.assertTrue(round(v12.y, 3) == 0.000)


class TestAngleFree(unittest.TestCase):
    """
    Test Momentum Angle free momentum_angle_free
    """

    def runTest(self) -> None:
        """

        :return:  void
        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0
        v11, v12 = momentum_angle_free(vector1, vector2, mass1, mass2, centre1, centre2)
        self.assertIsInstance(v11, Vector2)
        self.assertIsInstance(v12, Vector2)

        self.assertTrue(hasattr(v11, 'x'))
        self.assertTrue(hasattr(v11, 'y'))
        self.assertTrue(hasattr(v12, 'x'))
        self.assertTrue(hasattr(v12, 'y'))
        self.assertIsInstance(v11.x, float)
        self.assertIsInstance(v11.y, float)
        self.assertIsInstance(v12.x, float)
        self.assertIsInstance(v12.y, float)
        print("Momentum angle free - object1 vector : (x:%s y:%s) ", (v11.x, v11.y))
        print("Momentum angle free - object2 vector : (x:%s y:%s) ", (v12.x , v12.y))
        self.assertAlmostEqual(round(v11.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v11.y, 3), -round(math.sin(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.y, 3), round(math.sin(math.pi / 4.0), 3))

        # Invert is True both objects are not colliding (object with opposite direction)
        v11, v12 = momentum_angle_free(vector1, vector2, mass1, mass2, centre1, centre2, invert=True)

        self.assertAlmostEqual(round(v11.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v11.y, 3), round(math.sin(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.y, 3), -round(math.sin(math.pi / 4.0), 3))

        # Verification with angle free method
        v11, v12 = momentum_trigonometry(centre1, centre2, vector1, vector2, mass1, mass2)
        v11_, v12_ = momentum_angle_free(vector1, vector2, mass1, mass2, centre1, centre2)
        self.assertAlmostEqual(round(v11.x, 5), round(v11_.x, 5), places=4)
        self.assertAlmostEqual(round(v11.y, 5), round(v11_.y, 5), places=4)
        self.assertAlmostEqual(round(v12.x, 5), round(v12_.x, 5), places=4)
        self.assertAlmostEqual(round(v12.y, 5), round(v12_.y, 5), places=4)

        vector1 = Vector2(-0.707, -0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(0.707, 0.707)
        centre2 = Vector2(-1.4142, -1.4142)
        mass1 = 1.0
        mass2 = 1.0
        v11, v12 = momentum_angle_free(vector1, vector2, mass1, mass2, centre1, centre2, invert=False)
        self.assertTrue(round(v11.x, 3) == 0.707)
        self.assertTrue(round(v11.y, 3) == 0.707)
        self.assertTrue(round(v12.x, 3) == -0.707)
        self.assertTrue(round(v12.y, 3) == -0.707)

        vector1 = Vector2(-0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(0.707, -0.707)
        centre2 = Vector2(-1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0
        v11, v12 = momentum_angle_free(vector1, vector2, mass1, mass2, centre1, centre2, invert=False)
        self.assertTrue(round(v11.x, 3) == 0.707)
        self.assertTrue(round(v11.y, 3) == -0.707)
        self.assertTrue(round(v12.x, 3) == -0.707)
        self.assertTrue(round(v12.y, 3) == 0.707)


class TestGetMomentumTrigonometry_v1v2(unittest.TestCase):
    """
    Test Momentum Angle free momentum_angle_free
    """

    def runTest(self) -> None:
        """
        RETURN VECTORS V1 & V2 OF ORIGINAL OBJECTS AFTER COLLISION

        :return:  void
        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0

        v1, v2 = get_momentum_trigonometry_v1v2(
            centre1, centre2,
            vector1, vector2,
            mass1, mass2
        )
        print("Momentum Trigonometry - object1 vector : (x:%s y:%s) ", (v1.x, v1.y))
        print("Momentum Trigonometry - object2 vector : (x:%s y:%s) ", (v2.x, v2.y))
        self.assertIsInstance(v1, Vector2)
        self.assertIsInstance(v2, Vector2)

        self.assertTrue(hasattr(v1, 'x'))
        self.assertTrue(hasattr(v1, 'y'))
        self.assertTrue(hasattr(v2, 'x'))
        self.assertTrue(hasattr(v2, 'y'))
        self.assertIsInstance(v1.x, float)
        self.assertIsInstance(v1.y, float)
        self.assertIsInstance(v2.x, float)
        self.assertIsInstance(v2.y, float)
        self.assertAlmostEqual(round(v1.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v1.y, 3), round(math.sin(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v2.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v2.y, 3), -round(math.sin(math.pi / 4.0), 3))


class TestGetV1(unittest.TestCase):
    """
    Test Momentum get_v1

    cdef inline vector2d get_v1(
        float v1_, float v2_,
        float theta1_,
        float theta2_,
        float phi_,
        float m1_,
        float m2_
    )nogil:

    """

    def runTest(self) -> None:
        """
        RETURN SCALAR SIZE V1 OF THE ORIGINAL OBJECT REPRESENTED BY (V1, THETA1, M1)
        :return:  void
        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0

        v1 = get_v11(
            vector1, vector2,
            get_theta_angle_(vector1),
            get_theta_angle_(vector2),
            get_contact_angle_(centre1.x, centre1.y, centre2.x, centre2.y),
            mass1, mass2
        )
        print("Momentum Trigonometry - object 1 vector : (x:%s y:%s) ", (v1.x, v1.y))

        self.assertIsInstance(v1, Vector2)

        self.assertTrue(hasattr(v1, 'x'))
        self.assertTrue(hasattr(v1, 'y'))

        self.assertIsInstance(v1.x, float)
        self.assertIsInstance(v1.y, float)

        self.assertAlmostEqual(round(v1.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v1.y, 3), -round(math.sin(math.pi / 4.0), 3))


class TestGetV2(unittest.TestCase):
    """
    Test Momentum get_v2

    cdef inline vector2d get_v2(
        float v1_, float v2_,
        float theta1_,
        float theta2_,
        float phi_,
        float m1_,
        float m2_
    )nogil:

    """

    def runTest(self) -> None:
        """
        RETURN SCALAR SIZE V2_ OF THE ORIGINAL OBJECT REPRESENTED BY (V2_, THETA2_, M2_)

        :return:  void
        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0

        v2 = get_v12(
            vector1, vector2,
            get_theta_angle_(vector1),
            get_theta_angle_(vector2),
            get_contact_angle_(centre1.x, centre1.y, centre2.x, centre2.y),
            mass1, mass2
        )

        print("Momentum Trigonometry - object 2 vector : (x:%s y:%s) ", (v2.x, v2.y))

        self.assertIsInstance(v2, Vector2)

        self.assertTrue(hasattr(v2, 'x'))
        self.assertTrue(hasattr(v2, 'y'))

        self.assertIsInstance(v2.x, float)
        self.assertIsInstance(v2.y, float)

        self.assertAlmostEqual(round(v2.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v2.y, 3), round(math.sin(math.pi / 4.0), 3))


class TestGetV1AngleFree(unittest.TestCase):
    """
    Test get_v1_angle_free_vec

    cdef inline vector2d get_v1_angle_free_vec(
        vector2d v1,
        vector2d v2,
        float m1,
        float m2,
        vector2d x1,
        vector2d x2
    )nogil:

    """

    def runTest(self) -> None:
        """
        SCALAR SIZE V1_ OF THE ORIGINAL OBJECT SPEED REPRESENTED BY (V1_, M1_, X1 ARGUMENTS).
        :return:  void
        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0

        v1 = get_v1_angle_free_v1(vector1, vector2, mass1, mass2, centre1, centre2)
        print("Momentum angle free - object 1 vector : (x:%s y:%s) ", (v1.x, v1.y))
        self.assertIsInstance(v1, Vector2)

        self.assertTrue(hasattr(v1, 'x'))
        self.assertTrue(hasattr(v1, 'y'))

        self.assertIsInstance(v1.x, float)
        self.assertIsInstance(v1.y, float)

        self.assertAlmostEqual(round(v1.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v1.y, 3), -round(math.sin(math.pi / 4.0), 3))


class TestGetV2AngleFree(unittest.TestCase):
    """
    Test get_v2_angle_free_vec

    cdef inline vector2d get_v2_angle_free_vec(
        vector2d v1,
        vector2d v2,
        float m1,
        float m2,
        vector2d x1,
        vector2d x2
    )nogil:
    """

    def runTest(self) -> None:
        """
        scalar size v2_ of the original object speed represented by (v2_, m2_, x2 arguments).
        :return:  void
        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0

        v2 = get_v2_angle_free_v2(vector1, vector2, mass1, mass2, centre1, centre2)
        print("Momentum angle free - object 2 vector : (x:%s y:%s) ", (v2.x, v2.y))
        self.assertIsInstance(v2, Vector2)

        self.assertTrue(hasattr(v2, 'x'))
        self.assertTrue(hasattr(v2, 'y'))

        self.assertIsInstance(v2.x, float)
        self.assertIsInstance(v2.y, float)

        self.assertAlmostEqual(round(v2.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v2.y, 3), round(math.sin(math.pi / 4.0), 3))


class TestAngleFreeVec(unittest.TestCase):
    """
    Test get_angle_free_vec

    cdef inline v_struct get_angle_free_vec(
        vector2d v1,
        vector2d v2,
        float m1,
        float m2,
        vector2d x1,
        vector2d x2
    """

    def runTest(self) -> None:
        """
        RETURN V1 & V2 angle free method
        :return:  void
        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0

        v1, v2 = get_angle_free_v1v2(vector1, vector2, mass1, mass2, centre1, centre2)
        print("Momentum angle free - object 1 vector : (x:%s y:%s) ", (v1.x, v1.y))
        self.assertIsInstance(v1, Vector2)

        self.assertTrue(hasattr(v1, 'x'))
        self.assertTrue(hasattr(v1, 'y'))

        self.assertIsInstance(v1.x, float)
        self.assertIsInstance(v1.y, float)

        self.assertAlmostEqual(round(v1.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v1.y, 3), round(math.sin(math.pi / 4.0), 3))

        print("Momentum angle free - object 2 vector : (x:%s y:%s) ", (v2.x, v2.y))
        self.assertIsInstance(v2, Vector2)

        self.assertTrue(hasattr(v2, 'x'))
        self.assertTrue(hasattr(v2, 'y'))

        self.assertIsInstance(v2.x, float)
        self.assertIsInstance(v2.y, float)

        self.assertAlmostEqual(round(v2.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v2.y, 3), -round(math.sin(math.pi / 4.0), 3))


class TestThetaAngle(unittest.TestCase):
    """
    Test get_theta_angle
    """

    def runTest(self) -> None:
        """
        RETURN THETA ANGLE Θ IN RADIANS [Π, -Π]
        cdef inline float get_theta_angle(vector2d vector_)nogil

        :return:  void
        """
        v1 = Vector2(0, 0)
        self.assertIsInstance(get_theta_angle_(v1), float)

        # Object is static (no motion, the function should return 0.0 degrees)
        self.assertEqual(get_theta_angle_(v1), 0.0)

        # Theta angle must stay in range [-pi, pi]
        for r in range(361):
            angle_rad = r * math.pi / 180.0
            x = math.cos(angle_rad)
            y = math.sin(angle_rad)
            v = Vector2(x, y)
            angle_in_radian = get_theta_angle_(v)
            self.assertLess(round(angle_in_radian, 5), math.pi)
            self.assertGreater(round(angle_in_radian, 5), -math.pi)

        v1 = Vector2(0.707, 0.707)  # 45 degrees
        self.assertAlmostEqual(get_theta_angle_(v1), math.pi/4.0, places=3)
        v1 = Vector2(0.0, 1.0)  # 90 degrees
        self.assertAlmostEqual(get_theta_angle_(v1), math.pi / 2.0, places=3)
        v1 = Vector2(-0.707, 0.707)  # 135 degrees
        self.assertAlmostEqual(get_theta_angle_(v1), 3 * math.pi / 4.0, places=3)
        v1 = Vector2(-0.707, -0.707)  # -135 degrees
        self.assertAlmostEqual(get_theta_angle_(v1), -3 * math.pi / 4.0, places=3)
        v1 = Vector2(0.0, -0.707)  # -90 degrees
        self.assertAlmostEqual(get_theta_angle_(v1), -math.pi / 2.0, places=3)
        v1 = Vector2(0.707, -0.707)  # -45 degrees
        self.assertAlmostEqual(get_theta_angle_(v1), -math.pi / 4.0, places=3)
        v1 = Vector2(1.0, 0.0)  # 0 degrees
        self.assertAlmostEqual(get_theta_angle_(v1), 0, places=3)


class TestGetContactAngle(unittest.TestCase):
    """
    Test get_contact_angle
    """

    def runTest(self) -> None:
        """
        RETURN THE CONTACT ANGLE Φ [Π, -Π] IN RADIANS BETWEEN OBJ1 AND OBJ2.

        cdef inline float get_contact_angle(float v1x, float v1y, float v2x, float v2y)nogil:

        :return:  void
        """
        centre1 = Vector2(0, 0)  # centre at origin

        # Theta angle must stay in range [0...-2pi]
        # Rotating object 2 (360 degrees) around object 1 place at origin (0, 0)
        for r in range(361):
            angle_rad = r * math.pi / 180.0
            x = math.cos(angle_rad)
            y = math.sin(angle_rad)
            centre2 = Vector2(x, y)
            angle_in_radian = get_contact_angle_(centre1.x, centre1.y, centre2.x, centre2.y)

            self.assertLess(round(angle_in_radian, 3), 0.0001)
            self.assertGreater(round(angle_in_radian, 3), -2*math.pi)

        # ** Superposing object 1 and object 2 (should return 0 radians)
        angle_in_radian = get_contact_angle_(centre1.x, centre1.y, 0, 0)
        self.assertEqual(angle_in_radian, 0.0)

        angle_in_radian = get_contact_angle_(centre1.x, centre1.y, 0, -0.5) * 180.0 / math.pi
        print(angle_in_radian)
        self.assertEqual(round(angle_in_radian, 2), -90.0)

        angle_in_radian = get_contact_angle_(centre1.x, centre1.y, 0, 0.5) * 180.0 / math.pi
        print(angle_in_radian)
        self.assertEqual(round(angle_in_radian, 2), -270)


class TestMomentumAngleFreeC(unittest.TestCase):
    """
    Test momentum_angle_free_c (External C version)
    """

    def runTest(self) -> None:
        """
        RETURN VECTORS V1 & V2 AFTER OBJECT COLLISION (ANGLE FREE METHOD)

        cpdef tuple momentum_angle_free_c(
        v1_x: float, v1_y: float,
        v2_x: float, v2_y: float,
        m1: float, m2: float,
        x1_x: float, x1_y: float,
        x2_x: float, x2_y: float,
        invert:bint=False

        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0
        v11, v12 = momentum_angle_free_c(
            vector1.x, vector1.y,
            vector2.x, vector2.y,
            mass1, mass2,
            centre1.x, centre1.y,
            centre2.x, centre2.y)
        self.assertIsInstance(v11, Vector2)
        self.assertIsInstance(v12, Vector2)

        self.assertTrue(hasattr(v11, 'x'))
        self.assertTrue(hasattr(v11, 'y'))
        self.assertTrue(hasattr(v12, 'x'))
        self.assertTrue(hasattr(v12, 'y'))
        self.assertIsInstance(v11.x, float)
        self.assertIsInstance(v11.y, float)
        self.assertIsInstance(v12.x, float)
        self.assertIsInstance(v12.y, float)
        print("Momentum angle free - object1 vector : (x:%s y:%s) ", (v11.x, v11.y))
        print("Momentum angle free - object2 vector : (x:%s y:%s) ", (v12.x, v12.y))
        self.assertAlmostEqual(round(v11.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v11.y, 3), round(math.sin(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.y, 3), -round(math.sin(math.pi / 4.0), 3))

        # Testing Y-axis inversion
        # After inverting the Y-axis both object are moving in an opposite direction
        # and will not collide, the result should be the original vector direction/trajectory
        # with the y vector component inverted
        v11, v12 = momentum_angle_free_c(
            vector1.x, vector1.y,
            vector2.x, vector2.y,
            mass1, mass2,
            centre1.x, centre1.y,
            centre2.x, centre2.y,
            invert=True
        )
        print(v11, v12)
        self.assertAlmostEqual(round(v11.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v11.y, 3), -round(math.sin(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.y, 3), round(math.sin(math.pi / 4.0), 3))


class TestMomentumTrigonometryC(unittest.TestCase):
    """
    Test momentum_trigonometry_c (External C version)
    """

    def runTest(self) -> None:
        """
        RETURN VECTORS V1 & V2 AFTER OBJECT COLLISION (TRIGONOMETRY)

        cpdef tuple momentum_trigonometry_c(
        v1x: float, v1y: float,
        m1: float,
        x1x: float, x1y: float,
        v2x: float, v2y: float,
        m2 : float,
        x2x: float, x2y : float,
        invert: bint=False

        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0
        v11, v12 = momentum_trigonometry_c(
            vector1.x, vector1.y,
            mass1,
            centre1.x, centre1.y,
            vector2.x, vector2.y,
            mass2,
            centre2.x, centre2.y)
        self.assertIsInstance(v11, Vector2)
        self.assertIsInstance(v12, Vector2)

        self.assertTrue(hasattr(v11, 'x'))
        self.assertTrue(hasattr(v11, 'y'))
        self.assertTrue(hasattr(v12, 'x'))
        self.assertTrue(hasattr(v12, 'y'))
        self.assertIsInstance(v11.x, float)
        self.assertIsInstance(v11.y, float)
        self.assertIsInstance(v12.x, float)
        self.assertIsInstance(v12.y, float)
        print("Momentum angle free - object1 vector : (x:%s y:%s) ", (v11.x, v11.y))
        print("Momentum angle free - object2 vector : (x:%s y:%s) ", (v12.x, v12.y))
        self.assertAlmostEqual(round(v11.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v11.y, 3), round(math.sin(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.y, 3), -round(math.sin(math.pi / 4.0), 3))

        # Testing Y-axis inversion
        # After inverting the Y-axis both object are moving in an opposite direction
        # and will not collide, the result should be the original vector direction/trajectory
        # with the y vector component inverted
        v11, v12 = momentum_trigonometry_c(
            vector1.x, vector1.y,
            mass1,
            centre1.x, centre1.y,
            vector2.x, vector2.y,
            mass2,
            centre2.x, centre2.y,
            invert=True
        )
        print(v11, v12)
        self.assertAlmostEqual(round(v11.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v11.y, 3), -round(math.sin(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.y, 3), round(math.sin(math.pi / 4.0), 3))


def run_testsuite():
    """
    test suite

    :return: void
    """

    suite = unittest.TestSuite()

    suite.addTests([
        TestMomentumTrigonometry(),
        TestAngleFree(),
        TestGetMomentumTrigonometry_v1v2(),
        TestGetV1(),
        TestGetV2(),
        TestGetV1AngleFree(),
        TestGetV2AngleFree(),
        TestAngleFreeVec(),
        TestThetaAngle(),
        TestGetContactAngle(),
        # C external function testing
        TestMomentumAngleFreeC(),
        TestMomentumTrigonometryC()
    ])

    unittest.TextTestRunner().run(suite)
    pygame.quit()


if __name__ == '__main__':
    run_testsuite()
    pygame.quit()
