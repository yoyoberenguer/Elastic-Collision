
/* 
Elastic collision C implementation (Two dimensional with two moving objects) 

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
   centres x1 and x2 at the time of contact as

Considerations:
 
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
 In other words, display's Y-axis is invert and this difference has to be taken into
 account in the elastic collision equations. 
 This can be easily implemented by reversing the (Y) vectors components of each objects 
 before or after contact.
  
 * If the trigonometric method is used in a real domain then the equation can be use as is,
   otherwise (Y) vector component has to be inverted.
 
 * If the angle free method is used in a real domain then the equation can be use as is, 
   otherwise (Y) vector component has to be inverted.

 Example 
 - Before contact:
  v1 and v2 being respectively velocity vectors of both objects (1) & (2) before impact; 
  * v1(x, y) become v1(x, y * -1) for object 1
  * v2(x, y) become v2(x, y * -1) for object 2 
 OR 
 - After contact:
  v12 and v21 being the final velocity vector of both objects (deflection);
  * v12(x, y) become v12(x, y * -1) for object 1 final velocity
  * v21(x, y) become v21(x, y * -1) for object 2 final velocity
 
Requirement: 
 This program use the library "vector.c" containing all the vector functions needed.
 Refer to the file vector.c to check vector functions and structures.
 
Observation: 
 The angle free method gives a better result in terms of overall calculation speed. 
 See section timing for more details. 

Timing:
 Trigonometry 0.85 seconds for million calculations (850 ns/each)
 Angle free  0.17 seconds for million calculations (170 ns/each)

 HOW TO EXAMPLE:

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
// If you represent the objects in a 2d Cartesian coordinate system, 
// you will realised that no collision will occur with the given 
// direction vectors v1(0.707, 0.707) with centre C1(100, 200) 
// and v2(-0.707, -0.707) centre C2(200, 100).
// That said, if you place now the objects on the screen, the collision 
// between both objects will become evident. 
// This is due to the fact that the screen  Y-Axis is inverse in comparison to 
// the Cartesian domain.
// Therefore as explained above, (Y) component of vectors have to be inverse 
// in order to represent the objects collision correctly onto the screen.
// After applying those changes to both vectors,  we can see that both objects will  
// not collide on screen as it should be in the Cartesian system. 
// If you have drawn the object onto an A4 page (instead of your display),
// flip the page over, draw the X-axis and Y-axis (Cartesian system) and check that the 
// vectors direction are now aline to the original vectors values before axis inversion. 
// The result of vectors v12 and v21 should be equal to v1 and v2 (original velocity).
// if v12 = v1 and v21 = v2 then we can say that both objects did not collide.
// v12(0.707, 0.707) & v21(-0.707, -0.707) 
vec1 = momentum_t(obj1, obj2);
printf("\nTRIGONOMETRY - object1 vector : (x:%f y:%f) ", vec1.v12.x, vec1.v12.y);
printf("\nTRIGONOMETRY - object2 vector : (x:%f y:%f) ", vec1.v21.x, vec1.v21.y);

// Now remember, angle free method can be applied without modification for real domain 
// so we should get the same results for v12 and v21 (no collision)
 
// -- ANGLE FREE METHOD 
  
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
// both methods are showing the exact same result after inverting y values of both
// object's velocity vectors.

Recommendation: 
 I recommend to use the angle free method over the trigonometric Technic. 
 It is much faster and Y-axis inversion is not required.

 
__author__ = "Yoann Berenguer"
__copyright__ = "Copyright 2007."
__credits__ = ["Yoann Berenguer"]
__maintainer__ = "Yoann Berenguer"
__email__ = "yoyoberenguer@hotmail.com"


TODO SECTION:
 * Need to check collision with object of mass null
 * Check div by zero
*/

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include <math.h>
#include <float.h>
#include <assert.h>
#include <ctype.h>
#include <setjmp.h>
#include <time.h>
#include "vector.c"

#define TRY do{ jmp_buf ex_buf__; if( !setjmp(ex_buf__) ){
#define CATCH } else {
#define ETRY } }while(0)
#define THROW longjmp(ex_buf__, 1)

#define max(a,b) \
  ({ __auto_type _a = (a); \
      __auto_type _b = (b); \
    _a > _b ? _a : _b; })

/*
  Use structure <collider_object> to reference colliding objects
  Initialized the attributes vector, mass and centre (see description below)
 */
struct collider_object
{
  struct vector2d vector;   // object direction and velocity (2d vector)
  float mass;			    // Mass in kg (float)
  struct vector2d centre;	// 2d vector; centre of the object  
                            // position in a 2d cartesian coodinates system.
};


