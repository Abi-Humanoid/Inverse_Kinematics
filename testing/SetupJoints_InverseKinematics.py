from vpython import *
import numpy as np
# Uses Kajita matlab script as basis
#SetupBiped sets parameters of each joint. Child and sister empty as sister only relevant for top hip joint, and child not relevant for foot.
# Number is joint number, a is joint axis, q is joint velocity
class SetupBiped:
    def __init__(self, number, a, q, pos, rm, b = None, parent = None):
        self.number = number
        self.child = []
        self.sister = None
        self.a = a
        self.q = q
        self.pos=pos
        self.parent = parent
        self.b = b
        self.rm = rm #np.array([[1, 0, 0],[0,1,0],[0,0,1]])
       
        if self.parent is not None:
            self.parent.child.append(self)
            #self.tm_0_i = np.array([[1,0,0,self.pos.x-self.parent.pos.x],[0,1,0,self.pos.y-self.parent.pos.y],[0, 0, 1, self.pos.z-self.parent.pos.z],[0,0,0,1]])
        #if self.parent is None:
            #condition here

    
    def ForwardKinematics(self, joint_angle):
        # cant do dot product on 3x3 vector, so seperate operations, make into vector parent_RM_mult_b that is 1x3
        # equivalent to rm * b
        parent_rm_mul_b= vector(dot(self.parent.rm[0], self.b), dot(self.parent.rm[1], self.b), dot(self.parent.rm[2], self.b))
        self.pos = parent_rm_mul_b + self.parent.pos

        #Rodrigues formula
        eye = [[1,0,0],[0,1,0],[0,0,1]] #for rodrigues
        wedge = np.array([[0, -self.a.z, self.a.y], [self.a.z, 0, -self.a.x], [-self.a.y, self.a.x, 0]])#3x3
        squared = wedge.dot(wedge)
        e = np.array(eye + wedge*sin(joint_angle) + squared*(1-cos(joint_angle))) #R = eye(3) + w_wedge * sin(th) + w_wedge^2 * (1-cos(th));
        #print("e = ",e)
        
        #convert parent's rotation matrix (vector) to array so that dot product works
        rm_to_array = np.array([[self.parent.rm[0].x, self.parent.rm[0].y, self.parent.rm[0].z],[self.parent.rm[1].x, self.parent.rm[1].y,self.parent.rm[1].z],[ self.parent.rm[2].x, self.parent.rm[2].y, self.parent.rm[2].z]])
        self.rm =np.dot(rm_to_array, e)

        #convert back to make into array of vectors as used to update position, a vector
        row_1 = vector(self.rm[0,0], self.rm[0,1], self.rm[0,2])
        row_2 = vector(self.rm[1,0], self.rm[1,1], self.rm[1,2])
        row_3 = vector(self.rm[2,0], self.rm[2,1], self.rm[2,2])
        self.rm = [row_1,row_2,row_3]
        
        self.draw()

    def draw(self):
        joint_rad = 4
        #toggle visibility??
        joint_drawing = sphere(pos=self.pos, radius=joint_rad)
        if self.parent is not None:
            leg_drawing = curve([self.pos, self.parent.pos], radius = 1.5)

    
    def CalcVWerr(self, target): #do we need a target link or substitute as foot
        #calculate error in position
        perr = target.pos - self.pos
        print('perr',perr)
        #convert rotation matrices of self and target joint to matrices
        self_rm_array = np.array([[self.rm[0].x, self.rm[0].y, self.rm[0].z],[self.rm[1].x, self.rm[1].y,self.rm[1].z],[self.rm[2].x, self.rm[2].y, self.rm[2].z]])
        target_rm_array = np.array([[target.rm[0].x, target.rm[0].y, target.rm[0].z],[target.rm[1].x, target.rm[1].y,target.rm[1].z],[target.rm[2].x, target.rm[2].y, target.rm[2].z]])
        #error in rotation 
        print('self rm',self_rm_array)
        print('target rm', target_rm_array)
        #print('self rm trans',np.transpose(self_rm_array))
        Rerr = np.matmul(np.transpose(self_rm_array), target_rm_array)
        #print('Rerr',Rerr)

        #rot2omega - Transform rotation matrix into the corresponding angular velocity vector T.Sugihara, Humanoids 2009
        #uses Rerr to get error in angle (werr)
        el = np.array([[Rerr[2,1]-Rerr[1,2]], [Rerr[0,2] - Rerr[2,0]], [Rerr[1,0] - Rerr[0,1]]])
        
        norm_el = np.linalg.norm(el)
        #print('norm_el', norm_el)

        if norm_el > 2^(-52):
            #print('tan norm_el', atan2(norm_el, np.trace(Rerr)-1))
            
            w = atan2(norm_el, np.trace(Rerr)-1)/norm_el * el
            #print('1, w', w)
        elif Rerr[0,0]> 0 and Rerr[1,1] >0 and Rerr[2,2] > 0:
            w = np.array[0,0,0]
            print('2, w', w)
        else:
            w = pi/2 * np.array([[Rerr[0,0] +1], [Rerr[1,1] +1], [Rerr[2,2]+1]])
            print('3, w', w)
        print('w',w)
        print('self rm array',self_rm_array)
        #use angular velocity vector to calculate error in angle
        werr = np.matmul(self_rm_array, w)
        print('werr',werr)

        #put into 6x1 array, change perr from vector
        err = np.array([perr.x, perr.y, perr.z, werr[0,0], werr[1,0], werr[2,0]])

        print('err',err)
        #return both errors
        return err

    def CalcJacobian(self):
        #jacobian is 6x6
        J = np.zeros((6,6))
        joint_array = np.array([self, self.child, self.child.child, self.child.child.child, self.child.child.child.child, self.child.child.child.child.child])
        print('self rm', self.rm)
        # dont need to do joint 1, so range is 6 joints, for loop doesn't run for n = 7
        for n in range(6):
            #iterate through each in route from body to target link, which is usually the foot
            joint = joint_array[n]
            print('joint',joint.number)
            print('joint r,',joint.rm)
            print('joints a,',joint.a)
            # a = joint.rm * joint.a (joint axis vector in world frame)
            a = vector(dot(joint.rm[0], joint.a), dot(joint.rm[1], joint.a), dot(joint.rm[2], joint.a))
            print('a',a)
            #need array to append into Jacobian
            a_to_array = np.array([a.x, a.y, a.z])
            #print('a',a_to_array)
            cross_product = cross(a, self.child.child.child.child.child.pos - joint.pos)
            print('minus ', self.child.child.child.child.child.pos - joint.pos)
            print('cross_product',cross_product)
            
            cross_product_array = np.array([cross_product.x, cross_product.y, cross_product.z])
            print('cross into array',cross_product_array)
            #all rows in column n

            column = np.append([cross_product_array], [a_to_array])
            print('column', column)
            J[:,n] = np.transpose(column) #right notation for matrix, or use np.array?
        
        J = np.matrix(J)
        print('J', J)
        return J

    def InverseKinematics(self, target):
        #finds links from self through to foot
        #while self.number > route.len():
        #    route.append(route.len() + 1)

        #update all joints 
        # what to do with joint 1????!!!! Still need to update position and rotation of base j1
        joint_array = np.array([self, self.child, self.child.child, self.child.child.child, self.child.child.child.child, self.child.child.child.child.child])
        
        for joint in joint_array:
            joint.ForwardKinematics(0)
        
        #calculate errors
        err = self.CalcVWerr(target)
        print('norm of err', np.linalg.norm(err))
        #for loop to break at error
        for n in range(1,10): #10 iterations for numerical answer
            if np.linalg.norm(err) < 10^(-6):
                break

            #calculate Jacobian
            J = self.CalcJacobian()

            #calculate adjustments - delta q - of joint angles based on errors in position and attitude
            set_lambda = 0.9
            # eq 2.77, inverse of eq 2.75. J-1 * [vectors of end effector speed]
            print('J inv',np.linalg.inv(J))
            dq1 = np.divide(np.linalg.inv(J), err)
            dq = np.multiply(set_lambda, dq1)

            #update joint velocity of each joint through addition of q + dq
            for joint in joint_array: #length of base to foot
                idx = 0
                joint.q = joint.q + dq[idx]
                idx = idx + 1
            
            #update ForwardKinematics again for all joints
            for joint in joint_array:
                joint.ForwardKinematics(0)

            #calc error again until satisfies 
            err = self.CalcVWerr(target)

            return 
    



