""""
TEST LIBRARY ec_real
"""

import unittest
import math

try:
    import pygame

except ImportError:
    raise ImportError("\n<pygame> library is missing on your system."
                      "\nTry: \n   C:\\pip install pygame on a window command prompt.")

from pygame.math import Vector2
from ElasticCollision.ec_real import momentum_trigonometry_real, momentum_angle_free_real


class TestMomentumTrigonometryReal(unittest.TestCase):
    """
    Test Momentum Trigonometry momentum_trigonometry_real
    """

    def runTest(self) -> None:
        """
        cpdef tuple momentum_trigonometry_real(
        obj1_centre : Vector2,
        obj2_centre : Vector2,
        obj1_vector : Vector2,
        obj2_vector : Vector2,
        obj1_mass   : float,
        obj2_mass   : float,
        invert      : bool=False
         ):
        :return:  void
        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0
        v11, v12 = momentum_trigonometry_real(centre1, centre2, vector1, vector2, mass1, mass2)
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
        v11, v12 = momentum_trigonometry_real(centre1, centre2, vector1, vector2, mass1, mass2)

        self.assertAlmostEqual(round(v11.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v11.y, 3), -round(math.sin(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.y, 3), round(math.sin(math.pi / 4.0), 3))

        # Verification with angle free method
        v11, v12 = momentum_trigonometry_real(centre1, centre2, vector1, vector2, mass1, mass2)
        v11_, v12_ = momentum_angle_free_real(vector1, vector2, mass1, mass2, centre1, centre2)
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
        v11, v12 = momentum_trigonometry_real(centre1, centre2, vector1, vector2, mass1, mass2)
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
        v11, v12 = momentum_trigonometry_real(centre1, centre2, vector1, vector2, mass1, mass2)
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
        v11, v12 = momentum_trigonometry_real(centre1, centre2, vector1, vector2, mass1, mass2)
        self.assertTrue(round(v11.x, 3) == 0.707)
        self.assertTrue(round(v11.y, 3) == 0.000)
        self.assertTrue(round(v12.x, 3) == -0.707)
        self.assertTrue(round(v12.y, 3) == 0.000)


class TestAngleFreeReal(unittest.TestCase):
    """
    Test Momentum Angle free momentum_angle_free
    """

    def runTest(self) -> None:
        """
        cpdef tuple momentum_angle_free_real(
        obj1_vector  : Vector2,
        obj2_vector  : Vector2,
        obj1_mass    : float,
        obj2_mass    : float,
        obj1_centre  : Vector2,
        obj2_centre  : Vector2,
        invert       : bool=False):
        :return:  void
        """
        vector1 = Vector2(0.707, 0.707)
        centre1 = Vector2(0.0, 0.0)
        vector2 = Vector2(-0.707, -0.707)
        centre2 = Vector2(1.4142, 1.4142)
        mass1 = 1.0
        mass2 = 1.0
        v11, v12 = momentum_angle_free_real(vector1, vector2, mass1, mass2, centre1, centre2)
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
        v11, v12 = momentum_angle_free_real(vector1, vector2, mass1, mass2, centre1, centre2)

        self.assertAlmostEqual(round(v11.x, 3), -round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v11.y, 3), -round(math.sin(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.x, 3), round(math.cos(math.pi / 4.0), 3))
        self.assertAlmostEqual(round(v12.y, 3), round(math.sin(math.pi / 4.0), 3))

        # Verification with angle free method
        v11, v12 = momentum_trigonometry_real(centre1, centre2, vector1, vector2, mass1, mass2)
        v11_, v12_ = momentum_angle_free_real(vector1, vector2, mass1, mass2, centre1, centre2)
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
        v11, v12 = momentum_angle_free_real(vector1, vector2, mass1, mass2, centre1, centre2)
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
        v11, v12 = momentum_angle_free_real(vector1, vector2, mass1, mass2, centre1, centre2)
        self.assertTrue(round(v11.x, 3) == 0.707)
        self.assertTrue(round(v11.y, 3) == -0.707)
        self.assertTrue(round(v12.x, 3) == -0.707)
        self.assertTrue(round(v12.y, 3) == 0.707)


def run_testsuite():
    """
    test suite

    :return: void
    """

    suite = unittest.TestSuite()

    suite.addTests([
        TestMomentumTrigonometryReal(),
        TestAngleFreeReal(),
    ])

    unittest.TextTestRunner().run(suite)
    pygame.quit()


if __name__ == '__main__':
    run_testsuite()
    pygame.quit()
