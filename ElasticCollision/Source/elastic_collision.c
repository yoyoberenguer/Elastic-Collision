
/* 
Elastic collision C implementation (Two dimensional with two moving objects) 

MIT License

Copyright (c) 2019 Yoann Berenguer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

// gcc -O3 -o elastic_collision elastic_collision.c

*/

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include <math.h>
#include <float.h>
#include <assert.h>
#include <setjmp.h>
#include <time.h>
#include "vector.c"

#define TRY do{ jmp_buf ex_buf__; if( !setjmp(ex_buf__) ){
#define CATCH } else {
#define ETRY } }while(0)
#define THROW longjmp(ex_buf__, 1)


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
struct collision_vectors momentum_angle_free(register float v1_x, register float v1_y,
    register float v2_x, register float v2_y,register float m1, register float m2,
    register float  x1_x, register float x1_y, register float x2_x, register float x2_y);
                    
// Equivalent to momentum_angle_free method (using structural objects)
struct collision_vectors momentum_angle_free1(struct collider_object obj1, struct collider_object obj2);

// ------------------------------------- IMPLEMENTATION -----------------------------------------

// Return the contact angle φ [π, -π] in radians between obj1 and obj2 (float)
float contact_angle(struct vector2d object1, struct vector2d object2)
{
 float phi =  (float)atan2(object2.y - object1.y, object2.x - object1.x);
 if (phi > 0.0) {
   phi = phi - 2.0f * M_PI;
 } 
 // phi *= -1.0;
 return phi;
}


// Return theta angle Θ in radians [π, -π] (float)
float theta_angle(struct vector2d vector)
{ 
  float theta = 0.0f;
  float length = vlength(&vector);
  assert (length!=0.0);
  TRY
  {
    theta = (float)acos(vector.x/length);
    // THROW;
  }
  CATCH
  {
    printf("\nDivision by zero, vector length cannot be zero ");
    return -1;
  }
  ETRY;
  if (vector.y<0.0) {
    theta *= -1.0f;
  }
  theta = (float)fmin(theta, M_PI);
  theta = (float)fmax(theta, -M_PI);
  return (float)theta;
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
  float m12 = m1 + m2;
  // float inv_mass = (float)(1.0f/(m1+m2));
  float theta1_phi = theta1-phi;

  assert ((v1>= 0.0) && (v2>= 0.0));    // |v1| and |v2| magnitude must be >= 0
  assert ((m1+m2)>0.0);      			// m1 + m2 must be > 0 to avoid a div by zero.

  struct vector2d v12;
  float numerator=v1*(float)cos(theta1_phi)*(m1-m2)+(float)(2.0f*m2*v2)*(float)cos(theta2-phi);
  vecinit(&v12, numerator*(float)cos(phi)/m12 + v1*(float)sin(theta1_phi)*(float)cos(phi+M_PI2),
                numerator*(float)sin(phi)/m12 + v1*(float)sin(theta1_phi)*(float)sin(phi+M_PI2));

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

  float inv_mass = (float)(1.0f/(m1+m2));
  float theta2_phi = theta2-phi;

  assert ((v1>= 0.0) && (v2>= 0.0));    // |v1| and |v2| magnitude must be >= 0
  assert (m1+m2>0.0);      			    // m1 + m2 must be > 0 to avoid a div by zero.

  struct vector2d v21;
  float numerator=v2*(float)cos(theta2_phi)*(m2-m1)+(float)(2.0f*m1*v1)*(float)cos(theta1-phi);
  vecinit(&v21, numerator*(float)cos(phi) * inv_mass + v2*(float)sin(theta2_phi)*(float)cos(phi+M_PI2),
                numerator*(float)sin(phi) * inv_mass + v2*(float)sin(theta2_phi)*(float)sin(phi+M_PI2));

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
//	     object mass and centre. obj1 must be initialized before calling the function momentum_t
//    obj2 : struct collider_object;
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
	float mass = (float)(2.0f * m2 / (m1 + m2)); 	        // mass coefficient in the equation
	struct vector2d v12, x12;		            // 2d vector declaration v12 & x12
	// vector initialization 
	vecinit(&v12, 0.0f, 0.0f);
	vecinit(&x12, 0.0f, 0.0f);
	v12 = subcomponents(v1, v2);		        // subtract v1 and v2 (v1 - v2).
	                                            // subcomponents return a new vector v12,
	                                            // original vector v1 & v2 components remain unchanged.
    x12 = subcomponents(x1, x2);             	// Objects centre difference (x1 - x2). subcomponents return a new vector x12
    // x1 & x2 vector components remain unchanged.
	float x12_length = vlength(&x12);    	    // x12 vector length (scalar)
	float d = dot(&v12, &x12);	                // vector dot product v12 & x12, return a scalar value (float)
	// rescale vector x12 
	scale_inplace((float)((mass * d) / (x12_length * x12_length)), &x12);
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
	float mass = (float)(2.0f * m1 / (m1 + m2)); 	        // mass coefficient in the equation
	struct vector2d v21, x21;		            // 2d vector declaration v21 & x21
	// vector initialization 
	vecinit(&v21, 0.0f, 0.0f);
	vecinit(&x21, 0.0f, 0.0f);
	v21 = subcomponents(v2, v1);		        // substract v2 and v1 (v2 - v1). subcomponents return a new vector v21,
						                        // original vector v2 & v1 components remain unchanged.
    x21 = subcomponents(x2, x1);            	// Objects centre difference (x2 - x1). subcomponents return a new vector x21
						                        // x2 & x1 vector components remain unchanged.
	float x21_length = vlength(&x21);	        // x21 vector length (scalar)
	float d = dot(&v21, &x21);	                // vector dot product v21 & x21, return a scalar value (float)
	// rescale vector x21 
	scale_inplace((float)((mass * d) / (x21_length * x21_length)), &x21);
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
struct collision_vectors momentum_angle_free(register float v1_x, register float v1_y,
    register float v2_x, register float v2_y,register float m1, register float m2,
    register float  x1_x, register float x1_y, register float x2_x, register float x2_y)

{
	struct collision_vectors vec;
	struct vector2d v1, v2, x1, x2, v12, v21;
	vecinit(&v1, v1_x, v1_y);
	vecinit(&v2, v2_x, v2_y);
	vecinit(&x1, x1_x, x1_y);
	vecinit(&x2, x2_x, x2_y);
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
//	vecinit(&v12, 0.0, 0.0);
//	vecinit(&v21, 0.0, 0.0);
	struct collision_vectors vec; 
    v12 = v1_vector_components(obj1.vector, obj2.vector, obj1.mass, obj2.mass, obj1.centre, obj2.centre);
    v21 = v2_vector_components(obj1.vector, obj2.vector, obj1.mass, obj2.mass, obj1.centre, obj2.centre);
	vec.v12 = v12;
	vec.v21 = v21;
        return vec;
}



int main(){

return 0;
}
