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
posv = [50,0,0]
pos = vector(50,0,0)

r_foot = box(pos=vector(posv[0],posv[1]-(joint_rad+(ped_size[1]/2)),posv[2]),
                size=vector(ped_size[0],ped_size[1],ped_size[2]))
rjoint_6 = sphere(pos=pos, radius=joint_rad)
rleg_5 = box(pos=rjoint_6.pos+vector(0,joint_rad+length5/2,0),
                size=vector(link_width,length5+2*joint_rad,link_width))
rjoint_5 = sphere(pos=rleg_5.pos+vector(0,joint_rad+length5/2,0),
                radius=joint_rad)
rleg_4 = box(pos=rjoint_5.pos+vector(0,joint_rad+length4/2,0),
                size=vector(link_width,2*joint_rad+length4,link_width))
rjoint_4 = sphere(pos=rleg_4.pos+vector(0,joint_rad+length4/2,0),
                radius=joint_rad)
rleg_3 = box(pos=rjoint_4.pos+vector(0,joint_rad+length3/2,0),
                size=vector(link_width,2*joint_rad+length3,link_width))
rjoint_3 = sphere(pos=rleg_3.pos+vector(0,joint_rad+length3/2,0),
                radius=joint_rad)
rjoint_2 = sphere(pos=rjoint_3.pos+vector(2*joint_rad,0,0),
                radius=joint_rad)
rjoint_1 = sphere(pos=rjoint_2.pos+vector(0,2*joint_rad,0),
                radius=joint_rad)

print('r_foot',r_foot.pos)
print('rjoint_6',rjoint_6.pos)
print('rjoint_5',rjoint_5.pos)
print('rjoint_4',rjoint_4.pos)
print('rjoint_3',rjoint_3.pos)
print('rjoint_2',rjoint_2.pos)
print('rjoint_1',rjoint_1.pos)
print('rleg_5',rleg_5.pos)
print('rleg_4',rleg_4.pos)
print('rleg_3',rleg_3.pos)



body = box(pos=rjoint_1.pos+vector(joint_rad+bod_size[0]/2,0,0),
                size=vector(bod_size[0],bod_size[1],bod_size[2]))
print("body",body.pos)

ljoint_7 = sphere(pos=vector(posv[0]+4*joint_rad+bod_size[0],posv[1]+all_length,posv[2]),
                radius=joint_rad)
ljoint_8 = sphere(pos=vector(posv[0]+4*joint_rad+bod_size[0],posv[1]+llength+6*joint_rad,posv[2]),
                radius=joint_rad)
ljoint_9 = sphere(pos=vector(posv[0]+6*joint_rad+bod_size[0],posv[1]+llength+6*joint_rad,posv[2]),
                radius=joint_rad)
lleg_9 = box(pos=vector(posv[0]+6*joint_rad+bod_size[0],posv[1]+5*joint_rad+length5+length4+(length3/2.0),posv[2]),
                size=vector(link_width,2*joint_rad+length3,link_width))
ljoint_10 = sphere(pos=vector(posv[0]+6*joint_rad+bod_size[0],posv[1]+4*joint_rad+length5+length4,posv[2]),
                radius=joint_rad)
lleg_10 = box(pos=vector(posv[0]+6*joint_rad+bod_size[0],posv[1]+3*joint_rad+length5+(length4/2),posv[2]),
                size=vector(link_width,2*joint_rad+length4,link_width))
ljoint_11 = sphere(pos=vector(posv[0]+6*joint_rad+bod_size[0],posv[1]+2*joint_rad+length5,posv[2]),
                radius=joint_rad)
lleg_11 = box(pos=vector(posv[0]+6*joint_rad+bod_size[0],posv[1]+joint_rad+(length5/2.0),posv[2]),
                size=vector(link_width,length5+2*joint_rad,link_width))
ljoint_12 = sphere(pos=vector(posv[0]+6*joint_rad+bod_size[0],posv[1],posv[2]),
                radius=joint_rad)
l_foot = box(pos=vector(posv[0]+6*joint_rad+bod_size[0],posv[1]-(joint_rad+(ped_size[1]/2)),posv[2]),
                size=vector(ped_size[0],ped_size[1],ped_size[2]))


print('l_foot',r_foot.pos)
print("ljoint_7",ljoint_7.pos)
print("ljoint_8",ljoint_8.pos)
print("ljoint_9",ljoint_9.pos)
print("ljoint_10",ljoint_10.pos)
print("ljoint_11",ljoint_11.pos)
print("ljoint_12",ljoint_12.pos)

def make_axes(length):
    x_axis = arrow(pos=vector(0,0,0), axis=length*vector(1,0,0), color=color.red)
    neg_xaxis = x_axis.clone()
    neg_xaxis.axis *= -1

    y_axis = arrow(pos=vector(0,0,0), axis=length*vector(0,1,0), color=color.green)
    neg_yaxis = y_axis.clone()
    neg_yaxis.axis *= -1

    z_axis = arrow(pos=vector(0,0,0), axis=length*vector(0,0,1), color=color.blue)
    neg_zaxis = z_axis.clone()
    neg_zaxis.axis *= -1

    xlabel = label(text="x", color=color.red, pos=x_axis.pos+x_axis.axis)

    return


while True:
    make_axes(20)
    pass
