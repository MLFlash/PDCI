
import numpy as np
from heapq import heappush, heappop
from classes.calc_distance import calc_distance


class queries:
    def __init__(self):
        euclidean_object = calc_distance()
        pass

    def QUERY(self, q, uvecs, trees, sorted_trees, q_projs, D, k0, k1, k):
        '''
        Time Complexity:
        heapq.push() and heapq.pop(): O(log(m))
        k1 refers how many points popped from a heap
        k0 refers how many candidates a composite index can have

        in fact:

        '''
        n = D.shape[0]
        m = uvecs.shape[0]
        L = uvecs.shape[1]
        Cls = np.zeros((L, n))
        Sls = np.zeros(L, dtype=object)
        for l in range(L):  # L
            Sls[l] = set()
        Pls = np.zeros(L, dtype=object)
        for l in range(L):  # L
            Pls[l] = []

        for l in range(L):  # L * m * (log(n) + log(m))
            for j in range(m):
                #p_proj, pt = trees[j,l].query(q_projs[j,l], 0)
                p_proj, pt = self.query(sorted_trees[j, l], 0)
                priority = abs(p_proj - q_projs[j, l])
                heappush(Pls[l], (priority, pt, j, l, 0))

        count = 0
        for i in range(int(k1)):  # k1 * L * k0 * ((m+3)log(m) + log(n))
            for l in range(L):
                if len(Sls[l]) < k0:
                    cp_Pl = Pls[l][:]  # m
                    while(cp_Pl[0][4] == n - 1):  # m * log(m)
                        heappop(cp_Pl)
                    popped_pt = None
                    if len(cp_Pl) == 0:
                        popped_pt = heappop(Pls[l])[1]  # log(m)
                    else:
                        popped_pt = heappop(Pls[l])[1]  # log(m)
                        point, origin_j, origin_l, ith = cp_Pl[0][1:5]
                        # p_proj, pt = trees[origin_j,
                        # origin_l].query(q_projs[origin_j, origin_l], ith+1) #
                        # log(n)
                        p_proj, pt = self.query(
                            sorted_trees[origin_j, origin_l], ith + 1)
                        priority = abs(p_proj - q_projs[origin_j, origin_l])
                        heappush(Pls[l], (priority, pt, origin_j,
                                          origin_l, ith + 1))  # log(m)
                    Cls[l, popped_pt] += 1
                    if Cls[l, popped_pt] == 70 * m / 100:
                        # if Cls[l, popped_pt] == m:
                        Sls[l].add(popped_pt)
                    count += 1

        print("The number of points visisted:", count)
        for l in range(L):
            print("The number of points in " + str(l) +
                  "th candidate set:", len(Sls[l]))
        candidates = set()
        for l in range(L):
            candidates = candidates.union(Sls[l])
        print("The number of candidates:", len(candidates))
        candi_pt = []
        candi_eudist = []
        for pt in candidates:
            candi_pt.append(pt)
            candi_eudist.append(self.euclidean_object.euclidean_dist(D[pt], q))

        k_neighbours = []
        sorted_eudist = np.argsort(candi_eudist)
        i = 0
        while i < k:
            k_neighbours.append(candi_pt[sorted_eudist[i]])
            i += 1

        return np.array(k_neighbours)

    def QUERY2(self, q, uvecs, trees, D, k):
        n = D.shape[0]
        m = uvecs.shape[0]
        L = uvecs.shape[1]
        Cls = np.zeros((L, n))
        Sls = np.zeros(L, dtype=object)
        for l in range(L):  # L
            Sls[l] = set()
        q_projs = np.zeros((m, L))
        for j in range(m):  # m * L * d
            for l in range(L):
                # slow, need to remove loops
                q_projs[j, l] = np.dot(uvecs[j, l], q)

        count = 0
        for i in range(n):
            for l in range(L):
                for j in range(m):
                    p_proj, pt = trees[j, l].query(q_projs[j, l], i)
                    Cls[l, pt] += 1
                if Cls[l, pt] == 70 * m / 100:  # hack
                    Sls[l].add(pt)
            count += 1
            print(count)
            # FIXME: need stopping condition!!!

        print("The number of points visisted:", count)
        for l in range(L):
            print("The number of points in " + str(l) +
                  "th candidate set:", len(Sls[l]))

        candidates = set()
        for l in range(L):
            candidates = candidates.union(Sls[l])

        candi_pt = []
        candi_eudist = []
        for pt in candidates:
            candi_pt.append(pt)
            candi_eudist.append(self.euclidean_object.euclidean_dist(D[pt], q))

        k_neighbours = []
        sorted_eudist = np.argsort(candi_eudist)
        i = 0
        while i < k:
            k_neighbours.append(candi_pt[sorted_eudist[i]])
            i += 1

        return np.array(k_neighbours)
