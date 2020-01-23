# Elastic Collision 

WIKIPEDIA

An elastic collision is an encounter between two bodies in which the total kinetic energy of the two bodies after the encounter is equal to their total kinetic energy before the encounter. Perfectly elastic collisions occur only if there is no net conversion of kinetic energy into other forms (such as heat or noise) and therefore they do not normally occur in reality.
During the collision of small objects, kinetic energy is first converted to potential energy associated with a repulsive force between the particles (when the particles move against this force, i.e. the angle between the force and the relative velocity is obtuse), then this potential energy is converted back to kinetic energy (when the particles move with this force, i.e. the angle between the force and the relative velocity is acute).
The collisions of atoms are elastic collisions (Rutherford backscattering is one example).

# Two-dimensional
For the case of two colliding bodies in two dimensions, the overall velocity of each body must be split into two perpendicular velocities: one tangent to the common normal surfaces of the colliding bodies at the point of contact, the other along the line of collision. Since the collision only imparts force along the line of collision, the velocities that are tangent to the point of collision do not change. The velocities along the line of collision can then be used in the same equations as a one-dimensional collision. The final velocities can then be calculated from the two new component velocities and will depend on the point of collision. Studies of two-dimensional collisions are conducted for many bodies in the framework of a two-dimensional gas.

In a center of momentum frame at any time the velocities of the two bodies are in opposite directions, with magnitudes inversely proportional to the masses. In an elastic collision these magnitudes do not change. The directions may change depending on the shapes of the bodies and the point of impact. For example, in the case of spheres the angle depends on the distance between the (parallel) paths of the centers of the two bodies. Any non-zero change of direction is possible: if this distance is zero the velocities are reversed in the collision; if it is close to the sum of the radii of the spheres the two bodies are only slightly deflected.
Assuming that the second particle is at rest before the collision, the angles of deflection of the two particles, v1 and v2, 
are related to the angle of deflection theta in the system of the center of mass by

