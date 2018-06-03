# 2D Elastic Collision 

2D elastic collision engine implemented in python. 
It contains two distinc methods (trigonometry and free angle representation). 
Both technics have been tested and show exactly the same results. 

The following classes can be easily implemented into a 2D game (top down or horizontal/vertical scrolling) to generate
a real time elastic collision engine.

# * If you are using the trigonometry method, don't forget to inverse v1.y and v2.y before caluclation 
e.g :
  v1 = pygame.math.Vector2(x1, y1).normalize()   # vector v1 (object1) prior collision 
  v2 = pygame.math.Vector2(x2, y2).normalize()   # vector v2 (object2) prior collision
  
  v1.y *= -1
  v2.y *= -1

  m1, m2 = 10, 100  #  Object's mass 
  
  # Rect1 is a pygame rectangle with the centre is the centre of the object1 
  object1 = TestObject(v1.x, v1.y, m1, Rect1) 
  # Rect2 is a pygame rectangle whom the centre is the cenre of the object2
  object2 = TestObject(v2.x, v2.y, m2, Rect2)

  v1_final = Momentum.process_v1(obj1, obj2)
  v2_final = Momentum.process_v2(obj1, obj2) 

                        


# - TRIGONOMETY : Timing result for 100000 iterations  : 2.093596862793334s
# - ANGLE FREE  : Timing result for 100000 iterations  : 0.4719169265488081s

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

