"""
Routines for plotting clusters of counties using matplotlib.
Most of this code was authored by the MOOC instructors (though not the
docstrings)

Functions:
circle_area:    Computes an area proportional to a given input population
plot_clusters:  Uses a map of the continental US as a backdrop for a plot
                of a cluster of counties

Last edited on June 7, 2017
Most recent author:  Pat Kohl
"""

import math
import matplotlib.pyplot as plt


# URL for map backdrop
# Note that a copy of this file should be present with the code package
# in the resource_files subdirectory - the active code uses the local file.
#DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
#MAP_URL = DIRECTORY + "data_clustering/USA_Counties.png"

# Define colors for clusters.  Display a max of 16 clusters.
COLORS = ['Aqua', 'Yellow', 'Blue', 'Fuchsia', 'Black', 'Green', 'Lime', 
          'Maroon', 'Navy', 'Olive', 'Orange', 'Purple', 'Red', 'Brown', 
          'Teal']



# Helper functions

def circle_area(pop):
    """
    Input:  County population
    Output: Circle area
    
    Magic number:  200 scales populations of given counties to circle areas
    that fit reasonably well on the map being used.
    """
    return math.pi * pop / (200.0 ** 2)


def plot_clusters(data_table, cluster_list, draw_centers = False):
    """
    Input:  Table of cancer risks by county (data_table), list of county
    clusters, flag indicating whether to draw lines from counties to the
    centers of their corresponding clusters.
    
    Output:  Plot of a cluster of counties
    """

    fips_to_line = {}
    for line_idx in range(len(data_table)):
        fips_to_line[data_table[line_idx][0]] = line_idx
     
    map_img = plt.imread("resource_files/USA_counties.png")
    #map_img = plt.imread(MAP_URL)

    # Scale plot to get size similar to CodeSkulptor version
    ypixels, xpixels, bands = map_img.shape
    DPI = 60.0                  # adjust this constant to resize your plot
    xinch = xpixels / DPI
    yinch = ypixels / DPI
    plt.figure(figsize=(xinch,yinch))
    plt.imshow(map_img)
   
    # draw the counties colored by cluster on the map
    if not draw_centers:
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            for fips_code in cluster.fips_codes():
                line = data_table[fips_to_line[fips_code]]
                plt.scatter(x = [line[1]], y = [line[2]], 
                            s = circle_area(line[3]), lw = 1,
                            facecolors = cluster_color, 
                            edgecolors = cluster_color)

    # add cluster centers and lines from center to counties            
    else:
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            for fips_code in cluster.fips_codes():
                line = data_table[fips_to_line[fips_code]]
                plt.scatter(x = [line[1]], y = [line[2]], 
                            s =  circle_area(line[3]), lw = 1,
                            facecolors = cluster_color, 
                            edgecolors = cluster_color, zorder = 1)
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            cluster_center = (cluster.horiz_center(), cluster.vert_center())
            for fips_code in cluster.fips_codes():
                line = data_table[fips_to_line[fips_code]]
                plt.plot([cluster_center[0], line[1]], 
                         [cluster_center[1], line[2]], 
                          cluster_color, lw=1, zorder = 2)
        for cluster_idx in range(len(cluster_list)):
            cluster = cluster_list[cluster_idx]
            cluster_color = COLORS[cluster_idx % len(COLORS)]
            cluster_center = (cluster.horiz_center(), cluster.vert_center())
            cluster_pop = cluster.total_population()
            plt.scatter(x = [cluster_center[0]], y = [cluster_center[1]], 
                        s =  circle_area(cluster_pop), lw = 2,
                        facecolors = "none", edgecolors = "black", zorder = 3)

    plt.show()
