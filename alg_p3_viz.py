"""
Routines for importing data files for the sake of cluster generation, and 
support for producing plots.

Functions:
circle_area:    Computes an area proportional to a given input population
plot_clusters:  Uses a map of the continental US as a backdrop for a plot
                of a cluster of counties

Last edited on June 7, 2017
Most recent author:  Pat Kohl
"""

#import urllib.request
import math
import alg_cluster
import alg_p3_core      
import alg_clusters_matplotlib


# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table
# Note that copies of these files should be present with the code package
# in the resource_files subdirectory - the active code uses the local files
#DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
#DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
#DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
#DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
#DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def num_to_path(num):
    """
    Return a path to a local data file containing num counties.
    
    Input:  Number of counties in the requested data set.
    
    Output: A string providing the path to the corresponding data file.
    """
    switcher = {
            111 : "resource_files/unifiedCancerData_111.csv",
            290 : "resource_files/unifiedCancerData_290.csv",
            896 : "resource_files/unifiedCancerData_896.csv",
            3108 : "resource_files/unifiedCancerData_3108.csv"
            }
    return switcher.get(num)
    

def load_data_table(num):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    
    Input:  The number of counties in the desired data file
    
    Output: A num x 5 matrix, with each row providing the following for a 
    single county:  FIPS code, horizontal center, vertical center, 
    population, and mean cancer incidence.
    """
    file_name = num_to_path(num)
    in_file = open(file_name)
    data_string = in_file.read()
    foo_lines = data_string.split('\n')
    foo_tokens = [line.split(',') for line in foo_lines]

    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), 
            float(tokens[4])] for tokens in foo_tokens]


def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    
    Input:   data_table, a matrix whose rows have data for individual counties
             (see load_data_table above)
             num_clusters, the number of clusters to return
        
    Output:  a list of clusters
    
    Note:  Function is currently unused.
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

def run_example(num):
    """
    Test version of afunction to load a data table, compute a list of clusters 
    and plot the list of clusters.  Not for general use.
    
    Input:  The number of counties in the dataset to be used.
    Output: Sends a plot to the console.
    """
    
    data_table = load_data_table(num)

    # build up a list of cluster objects using data from the data table
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], 
                                                  line[2], line[3], line[4]))

    # use the k-means algorithm to create nine clusters using five iterations
    # of the algorithms - 9 and 5 hardcoded for testing purposes
    # general instances of this function exist in main.py
    cluster_list = alg_p3_core.kmeans_clustering(singleton_list, 9, 5)	
    print("Displaying", len(cluster_list), "k-means clusters for", num,
          "county dataset")
            
    # draw the clusters using matplotlib
    alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)