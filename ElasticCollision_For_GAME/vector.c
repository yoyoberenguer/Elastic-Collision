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



#define M_PI 3.14159265358979323846
#define M_PI2 3.14159265358979323846/2.0
#define RAD_TO_DEG 180.0/M_PI
#define DEG_TO_RAD M_PI/180.0

#define TRY do{ jmp_buf ex_buf__; if( !setjmp(ex_buf__) ){
#define CATCH } else {
#define ETRY } }while(0)
#define THROW longjmp(ex_buf__, 1)

#define c_max(a,b) \
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

struct rect_p
{
    int x;
    int y;
};


// PACK TO VECTORS
struct v_struct
{
   struct vector2d vector1;
   struct vector2d vector2;
};

/*
Use this function to initialized a vector
timing : 0.161s for 10 millions iterations.
e.g:
  vecinit(v, 0.0, 0.0)  --> v(0.0, 0.0)
  vecinit(v, cos(90), sin(90))
*/
void vecinit(struct vector2d *v, register float x, register float y)
{
 v->x = x;
 v->y = y;
}

/*
Calculate the distance between two vectors ex v1 & v2
Return a float representing the cartesian distance between v1 and v2
timing : 0.182s for 10 millions iterations.
e.g:
  struct vector2d v1, v2;
  vecinit(&v1, -1.0, 2.0);
  vecinit(&v2, 5.0, -5.0);
  float distance = distance_to(v1, v2);
*/
float distance_to(struct vector2d v1, struct vector2d v2)
{
 register float vx, vy;
 vx = v1.x - v2.x;
 vy = v1.y - v2.y;
 return (float)sqrt(vx * vx + vy * vy);
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
 return (float)sqrt(v->x * v->x + v->y * v->y);
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
Return a vector with magnitude equal zero when division by zero.
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
   struct vector2d v;
   vecinit(&v, 0, 0);
   return v;
 }
 ETRY;
}

/*
Multiply a vector with a scalar c (scaling a vector)
Return a re-scale vector v with components vx = vx * (scalar c) and vy = vy * (scalar c)
*/
void scale_inplace(float c, struct vector2d *v)
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
 double rad;
 rad=(atan2(v->y, v->x) * RAD_TO_DEG + deg) * DEG_TO_RAD;
 v->x = (float)cos(rad);
 v->y = (float)sin(rad);
}

/*
Rotates a vector by a given angle in radians.
*/
void vrotate_rad(struct vector2d *v, float rad)
{
 double angle;
 angle = (atan2(v->y, v->x) + rad);
 v->x = (float)cos(angle);
 v->y = (float)sin(angle);
}
/*
Calculates the angle to a given vector in degrees (v2 angle - v1 angle)
*/
float angle_to(struct vector2d v1, struct vector2d v2)
{
 float v1_rad, v2_rad;
 v1_rad=(float)atan2(v1.y, v1.x);
 v2_rad=(float)atan2(v2.y, v2.x);
 return (float)(v2_rad - v1_rad) * RAD_TO_DEG;
}

/*
Return the vector angle in radians.
*/
float vangle_rad(struct vector2d v)
{
 return (float)atan2(v.y, v.x);
}

/*
Return the vector angle in degrees.
*/
float vangle_deg(struct vector2d v)
{
 return (float)atan2(v.y, v.x) * RAD_TO_DEG;
}


struct vector2d adjust_vector(struct vector2d player, struct vector2d rect, struct vector2d speed)
{
  struct vector2d new_vector;
  float angle_radian = (float)(-atan2(player.y - rect.y, player.x - rect.x));
  vecinit(&new_vector, (float)(cos(angle_radian) * vlength(&speed)),
 	(float)(-sin(angle_radian) * vlength(&speed)));
  return new_vector;
}

//
///*
//Scale a vector to a random length (int) and toward a given angle
//angle is in radian.
//*/
//struct vector2d RandAngleVector2d(int minimum, int maximum, float angle)
//{
//  struct vector2d new_vector;
//  float n = (float)randRange(minimum, maximum);
//  vecinit(&new_vector, (float)(cos(angle) * n),  (float)(sin(angle) * n));
//  return new_vector;
//}
//
///*
//Scale a vector inplace to a random length (int) and toward a given angle
//angle is in radian.
//
//*/
//void RandAngleVector2d_inplace(struct vector2d *v, int minimum, int maximum, float angle)
//{
//  float n = (float)randRange(minimum, maximum);
//  vecinit(v, (float)(cos(angle) * n),  (float)(sin(angle) * n));
//
//}
//
///*
//Scale a vector to a random length (float) and toward a given angle
//angle is in radian.
//*/
//struct vector2d RandAngleVector2df(float minimum, float maximum, float angle)
//{
//  struct vector2d new_vector;
//  float n = randRangeFloat(minimum, maximum);
//  vecinit(&new_vector, (float)(cos(angle) * n),  (float)(sin(angle) * n));
//  return new_vector;
//}
//
///*
//Scale a vector inplace to a random length (float) and toward a given angle
//angle is in radian.
//
//*/
//void RandAngleVector2d_inplacef(struct vector2d *v, float minimum, float maximum, float angle)
//{
//  float n = randRangeFloat(minimum, maximum);
//  vecinit(v, (float)(cos(angle) * n),  (float)(sin(angle) * n));
//
//}
//



