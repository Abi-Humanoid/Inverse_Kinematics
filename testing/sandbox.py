from vpython import *
from time import *

scene.userzoom = True
scene.width = scene.height = 600
scene.range = 180

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
pos = [50,0,0]

rjoint_6 = sphere(pos=vector(pos[0],pos[1],pos[2]), radius=joint_rad)
rleg_5 = box(pos=vector(pos[0],pos[1]+joint_rad+(length5/2.0),pos[2]),
                size=vector(link_width,length5+2*joint_rad,link_width))


r_foot = box(pos=rjoint_6.pos+vector(0,-(joint_rad+(ped_size[1]/2)),0),
                size=vector(ped_size[0],ped_size[1],ped_size[2]))

while True:
    pass
