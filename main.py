"""
End-of-the line routines for processing data and producing plots for the 
sake of specific tasks, often involving comparing the properties of different
clustering algorithms.

Functions:
time_pair_algorithm:    Generates a graph showing the run times of 
                        slow_closest_pair and fast_closest_pair
                        
    
    
Last edited on June 12, 2017
Most recent author:  Pat Kohl
"""

import numpy as np
import time
import alg_cluster
import matplotlib.pyplot as plt
import alg_p3_core      
import alg_clusters_matplotlib
import alg_p3_viz


def time_pair_algorithms(min_points, max_points, step):
    """
    Generates a graph showing the run time of the slow_closest_pair and
    fast_closest_pair algorithms as a function of the number of clusters being
    searched.
    
    Input:  Minimum and maximum number of clusters to search, and step size.
    
    Output: Plot printed to console.
    """
    
    timing_list_slow = []
    timing_list_fast = []
    
    # generate points on graph
    for idx in range(min_points, max_points, step):
    
        # produce a set of clusters with random positions
        cluster_list = alg_p3_core.gen_random_clusters(idx)
        
        # time the slow_closest_pair algorithm
        start_time = time.clock()
        alg_p3_core.slow_closest_pair(cluster_list)
        timing_list_slow.append(time.clock() - start_time)
        
        # time the fast_closest_pair algorithm
        start_time = time.clock()
        alg_p3_core.fast_closest_pair(cluster_list)
        timing_list_fast.append(time.clock() - start_time)

    # generate scatter plot with polynomial fits
    xvals = range(min_points, max_points, step)

    slow_poly = np.poly1d(np.polyfit(xvals, timing_list_slow, 2))
    fast_poly = np.poly1d(np.polyfit(xvals, timing_list_fast, 1))

    plt.plot(xvals, slow_poly(xvals))
    plt.plot(xvals, fast_poly(xvals))
    plt.scatter(xvals, timing_list_slow, label='slow_closest_pair')
    plt.scatter(xvals, timing_list_fast, label='fast_closest_pair')
    plt.xlabel('Number of initial clusters', size = 'xx-large')
    plt.ylabel('Runtime, in seconds', size = 'xx-large')
    plt.title('Speed of clustering algorithms vs. number of initial clusters, \
              on desktop Python', size = 'xx-large')
    plt.legend(loc = 'upper right', fontsize = 'xx-large')
    plt.legend(loc='upper right')
    plt.show()


def basic_clustering(num_counties, num_clusters, cluster_alg, iterations = 0):
    """
    Generates a plot of the US with counties displayed in clusters formed
    using either the k-means or hierarchical clustering algorithms.  County
    area is proportional to county population.
    
    Inputs:
    num_counties:  Number of counties in the dataset to be used
                   (see options in alg_p3_viz).
    num_clusters:  Number of clusters to form.
    cluster_alg:   Algorithm to use to form clusters.  Can be string
                   "kmeans" or "hierarch".
    iterations:    If using k-means clustering, number of iterations to apply.
    
    Output:        Prints a plot to the console.
    """
    do_plot = True
    data_table = alg_p3_viz.load_data_table(num_counties)

    # build up a list of cluster objects using data from the data table
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], 
                                                  line[2], line[3], line[4]))

    # if cluster_alg == "kmeans", use the k-means algorithm to create 
    # num_clusters clusters using iterations iterations, then display a plot
    
    if cluster_alg == "kmeans":
        cluster_list = alg_p3_core.kmeans_clustering(singleton_list,
                                   num_clusters, iterations)
    elif cluster_alg == "hierarch":
        cluster_list = alg_p3_core.hierarch_clustering(singleton_list,
                                   num_clusters)
    else:
        print("Invalid algorithm type.  Valid types are kmeans and hierarch.")
        do_plot = False
    
    # draw the clusters using matplotlib
    if do_plot:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)


def distortion_vs_algorithm(num_counties, min_clusters, max_clusters, 
                            iterations):
    """
    Generates clusterings with numbers of clusters between min_clusters and
    max_clusters (inclusive), using k-means and hierarchical clustering
    algorithms.  Calculates distortion for each clustering.  Plots distortion
    vs. number of clusters.
    
    Note:  Step size is currently fixed at one cluster.
    
    Inputs:
    num_counties:  Number of counties in the dataset to be used
                   (see options in alg_p3_viz).
    min_clusters:  Minimum number of clusters to form and test.
    max_clusters:  Maximum number of clusters to form and test.
    iterations:    If using k-means clustering, number of iterations to apply.
    
    Output:        Prints a plot to the console.
    """
    
    # generate list of distortions
    yvals = alg_p3_core.dist_vs_clusters(num_counties, min_clusters, 
                                               max_clusters, iterations)
    
    # create plot
    xvals = range(min_clusters, max_clusters + 1)
    plot_title = 'Distortion vs. number of clusters, ' + str(num_counties) + \
                 ' county dataset, on desktop Python'
    plt.plot(xvals, yvals[0], label='k-means clustering')
    plt.plot(xvals, yvals[1], label='hierarchical clustering')
    plt.xlabel('Number of clusters', size = 'xx-large')
    plt.ylabel('Distortion', size = 'xx-large')
    plt.title(plot_title, size = 'xx-large')
    plt.legend(loc = 'upper right', fontsize = 'xx-large')
    plt.legend(loc='upper right')
    plt.show()


# examples of the routines from above
    
#time_pair_algorithms(2, 200, 10)
#basic_clustering(111, 9, "hierarch")
#basic_clustering(3108, 11, "kmeans", 5)
distortion_vs_algorithm(111, 6, 20, 5)

