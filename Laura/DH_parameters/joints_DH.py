import numpy as np
import math
from matplotlib import pyplot as plt
from numpy.core.numeric import cross

class joint:
    def __init__(self,a, alpha, d, theta0,parent=None) -> None:
        #can define a joint using 4 parameters if they are defined following DH convention
        #zi intersects the axis of rotation (revolute joint)
        #xi-1 intersects zi perpendicularly
        #a,alpha,d and theta0 remain constant (depend on the design of the robot)
        self.q=0
        self.a=a
        self.alpha=alpha
        self.d=d
        self.theta0=theta0
        self.theta=self.theta0+self.q
        self.tm=np.array([1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]).reshape(4,4)
        self.tm=self.transformationMatrix()
        #if the joint has a parent (joint above)
        self.parent=parent
        self.child=[]
        if self.parent is not None:
            #if it has a parent, then the parent's child is this joint
            self.parent.child.append()
            #doing it with append for the case when joint has multiple children, for example hip has left and right children

        pass

    def transformationMatrix(self):
        a=self.a
        alpha=self.alpha
        d=self.d
        theta=self.theta

        Dx=np.array([1,0,0,a,0,1,0,0,0,0,1,0,0,0,0,1]).reshape(4,4)
        Rx=np.array([1,0,0,0,0,math.cos(alpha),-math.sin(alpha),0,0,math.sin(alpha),math.cos(alpha),0,0,0,0,1]).reshape(4,4)
        Dz=np.array([1,0,0,0,0,1,0,0,0,0,1,d,0,0,0,1]).reshape(4,4)
        Rz=np.array([math.cos(theta),-math.sin(theta),0,0,math.sin(theta),math.cos(theta),0,0,0,0,1,0,0,0,0,1]).reshape(4,4)
        #it seems matrix multiplication is done with the dot function 
        #multiply the matrices in the order given (translate in x, rotate about x, translate in z, rotate about z)
        product1=np.matmul(Dx,Rx)
        product2=np.matmul(Dz,Rz)
        tm=np.matmul(product1,product2)
        self.tm=tm

        """
        print("product 2: {}".format(product2))
        print("DZ: {}".format(Dz))
        print("RZ: {}".format(Rz))
        print("Transformation matrix: {}".format(tm))
        """
        return tm


    def updateTheta(self,new_q):
        self.q=new_q
        self.theta=self.theta0+self.q 
        self.transformationMatrix()

class initial_joint_left(joint):
    def __init__(self,x,y,z,theta0) -> None:
        #get the 
        self.theta0=theta0
        self.x=x
        self.y=y
        self.z=z
        self.q=0
        self.theta=self.theta0+self.q
        self.tm=tm=np.array([math.cos(theta0),-math.sin(theta0),0,x,0,0,1,y,-math.sin(theta0),-math.cos(theta0),0,z,0,0,0,1]).reshape(4,4)
        self.tm=self.transformationMatrix()
        
        pass

    def transformationMatrix(self):
        x=self.x
        y=self.y
        z=self.z
        theta=self.theta
        #transformation matrix here is different, confirm that the one going from the first joint to the hip is this
        tm=np.array([math.cos(theta),-math.sin(theta),0,x,0,0,1,y,-math.sin(theta),-math.cos(theta),0,z,0,0,0,1]).reshape(4,4)
        self.tm=tm
        #print(tm)
        return tm

    """
    def updateTheta(self,new_q):
        self.q=new_q
        self.theta=self.theta0+self.q 
        self.transformationMatrix()
        """

class initial_joint_right(joint):
    def __init__(self,x,y,z,theta0) -> None:
        #get the 
        self.theta0=theta0
        self.x=x
        self.y=y
        self.z=z
        self.q=0
        self.theta=self.theta0+self.q
        self.tm=tm=np.array([-math.cos(theta0),math.sin(theta0),0,x,0,0,1,y,math.sin(theta0),math.cos(theta0),0,z,0,0,0,1]).reshape(4,4)
        self.tm=self.transformationMatrix()
        
        pass

    def transformationMatrix(self):
        x=self.x
        y=self.y
        z=self.z
        theta=self.theta
        #transformation matrix here is different, confirm that the one going from the first joint to the hip is this
        tm=np.array([math.cos(theta),-math.sin(theta),0,x,0,0,1,y,-math.sin(theta),-math.cos(theta),0,z,0,0,0,1]).reshape(4,4)
        self.tm=tm
        #print(tm)
        return tm


    """
    def updateTheta(self,new_q):
        self.q=new_q
        self.theta=self.theta0+self.q 
        self.transformationMatrix()
        """

