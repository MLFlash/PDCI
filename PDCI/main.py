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
from visualization.scatter_plot import scatter_plot
from sklearn.datasets import fetch_openml


if __name__ == "__main__":
    # creating object
    construct_object = construct()
    queries_object = queries()
    calc_acc_object = calc_acc()
    bruteforce_object = bruteforce()
    scatter_plot_object = scatter_plot()

    # defining the variables
    n = 100
    ambient_dimensionality = 50
    Intrinsic_dimen = 50
    simple_indice = 20
    composite_indice = 20
    D, labels_true = make_blobs(
        n_samples=n, n_features=ambient_dimensionality, centers=10, cluster_std=5, random_state=0)
    #mnist = fetch_openml('mnist_784')
    #D = mnist.data
    # print(len(D[1]))
    # For understanding ploting of data points and query point
    Y, labels_true = make_blobs(
        n_samples=n, n_features=ambient_dimensionality, centers=10, cluster_std=5, random_state=5)
    print("Scatter Plot", scatter_plot_object.scatter_plot(D, Y))

    k = 10
    pt = 50
    q = D[pt]
    k0 = int(k * max(np.log(n / k), (n / k) **
                     (1 - float(simple_indice) / Intrinsic_dimen)))
    k1 = int(simple_indice * k * max(np.log(n / k), (n / k)
                                     ** (1 - float(1) / Intrinsic_dimen)))

    bf_points = bruteforce_object.bruteforce(q, D, k)

    print("*************** To find top", k,
          "nearest points from", n, "points ***************")
    print("Configuration:")
    print("Ambient dimensionality \t\t\t\t\t\td =", ambient_dimensionality)
    print("Intrinsic dimensionality \t\t\t\t\td_prime =", Intrinsic_dimen)
    print("The number of simple indices \t\t\t\t\tm =", simple_indice)
    print("The number of composite indices \t\t\t\tL =", composite_indice)
    print("The number of points to retrieve for one composite index \tk0 =", k0)
    print("The number of points to visit for one composite index \t\tk1 =", k1)
    print("the query point \t\t\t\t\t\tq = ", pt)
    print("******************************************************************************\n")

    print("******************************************************************************")
    print("Construction\n")
    t_start = datetime.now()
    uvecs, trees, sorted_trees, q_projs = construct_object.CONSTRUCT(
        D, simple_indice, composite_indice, q, n)
    t_end = datetime.now()
    print("Construction Time: ", t_end - t_start)
    print("Done!")
    print("******************************************************************************\n")

    print("******************************************************************************")
    print("Algorithm- PDCI\n")
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