/*
 Use the structure <collision_vectors> to define the vectors v12 & v21, 
 that detemines directions and velocities of the objects after collision.
*/
struct collision_vectors
{
 struct vector2d v12;   // object1 vector resultant after contact
 struct vector2d v21;   // object2 ---
};

 
// --------------------------------------- INTERFACE --------------------------------------------------
// STRUCTURES 
struct collider_object;
struct collision_vectors;

// --------------------------------------- TRIGONOMETRY -------------------------------------------
// Determine contact angle between object 1 and object 2.
float contact_angle(struct vector2d object1, struct vector2d object2);

float theta_angle(struct vector2d vector);

// determine object 1 vector direction and velocity after contact.
struct vector2d v12_vector_components(float v1, float v2, float theta1, float theta2, float phi, float m1, float m2);

// determine object 2 vector direction and velocity after contact.
struct vector2d v21_vector_components(float v1, float v2, float theta1, float theta2, float phi, float m1, float m2);

// determine object 1 and object 2 directions and velocities after contact. 
struct collision_vectors momentum_t(struct collider_object obj1, struct collider_object obj2);

// ------------------------------------- ANGLE FREE VERSION --------------------------------------
// Determine object1 vector direction and velocity after impact.
struct vector2d v1_vector_components(struct vector2d v1, struct vector2d v2, float m1, float m2, 
                     struct vector2d x1, struct vector2d x2);

// Determine object2 vector direction and velocity after impact.
struct vector2d v2_vector_components(struct vector2d v1, struct vector2d v2, float m1, float m2, 
                     			struct vector2d x1, struct vector2d x2);

// Determine object1 & object2 directions and velocities after collision.
struct collision_vectors momentum_angle_free(struct vector2d v1, struct vector2d v2, float m1, float m2, struct vector2d x1, struct vector2d x2);
                    
// Equivalent to momentum_angle_free method (using structural objects)
struct collision_vectors momentum_angle_free1(struct collider_object obj1, struct collider_object obj2);

// ------------------------------------- IMPLEMENTATION -----------------------------------------

// Return the contact angle φ [π, -π] in radians between obj1 and obj2 (float)
float contact_angle(struct vector2d object1, struct vector2d object2)
{
 float phi =  atan2(object2.y - object1.y, object2.x - object1.x);
 if (phi > 0.0) {
   phi = phi - 2.0 * M_PI;
 } 
 phi *= -1.0;
 return phi;
}


// Return theta angle Θ in radians [π, -π] (float)
float theta_angle(struct vector2d vector)
{ 
  float theta = 0.0;
  float length = vlength(&vector);
  assert (length!=0.0);
  TRY
  {
    theta = acos(vector.x/length);
    // THROW;
  }
  CATCH
  {
    printf("\nDivision by zero, vector length cannot be zero ");
    return -1;
  }
  ETRY;
  if (vector.y<0.0) {
    theta *= -1.0;
  }
  return theta;
}


// -------------------------- TRIGONOMETRY METHOD  ------------------------------------------------------


/*
****************************************************************
*	return scalar size v1 of the original object represented   *
*   by (v1, theta1, m1) after collision                        *
****************************************************************
//    where v1 and v2 are the scalar sizes of the two original speeds of the objects, m1 and m2
//    are their masses, θ1 and θ2 are their movement angles such as : v1x = v1.cos(θ1) , v1y = v1.sin(θ1)
//    (meaning moving directly down to the right is either a -45° angle, or a 315°angle), and lowercase phi (φ)
//    is the contact angle.
//
//	  v1: float, object1 vector length
//    v2: float, object2 vector length
//    theta1: float, Θ1 angle in radians (object1)
//    theta2: float, Θ2 angle in radians (object2)
//    phi:float,  φ contact angle in radians
//    m1: float, Mass in kilograms, must be > 0 (object1)
//    m2: float, Mass in kilograms, must be > 0 (object2)
//
//    return: Returns a vector 2d representing the direction
//            and velocity of object1 after collision.
//
*/
struct vector2d v12_vector_components(float v1, float v2, float theta1, float theta2, float phi, float m1, float m2)
{

  float inv_mass = 1.0/(m1+m2);
  float theta1_phi = theta1-phi;

  assert ((v1>= 0.0) && (v2>= 0.0));    // |v1| and |v2| magnitude must be >= 0
  assert ((m1+m2)>0.0);      			// m1 + m2 must be > 0 to avoid a div by zero.

