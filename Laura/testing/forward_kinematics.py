# Testing initial forward kinematics commands on only the knee joint

from vpython import *
from time import *
import numpy as np

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
                axis=vector(1,0,0), radius=joint_rad)

rjoint_2 = sphere(pos=rjoint_3.pos+vector(2*joint_rad,0,0),
                radius=joint_rad)

rjoint_1 = sphere(pos=rjoint_2.pos+vector(0,2*joint_rad,0),
                radius=joint_rad)

body = box(pos=rjoint_1.pos+vector(joint_rad+bod_size[0]/2,0,0),
                size=vector(bod_size[0],bod_size[1],bod_size[2]))

def relative_pos(current, parent): #joint position relative to *parent*
    b = current - parent
    return b

######## finding position of current joint ####
parent = rjoint_3
# set rotation matrix of parent (may be identity)
ex = vector(1,0,0) #vector(1,0,0)
ey = vector(0,1,0) #vector(0,0,1)
ez = vector(0,0,1) #vector(0,-1,0)
parent_RM = [ex, ey, ez] #x, y, z 
#print("A[:,0] =",parent_RM[:,0]) # First Column
b1 = relative_pos(rjoint_4.pos,parent.pos)
print("rjoint_4 pos = ",rjoint_4.pos) 
#uLINK(mom).R * uLINK(j).b
# cant do dot product on 3x3 vector, so seperate operations, make into vector parent_RM_mult_b that is 1x3
parent_RM_mult_b = vector(dot(parent_RM[0], b1), dot(parent_RM[1], b1), dot(parent_RM[2], b1))

#uLINK(j).p = uLINK(mom).R * uLINK(j).b + uLINK(mom).p;
rjoint_4.pos = parent_RM_mult_b + parent.pos 

b2 = relative_pos(rleg_3.pos,parent.pos)
parent_RM_mult_b2 = vector(dot(parent_RM[0], b2), dot(parent_RM[1], b2), dot(parent_RM[2], b2))
rleg_3.pos = parent_RM_mult_b2 + parent.pos 

print("parentRM = ",parent_RM) # all
print("b1 = ",b1) # three
print("dot = ",dot(parent_RM[0], b1)) 
print("parent_RM_mult_b = ",parent_RM_mult_b)
print("parent pos = ",parent.pos) 
print("rjoint_4 pos = ",rjoint_4.pos) 

######## finding attitude of current joint #### #uLINK(j).R = uLINK(mom).R (3x3) * Rodrigues(uLINK(j).a, uLINK(j).q) (3x3); a is joint axis vector relative to parent, q is joint angle

# setting a, joint axis vector (roll, pitch, yaw)
UX = vector(1,0,0)
UY = vector(0,1,0)
UZ =vector(0,0,1)

print("Ux one= ",UX.x)
eye = [[1,0,0],[0,1,0],[0,0,1]] #for rodrigues

def Rodrigues(joint_axis, joint_angle): #rotation matrix from angular velocity
    #do we need norm?
    #norm_axis = norm(joint_axis) 
    th = joint_angle
    wedge = np.array([[0, -joint_axis.z, joint_axis.y], [joint_axis.z, 0, -joint_axis.x], [-joint_axis.y, joint_axis.x, 0]])#3x3
    print("wedge= ",wedge) 
    squared = wedge.dot(wedge)
    e = np.array(eye + wedge*sin(th) + squared*(1-cos(th))) #R = eye(3) + w_wedge * sin(th) + w_wedge^2 * (1-cos(th));
    print("wedge*sin= ",wedge*sin(th)) 
    print("wedg*wedge*cos= ",squared*(1-cos(th)))
    return e

def RMtoArray(vect_list): #make into array so can multiply as array
    toArray = np.array([[vect_list[0].x, vect_list[0].y,vect_list[0].z],[vect_list[1].x, vect_list[1].y,vect_list[1].z],[vect_list[2].x, vect_list[2].y,vect_list[2].z]])
    return toArray

#rodrigues takes a (relevant UX, UY, UZ) and q is joint angle, from Inverse Kinematics
q = 0
current_RM = np.dot(RMtoArray(parent_RM), Rodrigues(UX, q)) # x, y, z; matrix not transposed
current_RM = current_RM.transpose() #transpose so appropriate for indexing for euler

print("current RM= ",current_RM)
print("current RM 0 2= ",current_RM[0, 2])

if (current_RM[0, 2] == 1) | (current_RM[0, 2] == -1): 
    # special case 
    yaw = 0
    #set arbitrarily
    dlt = np.arctan2(current_RM[0, 1], current_RM[0, 2])
    if current_RM[0, 2] == -1: 
        pitch = np.pi/2 
        roll = yaw + dlt
    else:
        pitch = -np.pi/2 
        roll = -yaw + dlt
else:
    pitch = -np.arcsin(current_RM[0, 2])
    roll = np.arctan2(current_RM[1, 2]/np.cos(pitch), current_RM[2, 2]/np.cos(pitch)) 
    yaw = np.arctan2(current_RM[0, 1]/np.cos(pitch), current_RM[0, 0]/np.cos(pitch)) 
    
test1 = [vector(1,2,3), vector(4,5,6), vector(7,8,9)]
b1 = vector(-9,0,0)
test1 = np.array([[test1[0].x, test1[0].y, test1[0].z],[test1[1].x, test1[1].y,test1[1].z],[test1[2].x,test1[2].y, test1[2].z]])
test1 = np.transpose(test1)   
row_1 = vector(test1[0,0], test1[0,1], test1[0,2])
row_2 = vector(test1[1,0], test1[1,1], test1[1,2])
row_3 = vector(test1[2,0], test1[2,1], test1[2,2])
test1= [row_1,row_2,row_3]
testing= vector(dot(test1[0], b1), dot(test1[1], b1), dot(test1[2], b1))
print("testing",testing)

Euler_matrix = [roll, pitch, yaw]
print("Euler Matrix= ",Euler_matrix)

rjoint_4.rotate(angle=roll, 
        axis=UX)
        
# roll - z  -> y
rleg_3.rotate(angle=roll, 
        axis=UX)    

#pitch - y  -> x    
rleg_3.rotate(angle=pitch, 
        axis=UY)    
#yaw - x  -> z       
rleg_3.rotate(angle=yaw, 
        axis=UZ)   


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