# setting a, joint axis vector (roll, pitch, yaw)
UX = vector(1,0,0)
UY = vector(0,1,0)
UZ = vector(0,0,1)

""""
j1.pos = vector(67, 86, 0)
j2.pos = vector(50, 86, 0)
j3.pos = vector(50, 78, 0)
j4.pos = vector(50, 78, 0)
j5.pos = vector(50, 44, 0)
j6.pos = vector(50, 19, 0)
j7.pos = vector(50, 0, 0)

j8.pos = vector(76, 86, 0)
j9.pos = vector(76, 78, 0)
j10.pos = vector(84, 78, 0)
j11.pos = vector(84, 44, 0)
j12.pos = vector(84, 19, 0)
j13.pos = vector(84, 0, 0)
"""
ex = vector(1,0,0) #vector(1,0,0)
ey = vector(0,1,0) #vector(0,0,1)
ez = vector(0,0,1) #vector(0,-1,0)
eye_rm = [ex, ey, ez] #x, y, z

#joint 1 is body, increasing joint no = down right leg, j7 is foot
#Axis as defined in VPython setup
#Need to make b a parameter from initial setup
j1 = SetupBiped(1, UY, 0, vector(67, 86, 0), eye_rm )
j2 = SetupBiped(2, UY, 0, vector(58, 86, 0), eye_rm, vector(-9,0,0),  j1)
j3 = SetupBiped(3, UZ, 0, vector(58, 78, 0),  eye_rm, vector(0, 78-86,0),j2)
j4 = SetupBiped(4, UX, 0, vector(50, 78, 0), eye_rm,vector(50-58,0,0), j3)
j5 = SetupBiped(5, UX, 0, vector(50, 44, 0),  eye_rm,vector(0,44-78,0), j4)
j6 = SetupBiped(6, UX, 0, vector(50, 19, 0),  eye_rm, vector(0, 19-44,0),j5)
j7 = SetupBiped(7, UZ, 0, vector(50, 0, 0),  eye_rm, vector(0, -19,0),j6)

