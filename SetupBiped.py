from vpython import *


class SetupBiped:
    def __init__(self, number, a, q):
        self.number = number
        self.child = None
        self.sister = None
        self.a = a
        self.q = q
        self.pos=vector(0,0,0)
    def  draw(self,pos):
        joint_rad = 4
        sphere(pos=self.pos, radius=joint_rad)
        
# setting a, joint axis vector (roll, pitch, yaw)
UX = vector(1,0,0)
UY = vector(0,1,0)
UZ =vector(0,0,1)

j1 = SetupBiped(1, UY, 0)
j2 = SetupBiped(2, UY, 0)
j3 = SetupBiped(3, UZ, 0)
j4 = SetupBiped(4, UX, 0)
j5 = SetupBiped(5, UX, 0)
j6 = SetupBiped(6, UX, 0)
j7 = SetupBiped(7, UZ, 0)

#left leg
j8 = SetupBiped(8, UY, 0)
j9 = SetupBiped(8, UZ, 0)
j10 = SetupBiped(8, UX, 0)
j11 = SetupBiped(8, UX, 0)
j12 = SetupBiped(8, UX, 0)
j13 = SetupBiped(8, UZ, 0)

j1.child = [j2, j8] 

j2.child = j3
#j2.sister = j8

j3.child = j4
j4.child = j5
j5.child = j6
j6.child = j7

j8.child = j9
j9.child = j10
j10.child = j11
j12.child = j13