  struct vector2d v12;
  float numerator=v1*cos(theta1_phi)*(m1-m2)+2.0*m2*v2*cos(theta2-phi);
  vecinit(&v12, numerator*cos(phi)*inv_mass + v1*sin(theta1_phi)*cos(phi+M_PI2),
                numerator*sin(phi)*inv_mass + v1*sin(theta1_phi)*sin(phi+M_PI2));
  if (v12.y != 0.0){
    v12.y *= -1.0;
  }
  else {
    v12.y = 0.0;
  }
//  if (v12.x < 0.1e-10){
//    v12.x = 0.0;
//  }
//  if (v12.y < 0.1e-10){
//    v12.y = 0.0;
//  }
  return v12;
}


/*
****************************************************************
*	return object 2 vector resultant after impact represented  *
*   by (v2, theta2, m2) after collision                        *
****************************************************************
//    where v1 and v2 are the scalar sizes of the two original speeds of the objects, m1 and m2
//    are their masses, θ1 and θ2 are their movement angles such as : v2x = v2.cos(θ2) , v2y = v2.sin(θ2)
//    (meaning moving directly down to the right is either a -45° angle, or a 315°angle), and lowercase phi (φ)
//    is the contact angle.
//
//	  v1: float, object1 vector length
//    v2: float, object2 vector length
//    theta1: float, Θ1 angle in radians (object1)
//    theta2: float, Θ2 angle in radians (object2)
//    phi:float,  φ contact angle in radians
//    m1: float, Mass in kilograms, must be > 0 (object1)
//    m2: float, Mass in kilograms, must be > 0 (object2)
//
//    return: Returns a vector 2d representing the direction
//            and velocity of object2 after collision.

*/
struct vector2d v21_vector_components(float v1, float v2,
	float theta1, float theta2, float phi, float m1, float m2)
{

  float inv_mass = 1.0/(m1+m2);
  float theta2_phi = theta2-phi;

  assert ((v1>= 0.0) && (v2>= 0.0));    // |v1| and |v2| magnitude must be >= 0
  assert (m1+m2>0.0);      			    // m1 + m2 must be > 0 to avoid a div by zero.

  struct vector2d v21;
  float numerator=v2*cos(theta2_phi)*(m2-m1)+2.0*m1*v1*cos(theta1-phi);
  vecinit(&v21, numerator*cos(phi) * inv_mass + v2*sin(theta2_phi)*cos(phi+M_PI2),
                numerator*sin(phi) * inv_mass + v2*sin(theta2_phi)*sin(phi+M_PI2));
  if (v21.y != 0.0){
    v21.y *= -1.0;
  }
  else {
    v21.y = 0.0;
  }
//  if (v21.x < 0.1e-10){
//    v21.x = 0.0;
//  }
//  if (v21.y < 0.1e-10){
//    v21.y = 0.0;
//  }
  return v21;
}

/*
********************************************************************************************
  Object1 and object2 final velocities and directions vectors in a 2d cartesian coordinates 
  system (after contact).
********************************************************************************************
//    Trigonometric method
//    The changed velocities are computed
//    using centers x1 and x2 at the time of contact.
//
//    All vectors have to be initialised with the method vecinit
//
//    obj1 : struct collider_object; 
// 	     Structure containing object 1 vector (velocity and direction), 
//	     object mass and centre. obj1 must be inintialized before calling the function momentum_t	
//    obj2 : struc collider_object;
	     Structure containing object

//
//    return: v11 Resultant force vector (2d) representing object1 direction and velocity such as
//	    (v11.x, v11y) are the vector components in a 2d cartesian system and length of the
//	    vector its speed.

****************************************************************
*/
struct collision_vectors momentum_t(struct collider_object obj1, struct collider_object obj2)
{
  struct vector2d v12, v21;
  struct collision_vectors vec;
  float phi = contact_angle(obj1.centre, obj2.centre);
  float theta1 = theta_angle(obj1.vector);
  float theta2 = theta_angle(obj2.vector);
  float v1 = vlength(&obj1.vector);
  float v2 = vlength(&obj2.vector);
  v12 = v12_vector_components(v1, v2, theta1, theta2, phi, obj1.mass, obj2.mass);
  v21 = v21_vector_components(v1, v2, theta1, theta2, phi, obj1.mass, obj2.mass);
  vec.v12 = v12;
  vec.v21 = v21;
  return vec;
}

// ------------------------- ANGLE FREE METHOD ---------------------------------------------


