
import numpy as np
import math

"""
Definitions related to standard matrices
"""

EYE_MATRIX = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])

class Matrix:
    def __init__(self, listOfLists = EYE_MATRIX):
        self.rows = len(listOfLists)
        self.cols = len(listOfLists[0])
        self.matrix = []
        if self.verifyMatrix() is True:
            self.matrix = listOfLists
    
    def verifyMatrix(self):
        for list in self.matrix:
            if len(list) != self.cols:
                return False
        return True
    
    def inverse(self):
        pass
    

EYE_MATRIX_ALTERNATE = Matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
])

# Add a Rotation Matrix Solver in terms of theta, phi and psi (Roll, Pitch, Yaw)
# Add a Wedge and hat function for ease of computation later on. 
# Will have to test these functions 

def wedge(vector):
    # Vector's in the kinematics calculations are usuallly stored as 3x1 
    # Add part of function that checks for the vector dimensions 
    # This function returns the resultant matrix of the wedge operation; 
    wedge = np.array([
         [0, -vector[2], vector[1]],
         [vector[2], 0, -vector[0]], 
         [-vector[1], vector[0], 0]])
    return wedge 
    

def hat(matrix):
    # Add the part of the function that checks for the matrix dimensions 

    x = matrix[2][1]
    y = matrix[0][2]
    z = matrix[1][0]

    vector = [x, y, z]
    return vector
    
def rotationmatrix(roll, pitch, yaw):
    # Function generates rotation matrix given the roll, pitch and yaw of the joint+link 
    # Create Matrices, Rx, Ry and Rz 
    Rx = np.array([
        [1, 0, 0],
        [0, math.cos(roll), -math.sin(phi)], 
        [0, math.sin(phi), math.cos(phi)]
        ])
    Ry = np.array([
        [math.cos(theta), 0, math.sin(theta)], 
        [0, 1, 0],
        [-math.sin(theta), 0, math.cos(theta)]
        ])
    Rz = np.array([
        [math.cos(psi), -math.sin(psi), 0], 
        [math.sin(psi), math.cos(psi), 0], 
        [0, 0, 1]
        ])
    mat1 = np.matmul(Ry,Rz)
    # Hence the rotation matrix is: 
    Rmat = np.matmul(Rx, mat1)
    return Rmat
    

