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

