from typing import List
from Matrix import *

class Vector(Matrix):
    def __init__(self, list):
        self.rows = 1
        self.cols = len(list)
        if self.verifyVector() is True:
            self.matrix = list
    
    def verifyVector(self):
        return type(list[0]) is not List