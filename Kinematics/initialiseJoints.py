# from vpython import *
from time import *
import numpy as np

import config.joints as js
from classes.Joints import *

def main():
    joints = Joints()
    joints.initialiseJoints(js.DATA)

    print ("pls print this thx")
    print ("pos J1: ", joints.getJoint(1).pos)

if __name__ == "__main__":
    main()