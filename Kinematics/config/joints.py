from classes.Matrix import EYE_MATRIX

"""
Definitions related to ABI's joints
The information about each joint is stored in a dictionary of parameters
"""
# Joint axis vectors (to be moved to a separate file, maybe)
UX = [1, 0, 0]
UY = [0, 1, 0]
UZ = [0, 0, 1]

"""
Body
"""

J1 = {
    "number": 1,
    "a": UY,
    "q": 0,
    "pos": [67, 86, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": None,
    "sister": None,
    "child": [2, 8]
}

"""
Right leg
"""

J2 = {
    "number": 2,
    "a": UY,
    "q": 0,
    "pos": [58, 86, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 1,
    "sister": None,
    "child": [3]

}

J3 = {
    "number": 3,
    "a": UY,
    "q": 0,
    "pos": [58, 86, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 2,
    "sister": None,
    "child": [4]
}

J4 = {
    "number": 4,
    "a": UX,
    "q": 0,
    "pos": [58, 78, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 3,
    "sister": None,
    "child": [5]
}

J5 = {
    "number": 5,
    "a": UX,
    "q": 0,
    "pos": [50, 44, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 4,
    "sister": None,
    "child": [6]
}

J6 = {
    "number": 6,
    "a": UX,
    "q": 0,
    "pos": [50, 19, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 5,
    "sister": None,
    "child": [7]
}

J7 = {
    "number": 7,
    "a": UZ,
    "q": 0,
    "pos": [50, 0, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 6,
    "sister": None,
    "child": []
}

"""
left leg
"""

J8 = {
    "number": 8,
    "a": UY,
    "q": 0,
    "pos": [76, 86, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 1,
    "sister": None,
    "child": [9]
}

J9 = {
    "number": 9,
    "a": UZ,
    "q": 0,
    "pos": [76, 78, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 8,
    "sister": None,
    "child": [10]
}

J10 = {
    "number": 10,
    "a": UX,
    "q": 0,
    "pos": [84, 78, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 9,
    "sister": None,
    "child": [11]
}

J11 = {
    "number": 11,
    "a": UX,
    "q": 0,
    "pos": [84, 44, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 10,
    "sister": None,
    "child": []
}

J12 = {
    "number": 12,
    "a": UX,
    "q": 0,
    "pos": [84, 19, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 11,
    "sister": None,
    "child": [13]
}

J13 = {
    "number": 13,
    "a": UZ,
    "q": 0,
    "pos": [84, 0, 0],
    "rm": EYE_MATRIX,
    "b":  None,
    "parent": 12,
    "sister": None,
    "child": []
}
# Joints Data array to iterate over when initialising Joints
DATA = [
    J1,                         # body
    J2, J3, J4, J5, J6, J7,     # right leg
    J8, J9, J10, J11, J12, J13  # left leg
]