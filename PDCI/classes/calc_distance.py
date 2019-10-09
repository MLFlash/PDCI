'''
Created on 08-Oct-2019

@author: akash
'''
import numpy as np


class calc_distance:
    def __init__(self):
        pass

    def euclidean_dist(self, p, q):
        '''
        Time Complexity: O(d)
        '''
        return np.dot(p - q, p - q)**0.5
