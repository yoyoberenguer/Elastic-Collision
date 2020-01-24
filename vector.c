/* C implementation */

/*
TODO lerp
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

// Vector intialization
struct vector2d;
void vecinit(struct vector2d *v, float x, float y);
// Vector distance
float distance_to(struct vector2d v1, struct vector2d v2);
float distance_squared_to(struct vector2d v1, struct vector2d v2);
// Vector length
float vlength(struct vector2d *v);
float length_squared(struct vector2d v);

// Vectors operations inplace (similar to elementwise in pygame.math.Vector2 library)
// the result of the operation is assigned to the variable v1 (v2 remains unchanged)
void subv_inplace(struct vector2d *v1, struct vector2d v2);
void addv_inplace(struct vector2d *v1, struct vector2d v2);
void divv_inplace(struct vector2d *v1, struct vector2d v2);
void mulv_inplace(struct vector2d *v1, struct vector2d v2);

// Vector operations elementwise (similar to elementwise in pygame.math.Vector2 library)
// Return a new vector2d (v1 and v2 remains unchanged)
struct vector2d mulcomponents(struct vector2d v1, struct vector2d v2);
struct vector2d addcomponents(struct vector2d v1, struct vector2d v2);
struct vector2d subcomponents(struct vector2d v1, struct vector2d v2);
struct vector2d divcomponents(struct vector2d v1, struct vector2d v2);

// Scaling vectors 
void scalevector2d_self(float c, struct vector2d *v);
struct vector2d scalevector2d(float c, struct vector2d *v);
float dot(struct vector2d *v1, struct vector2d *v2);
// float cross(struct vector2d *v1, struct vector2d *v2);
void normalize (struct vector2d *v);
// Vector rotation, angle etc
void vrotate_deg(struct vector2d *v, float deg);
void vrotate_rad(struct vector2d *v, float rad);
float angle_to(struct vector2d v1, struct vector2d v2);
float vangle_rad(struct vector2d v);
float vangle_deg(struct vector2d v);


#define M_PI 3.14159265358979323846
#define M_PI2 3.14159265358979323846/2.0
#define RAD_TO_DEG 180.0/M_PI
#define DEG_TO_RAD M_PI/180.0

#define TRY do{ jmp_buf ex_buf__; if( !setjmp(ex_buf__) ){
#define CATCH } else {
#define ETRY } }while(0)
#define THROW longjmp(ex_buf__, 1)

#define max(a,b) \
  ({ __auto_type _a = (a); \
      __auto_type _b = (b); \
    _a > _b ? _a : _b; })

/*
2d Vector structure with components x & y (floats)
Use the structure vector2d to declare vector type object
e.g struct vector2d v-> v(x, y)
*/
struct vector2d
{
   float x;
   float y;
};

/*
Use this function to initialized a vector 
timing : 0.161s for 10 millions iterations.
e.g:
  vecinit(v, 0.0, 0.0)  --> v(0.0, 0.0)
  vecinit(v, cos(90), sin(90))
*/
void vecinit(struct vector2d *v, float x, float y)
{
 v->x = x;
 v->y = y;
} 

/*
Calculate the distance between two vectors ex v1 & v2
Return a float representing the cartesienne distance between v1 and v2
timing : 0.182s for 10 millions iterations.
e.g: 
  struct vector2d v1, v2;
  vecinit(&v1, -1.0, 2.0);
  vecinit(&v2, 5.0, -5.0);
  float distance = distance_to(v1, v2);
*/
float distance_to(struct vector2d v1, struct vector2d v2)
{
 float vx, vy;
 vx = v1.x - v2.x;
 vy = v1.y - v2.y; 
 return sqrt(vx * vx + vy * vy);
}


/*
Calculate distance between two vectors ex v1 & v2
Return a float representing the square distance between v1 & v2
timing : 0.099s for 10 millions iterations
e.g:
  float distance = distance_to(v1, v2);
*/
float distance_squared_to(struct vector2d v1, struct vector2d v2)
{
 float vx, vy;
 vx = v1.x - v2.x;
 vy = v1.y - v2.y;
 return vx * vx + vy * vy;
}

/*
Returns the Euclidean length of the vector (vector magnitude).
e.g:
  float length = vlength(&v1);
*/
float vlength(struct vector2d *v)
{
 return sqrt(v->x * v->x + v->y * v->y);
}

/*
Substract vector components such as v1 = v1 - v2 
v1.x = v1.x - v2.x and v1.y = v1.y - v2.y 
*/
void subv_inplace(struct vector2d *v1, struct vector2d v2)
{
 vecinit(v1, v1->x - v2.x, v1->y - v2.y);
}

/*
Add vector components such as v1 = v1 + v2
v1.x = v1.x + v2.x and v1.y = v1.y + v2.y 
*/
void addv_inplace(struct vector2d *v1, struct vector2d v2)
{
 vecinit(v1, v1->x + v2.x, v1->y + v2.y);
}

/*
Divide vector components such as v1 = v1 / v2
v1.x = v1.x / v2.x and v1.y = v1.y / v2.y  (with v2.x and v2.y !=0)
*/
void divv_inplace(struct vector2d *v1, struct vector2d v2)
{

 TRY{
 if ((v2.x == 0.0) || (v2.y == 0.0)){
   THROW;
 }
 //assert (v2.x != 0);
 //assert (v2.y != 0); 
 vecinit(v1, v1->x / v2.x, v1->y / v2.y);
 }
 CATCH{
   printf("\n Division by zero!"); 
   printf("\n[-] Vector length cannot be null.");
   printf("\n[-] Vector components (x:%f, y:%f)", v2.x, v2.y);
 }
 ETRY;
}