//
//#define TRY do{ jmp_buf ex_buf__; if( !setjmp(ex_buf__) ){
//#define CATCH } else {
//#define ETRY } }while(0)
//#define THROW longjmp(ex_buf__, 1)
//
//
//
//struct mla_pack trajectory(struct vector2d p1, struct vector2d p2, struct vector2d v1, struct vector2d v2);
//
//struct mla_pack trajectory(struct vector2d p1, struct vector2d p2, struct vector2d v1, struct vector2d v2)
//{
//
//  // Contains missile trajectory (2d vector)
//  // and collision coordinates (2d vector)
//  struct mla_pack mlav;
//  struct vector2d v = subcomponents(p2, p1);
//  struct vector2d q = addcomponents(p2, v2) ;
//  float r = vlength(&v1);
//  float a = dot(&v, &v);
//
//  if (a == 0.0){
//    vecinit(&mlav.vector, 0.0, 0.0);
//    vecinit(&mlav.collision, 0.0, 0.0);
//    return mlav;
//  }
//  struct vector2d tmp = subcomponents(p1, q);
//  float b = 2 * dot(&v, &tmp);
//  float c = (dot(&p1, &p1) + dot(&q, &q)) - (2 * dot(&p1, &q)) - (r * r);
//  float disc = (b * b) - (4 * a * c);
//
//  if (disc<0) {
//    vecinit(&mlav.vector, 0.0, 0.0);
//    vecinit(&mlav.collision, 0.0, 0.0);
//    return mlav;
//  }
//
//  float disc_sqrt = (float)sqrt(disc);
//  // first intersection between the line and circle
//  float t1 = (-b + disc_sqrt) / (2 * a);
//  // second intersection between the line and circle
//  float t2 = (-b - disc_sqrt) / (2 * a);
//  // If neither of these is between 0 and 1, then the line segment
//  // misses the circle (but would hit it if extended)
//  if (!(((t1 >= 0) && (t1 <= 1)) || ((t2 >=0) && (t2 <= 1))))
//  {
//      vecinit(&mlav.vector, 0.0, 0.0);
//      vecinit(&mlav.collision, 0.0, 0.0);
//      return mlav;
//  }
//
//  struct vector2d i1 =  addcomponents(p1, scalevector2d(t1, &v));  // intersection 1 in the Cartesian plane
//  struct vector2d i2 =  addcomponents(p1, scalevector2d(t2, &v));  // intersection 2 in the Cartesian plane
//
//  struct vector2d intersection;
//  if (distance_to(p1, i1) > distance_to(p1, i2)){
//	vecinit(&intersection, i2.x, i2.y);
//  }
//  else {
//    vecinit(&intersection, i1.x, i1.y);
//  }
//
//  struct vector2d vector = subcomponents(q, intersection);
//
//  // float angle = atan2(vector.y, vector.x) * RAD_TO_DEG;     // --> this is not used
//
//  float dist1 = distance_to(intersection, p2);   // scalar distance between intersection and p2
//  float dist2 = distance_to(p1, p2);             // scalar distance between p1 and p2
//
//  float ratio;
//  TRY
//  {
//    assert (dist1!=0.0);
//    ratio = dist2 / dist1;
//    THROW;
//  }
//  CATCH
//  {
//   ;
//  }
//  ETRY;
//
//  struct vector2d collision = addcomponents(p1, scalevector2d(ratio, &vector));    // collision coordinates 2d vector
//
//  vecinit(&mlav.vector, vector.x, vector.y);
//  vecinit(&mlav.collision, collision.x, collision.y);
//  return mlav;
//}
//
//int main(){
////int i, n = 1000000.0;
////struct vector2d p1, p2, v1, v2;
////vecinit(&p1, 5, 1);
////vecinit(&p2, 10, 5);
////vecinit(&v1, 1, 1);
////vecinit(&v2, -1, 1);
////struct mla_pack pack;
////clock_t begin = clock();
////for (i=0; i<=n; ++i){
////    pack = trajectory(p1, p2, v1, v2);
////}
////clock_t end = clock();
////float time_spent = (float)(end - begin) / CLOCKS_PER_SEC;
////printf("\nTotal time for %i iterations : %f ", n, time_spent/(double)n);
//
//return 0;
//}
