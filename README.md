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

```
FOLDER ElasticCollision_For_GAME: 

This folder contains all the scripts design to works with 2D cartesian coordinate 
system with Y-axis inverted (game application). 

FOLDER Elastic_collision_REAL : 

Contains all the cython/C scripts for REAL domain application.

All cython scripts requires to be compiled before being imported into your favorite python IDE,
please refer to the compilation section for more details.
This library does not include a collision detection engine capable to determine object's 
centre position at time of contact. As a result, all values used in the functions calls (method 
free angle and trigonometric) are considered, initial values (velocity/position) of both objects prior 
impact (velocity vector v1 & v2,  and object positions x1 , x2).

In order to use both elastic collision algorithm you will have to provide a set of values such as:
- Object's velocity and direction 
- Object's positions (centre coordinate) 
- Object's mass
```

## DESCRIPTION:
```
This library contains 2 distinct methods (trigonometry and free angle representation).
Both techniques are using different approach:

Angle free is by far the fastest method as it does not require trigonometric functions
such as (cos, sin, atan … etc) in order to solve object's vector components at the time of contact.
Angle free method rely on vector calculation instead (file vector.c for more details).

Trigonometry method requires calculation of object's contact angle and angle theta at point of contact prior
solving object's resultant vectors.
```
## COMPILATION :
```
BUILDING THE GAME VERSION
In a command prompt and under the directory containing the source files
e.g : 
C:\ElasticCollision_For_GAME>python setup_ProjectC.py build_ext --inplace   -> Build Cython code (hooks to the C version)
C:\ElasticCollision_For_GAME>python setup_Project.py build_ext --inplace    -> Build Cython code 

BUIDLING THE REAL DOMAIN VERSION
C:\ElasticCollision_REAL>python setup_ProjectC.py build_ext --inplace   -> Build Cython code (hooks to the C version)
C:\ElasticCollision_REAL>python setup_Project.py build_ext --inplace    -> Build Cython code 

*If the compilation fail, refers to the requirement section and make sure cython
and a C-compiler are correctly install on your system.
```
## REQUIREMENTS :
```
- Pygame 3
- Numpy
- Cython (C extension for python)
- A C compiler for windows (Visual Studio, MinGW etc) install on your system
  and linked to your windows environment.
  Note that some adjustment might be needed once a compiler is install on your system,
  refer to external documentation or tutorial in order to setup this process.
  e.g https://devblogs.microsoft.com/python/unable-to-find-vcvarsall-bat/
```
## HOW TO :
```
# Import elastic collision (Game version) library in your favorite python IDE 

from EC_GAME import momentum_angle_free

# Define Objects positions and velocity at time of contact.

v1 = Vector2(0.707, 0.707)    # V1 is object1 direction/speed vector
x1 = Vector2(0, 0)            # X1 is object1 centre coordinates tuple (x, y)
v2 = Vector2(-0.707, -0.707)  # V2 is object2 direction/speed vector
x2 = Vector2(1.4142, 1.4142)  # X2 is object2 centre coordinates tuple (x, y)
m1 = 1.0                      # Object 1 mass
m2 = 1.0                      # Object 2 mass

invert = False                # Assume coordinate to be already inverted

# RESULTS

vec1, vec2 = momentum_angle_free(v1.x, v1.y, v2.x, v2.y, m1, m2, x1.x, x1.y, x2.x, x2.y, invert)
print("\nANGLE FREE - object1 vector : (x:%s y:%s) ", (vec1['x'], vec1['y']))
print("\nANGLE FREE - object2 vector : (x:%s y:%s) ", (vec2['x'], vec2['y']))
```

## TIMING:
```
For millions iterations
ANGLE FREE      :  0.7796687 seconds
TRIGONOMETRY    :  1.1638778 seconds
```