/*
Multiply vector components such as v1 = v1 * v2
v1.x = v1.x * v2.x and v1.y = v1.y * v2.y 
*/
void mulv_inplace(struct vector2d *v1, struct vector2d v2)
{
 vecinit(v1, v1->x * v2.x, v1->y * v2.y);
}

/*
multiply components of 2 vectors (v1 * v2).
Return a new 2d vector v with components vx = v1.x * v2.x and vy = v1.y * v2.y
*/
struct vector2d mulcomponents(struct vector2d v1, struct vector2d v2)
{
 struct vector2d v;
 vecinit(&v, v1.x * v2.x, v1.y * v2.y);
 return v;
}

/*
Add components of 2 vectors (v1 + v2).
Return a new 2d vector v with components vx = v1.x + v2.x and vy = v1.y + v2.y
*/
struct vector2d addcomponents(struct vector2d v1, struct vector2d v2)
{
 struct vector2d v;
 vecinit(&v, v1.x + v2.x, v1.y + v2.y);
 return v;
}

/*
Substract components of 2 vectors (v1 - v2).
Return a new 2d vector v with components vx = v1.x - v2.x and vy = v1.y - v2.y
*/
struct vector2d subcomponents(struct vector2d v1, struct vector2d v2)
{
 struct vector2d v;
 vecinit(&v, v1.x - v2.x, v1.y - v2.y);
 return v;
}

/*
divide components of 2 vectors (v1 / v2).
Return a new 2d vector v with components vx = v1.x / v2.x and vy = v1.y / v2.y
*/
struct vector2d divcomponents(struct vector2d v1, struct vector2d v2)
{
 TRY{
 if ((v2.x==0.0) || (v2.y==0.0)){
 THROW;
 }
 struct vector2d v;
 //assert (v2.x != 0);
 //assert (v2.y != 0); 
 vecinit(&v, v1.x / v2.x, v1.y / v2.y); 
 return v;
 }
 CATCH{
   printf("\n Division by zero!");
   printf("\n[-] Vector length cannot be null.");
   printf("\n[-] Vector components (x:%f, y:%f)", v2.x, v2.y);
 }
 ETRY;
}

/*
Multiply a vector with a scalar c (scaling a vector)
Return a re-scale vector v with components vx = vx * (scalar c) and vy = vy * (scalar c) 
*/
void scalevector2d_self(float c, struct vector2d *v)
{
  v->x = v->x * c;
  v->y = v->y * c;
}

/*
Multiply a vector with a scalar c (scaling a vector)
Return a re-scale vector v with components vx = vx * (scalar c) and vy = vy * (scalar c) 
*/
struct vector2d scalevector2d(float c, struct vector2d *v)
{
  struct vector2d new_vector; 
  vecinit(&new_vector, 0, 0);
  new_vector.x = v->x * c;
  new_vector.y = v->y * c;
  return new_vector; 
}

/*
Vector normalisation (dividing components x&y by vector magnitude) v / |v|
*/
void normalize (struct vector2d *v)
{
 float length_ = vlength(v);
 // assert (length_ !=0);
 TRY{
   if (length_==0.0){
     THROW;
   }
   v->x = v->x / length_;
   v->y = v->y / length_;
 }
 CATCH{
   printf("\n[-] Division by zero!");
   printf("\n[-] Vector length cannot be null.");
   printf("\n[-] Vector components (x:%f, y:%f)", v->x, v->y);
 }
 ETRY;
}

/*
Normalize a 2d vector and rescale it to a given length. (v / |v|) * scalar 
*/
void scale_to_length(struct vector2d *v, float length)
{
  normalize(v);
  v->x = v->x * length;
  v->y = v->y * length;
}


/*
Returns the squared Euclidean length of a vector (vector magnitude).
*/
float length_squared(struct vector2d v)
{
 return v.x * v.x + v.y * v.y;
}

/*
dot product (scalar product).
a · b = |a| × |b| × cos(θ)
|a| is the magnitude (length) of vector a
|b| is the magnitude (length) of vector b
θ is the angle between a and b
or -> a · b = ax × bx + ay × by
 * */
float dot(struct vector2d *v1, struct vector2d *v2)
{
 return v1->x * v2->x + v1->y * v2->y;

}


/*
Cross product (vector product).
|u x v| = |u||v|sin θ
float cross(struct vector2d *v1, struct vector2d *v2)
{
return vlength(v1) * vlength(v2) * sqrt(1 - dot(v1, v2));
}
*/

/*
Rotates a vector by a given angle in degrees.
*/
void vrotate_deg(struct vector2d *v, float deg)
{
 float rad;
 rad=(atan2(v->y, v->x) * RAD_TO_DEG + deg) * DEG_TO_RAD;
 v->x = cos(rad);
 v->y = sin(rad);
}

/*
Rotates a vector by a given angle in radians.
*/
void vrotate_rad(struct vector2d *v, float rad)
{
 float angle;
 angle = (atan2(v->y, v->x) + rad);
 v->x = cos(angle);
 v->y = sin(angle);
}
/*
Calculates the angle to a given vector in degrees (v2 angle - v1 angle)
*/
float angle_to(struct vector2d v1, struct vector2d v2)
{
 float v1_rad, v2_rad;
 v1_rad=atan2(v1.y, v1.x);
 v2_rad=atan2(v2.y, v2.x);
 return (v2_rad - v1_rad) * RAD_TO_DEG;
}

/*
Return the vector angle in radians.
*/
float vangle_rad(struct vector2d v)
{
 return atan2(v.y, v.x);
}

/*
Return the vector angle in degrees.
*/
float vangle_deg(struct vector2d v)
{
 return atan2(v.y, v.x) * RAD_TO_DEG;
}

/*
int main()
{

return 0;
}
*/