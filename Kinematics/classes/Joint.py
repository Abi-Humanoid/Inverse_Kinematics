
"""
Joint class
Takes the parameters:
  - number: number of joint
  - axis: axis of joint
"""
class Joint:
    def __init__(self, number, a, q, pos, rm, b, parent = None, sister = None):
        """ Initialising joint properties """
        self.number = number  # number
        self.a = a            # axis
        self.q = q            # velocity
        self.pos = pos        # position (in world coordinates)
        self.rm = rm          # rotation matrix OR orientation
        self.b = b            # relative position
        self.parent = parent  # parent of this joint
        self.sister = None    # sister of this joint; set to None because it is currently unused?
        self.child = []       # children of this joint

        self.vpos = vector(self.pos) ### CHECK THIS ONE ###

        """ Dealing with parents """
        if self.parent is not None:
            self.parent.addChild(self)
            # include transition matrix from 0 to I here

    """ Mutators for encapsulation purposes """
    def addChild(self, childJoint):
        self.child.append(childJoint)  # adds the child joint to this joint
        childJoint.parent = self       # makes this joint the child's parent joint
