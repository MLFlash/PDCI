'''
Created on 08-Oct-2019

@author: akash
'''


class Node():
    def __init__(self, proj, point, parent=None):
        self.proj = proj
        self.points = []
        self.points.append(point)
        self.parent = parent
        self.left = None
        self.right = None
        self.balance = 0

    def has_left(self):
        return True if self.left != None else False

    def has_right(self):
        return True if self.right != None else False

    def is_left(self):
        return True if self == self.parent.left else False

    def is_right(self):
        return True if self == self.parent.right else False

    def is_root(self):
        return True if self.parent == None else False

    def is_leaf(self):
        return True if self.left == None and self.right == None else False
