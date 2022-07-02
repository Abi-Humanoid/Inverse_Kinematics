# OLD NOTES:
# Subbing in point COM for each joint in forward (or inverse) kinematics, to then calculate total COM
# Calculate COM for different walking phases
# Use CoM values as a trajectory 'x' -> generate ZMP via cart table model. (LIPM uses ZMP -> CoM). 
# Do smooth generation in Matlab, work backwards to get joint angles

# NEW NOTES 25/6/22 re Paul April 10th
# Use calculate_zmp as basis, sample scripts used in sections 3.3.5 (calcMC, calcCoM) and 4.3.1 (calcZMP):
# Calculate_zmp has calcCOM and calcZMP. calcCOM contains calcMC to use.
# This is a LIPM model
from vpython import *
from time import *
import random
import numpy as np
import math

from Laura.Kinematics.SetupJoints_InverseKinematics import SetupBiped

################################### SETTING BODY - JUST A COPY #########################################
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
#           number, a, q, pos,              rm,     b = None,       parent = None)
j1 = SetupBiped(1, UY, 0, vector(67, 86, 0), eye_rm )
j2 = SetupBiped(2, UZ, 0, vector(58, 86, 0), eye_rm, vector(-9,0,0),  j1)
j3 = SetupBiped(3, UY, 0, vector(58, 78, 0),  eye_rm, vector(0, 78-86,0),j2)
j4 = SetupBiped(4, UX, 0, vector(50, 78, 0), eye_rm,vector(50-58,0,0), j3)
j5 = SetupBiped(5, UX, 0, vector(50, 44, 0),  eye_rm,vector(0,44-78,0), j4)
j6 = SetupBiped(6, UX, 0, vector(50, 19, 0),  eye_rm, vector(0, 19-44,0),j5)
j7 = SetupBiped(7, UZ, 0, vector(50, 0, 0),  eye_rm, vector(0, -19,0),j6)

#Left leg going down, j13 is foot
j8 = SetupBiped(8, UZ, 0, vector(76, 86, 0), eye_rm, vector(76-67,0,0),j1)
j9 = SetupBiped(9, UY, 0, vector(76, 78, 0), eye_rm, vector(0,78-86,0),j8)
j10 = SetupBiped(10, UX, 0, vector(84, 78, 0), eye_rm, vector(84-76,0,0), j9)
j11 = SetupBiped(11, UX, 0, vector(84, 44, 0), eye_rm, vector(0,44-78,0), j10)
j12 = SetupBiped(12, UX, 0, vector(84, 19, 0), eye_rm, vector(0,19-44,0),j11)
j13 = SetupBiped(13, UZ, 0, vector(84, 0, 0), eye_rm, vector(0,-19,0), j12)

#** two children of body: left hip, right hip. Instead of one child and one sister for joint 2**
j1.child = [j2, j8] 
#right leg
j2.child = j3
j3.child = j4
j4.child = j5
j5.child = j6
j6.child = j7
#left leg
j8.child = j9
j9.child = j10
j10.child = j11
j11.child = j12
j12.child = j13
######################################################################################################################

#specify initial conditions
M = 100; #TotalMass from body downwards

#initialise body + feet: position, rotation, veloctiy and angular velocity (set to zero) // do we need velocity???
# Know that body -> j1.pos = vector(67, 86, 0), rotation set to eye_rm
# Assume velocities are zero for now?

#Calc CoM
def calcMC(): #calculate the total moment about the origin of the world coordinates, outputs a 3x1 array
    MC = 
    return

def calcCoM():
    M  = TotalMass(1)
    MC = calcMC(1)
    com = MC / M
    return

def main():
