/* C implementation

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

