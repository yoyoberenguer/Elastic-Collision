
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

int main(){

clock_t begin = clock();
clock_t end = clock();
int i=0;
double time_spent;
double n2 = 10000000.0;

// ---------------- vecinit -----------------------------
struct vector2d v, v1, v2;
printf("\nVector initialisation ");
vecinit(&v, 0.0, 0.0);
printf("\n v(x:%f, y:%f) ", v.x, v.y);
vecinit(&v1, 0.707, 0.707);
printf("\n v1(x:%f, y:%f) ", v1.x, v1.y);
vecinit(&v2, -0.707, -0.707);
printf("\n v2(x:%f, y:%f) ", v2.x, v2.y);

// ------ TIMING TEST 
begin = clock();

for (i=0; i<=n2; ++i){
 vecinit(&v, 0.0, 0.0);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] vecinit total time %f seconds, %g.", time_spent, time_spent/n2); 


// ------------- distance_to ---------------------------
float distance = distance_to(v1, v2);
printf("\n distance_to v1 & v2: %f ", distance);

begin = clock();
for (i=0; i<=n2; ++i){
 distance_to(v1, v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] distance_to total time %f :", time_spent); 


// ------------- distance_squared_to -------------------
distance = distance_squared_to(v1, v2);
printf("\n distance_squared_to v1 & v2: %f ", distance);

begin = clock();
for (i=0; i<=n2; ++i){
 distance_squared_to(v1, v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] distance_squared_to total time %f :", time_spent); 


// ------------------- vlength -------------------------
float length = vlength(&v1);
printf("\n vlength v1: %f ", length);

begin = clock();
for (i=0; i<=n2; ++i){
  vlength(&v1);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] vlength total time %f :", time_spent); 


// ------------------- length_squared ---------------------
length = length_squared(v1);
printf("\n length_squared v1: %f ", length);

begin = clock();
for (i=0; i<=n2; ++i){
  length_squared(v1);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] length_squared total time %f :", time_spent); 

// ------------------- subv_inplace---------------------
subv_inplace(&v1, v2);
printf("\n sub inplace v1(x:%f, y:%f) ", v1.x, v1.y);

begin = clock();
for (i=0; i<=n2; ++i){
  subv_inplace(&v1, v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] subv_inplace total time %f :", time_spent); 


// ------------------- addv_inplace -------------------
addv_inplace(&v1, v2);
printf("\n add inplace  v1(x:%f, y:%f) ", v1.x, v1.y);
begin = clock();
for (i=0; i<=n2; ++i){
  addv_inplace(&v1, v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] addv_inplace  total time %f :", time_spent); 

// ------------------- mulv_inplace  -------------------
mulv_inplace(&v1, v2);
printf("\n mul inplace  v1(x:%f, y:%f) ", v1.x, v1.y);

begin = clock();
for (i=0; i<=n2; ++i){
  mulv_inplace(&v1, v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] mulv_inplace  total time %f :", time_spent); 

// ------------------- divv_inplace -------------------
divv_inplace(&v1, v2);
printf("\n div inplace  v1(x:%f, y:%f) ", v1.x, v1.y);
vecinit(&v, 0.0, 0.0);
divv_inplace(&v1, v);

begin = clock();
for (i=0; i<=n2; ++i){
  divv_inplace(&v1, v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] divv_inplace total time %f :", time_spent); 


vecinit(&v1, 0.707, 0.707);
// ------------------- subcomponents -------------------
v1 = subcomponents(v1, v2);
printf("\n sub v1(x:%f, y%f) ", v1.x, v1.y);

begin = clock();
for (i=0; i<=n2; ++i){
  subcomponents(v1, v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] subcomponents  total time %f :", time_spent); 


// ------------------ addcomponents -------------------
v1 = addcomponents(v1, v2);
printf("\n add v1(x:%f, y%f) ", v1.x, v1.y);

begin = clock();
for (i=0; i<=n2; ++i){
  addcomponents(v1, v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] addcomponents total time %f :", time_spent); 



// ------------------- mulcomponents -----------------
v1 = mulcomponents(v1, v2);
printf("\n mul v1(x:%f, y:%f) ", v1.x, v1.y);

begin = clock();
for (i=0; i<=n2; ++i){
  mulcomponents(v1, v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] mulcomponents total time %f :", time_spent); 


// ------------------- divcomponents -------------------
v1 = divcomponents(v1, v2);
printf("\n div v1(x:%f, y:%f) ", v1.x, v1.y);
vecinit(&v, 0.0, 0.0);
divcomponents(v1, v);

begin = clock();
for (i=0; i<=n2; ++i){
  divcomponents(v1, v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] divcomponents total time %f :", time_spent); 


vecinit(&v1, 0.707, 0.707);
// ------------------- scalevector2d_self ----------------
scalevector2d_self(2, &v1);
printf("\n scale inplace v1(x:%f, y:%f) ", v1.x, v1.y);

// ------------------- scalevector2d --------------------
v1 = scalevector2d(2, &v1);
printf("\n scale v1(x:%f, y:%f) ", v1.x, v1.y);

// ------------------- dot ------------------------
vecinit(&v1, 0.707, 0.707);
float d = dot(&v1, &v2);
printf("\n dot %f ", d);
begin = clock();
for (i=0; i<=n2; ++i){
  float d = dot(&v1, &v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] dot total time %f :", time_spent); 

// ------------------- normalize ------------------------
vecinit(&v1, 7.07, 7.07);
normalize(&v1);
printf("\n scale v1(x:%f, y:%f) ", v1.x, v1.y);
vecinit(&v1, 0.0, 0.0);
normalize(&v1);

// ------------------- vrotate_deg ----------------------
vecinit(&v1, 7.07, 7.07);
vrotate_deg(&v1, 45);
printf("\n vrotate_deg 45 degrees v1(x:%f, y:%f) ", v1.x, v1.y);

// ------------------- vrotate_rad----------------------
vecinit(&v1, 7.07, 7.07);
vrotate_rad(&v1, M_PI/4);
printf("\n vrotate_deg pi/4 rad v1(x:%f, y:%f) ", v1.x, v1.y);

// ------------------- angle_to ----------------------
vecinit(&v1, 7.07, 7.07);
float a = angle_to(v1, v2);
printf("\n angle_to %f ", a);
begin = clock();
for (i=0; i<=n2; ++i){
  angle_to(v1, v2);
}
end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("\n[+] angle_to total time %f :", time_spent); 

// ------------------- vangle_rad ----------------------
vecinit(&v1, 7.07, 7.07);
a = vangle_rad(v1);
printf("\n vangle_rad %f ", a);

// ------------------- vangle_deg ----------------------
vecinit(&v1, 7.07, 7.07);
a = vangle_deg(v1);
printf("\n vangle_deg %f ", a);

return 0;
}