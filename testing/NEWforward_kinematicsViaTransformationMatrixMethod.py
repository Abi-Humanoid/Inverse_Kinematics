#Testing SetupJoints script using transformations matrices

from vpython import *
from time import *
import numpy as np
from SetupJointsViaTransformationMatrixMethod import SetupBiped

# setting a, joint axis vector (roll, pitch, yaw)
UX = vector(1,0,0)
UY = vector(0,1,0)
UZ = vector(0,0,1)

ex = vector(1,0,0) #vector(1,0,0)
ey = vector(0,0,1) #vector(0,0,1)
ez = vector(0,-1,0) #vector(0,-1,0)
eye_rm = [ex, ey, ez] #x, y, z

#joint 1 is body, increasing joint no = down right leg, j7 is foot
#Axis as defined in VPython setup
#Need to make b a parameter from initial setup
#change square brackets to ()
"""""
j1 = SetupBiped(1, UY, 0, vector(67, 86, 0), eye_rm )
j2 = SetupBiped(2, UY, 0, vector(58, 86, 0), eye_rm, vector(-9,0,0),  j1)
j3 = SetupBiped(3, UZ, 0, vector(58, 78, 0),  eye_rm, vector(0, 78-86,0),j2)
j4 = SetupBiped(4, UX, 0, vector(50, 78, 0), eye_rm, vector(50-58,0,0), j3)
j5 = SetupBiped(5, UX, 0, vector(50, 44, 0),  eye_rm,vector(0,44-78,0), j4)
j6 = SetupBiped(6, UX, 0, vector(50, 19, 0),  eye_rm, vector(0, 19-44,0),j5)
j7 = SetupBiped(7, UZ, 0, vector(50, 0, 0),  eye_rm, vector(0, -19,0),j6)

#Left leg going down, j13 is foot
j8 = SetupBiped(8, UY, 0, vector(76, 86, 0), eye_rm, vector(76-67,0,0),j1)
j9 = SetupBiped(9, UZ, 0, vector(76, 78, 0), eye_rm, vector(0,78-86,0),j8)
j10 = SetupBiped(10, UX, 0, vector(84, 78, 0), eye_rm, vector(84-76,0,0), j9)
j11 = SetupBiped(11, UX, 0, vector(84, 44, 0), eye_rm, vector(0,44-78,0), j10)
j12 = SetupBiped(12, UX, 0, vector(84, 19, 0), eye_rm, vector(0,19-44,0),j11)
j13 = SetupBiped(13, UZ, 0, vector(84, 0, 0), eye_rm, vector(0,-19,0), j12)
"""""
j1 = SetupBiped(1, UY, 0, vector(67, 86, 0) )
j2 = SetupBiped(2, UY, 0, vector(58, 86, 0), vector(-9,0,0),  j1)
j3 = SetupBiped(3, UZ, 0, vector(58, 78, 0),   vector(0, 78-86,0),j2)
j4 = SetupBiped(4, UX, 0, vector(50, 78, 0), vector(50-58,0,0), j3)
j5 = SetupBiped(5, UX, 0, vector(50, 44, 0),  vector(0,44-78,0), j4)
j6 = SetupBiped(6, UX, 0, vector(50, 19, 0),  vector(0, 19-44,0),j5)
j7 = SetupBiped(7, UZ, 0, vector(50, 0, 0), vector(0, -19,0),j6)

#Left leg going down, j13 is foot
j8 = SetupBiped(8, UY, 0, vector(76, 86, 0),  vector(76-67,0,0),j1)
j9 = SetupBiped(9, UZ, 0, vector(76, 78, 0), vector(0,78-86,0),j8)
j10 = SetupBiped(10, UX, 0, vector(84, 78, 0),vector(84-76,0,0), j9)
j11 = SetupBiped(11, UX, 0, vector(84, 44, 0), vector(0,44-78,0), j10)
j12 = SetupBiped(12, UX, 0, vector(84, 19, 0), vector(0,19-44,0),j11)
j13 = SetupBiped(13, UZ, 0, vector(84, 0, 0), vector(0,-19,0), j12)


#** two children of body: left hip, right hip. Instead of one child and one sister for joint 2**
j1.child = [j2, j8] 

#j2.sister = j8
j2.child = j3
#right leg
j3.child = j4
j4.child = j5
j5.child = j6
j6.child = j7
#left leg
j8.child = j9
j9.child = j10
j10.child = j11
j12.child = j13

j1.draw()
j2.draw()
j3.draw()
j4.draw()
j5.draw()
j6.draw()
j7.draw()
j8.draw()
j9.draw()
j10.draw()
j11.draw()
j12.draw()
j13.draw()

scene.userzoom = True
scene.width = scene.height = 600
scene.range = 180

# set rotation matrix of parent (may be identity)
#rotates x axis for 60 degrees
ex = vector(1,0,0)
ey = vector(0,0.5,-0.86)
ez = vector(0,0.86,0.5)
parent_RM = [ex, ey, ez] #x, y, z 


j4.rm = parent_RM

"""
print("before: rjoint_5 pos = ",j5.pos)
print("before: rjoint_5 RM = ",j5.rm) 
j5.ForwardKinematics(0)

print("after: rjoint_5 pos = ",j5.pos)
print("after: rjoint_5 RM = ",j5.rm)  

print("before: rjoint_6 pos = ",j6.pos)
print("before rjoint_6 RM = ",j6.rm) 

j6.ForwardKinematics(0)
print("after: rjoint_6 pos = ",j6.pos)
print("after rjoint_6 RM = ",j6.rm) 

print("before: rjoint_7 pos = ",j7.pos)
print("before rjoint_7 RM = ",j7.rm) 
j7.ForwardKinematics(0)
print("after: rjoint_7 pos = ",j7.pos)
print("after rjoint_7 RM = ",j7.rm) 


j5.Rod(0)
"""


def make_axes(length):
    x_axis = arrow(pos=vector(0,0,0), axis=length*vector(1,0,0), color=color.red)
    neg_xaxis = x_axis.clone()
    neg_xaxis.axis *= -1

    y_axis = arrow(pos=vector(0,0,0), axis=length*vector(0,1,0), color=color.green)
    neg_yaxis = y_axis.clone()
    neg_yaxis.axis *= -1

    z_axis = arrow(pos=vector(0,0,0), axis=length*vector(0,0,1), color=color.blue)
    neg_zaxis = z_axis.clone()
    neg_zaxis.axis *= -1

    xlabel = label(text="x", color=color.red, pos=x_axis.pos+x_axis.axis)
    ylabel = label(text="y", color=color.green, pos=y_axis.pos+y_axis.axis)
    zlabel = label(text="z", color=color.blue, pos=z_axis.pos+z_axis.axis)
    return

while True:
    make_axes(20)
    pass
