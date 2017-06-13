"""
Routines for creating clusters of counties using k means and hierarchical
clustering algorithms.

Functions:
pair_distance:       Computes the distance between the centers of two clusters.
slow_closest_pair:   Brute force computation of the two closest together
                     clusters in a set of clusters.
fast_closest_pair:   Divide and conquer method for finding the two closest
                     clusters in a set of clusters.
closest_pair_strip:  Finds the two closest together clusters in a vertical
                     geographical strip of specified width.
hierarch_clustering: Generates a clustering using the hierarchical clustering
                     algorithm.
kmeans_clustering:   Generates a clustering using the k means clustering
                     algorithm.
gen_random_clusters: Generates a list of clusters with coordinates randomly
                     distributed between -1 and 1.
compute_distortion:  Calculates the distortion of a cluster as the sum of the
                     squares of the distances from a cluster center to its 
                     constituent counties
dist_vs_clusters:    Calculates distortion as a function of cluster size for
                     both hierarchical and k means clusterings.

Last edited on June 12, 2017
Author:  Pat Kohl
"""

import random
import alg_cluster
import alg_p3_viz


def pair_distance(cluster_list, idx_1, idx_2):
    """
    Helper function that computes Euclidean distance between two clusters in 
    a list

    Input: cluster_list is list of clusters; idx_1 and idx_2 are integer 
    indices for two clusters
    
    Output: tuple (dist, idx_1, idx_2) where dist is distance between
    cluster_list[idx_1] and cluster_list[idx_2]
    """
    return (cluster_list[idx_1].distance(cluster_list[idx_2]), 
            min(idx_1, idx_2), max(idx_1, idx_2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx_1, idx_2) where the centers of the 
    clusters cluster_list[idx_1] and cluster_list[idx_2] have minimum 
    distance dist.       
    """
    # brute force check the difference between every possible pairing
    dist_d = [float('inf'), -1, -1]
    num_clusters = len(cluster_list)
    for idx_1 in range(num_clusters):
        for idx_2 in range(num_clusters):
            if idx_1 != idx_2:
                temp_dist = list(pair_distance(cluster_list, idx_1, idx_2))
                if  temp_dist[0] < dist_d[0]:
                    dist_d[0] = temp_dist[0]
                    dist_d[1] = idx_1
                    dist_d[2] = idx_2
    dist_tuple = tuple(dist_d)
    return dist_tuple


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters sorted such that horizontal 
    positions of their centers are in ascending order
    
    Output: tuple of the form (dist, idx_1, idx_2) where the centers of the 
    clusters cluster_list[idx_1] and cluster_list[idx_2] have minimum 
    distance dist.       
    """
    
    idx_n = len(cluster_list)
    
    # for small sets, use the slow_closest_pair algorithm
    # serves as recursive base case
    if idx_n <= 3:
        dist_d = slow_closest_pair(cluster_list)
    
    # otherwise, divide and conquer
    else:
        idx_m = int(idx_n / 2)
        # find the distance distance between the closest pair of clusters
        # in the left and right halves of the list (note again that the
        # clusters are sorted by horizontal coordinate)
        cluster_list_left = cluster_list[:idx_m]
        cluster_list_right = cluster_list[idx_m:]
        dist_left = fast_closest_pair(cluster_list_left)
        dist_right = fast_closest_pair(cluster_list_right)
        if dist_left[0] <= dist_right[0]:
            dist_d_temp = dist_left
        else:
            dist_d_temp = (dist_right[0], dist_right[1] + idx_m, 
                           dist_right[2] + idx_m)
        

        mid = 0.5 * (cluster_list[idx_m - 1].horiz_center() + 
                     cluster_list[idx_m].horiz_center())
        
        strip_d = closest_pair_strip(cluster_list, mid, dist_d_temp[0])
        if dist_d_temp[0] <= strip_d[0]:
            dist_d = dist_d_temp
        else:
            dist_d = strip_d
        
    return dist_d


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal 
    distance that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the 
    clusters cluster_list[idx1] and cluster_list[idx2] lie in the strip and 
    have minimum distance dist.       
    """

    # find all the clusters within the specified vertical strip, and store
    # them in list_s
    list_s = []
    for single_cluster in cluster_list:
        if abs(single_cluster.horiz_center() - horiz_center) <= half_width:
            list_s.append(single_cluster)

    dist_d = [float('inf'), -1, -1]

    # sort clusters according their vertical coordinates
    list_s.sort(key = lambda item: item.vert_center())
    idx_n = len(list_s)
    
    # brute force check of all pairs of clusters, with indices chosen to 
    # minimize redundant comparisons
    for idx_1 in range(idx_n - 1):
        for idx_2 in range(idx_1 + 1, min(idx_1 + 3, idx_n - 1) + 1):
            if idx_1 != idx_2:
                temp_dist = list(pair_distance(list_s, idx_1, idx_2))
                if temp_dist[0] < dist_d[0]:
                    dist_d[0] = temp_dist[0]
                    
                    dist_d[1]=cluster_list.index(list_s[idx_1])
                    dist_d[2]=cluster_list.index(list_s[idx_2])

        if dist_d[1] > dist_d[2]:
            temp = dist_d[2]
            dist_d[2] = dist_d[1]
            dist_d[1] = temp
                          
    dist_tuple = tuple(dist_d)
    return dist_tuple


def hierarch_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters.
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    
    # find the closest two clusters in cluster_list and merge them
    # repeat until number of clusters matches num_clusters 
    while len(cluster_list) > num_clusters:
        # sort the clusters (prerequisite for fast_closest_pair)
        cluster_list.sort(key = lambda item: item.horiz_center())
        closest_pair = fast_closest_pair(cluster_list)
        first_point = cluster_list[closest_pair[1]]
        second_point = cluster_list[closest_pair[2]]
        
        temp_cluster = first_point
        new_cluster = temp_cluster.merge_clusters(second_point)

        cluster_list.append(new_cluster)
        cluster_list.remove(first_point)
        cluster_list.remove(second_point)        
    
    return cluster_list

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters.
    Initialize num_clusters centers.  
    Iterate num_iterations times:
            Add each cluster to the closest available center.
            Recalculate centers.
    
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of 
    iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest 
    # populations
    # make a copy of cluster_list and sort it by population (descending)
    cluster_list_temp = list(cluster_list)
    cluster_list_temp.sort(key = lambda item: item.total_population(), 
                           reverse = True)
    
    n_size = len(cluster_list_temp)
    starting_clusters = cluster_list_temp[:num_clusters]
    
    # for num_iterations:  add each of 
    for _ in range(num_iterations):
        c_list = []
        # start with list of num_clusters empty sets
        for idx in range(num_clusters):
            c_list.append(alg_cluster.Cluster(set([]), 0, 0, 1, 0))

        for idx_1 in range(n_size):
            # find coordinates that minimize distance to coordinates indexed 
            # by idx_1
            min_dist = float('inf')
            min_index = -1
            for idx_2 in range(num_clusters):
                dist = cluster_list_temp[idx_1].distance(
                                                    starting_clusters[idx_2])
                if dist < min_dist:
                    min_dist = dist
                    min_index = idx_2
            c_list[min_index].merge_clusters(cluster_list_temp[idx_1])
        for idx_3 in range(num_clusters):
            starting_clusters[idx_3] = c_list[idx_3]
            
    return starting_clusters

            
def gen_random_clusters(num_clusters):
    """
    Generate a list of num_clusters clusters with center coordinates randomly
    distributed between -1 and 1.
    
    Input:  Desired number of clusters.
    Output: List of clusters with randomly-distributed centers.
    """
    cluster_list = []
    for idx in range(num_clusters):
        cluster_list.append(alg_cluster.Cluster(set([]), random.uniform(-1, 1), 
                            random.uniform(-1, 1), 0, 0))
    return cluster_list      


def compute_distortion(cluster_list, num_counties):
    """
    Generate a list of num_clusters clusters with center coordinates randomly
    distributed between -1 and 1.
    
    Input:  List of clusters, and table of county data.
    Output: Number representing distortion of the cluster list, with 
            distortion being a measure of the sum of the squared distances
            from a county to its cluster center, weighted by the population
            of the county.
    """
    data_table = alg_p3_viz.load_data_table(num_counties)
    distortion = 0
    for cluster in cluster_list:
        distortion += cluster.cluster_error(data_table)
    return distortion


def dist_vs_clusters(num_counties, min_clusters, max_clusters, 
                           num_iterations):
    """
    Iteratively produce a clustering using each of the k means and hierarchical
    clustering algorithms.  Track and report distortion as a function of 
    number of clusters remaining.
    
    Input:  Table of county data, list of clusters, final number of clusters
            to produce, and number of iterations to apply to the k means
            algorithm.
    Output: List of lists, with each of the top-level lists providing the
            distortion as a function of number of clusters for each of 
            the k means and hierarchical routines.  Lists will be in 
            ascending order of number of clusters.
    """
    # make cluster list from data table
    data_table = alg_p3_viz.load_data_table(num_counties)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], 
                                                  line[2], line[3], line[4]))
    
    # initialize data tables
    hierarch_distort = []
    kmeans_distortions = []
    
    # obtain kmeans data
    for idx in range(min_clusters, max_clusters + 1):
        cluster_list = kmeans_clustering(singleton_list, 
                                                        idx, num_iterations)
        kmeans_distortions.append(compute_distortion(cluster_list, num_counties))
        
    # obtain hierarchical clustering data, recycling larger sets into 
    # smaller sets
    cluster_list = hierarch_clustering(singleton_list, max_clusters)
    hierarch_distort.append(compute_distortion(cluster_list, num_counties))
    
    for idx in range(max_clusters - 1, min_clusters - 1, -1):
        cluster_list = hierarch_clustering(cluster_list, idx)
        hierarch_distort.append(compute_distortion(cluster_list, num_counties))
    
    # by default this routine produces data in descending order, so 
    # reverse it
    hierarch_distort.reverse()
    return [kmeans_distortions, hierarch_distort]