class leg:

    def __init__(self,joints) -> None:
        self.joints=joints
        #array with the matrices to the frame of the com
        self.T_matrix_to_com=self.get_T_matrix(self.joints)
    
    def get_T_matrix(self,joints):
        #start with the t_matrix that goes from start to center of mass (COM)
        T_matrix_to_com=[]
        i=0
        for element in joints:
            if i==0:
                #add to the array
                current_t_matrix_com=element.tm
            else:
                #then multiply the transformation matrix of the current joint with the ones from the previous ones
                current_t_matrix=element.tm
                #each one has the tmatrix from its frame to com, only need to multiply with the previous one
                previous_T_matrix_com=T_matrix_to_com[-1]
                current_t_matrix_com=np.matmul(previous_T_matrix_com,current_t_matrix)
            i+=1
            #print("i:{}, T matrix:{}".format(i,current_t_matrix_com))
            T_matrix_to_com.append(current_t_matrix_com)
        
        return T_matrix_to_com

    
    def forwardKinematics(self,new_angles_array):
        #new angles array must be in order for the kinematic chain
        #if angle is the same as before, write "None"

        #update the thetas for all the elements
        position=0
        for element in self.joints:
            new_q=new_angles_array[position]
            if(new_q!=None):
                element.updateTheta(new_q)

            position+=1
        T_matrix_to_com=self.get_T_matrix(self.joints)
        #return  T_matrix_to_com
        #drawing it for now
        self.drawChain(T_matrix_to_com)
        pass

    def drawChain(self,T_matrix_to_com):
        #Paint a node at the position of the xyz of all the transformation matrices with respect to the com
        x=[]
        y=[]
        z=[]
        print("Drawing")
        
        positions=T_matrix_to_com
        #t matrix includes rotation and position. Only interested in the position for plotting
        for tm in positions:
            #tm=element.tm
            x.append(tm[0,3])
            y.append(tm[1,3])
            z.append(tm[2,3])
        
        ax.scatter(x, y, z, c='red', s=100)
        ax.plot(x, y, z, color='black')
        #plt.plot()

        pass

    def jacobian(self):
        T_matrix_to_com=self.get_T_matrix(self.joints)
        #defining Jacobian with respect to the end effector (or joint 6 for now)
        #in the frame of the center of mass
        tm_from_end_to_com=T_matrix_to_com[-1]
        z_i_in_com=np.array([[None],[None],[None]])
        z_i_cross_riE=np.array([[None],[None],[None]])
        for element in T_matrix_to_com:
            #need to get the 3rd column of the matrix (that's zi)
            zi=element[0:3,2]
            #need to get the t matrix from end to frame i
            #the inverse of the transformation matrix is its transpose
            tm_from_com_to_i=np.transpose(element)
            tm_from_end_to_i=np.matmul(tm_from_com_to_i,tm_from_end_to_com)
            
            #the vector riE in frame i is the 4th column of that matrix
            riE_in_i=tm_from_end_to_i[0:3,3]
            #we need to riE in frame com, so need to multiply by rotation matrix R from i to com
            R_i_to_com=element[0:3,0:3]
            riE_in_com=np.matmul(R_i_to_com,riE_in_i)
            #the first 3 rows are going to be the cross product of z and r
            cross_i=np.cross(zi,riE_in_com)
            #append the results
            print("z_i_in_com:{}".format(z_i_in_com))
            print("z i: {}".format(zi.reshape(-1, 1)))

            z_i_in_com=np.concatenate((z_i_in_com,zi.reshape(-1, 1)),axis=1)
            z_i_cross_riE=np.concatenate((z_i_cross_riE,cross_i.reshape(-1, 1)),axis=1)
        z_i_in_com=z_i_in_com[0:,1:]
        z_i_cross_riE=z_i_cross_riE[0:,1:]
        print("Zi={}".format(z_i_in_com))
        print("cross={}".format(z_i_cross_riE))

        

#Set up the figure

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
fig = plt.figure()

ax = fig.add_subplot(projection="3d")
ax.set_xlim3d(-0.4,0.4)
ax.set_ylim3d(-1.2,1.2)
ax.set_zlim3d(-0.8,0.1)
ax.set(xlabel='X axis', ylabel='Y axis', zlabel='Z axis')

#Set up the joints (confirm in cad!)
AL1=0.05
DL1=0.04
AL3=0.26
AL4=0.18
AL5=0.08
AL6=0.1
DE=0

j1_l=joint(AL1,math.pi/2,-DL1,math.pi/2)
j2_l=joint(0,-math.pi/2,0,math.pi/2)
j3_l=joint(AL3,0,0,0)
j4_l=joint(AL4,0,0,0)
j5_l=joint(AL5,math.pi/2,0,0)
#j6=joint(AL6,0,DE,0)

XLEFT=0.1
YLEFT=0
ZLEFT=0
THETA0_left=0

left_hip=initial_joint_left(XLEFT,YLEFT,ZLEFT,THETA0_left)

#define left leg
left_leg=leg([left_hip,j1_l,j2_l,j3_l,j4_l,j5_l])
#Calculate angles and paint the left leg
left_leg.forwardKinematics([0,0,0,0,0,0,0])


#right leg
AR1=0.05
DR1=0.04
AR3=0.26
AR4=0.18
AR5=0.08
AR6=0.1
DE=0
#the way the joints are defined means that everything would be the same, except for the initial joint
j1_r=joint(AR1,math.pi/2,-DR1,math.pi/2)
j2_r=joint(0,-math.pi/2,0,math.pi/2)
j3_r=joint(AR3,0,0,0)
j4_r=joint(AR4,0,0,0)
j5_r=joint(AR5,math.pi/2,0,0)


#initial joint right leg
XRIGHT=-0.1
YRIGHT=0
ZRIGHT=0
THETA0_RIGHT=0
right_hip=initial_joint_right(XRIGHT,YRIGHT,ZRIGHT,THETA0_RIGHT)
#define right leg
right_leg=leg([right_hip,j1_r,j2_r,j3_r,j4_r,j5_r])
#Calculate angles and paint the left leg
right_leg.forwardKinematics([0,0,0,0,0,0,0])

plt.show()
left_leg.jacobian()