#Left leg going down, j13 is foot
j8 = SetupBiped(8, UY, 0, vector(76, 86, 0), eye_rm, vector(76-67,0,0),j1)
j9 = SetupBiped(9, UZ, 0, vector(76, 78, 0), eye_rm, vector(0,78-86,0),j8)
j10 = SetupBiped(10, UX, 0, vector(84, 78, 0), eye_rm, vector(84-76,0,0), j9)
j11 = SetupBiped(11, UX, 0, vector(84, 44, 0), eye_rm, vector(0,44-78,0), j10)
j12 = SetupBiped(12, UX, 0, vector(84, 19, 0), eye_rm, vector(0,19-44,0),j11)
j13 = SetupBiped(13, UZ, 0, vector(84, 0, 0), eye_rm, vector(0,-19,0), j12)

#** two children of body: left hip, right hip. Instead of one child and one sister for joint 2**
j1.child = [j2, j8] 

#j2.sister = j8
j2.child = j3
#right leg
j3.child = j4
j4.child = j5
j5.child = j6
j6.child = j7
#left leg
j8.child = j9
j9.child = j10
j10.child = j11
j12.child = j13


j1.draw()
j2.draw()
j3.draw()
j4.draw()
j5.draw()
j6.draw()
j7.draw()
j8.draw()
j9.draw()
j10.draw()
j11.draw()
j12.draw()
j13.draw()
