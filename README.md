# cluster-analysis-intro
Code for performing simple cluster analysis on US counties as part of a Python MOOC.

While the data files in this project include information on cancer incidence by county,
the project routines make no use of that information.  The project is based entirely on
analyzing different algorithms for clustering objects together.  In particular, we
examine a k-means clustering algorithm and a hierarchical clustering algorithm:

https://en.wikipedia.org/wiki/K-means_clustering

https://en.wikipedia.org/wiki/Hierarchical_clustering (agglomerative)

These algorithms take as inputs sets of counties, and form clusters of those counties
based on their locations and populations.  We characterize these algorithms according
to their run speed and according to how tight the resulting clusters are (measured
via distortion, as defined in alg_p3_core.py).  

Project files:

alg_cluster:     
Implements the cluster class.  Cluster objects contain collections of 
counties, their populations, and their coordinates.  
                 
alg_p3_core:     
Contains the core clustering algorithms, including those for building
up clusters using either k-means or hierarchical clustering, and those
for characterizing the quality of a cluster via distortion.
                 
alg_p3_viz:

Contains various utility routines for loading and visualizing data

main:

Functions that accomplish the specific tasks demanded by the project, involving
executing various algorithms and collecting and displaying the resulting data.

                 
