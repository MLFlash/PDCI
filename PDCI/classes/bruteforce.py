
'''
Created on 08-Oct-2019

@author: akash
'''

import numpy as np
from classes.calc_distance import calc_distance


class bruteforce:
    def __init__(self):
        self.calc_distance_object = calc_distance()

    def bruteforce(self, q, dataset, k):
        '''
        Time complexity: O(dn + nlog(n))
        '''
        dataset_eu_dist = []
        for i in range(len(dataset)):
            dataset_eu_dist.append(
                self.calc_distance_object.euclidean_dist(q, dataset[i]))
        return np.argsort(dataset_eu_dist)[:k]
