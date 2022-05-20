from vpython import *
from time import *

# Setting up web canvas
scene.userzoom = True               # user can zoom in & out
scene.width = scene.height = 600    # width x height
scene.range = 180                   # corresponds to field of view


if __name__ == "__main__":

    # inputs
    joint_rad = 4
    link_width = 2.5
    length5 = 11
    length4 = 17
    length3 = 26
    llength = length5 + length4 + length3   # all link lengths (no joints)
    all_length = llength + 8*joint_rad # all links and joints

    # pedibus (feet) size
    ped_size = [10,3,20]

    # body size
    bod_size = [10,2.5,2.5]

    # initial position
    posv = [50,0,0]
    pos = vector(50,0,0)
