# 2D Elastic Collision 

For Python language 

![alt text](https://raw.githubusercontent.com/yoyoberenguer/Elastic-Collision/version-1.0.1/Assets/BouncingBalls.gif)

### Simulation
```cmd
python simulation.py
```

### Definition (from wikipedia):
`WIKIPEDIA`

An elastic collision is an encounter between two bodies in which the total kinetic
energy of the two bodies after the encounter is equal to their total kinetic energy
before the encounter. 

Perfectly elastic collisions occur only if there is no net 
conversion of kinetic energy into other forms (such as heat or noise) and therefore
they do not normally occur in reality. 

During the collision of small objects, kinetic energy is first converted to potential
energy associated with a repulsive force between the particles (when the particles 
move against this force, i.e. the angle between the force and the relative velocity
is obtuse), then this potential energy is converted back to kinetic energy (when the
particles move with this force, i.e. the angle between the force and the relative 
velocity is acute). The collisions of atoms are elastic collisions 
(`Rutherford backscattering` is one example).

`Two-dimensional`
For the case of two colliding bodies in two dimensions, the overall velocity of each
body must be split into two perpendicular velocities: one tangent to the common 
normal surfaces of the colliding bodies at the point of contact, the other along the
line of collision. Since the collision only imparts force along the line of collision,
the velocities that are `tangent to the point of collision do not change`. 

The velocities along the line of collision can then be used in the same equations as a 
one-dimensional collision. The final velocities can then be calculated from the two 
new component velocities and will depend on the point of collision. Studies of 
two-dimensional collisions are conducted for many bodies in the framework of a 
two-dimensional gas.

In a center of momentum frame at any time the velocities of the two bodies are in 
opposite directions, with magnitudes `inversely proportional to the masses`. 

In an `elastic collision` these magnitudes do not change. The directions may change
depending on the shapes of the bodies and the point of impact. 

For example, in the case of spheres the angle depends on the distance between the 
(parallel) paths of the centers of the two bodies. Any non-zero change of direction
is possible: if this distance is zero the velocities are reversed in the collision;
if it is close to the sum of the radii of the spheres the two bodies are only slightly
deflected. 

Assuming that the second particle is at rest before the collision, the angles of
deflection of the two particles, v1 and v2, are related to the angle of deflection
theta in the system of the center of mass by

Assuming that the second particle is at rest before the collision, the angles of deflection of the two particles, $$<math>\theta_1</math>$$ and $$<math>\theta_2</math>$$, 
are related to the angle of deflection $$<math>\theta</math>$$ in the system of the center of mass by:

$$\tan \theta_1=\frac{m_2 \sin \theta}{m_1+m_2 \cos \theta},\qquad
\theta_2=\frac{{\pi}-{\theta}}{2}.$$

The magnitudes of the velocities of the particles after the collision are:

$$\begin{align}
v'_1 &= v_1\frac{\sqrt{m_1^2+m_2^2+2m_1m_2\cos \theta}}{m_1+m_2} \\
v'_2 &= v_1\frac{2m_1}{m_1+m_2}\sin \frac{\theta}{2}.
\end{align}$$

### Two-dimensional collision with two moving objects
The final x and y velocities components of the first ball can be calculated as:

$$\begin{align}
v'_{1x} &= \frac{v1\cos(\theta_1-\varphi)(m_1-m_2)+2m_2v2\cos(\theta_2-\varphi)}{m_1+m_2}\cos(\varphi)+v1\sin(\theta_1-\varphi)\cos(\varphi + \tfrac{\pi}{2})
\end{align}$$

$$\begin{align}
v'_{1y} &= \frac{v1\cos(\theta_1-\varphi)(m_1-m_2)+2m_2v2\cos(\theta_2-\varphi)}{m_1+m_2}\sin(\varphi)+v1\sin(\theta_1-\varphi)\sin(\varphi + \tfrac{\pi}{2})
\end{align}$$

where v'<sub>1</sub> and v'<sub>2</sub> are the scalar sizes of the two original speeds of the objects, m'<sub>1</sub> and m'<sub>2</sub> are their masses, θ'<sub>1</sub> and θ'<sub>2</sub> are their movement angles, that is, $$v_{1x} = v_1\cos\theta_1,\$$ ; 
$$v_{1y}=v_1\sin\theta_1$$ (meaning moving directly down to the right is either a −45° angle, or a 315° angle), and lowercase phi (φ) is the [[contact angle]]. (To get the x and y velocities of the second ball, one needs to swap all the '1' subscripts with '2' subscripts.)

This equation is derived from the fact that the interaction between the two bodies is easily calculated along the contact angle, meaning the velocities of the objects can be calculated in one dimension by rotating the x and y axis to be parallel with the contact angle of the objects, and then rotated back to the original orientation to get the true x and y components of the velocities.



In an angle-free representation, the changed velocities are computed using the centers **x<sub>1</sub>** and **x<sub>2</sub>** at the time of contact as

$$\begin{align}
\mathbf{v}'_1 &= \mathbf{v}_1-\frac{2 m_2}{m_1+m_2} \ \frac{\langle \mathbf{v}_1-\mathbf{v}_2,\,\mathbf{x}_1-\mathbf{x}_2\rangle}{\|\mathbf{x}_1-\mathbf{x}_2\|^2} \ (\mathbf{x}_1-\mathbf{x}_2),
\end{align}$$


$$\begin{align}
\mathbf{v}'_2 &= \mathbf{v}_2-\frac{2 m_1}{m_1+m_2} \ \frac{\langle \mathbf{v}_2-\mathbf{v}_1,\,\mathbf{x}_2-\mathbf{x}_1\rangle}{\|\mathbf{x}_2-\mathbf{x}_1\|^2} \ (\mathbf{x}_2-\mathbf{x}_1)
\end{align}$$


### Other conserved quantities
In the particular case of particles having equal masses, it can be verified by direct computation from the result above that the scalar product of the velocities before and after the collision are the same, that is $$<math>\langle \mathbf{v}'_1,\mathbf{v}'_2 \rangle = \langle \mathbf{v}_1,\mathbf{v}_2 \rangle.</math>$$ Although this product is not an additive invariant in the same way that momentum and kinetic energy are for elastic collisions, it seems that preservation of this quantity can nonetheless be used to derive higher-order conservation laws.


# Elastic Collision Library

This library provides efficient methods for resolving **2D elastic collisions**, implemented in **Cython** and **C** for high performance. It is designed to integrate seamlessly with **Python** and **Pygame**, enabling real-time simulations.

## Included Methods

- **Trigonometric Method**  
  This approach calculates the interaction between two bodies using the contact angle. It relies on trigonometric functions to determine the direction and magnitude of velocity changes after a collision.

- **Angle-Free Method**  
  This method avoids angle calculations entirely. Instead, it computes the post-collision velocities using only vector operations (e.g., dot product) based on the positions of the object centers (`x₁` and `x₂`) at the moment of impact.

## Key Features

- Optimized for **real-time simulations** such as:
  - 2D video games
  - Arcade-style games
  - Particle systems
  - Interactive object systems in Cartesian space

- Offers **fast and accurate collision resolution**, but is **not a full particle engine** — it focuses solely on the core logic required to resolve elastic collisions.

## Design Philosophy

The library emphasizes **simplicity and performance**, allowing you to build complex object interactions with ease and confidence.

## Performance Note

The **Angle-Free Method** is the fastest of the two, as it avoids computationally expensive trigonometric functions (`cos`, `sin`, `atan2`, etc.). It leverages vector math for collision resolution. In contrast, the **Trigonometric Method** requires calculating the contact angle and individual object angles before determining the resulting velocities (`v₁`, `v₂`).


## Considerations

- The elastic collision algorithm **must be called after detecting a collision** between objects.

- You can choose between two modules: `ec_game` and `ec_real`. These libraries are functionally similar, with one key difference:
  - `ec_game` includes an optional `invert` flag that allows you to invert the final velocity vectors.
  - This is useful if you're visualizing vectors on a standard 2D Cartesian plane (with the y-axis pointing up).
  - **Do not set `invert=True`** in typical 2D video game environments, where the y-axis is inverted. The default is `invert=False`.

- The **Trigonometric Method** is generally less accurate than the **Angle-Free Method**, due to:
  - Angle approximations
  - Use of single-precision floats (`float`) in the library
  - An associated error margin of approximately `1e-5`

- **Input vectors are not normalized** in order to conserve total **kinetic energy** during collision resolution.


 ### Difference Between Display Space and Cartesian Space

In a typical display (such as a game screen), the **Y-axis is inverted** compared to the standard Cartesian coordinate system.

If an object's position is at the center of the display:
- Decreasing its Y value moves it **upward**
- Increasing its Y value moves it **downward**

In other words, the display coordinate system increases Y downward, whereas in Cartesian space, Y increases upward.  
This inversion must be taken into account when applying elastic collision equations.

A common solution is to **invert the Y component of velocity vectors** before or after collision resolution, depending on your coordinate system.

---

#### Real Domain: ℝ(x, y)

| Vector Direction         | Resultant Velocity        | Object Center         |
|--------------------------|---------------------------|------------------------|
| **v₁ ( 0.707,  0.707 )** | **v₁′ (−0.707, −0.707 )** | **C₁ ( 0.000,  0.000 )** |
| **v₂ (−0.707, −0.707 )** | **v₂′ ( 0.707,  0.707 )** | **C₂ ( 1.414,  1.414 )** |


`figure 1`


**![alt text](https://raw.githubusercontent.com/yoyoberenguer/Elastic-Collision/master/Assets/RealDomain.PNG)**

This diagram illustrates a **2D elastic collision** between two circular objects, represented as colored spheres (C₁ and C₂), in a **top-down Cartesian space**.

### Object Properties:

- **C₁ (Blue Sphere)**
  - Center: (0.000, 0.000)
  - Initial Velocity `v₁ = (0.707, 0.707)` → Yellow arrow
  - Resultant Velocity `v₁′ = (−0.707, −0.707)` → green arrow

- **C₂ (Red Sphere)**
  - Center: (1.414, 1.414)
  - Initial Velocity `v₂ = (−0.707, −0.707)` → Red arrow
  - Resultant Velocity `v₂′ = (0.707, 0.707)` → Green arrow

### Key Notes:

- The X and Y axes are shown using bold black arrows.
- Vectors are labeled using LaTeX-like notation (v₁, v₂, v₁′, v₂′).
- The collision conserves both momentum and kinetic energy.
- The objects exchange velocities due to symmetry and equal mass.
- A velocity component table is included on the right to show precise vector values.

### Educational Use:

- This image is suitable for explaining elastic collisions in physics lectures.
- Ideal for use in presentations, simulation docs, or academic content.


---

* **Game environement (Y-Axis inverted )**

Vector direction        | Resultant                |  Object centre         |
------------------------|--------------------------|------------------------|
**v1( 0.707,  0.707)**  | **v1'(-0.707, -0.707)**  |**C1 ( 0, 0)**          | 
**v2(-0.707, -0.707)**  | **v2'( 0.707,  0.707)**  |**C2 (1.414, 1.414)**   | 


`Figure 2`

![alt text](https://github.com/yoyoberenguer/Elastic-Collision/blob/26c15da6369f236470123f50c4c2b55ccf9b6647/Assets/Improved_GameDomain.png)


## Converting Between Real Cartesian Space and 2D Game Display

While the **elastic collision equations** return the same vector values in both coordinate systems, their visual interpretation differs due to axis orientation.

In a **real Cartesian space ℝ(x, y)**:
- Positive Y points **upward**
- A velocity vector like `(0.707, 0.707)` moves the object **northeast**, at a **+45°** angle.

In a **2D game display space**:
- Positive Y points **downward**
- The same vector will appear as moving **southeast**, visually interpreted as **−45°**.

### Why This Matters:
To preserve the correct physical behavior in a game engine, the **Y-components of all vectors must be inverted** when transitioning from Cartesian space to display space.

### Example Conversion:

| Vector Direction      | Resultant in ℝ(x, y)     | After Inverting Y-component |
|-----------------------|--------------------------|------------------------------|
| v₁ = ( 0.707,  0.707) | v₁′ = (−0.707, −0.707)   | v₁′ = (−0.707,  0.707)       |
| v₂ = (−0.707, −0.707) | v₂′ = ( 0.707,  0.707)   | v₂′ = ( 0.707, −0.707)       |

### How to Apply It:
- After computing `v₁′` and `v₂′` using the elastic collision equations,
- Simply multiply the **Y-components by −1**:

* The project is under the `MIT license`

### Installation 

check the link for newest version https://pypi.org/project/ElasticCollision/

### Installation from pip

* Available python build 3.6, 3.7, 3.8, 3.9, 3.10 and source build
* Compatible WINDOWS and LINUX for platform x86, x86_64
```
pip install ElasticCollision 
```

* Checking the installed version 
  (*Imported module is case sensitive*) 
```python
>>>from ElasticCollision.ec_game import __version__
>>>__version__
```
---
### Installation from source code

*Download the source code and decompress the Tar or zip file*
* Linux
```bash
tar -xvf ElasticCollision-1.0.3.tar.gz
cd ElasticCollision-1.0.3
python3 setup.py bdist_wheel
cd dist 
pip3 install ElasticCollision-xxxxxx 
```
* Windows 

*Decompress the archive and enter ElasticCollision directory* 
```bash
python setup.py bdist_wheel 
cd dist
pip install ElasticCollision-xxxxxx
```

---


### Trigonometry quick example 

```python
# FOR 2D GAME (Y-AXIS INVERTED)
from pygame.math import Vector2
from ElasticCollision.ec_game import momentum_trigonometry

vector1 = Vector2(0.707, 0.707)
centre1 = Vector2(0.0, 0.0)
vector2 = Vector2(-0.707, -0.707)
centre2 = Vector2(1.4142, 1.4142)
mass1 = 1.0
mass2 = 1.0
v11, v12 = momentum_trigonometry(
    centre1, centre2, vector1, vector2, mass1, mass2, False)
print(v11, v12)
```

### angle_free quick example

```python
# FOR 2D GAME (Y-AXIS INVERTED)
from pygame.math import Vector2
from ElasticCollision.ec_game import momentum_angle_free

vector1 = Vector2(0.707, 0.707)
centre1 = Vector2(0.0, 0.0)
vector2 = Vector2(-0.707, -0.707)
centre2 = Vector2(1.4142, 1.4142)
mass1 = 1.0
mass2 = 1.0
v11, v12 = momentum_angle_free(
    vector1, vector2, mass1, mass2, centre1, centre2, False)
print(v11, v12)
```

```python
== RESTART: C:/Users/yoyob/AppData/Local/Programs/Python/Python36/test11.py ==
pygame 2.0.0 (SDL 2.0.12, python 3.6.3)
Hello from the pygame community. https://www.pygame.org/contribute.html
[-0.707, -0.707] [0.707001, 0.707]
[-0.707, -0.707] [0.707, 0.707]
>>> 
```


### Building cython code

#### When do you need to compile the cython code ? 

```
Each time you are modifying any of the following files 
ec_game.pyx, c_game.pyx,  ec_real.pyx or any external C code if applicable

1) open a terminal window
2) Go under the directory game   
3) run : python setup_ec_game.py build_ext --inplace --force
4) Go under the directory real
5) run : python setup_ec_real.py build_ext --inplace --force

If you have to compile the code with a specific python 
version, make sure to reference the right python version 
in (python38 setup_ec_real.py build_ext --inplace)

If the compilation fail, refers to the requirement section and 
make sure cython and a C-compiler are correctly install on your
 system.
- A compiler such visual studio, MSVC, CGYWIN setup correctly on 
  your system.
  - a C compiler for windows (Visual Studio, MinGW etc) install 
  on your system and linked to your windows environment.
  Note that some adjustment might be needed once a compiler is 
  install on your system, refer to external documentation or 
  tutorial in order to setup this process.e.g https://devblogs.
  microsoft.com/python/unable-to-find-vcvarsall-bat/
```

## Credit
Yoann Berenguer 

### Dependencies :
```
numpy >= 1.18
pygame >=2.0.0
cython >=0.29.21
```

### License :

MIT License

Copyright (c) 2019 Yoann Berenguer

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without 
restriction, including without limitation the rights to use, 
copy, modify, merge, publish, distribute, sublicense, and/or 
sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.


### Testing: 
```python
>>> from ElasticCollision import *
>>> from ElasticCollision.tests.test_ec_game import run_testsuite
>>> run_testsuite()

>>> from ElasticCollision import *
>>> from ElasticCollision.tests.test_ec_real import run_testsuite
>>> run_testsuite()
```



### Links 
```
Links

https://en.wikipedia.org/wiki/Elastic_collision
```
