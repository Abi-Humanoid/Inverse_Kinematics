from vpython import *
from time import *

# inputs
joint_rad = 4
link_width = 2.5
length5 = 11
length4 = 17
length3 = 26
llength = length5 + length4 + length3   # all link lengths
all_length = llength + 8*joint_rad

# pedibus (feet) size
ped_size = [10,3,20]

# body size
bod_size = [10,2.5,2.5]

# initial position
pos = [0,0,0]

r_foot = box(pos=vector(pos[0],pos[1]-(joint_rad+(ped_size[1]/2)),pos[2]),
                size=vector(ped_size[0],ped_size[1],ped_size[2]))
rjoint_6 = sphere(pos=vector(pos[0],pos[1],pos[2]), radius=joint_rad)
rleg_5 = box(pos=vector(pos[0],pos[1]+joint_rad+(length5/2.0),pos[2]),
                size=vector(link_width,length5+2*joint_rad,link_width))
rjoint_5 = sphere(pos=vector(pos[0],pos[1]+2*joint_rad+length5,pos[2]),
                radius=joint_rad)
rleg_4 = box(pos=vector(pos[0],pos[1]+3*joint_rad+length5+(length4/2),pos[2]),
                size=vector(link_width,2*joint_rad+length4,link_width))
rjoint_4 = sphere(pos=vector(pos[0],pos[1]+4*joint_rad+length5+length4,pos[2]),
                radius=joint_rad)
rleg_3 = box(pos=vector(pos[0],pos[1]+5*joint_rad+length5+length4+(length3/2.0),pos[2]),
                size=vector(link_width,2*joint_rad+length3,link_width))
rjoint_3 = sphere(pos=vector(pos[0],pos[1]+6*joint_rad+llength,pos[2]),
                color=color.blue, radius=joint_rad)
rjoint_2 = sphere(pos=vector(pos[0]+2*joint_rad,pos[1]+6*joint_rad+llength,pos[2]),
                radius=joint_rad)
rjoint_1 = sphere(pos=vector(pos[0]+2*joint_rad,pos[1]+8*joint_rad+llength,pos[2]),
                radius=joint_rad)

body = box(pos=vector(pos[0]+3*joint_rad+bod_size[0]/2,pos[1]+all_length,pos[2]),
                size=vector(bod_size[0],bod_size[1],bod_size[2]))

# keep here for now for visuals


while True:
    pass

