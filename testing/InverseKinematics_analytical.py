from vpython import *
import numpy as np
import math

#Analytical method as opposed to numerical. 

class SetupBiped:
    def __init__(self, number, a, q, pos, rm, b = None, parent = None):
        self.number = number
        self.child = []
        self.sister = None
        self.a = a
        self.q = q
        self.pos=pos
        self.parent = parent
        self.b = b
        self.rm = rm #np.array([[1, 0, 0],[0,1,0],[0,0,1]])

        if self.parent is not None:
            self.parent.child.append(self)
            #self.tm_0_i = np.array([[1,0,0,self.pos.x-self.parent.pos.x],[0,1,0,self.pos.y-self.parent.pos.y],[0, 0, 1, self.pos.z-self.parent.pos.z],[0,0,0,1]])
        #if self.parent is None:
            #condition here

    def Rroll(theta, self):
        c = np.cos(theta)
        s = np.sin(theta)
        Rr = np.matrix([[1, 0, 0],[0, c, -s],[0, s, c]])
        return Rr

    def Rpitch(theta, self): 
        c = np.cos(theta)
        s = np.sin(theta)
        Ry = np.matrix([[c, 0, s],[0, 1, 0],[-s, 0, c]])
        return Ry

    def IK(D, A, B, foot, self):
        # D: distance between the Body origin and the hip joint
        #Body: body joint 1
        #foot: last right or left leg joint
        #A: upper leg length is A
        #B: lower leg length is B
        
        #r is the changing trig distance between hip joint and foot = R7 * (p2 - p7)
        p2 = j1.pos + np.matmul(j1.rm, np.array([0, D, 0]))
        p7 = self.pos

        r = np.transpose(self.rm) * (p2 - p7)

        C = norm(r)
        c5 = (C^2 - A^2 - B^2)/(2.0*A*B) #cosine rule
        #c - local center of mass
        if c5 >= 1:
            q5 = 0.0
        elif c5 <= 1:
            q5 = math.pi
        else:
            q5 = np.arccos(c5) #knee pitch

        q7= np.arctan2(r[1],r[2]) #q7 = atan2(ry, rz)
        
        if q7 > math.pi/2:
            q7 = q7 - math.pi
        elif q7 < -math.pi/2:
            q7 = q7 + pi
        
        q6a = np.arcsin((A/C) * np.sin(math.pi-q5))
        q6 = np.arctan2(r[0], np.sign(r[2])* np.sqrt( r[1]^2 + r[2]^2)) - q6a # ankle pitch)

        #R = body.R' * Foot.R * Rroll(-q7) * Rpitch(-q6-q5) -- hipZ*hipX*hipY
        R = np.transpose(j1.rm) * self.rm * self.Rroll(-q7) * self.Rpitch(-q6 - q5)
        q2 = np.arctan2(-R[0,1],R[1,1]) #hip yaw
        cz = np.cos(q2)
        sz = np.sin(q2)

        q3 = np.arctan2(R[2,1],-R[0,1]*sz + R[1,1]*cz) #hip roll
        q4 = np.arctan2(-R[2,0], R[2,2]) #hip pitch

        q = np.array([q2, q3, q4, q5, q6, q7])

        

# setting a, joint axis vector (roll, pitch, yaw)
UX = vector(1,0,0)
UY = vector(0,1,0)
UZ = vector(0,0,1)

ex = vector(1,0,0) #vector(1,0,0)
ey = vector(0,1,0) #vector(0,0,1)
ez = vector(0,0,1) #vector(0,-1,0)
eye_rm = [ex, ey, ez] #x, y, z

#joint 1 is body, increasing joint no = down right leg, j7 is foot
#Axis as defined in VPython setup
#Need to make b a parameter from initial setup
j1 = SetupBiped(1, UY, 0, vector(67, 86, 0), eye_rm )
j2 = SetupBiped(2, UY, 0, vector(58, 86, 0), eye_rm, vector(-9,0,0),  j1)
j3 = SetupBiped(3, UZ, 0, vector(58, 78, 0),  eye_rm, vector(0, 78-86,0),j2)
j4 = SetupBiped(4, UX, 0, vector(50, 78, 0), eye_rm,vector(50-58,0,0), j3)
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
