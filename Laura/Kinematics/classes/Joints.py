from Joint import *

"""
Joint*s* class
Class that encapsulates all of ABI's joints
to be passed around for processing
"""

class Joints:
    def __init__(self):
        self.joints = []
    
    """
    Gets a list of joint detail dictionaries and initialises them
    """
    def initialiseJoints(self, jointsData):
        # Initialise all joint details
        for jointData in jointsData:
            self.joints.append(Joint(
                jointData["number"],
                jointData["a"],
                jointData["q"],
                jointData["pos"],
                jointData["rm"],
                jointData["b"]
            ))
        
        # Link parent and children joints together
        for jointData in jointsData:
            if len(jointData["child"]) > 0:
                for jointChildIndex in jointData["child"]:
                    self.getJoint(jointData["number"]).addChild(self.getJoint(jointChildIndex))
    
    def getJoint(self, number):
        return self.joints[number - 1]