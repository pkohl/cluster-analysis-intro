# -*- coding: utf-8 -*-


"""
Cluster class for Application 3 of Rice's algorithmic thinking MOOC
A cluster object contains a list of counties (indicated by FIPS codes), along 
with the horizontal and vertical coordinates of the geographic center of that 
collection of counties, the population of those counties, and the mean cancer 
risk in those counties. 

Note:  The geographic center comes from averaging the coordinates of each 
county, weighted by population.  

Additional note:  Most of this code was authored by the MOOC instructors
(though not the docstrings)

Properties:
fips_codes:   A list of the FIPS codes corresponding to the counties in the 
              cluster
horiz_pos:    The horizontal coordinate of the center of the cluster
vert_pos:     The vertical coordinate of the center of the cluster
population:   Total population of all the counties making up the cluster
risk:         Mean cancer risk in the cluster

Methods:
Getters:        fips_codes, horiz_center, vert_center, total_population, 
                averaged_risk
copy:           Returns a copy of the cluster
distance:       Returns the distance between one cluster and another specified
                cluster
merge_clusters: Returns a single cluster made up of two other clusters
cluster_error:  Returns the sum of the squared distances between the cluster
                center and the centers of the constituent counties
                
Last edited June 7, 2017
Most recent author:  Pat Kohl
"""

import math


class Cluster:
    """
    Class for creating and merging clusters of counties
    """
    
    def __init__(self, fips_codes, horiz_pos, vert_pos, population, risk):
        """
        Create a cluster based the models a set of counties' data
        """
        self._fips_codes = fips_codes
        self._horiz_center = horiz_pos
        self._vert_center = vert_pos
        self._total_population = population
        self._averaged_risk = risk
        
        
    def __repr__(self):
        """
        String representation assuming the module is "alg_cluster".
        """
        rep = "alg_cluster.Cluster("
        rep += str(self._fips_codes) + ", "
        rep += str(self._horiz_center) + ", "
        rep += str(self._vert_center) + ", "
        rep += str(self._total_population) + ", "
        rep += str(self._averaged_risk) + ")"
        return rep


    def fips_codes(self):
        """
        Get the cluster's set of FIPS codes
        """
        return self._fips_codes
    
    
    def horiz_center(self):
        """
        Get the averged horizontal center of cluster
        """
        return self._horiz_center
    
    
    def vert_center(self):
        """
        Get the averaged vertical center of the cluster
        """
        return self._vert_center
    
    
    def total_population(self):
        """
        Get the total population for the cluster
        """
        return self._total_population
    
    
    def averaged_risk(self):
        """
        Get the averaged risk for the cluster
        """
        return self._averaged_risk
   
        
    def copy(self):
        """
        Return a copy of a cluster
        """
        copy_cluster = Cluster(set(self._fips_codes), self._horiz_center,  
                               self._vert_center, self._total_population,  
                               self._averaged_risk)
        return copy_cluster


    def distance(self, other_cluster):
        """
        Compute the Euclidean distance between two clusters
        """
        vert_dist = self._vert_center - other_cluster.vert_center()
        horiz_dist = self._horiz_center - other_cluster.horiz_center()
        return math.sqrt(vert_dist ** 2 + horiz_dist ** 2)
        
    
    def merge_clusters(self, other_cluster):
        """
        Merge one cluster into another
        The merge uses the relative populations of each
        cluster in computing a new center and risk
        
        Note that this method mutates self
        """
        if len(other_cluster.fips_codes()) == 0:
            return self
        else:
            self._fips_codes.update(set(other_cluster.fips_codes()))
 
            # compute weights for averaging
            self_weight = float(self._total_population)                        
            other_weight = float(other_cluster.total_population())
            self._total_population = (self._total_population 
                + other_cluster.total_population())
            self_weight /= self._total_population
            other_weight /= self._total_population
                    
            # update center and risk using weights
            self._vert_center = (self_weight * self._vert_center   
                + other_weight * other_cluster.vert_center())
            self._horiz_center = (self_weight * self._horiz_center 
                + other_weight * other_cluster.horiz_center())     
            self._averaged_risk = (self_weight * self._averaged_risk    
                + other_weight * other_cluster.averaged_risk())
            return self
        
        
    def cluster_error(self, data_table):
        """
        Input: data_table is the original table of cancer data used in 
        creating the cluster.
        
        Output: The error as the sum of the square of the distance from each 
        county in the cluster to the cluster center (weighted by its 
        population)
        """
        # Build hash table to accelerate error computation
        fips_to_line = {}
        for line_idx in range(len(data_table)):
            line = data_table[line_idx]
            fips_to_line[line[0]] = line_idx
        
        # compute error as weighted squared distance from counties to cluster 
        # center
        total_error = 0
        counties = self.fips_codes()
        for county in counties:
            line = data_table[fips_to_line[county]]
            singleton_cluster = Cluster(set([line[0]]), line[1], line[2],   
                                        line[3], line[4])
            singleton_distance = self.distance(singleton_cluster)
            total_error += ((singleton_distance ** 2) 
                * singleton_cluster.total_population())
        return total_error
            