![alt text](https://github.com/yoyoberenguer/2DElasticCollision/blob/master/Assets/Graphics/math1.png)

The magnitudes of the velocities of the particles after the collision are:

![alt text](https://github.com/yoyoberenguer/2DElasticCollision/blob/master/Assets/Graphics/math2.png)

# Two-dimensional collision with two moving objects

The final x and y velocities components of the first ball can be calculated as

![alt text](https://github.com/yoyoberenguer/2DElasticCollision/blob/master/Assets/Graphics/math3.png)

where v1 and v2 are the scalar sizes of the two original speeds of the objects, m1 and m2 are their masses, Ɵ1 and Ɵ2 
are their movement angles, that is, v1x = v1cosƟ1, v1y = v1sinƟ1 (meaning moving directly down to the right is either a -45° angle, or a 315°angle), and lowercase phi (φ) is the contact angle. (To get the x and y velocities of the second ball, one needs to swap all the '1' subscripts with '2' subscripts.)
This equation is derived from the fact that the interaction between the two bodies is easily calculated along the contact angle, meaning the velocities of the objects can be calculated in one dimension by rotating the x and y axis to be parallel with the contact angle of the objects, and then rotated back to the original orientation to get the true x and y components of the velocities
In an angle-free representation, the changed velocities are computed using the centers x1 and x2 at the time of contact as

![alt text](https://github.com/yoyoberenguer/2DElasticCollision/blob/master/Assets/Graphics/math4.png)

where the angle brackets indicate the inner product (or dot product) of two vectors.

# 2D Elastic Collision Engine

2D elastic collision engine implemented in python. 
Two distinct methods (trigonometry and free angle representation). 
Both methods have been tested and show exactly the same results. 

The following classes can be easily implemented into a 2D game (top down or horizontal/vertical scrolling) to generate
a real time elastic collision engine, or used for educational purpose. 

## Python Angle free method 
```
# define velocity vector for object 1 before contact
v1 = pygame.math.Vector2(0.707, 0.707) 
# define velocity vector for object 2 before contact
v2 = pygame.math.Vector2(-0.707, -0.707)
# define mass in kg for both objects.
m1 = 10.0
m2 = 10.0
# define centre position of both objects in cartesian coordinate system
x1 = pygame.math.Vector2(100, 200.0)
x2 = pygame.math.Vector2(200, 100.0)
# determine the deflection between objects, v12 being the final 
# vector velocity (object 1) and v21 being the final vector velocity 
# for object 2. 
v12, v21 = Momentum.angle_free_calculator(v1, v2, m1, m2, x1, x2)
```
## Python Trigonometry method 
```
# Create pyhton objects obj_1 and obj_2 
# TestObject class define all the attributes needed for each objects.
# e.g:
# - object mass   (mass in kg)
# - object centre (position in the 2d cartesian coordinate system)
# - object vector (velocity vector)

centre1 = (100, 200)
obj_1 = TestObject(x=0.707, y=0.707, mass=10.0, centre=centre1)
centre2 = (200, 100)
obj_2 = TestObject(x=-0.707, y=-0.707, mass=10.0, centre=centre2)
obj_1.vector.y *= -1
obj_2.vector.y *= -1
c = Momentum(obj_1, obj_2)
v12, v21 = c.collision_calculator()          
```
# Python timings:
* - TRIGONOMETY : Timing result for 1000000 iterations  : 20.093596862793334s
* - ANGLE FREE  : Timing result for 1000000 iterations  : 4.719169265488081s

# Elastic collision C implementation 
```
This library contains two distinct methods to calculate the elastic collision 
between two objects. 

1) Trigonometry method
 * This equation is derived from the fact that the interaction between the two bodies 
   is easily calculated along the contact angle, meaning the velocities of the objects 
   can be calculated in one dimension by rotating the x and y axis to be parallel with 
   the contact angle of the objects, and then rotated back to the original orientation 
   to get the true x and y components of the velocities
2) Angle free method 
 * In an angle-free representation, the changed velocities are computed using the 
   centers x1 and x2 at the time of contact as
```
## Considerations:
 ```
 * When using these methods we are assuming that the objects will collide at some point 
   in time (and at least one object should be in motion). 
   A collision engine detection has to be implemented prior using these methods 
   to determine if two objects are collisioner.
 
 Both methods (Trigonometry and Angle free ) are equivalent, therefore you must be aware 
 that using these methods in a different Cartesian coordinates system such as the display
 interface will require modifications to the (Y) vector components of both objects (before 
 or after contact).
 e.g:  
 if an object position is at the centre of the display, we will have to decrease its (Y) 
 value in order to move it upward and increase its (Y) value to move it downward. 
 In other words, display's Y-axis is inversed and this difference has to be taken into
 account in the elastic collision equations. 
 This can be easily implemented by reversing the (Y) vectors components of each objects 
 before or after contact.
  
 * If the trigonometric method is used in a real domain then the equation can be use as is,
   otherwise (Y) vector component has to be inverted.
 
 * If the angle free method is used in a real domain then the equation can be use as is, 
   otherwise (Y) vector component has to be inverted.

 - Before contact:
  v1 and v2 being respectively velocity vectors of both objects (1) & (2) before impact; 
  * v1(x, y) become v1(x, y * -1) for object 1
  * v2(x, y) become v2(x, y * -1) for object 2 
 OR 
 - After contact:
  v12 and v21 being the final velocity vector of both objects (deflection);
  * v12(x, y) become v12(x, y * -1) for object 1 final velocity
  * v21(x, y) become v21(x, y * -1) for object 2 final velocity

 SEE EXAMPLE section.
``` 
## Requirement: 
```
 This program use the library "vector.c" containing all the vector functions needed.
 Refer to the file vector.c to check vector functions and structures.
```
## Observation(s):
```
 The angle free method gives a better result in terms of overall calculation speed. 
 See section timing for more details. 
```
## Timing:
```
 Trigonometry 0.85 seconds for million calculations (850 ns/each)
 Angle free  0.17 seconds for million calculations (170 ns/each)
```
## EXAMPLE:
```
// -- TRIGONOMETRY METHOD

 * struct collider_object obj1, obj2;
struct collision_vectors vec1;
// 4 Lines below defines the velocity vector and 
// objects's centre positions.
vecinit(&obj1.vector, 0.707, 0.707);
vecinit(&obj2.vector, -0.707, -0.707);
vecinit(&obj1.centre, 100.0, 200.0);
vecinit(&obj2.centre, 200.0, 100.0);
obj1.mass = 10.0;
obj2.mass = 10.0;
 * 
// If you represent the objects in a 2d cartesian coordinate system, 
// you will realized that no collision will occur with the given 
// direction vectors v1(0.707, 0.707) with centre C1(100, 200) 
// and v2(-0.707, -0.707) centre C2(200, 100).
// That said, if you place now the objects on the screen domain, the collision 
// between both objects will become evident. 
// This is due to the fact that the screen  Y-Axis is inverse in comparison to 
// the cartesian domain.
// Therefore as explained above, (Y) component of vectors have to be inversed 
// in order to represent the objects collision correctly onto the screen.
// After applying those changes to both vectors,  we can see that both objects will  
// collide on screen. If you have drawn the object onto an A4 page, flip the page over,
// draw the X-axis and Y-axis (cartesian system) and check that the 
// vectors directions are now aline to the orignal vectors values before axis inversion. 
// The result of vectors v12 and v21 should equal v1 and v2 (orignal velocity).
// if v12 = v1 and v21 = v2 then we can say that both objects are not colliding.
// v12(0.707, 0.707) & v21(-0.707, -0.707) 
vec1 = momentum_t(obj1, obj2);
printf("\nTRIGONOMETRY - object1 vector : (x:%f y:%f) ", vec1.v12.x, vec1.v12.y);
printf("\nTRIGONOMETRY - object2 vector : (x:%f y:%f) ", vec1.v21.x, vec1.v21.y);

// Now remember, angle free method can be applied without modification for real domain 
// so we should get the same results for v12 and v21 (no collision)
 
// -- ANGLE FREE METHOD 
 * 
struct vector2d v1, v2, x1, x2;
struct collision_vectors vec2;
float m1, m2;
vecinit(&v1, 0.707, 0.707);
vecinit(&v2, -0.707, -0.707);
vecinit(&x1, 100.0, 200.0);
vecinit(&x2, 200.0, 100.0);
m1 = 10.0;
m2 = 10.0;
vec2= momentum_angle_free(v1, v2, m1, m2, x1, x2);
printf("\nANGLE FREE - object1 vector : (x:%f y:%f) ", vec2.v12.x, vec2.v12.y);
printf("\nANGLE FREE - object2 vector : (x:%f y:%f) ", vec2.v21.x, vec2.v21.y);
// Result : v12(0.707, 0.707) & v21(-0.707, -0.707) 
// both methods are showing the exact same result after inversing y values of both
// object's velocity vectors.
```

## Recommandation: 
```
 I recommand to use the angle free method over the trigonometric technic. 
 It is much faster and Y-axis inversion is not required.

```


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

Please acknowledge and give reference if using the source code for your project

"""

