'''
Created on 08-Oct-2019

@author: akash
'''
import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from datetime import datetime
from classes.construct import construct
from classes.queries import queries
from classes.calc_acc import calc_acc
from classes.bruteforce import bruteforce

if __name__ == "__main__":
    # creating object
    construct_object = construct()
    queries_object = queries()
    calc_acc_object = calc_acc()
    bruteforce_object = bruteforce()

    # defining the variables
    n = 10000
    d = 5000
    d_prime = 50
    m = 20
    L = 20
    D, labels_true = make_blobs(
        n_samples=n, n_features=d, centers=10, cluster_std=5, random_state=0)
    #mnist = fetch_mldata('MNIST original')
    #D = mnist.data
    # print len(D[1])

    k = 10
    pt = 50
    q = D[pt]
    k0 = int(k * max(np.log(n / k), (n / k)**(1 - float(m) / d_prime)))
    k1 = int(m * k * max(np.log(n / k), (n / k)**(1 - float(1) / d_prime)))

    bf_points = bruteforce_object.bruteforce(q, D, k)

    print("*************** To find top", k,
          "nearest points from", n, "points ***************")
    print("Configuration:")
    print("Ambient dimensionality \t\t\t\t\t\td =", d)
    print("Intrinsic dimensionality \t\t\t\t\td_prime =", d_prime)
    print("The number of simple indices \t\t\t\t\tm =", m)
    print("The number of composite indices \t\t\t\tL =", L)
    print("The number of points to retrieve for one composite index \tk0 =", k0)
    print("The number of points to visit for one composite index \t\tk1 =", k1)
    print("the query point \t\t\t\t\t\tq = ", pt)
    print("******************************************************************************\n")

    print("******************************************************************************")
    print("Construction\n")
    t_start = datetime.now()
    uvecs, trees, sorted_trees, q_projs = construct_object.CONSTRUCT(
        D, m, L, q, n)
    t_end = datetime.now()
    print("Construction Time: ", t_end - t_start)
    print("Done!")
    print("******************************************************************************\n")

    print("******************************************************************************")
    print("Algorithm 4 - PDCI (Lower bound)\n")
    l_k0 = 15 * k0 / 100
    l_k1 = 55 * k1 / 100
    print("k0=", l_k0)
    print("k1=", l_k1)
    t_start = datetime.now()
    pdci_points = queries_object.QUERY(q, uvecs, trees, sorted_trees,
                                       q_projs, D, l_k0, l_k1, k)
    t_end = datetime.now()
    print("Output:", list(pdci_points))
    print("Time:", t_end - t_start)
    print("Accuracy:", calc_acc_object.accuracy(pdci_points, bf_points))
    print("******************************************************************************\n")

    print("******************************************************************************")
    print("Algorithm 4 - PDCI (Middle)\n")
    m_k0 = 55 * k0 / 100
    m_k1 = 80 * k1 / 100
    print("k0=", m_k0)
    print("k1=", m_k1)
    t_start = datetime.now()
    pdci_points = queries_object.QUERY(q, uvecs, trees, sorted_trees,
                                       q_projs, D, m_k0, m_k1, k)
    t_end = datetime.now()
    print("Output:\n", list(pdci_points))
    print("Time:", t_end - t_start)
    print("Accuracy:", calc_acc_object.accuracy(pdci_points, bf_points))
    print("******************************************************************************\n")

    print("******************************************************************************")
    print("Algorithm 4 - PDCI (Upper bound)\n")
    print("k0=", k0)
    print("k1=", k1)
    t_start = datetime.now()
    pdci_points = queries_object.QUERY(
        q, uvecs, trees, sorted_trees, q_projs, D, k0, k1, k)
    t_end = datetime.now()
    print("Output:\n", list(pdci_points))
    print("Time:", t_end - t_start)
    print("Accuracy:", calc_acc_object.accuracy(pdci_points, bf_points))
    print("******************************************************************************\n")