/*
********************************************************************************************
  ANGLE FREE 
  Object1 final velocity and directions in a 2d cartesian coordinates system after contact 
********************************************************************************************
//    Angle free representation.
//    The changed velocities are computed
//    using centers x1 and x2 at the time of contact.
//
//    All vectors have to be initialised with the method vecinit
//
//    v1 : Is a 2d vector with components (v1.x, v1.y) representing object1
//	       trajectory and velocity in a cartesian plan at the time of contact.
//    v2 : Is a 2d vector with components (v2.x, v2.y) representing object2
//	       trajectory and velocity in a cartesian plan at the time of contact.
//    m1 : floating value representing object1 mass (in kg), scalar value.
//    m2 : floating value representing object2 mass (in kg), scalar value.
//    x1 : 2d vector representing the object1 centre (x1.x, x1.y) (this is not the centre of mass)
//    x2 : 2d vector representing the object2 centre (x2.x, x2.y) at the time of contact
//	       (this is not the centre of mass)
//
//    return: v11 Resultant force vector (2d) representing object1 direction and velocity such as
//	    (v11.x, v11y) are the vector components in a 2d cartesian system and length of the
//	    vector its speed.

****************************************************************
*/


struct vector2d v1_vector_components(struct vector2d v1, struct vector2d v2, float m1, float m2, 
                     struct vector2d x1, struct vector2d x2)
{
	assert ((m1 + m2) > 0.0);		            // check the sum, should be != 0 to avoid division by zero
	assert ((x1.x != x2.x) && (x1.y != x2.y));  // object1 and object2 centres coordinates must be different
	float mass = 2.0 * m2 / (m1 + m2); 	        // mass coefficient in the equation
	struct vector2d v12, x12;		            // 2d vector declaration v12 & x12
	// vector initialization 
	vecinit(&v12, 0.0, 0.0);
	vecinit(&x12, 0.0, 0.0);
	v12 = subcomponents(v1, v2);		        // substract v1 and v2 (v1 - v2).
	                                            // subcomponents return a new vector v12,
	                                            // original vector v1 & v2 components remain unchanged.
    x12 = subcomponents(x1, x2);             	// Objects centre difference (x1 - x2). subcomponents return a new vector x12
    // x1 & x2 vector components remain unchanged.
	float x12_length = vlength(&x12);    	    // x12 vector length (scalar)
	float d = dot(&v12, &x12);	                // vector dot product v12 & x12, return a scalar value (float)
	// rescale vector x12 
	scalevector2d_self((mass * d) / (x12_length * x12_length), &x12);
	return subcomponents(v1, x12);
}

/*
***********************************************************************************************
    ANGLE FREE 
    Object2 final velocity and directions in a 2d cartesian coordinates system after contact
***********************************************************************************************
//    Angle free representation.
//    The changed velocities are computed
//    using centers x1 and x2 at the time of contact.
//
//    All vectors have to be initialised with the method vecinit
//
//    v1 : Is a 2d vector with components (v1.x, v1.y) representing object1
//	       trajectory and velocity in a cartesian plan at the time of contact.
//    v2 : Is a 2d vector with components (v2.x, v2.y) representing object2
//	       trajectory and velocity in a cartesian plan at the time of contact.
//    m1 : floating value representing object1 mass (in kg), scalar value.
//    m2 : floating value representing object2 mass (in kg), scalar value.
//    x1 : 2d vector representing the object1 centre (x1.x, x1.y) (this is not the centre of mass)
//    x2 : 2d vector representing the object2 centre (x2.x, x2.y) at the time of contact
//	 (this is not the centre of mass)
//
//    return: v21 Resultant force vector (2d) representing object2 direction and velocity such as
//	        (v21.x, v21y) are the vector components in a 2d cartesian system and length of the
//	        vector its speed.

****************************************************************
*/


struct vector2d v2_vector_components(struct vector2d v1, struct vector2d v2, float m1, float m2, 
                     			struct vector2d x1, struct vector2d x2)
{
	assert ((m1 + m2) > 0.0);		            // check the sum, should be != 0 to avoid division by zero
	assert ((x1.x != x2.x) && (x1.y != x2.y));  // object1 and object2 centres coordinates must be different
	float mass = 2.0 * m1 / (m1 + m2); 	        // mass coefficient in the equation
	struct vector2d v21, x21;		            // 2d vector declaration v21 & x21
	// vector initialization 
	vecinit(&v21, 0.0, 0.0);
	vecinit(&x21, 0.0, 0.0);
	v21 = subcomponents(v2, v1);		        // substract v2 and v1 (v2 - v1). subcomponents return a new vector v21,
						                        // original vector v2 & v1 components remain unchanged.
    x21 = subcomponents(x2, x1);            	// Objects centre difference (x2 - x1). subcomponents return a new vector x21
						                        // x2 & x1 vector components remain unchanged.
	float x21_length = vlength(&x21);	        // x21 vector length (scalar)
	float d = dot(&v21, &x21);	                // vector dot product v21 & x21, return a scalar value (float)
	// rescale vector x21 
	scalevector2d_self((mass * d) / (x21_length * x21_length), &x21);
	return subcomponents(v2, x21);
}

