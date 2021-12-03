from vpython import *
import numpy as np

#SetupBiped sets parameters of each joint. Child and sister empty as sister only relevant for top hip joint, and child not relevant for foot.
# Number is joint number, a is joint axis, q is joint velocity
class SetupBiped:
    def __init__(self, number, a, q, pos, parent = None):
        self.number = number
        self.child = []
        self.sister = None
        self.a = a
        self.q = q
        self.pos=pos
        self.parent = parent
        self.rm = np.array([[1, 0, 0],[0,1,0],[0,0,1]])

        if self.parent is not None:
            self.parent.child.append(self)
        

    def  draw(self):
        joint_rad = 4
        sphere(pos=self.pos, radius=joint_rad)
        if self.parent is not None:
            curve([self.pos, self.parent.pos], radius = 1.5)

# setting a, joint axis vector (roll, pitch, yaw)
UX = vector(1,0,0)
UY = vector(0,1,0)
UZ = vector(0,0,1)

""""
j1.pos = vector(67, 86, 0)
j2.pos = vector(50, 86, 0)
j3.pos = vector(50, 78, 0)
j4.pos = vector(50, 78, 0)
j5.pos = vector(50, 44, 0)
j6.pos = vector(50, 19, 0)
j7.pos = vector(50, 0, 0)

j8.pos = vector(76, 86, 0)
j9.pos = vector(76, 78, 0)
j10.pos = vector(84, 78, 0)
j11.pos = vector(84, 44, 0)
j12.pos = vector(84, 19, 0)
j13.pos = vector(84, 0, 0)
"""

#joint 1 is body, increasing joint no = down right leg, j7 is foot
#Axis as defined in VPython setup
j1 = SetupBiped(1, UY, 0, vector(67, 86, 0))
j2 = SetupBiped(2, UY, 0, vector(58, 86, 0), j1)
j3 = SetupBiped(3, UZ, 0, vector(58, 78, 0), j2)
j4 = SetupBiped(4, UX, 0, vector(50, 78, 0), j3)
j5 = SetupBiped(5, UX, 0, vector(50, 44, 0), j4)
j6 = SetupBiped(6, UX, 0, vector(50, 19, 0), j5)
j7 = SetupBiped(7, UZ, 0, vector(50, 0, 0), j6)

#Left leg going down, j13 is foot
j8 = SetupBiped(8, UY, 0, vector(76, 86, 0), j1)
j9 = SetupBiped(9, UZ, 0, vector(76, 78, 0), j8)
j10 = SetupBiped(10, UX, 0, vector(84, 78, 0), j9)
j11 = SetupBiped(11, UX, 0, vector(84, 44, 0), j10)
j12 = SetupBiped(12, UX, 0, vector(84, 19, 0), j11)
j13 = SetupBiped(13, UZ, 0, vector(84, 0, 0), j12)

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