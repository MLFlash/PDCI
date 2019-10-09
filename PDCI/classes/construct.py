'''
Created on 08-Oct-2019

@author: akash
'''
import numpy as np
from classes.AVLTree import AVLTree


class construct:
    def __init__(self):
        pass

    def CONSTRUCT(self, D, m, L, q, n):
        '''
        Time complexity: O(mL(nd+nlogn))
        Construct uvecs, projs and trees: mLd + mLnd + mLnlogn = m*L*(nd+nlogn)
        '''
        dims = D.shape[1]
        uvecs = np.zeros((m, L), object)
        trees = np.zeros((m, L), object)

        for j in range(m):
            for l in range(L):
                v = np.random.normal(0, 1, dims)
                mag = np.dot(v, v)**0.5
                uvec = v / mag
                uvecs[j, l] = uvec
                projs = np.dot(D, uvec)
                trees[j, l] = AVLTree()
                for i in range(len(projs)):
                    trees[j, l].insert(projs[i], i, trees[j, l].root)

        sorted_trees = np.zeros((m, L), object)
        q_projs = np.zeros((m, L))
        for j in range(m):  # m * L * d
            for l in range(L):
                q_projs[j, l] = np.dot(uvecs[j, l], q)
                sorted_trees[j, l] = trees[j, l].sort_tree(q_projs[j, l], n)

        return uvecs, trees, sorted_trees, q_projs