/*
*********************************************************************************
	ANGLE FREE
	return V1 (object 1) and V2 (object 2) vectors final velocities and 
	directions after contact.
*********************************************************************************
//    v1 : Is a 2d vector with components (v1.x, v1.y) representing object1
//	       trajectory and velocity in a cartesian plan at the time of contact.
//    v2 : Is a 2d vector with components (v2.x, v2.y) representing object2
//	       trajectory and velocity in a cartesian plan at the time of contact.
//    m1 : floating value representing object1 mass (in kg), scalar value.
//    m2 : floating value representing object2 mass (in kg), scalar value.
//    x1 : 2d vector representing the object1 centre (x1.x, x1.y) (this is not the centre of mass)
//    x2 : 2d vector representing the object2 centre (x2.x, x2.y) at the time of contact
//	       (this is not the centre of mass)
//
//    return: return the pair vector v12 & vector v21 representing the directions and velocities of
//	    both objects (object1 & object2) after collision.
*/
struct collision_vectors momentum_angle_free(struct vector2d v1, struct vector2d v2, 
					float m1, float m2, struct vector2d x1, struct vector2d x2)

{
        
	struct vector2d v12, v21;
	vecinit(&v12, 0.0, 0.0);
	vecinit(&v21, 0.0, 0.0);
	struct collision_vectors vec; 
    v12 = v1_vector_components(v1, v2, m1, m2, x1, x2);
    v21 = v2_vector_components(v1, v2, m1, m2, x1, x2);
	vec.v12 = v12;
	vec.v21 = v21;
    return vec;
}


// return Object 1 & Object 2 final velocities and directions after contact (use structural objects)
struct collision_vectors momentum_angle_free1(struct collider_object obj1, struct collider_object obj2)
{
        
	struct vector2d v12, v21;
	vecinit(&v12, 0.0, 0.0);
	vecinit(&v21, 0.0, 0.0);
	struct collision_vectors vec; 
    v12 = v1_vector_components(obj1.vector, obj2.vector, obj1.mass, obj2.mass, obj1.centre, obj2.centre);
    v21 = v2_vector_components(obj1.vector, obj2.vector, obj1.mass, obj2.mass, obj1.centre, obj2.centre);
	vec.v12 = v12;
	vec.v21 = v21;
        return vec;
}

// ---------------------------------- DEMONSTRATION ----------------------------------

int main(){

int i=0;

// -- TRIGONOMETRY METHOD
struct collider_object obj1, obj2;
struct collision_vectors vec1;
vecinit(&obj1.vector, 0.707, 0.707);
vecinit(&obj2.vector, -0.707, -0.707);
vecinit(&obj1.centre, 100.0, 200.0);
vecinit(&obj2.centre, 200.0, 100.0);
obj1.mass = 10.0;
obj2.mass = 10.0;
vec1 = momentum_t(obj1, obj2);
printf("\nTRIGONOMETRY - object1 vector : (x:%f y:%f) ", vec1.v12.x, vec1.v12.y);
printf("\nTRIGONOMETRY - object2 vector : (x:%f y:%f) ", vec1.v21.x, vec1.v21.y);
printf("\nAll vector (Y) components are *-1 ");
obj1.vector.y *= -1;
obj2.vector.y *= -1;
vec1 = momentum_t(obj1, obj2);
printf("\nTRIGONOMETRY - object1 vector : (x:%f y:%f) ", vec1.v12.x, vec1.v12.y);
printf("\nTRIGONOMETRY - object2 vector : (x:%f y:%f) ", vec1.v21.x, vec1.v21.y);

// ------ TIMING TEST 
clock_t begin = clock();
float n1 = 1000000;
/* here, do your time-consuming job */
for (i=0; i<=n1; ++i){
  vec1 = momentum_t(obj1, obj2);
}
clock_t end = clock();
double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\nTRIGONOMETRY - total time %f :", time_spent); 

// -- ANGLE FREE METHOD 
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

// ------ TIMING TEST 
begin = clock();
float n2 = 1000000;
/* here, do your time-consuming job */
for (i=0; i<=n2; ++i){
 vec2=momentum_angle_free(v1, v2, m1, m2, x1, x2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\nANGLE FREE - total time %f :", time_spent); 

return 0;
}
