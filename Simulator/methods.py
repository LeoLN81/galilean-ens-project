import random 
from random import choices
import networkx as nx
import numpy as np
from scipy.stats import lognorm
#import graphdata

#generate a directed graph (without parallel edges) with n nodes and a probability p that there is an edge between 2 nodes
def random_Bernoulli_graph_gen(n,p) : 
    G=nx.DiGraph()
    G.add_nodes_from(range(n))
    for u in range(n):
        for v in range(n):
            if u!=v :    #we don't allow loops 
                if choices([0,1], [1-p ,p])[0] :   #if we create an edge (with proba p)
                    G.add_edge(u,v)
    #print(G)
    return G

# n is the number of nodes and distrib[i][j] is the probability that there is j edges leaving the node i. 
def all_nodes_there(n,distrib):
    G=nx.DiGraph()
    G.add_nodes_from(range(n))
    for u in range (n):
        nb=random.choices(np.arange(len(distrib[u])),distrib[u])
        i=0
        while i!=nb[0]:
            j=random.randint(0,n-1)
            if(j!=u and (i==0 or not G.has_edge(u,j))):
                G.add_edge(u,j)
                i+=1
    return G

def random_1_from_distrib(n, distrib):
    """Generate a directed graph with a given number of nodes and a distribution of out-degrees.
    
    Parameters
    ----------
    n : int
        The number of nodes in the graph.
    distrib : list
        A list of probabilities corresponding to the number of out-degrees.
        
    Returns
    -------
    networkx.DiGraph
        The generated directed graph.
    """
    # Initialize a directed graph
    G = nx.DiGraph()
    
    # Add the nodes to the graph
    G.add_nodes_from(range(n))
    
    # Loop through each node
    for u in range(n):
        # Sample a number of out-degrees from the distribution
        nb = random.choices(np.arange(len(distrib)), distrib)
        
        # Initialize a counter for the number of out-degrees
        i = 0
        
        # Loop until the desired number of out-degrees is reached
        while i != nb[0]:
            # Choose a random node to connect to
            j = random.randint(0, n - 1)
            
            # Check if the edge is valid (i.e., not self-loop and no duplicate edges)
            if j != u and (i == 0 or not G.has_edge(u, j)):
                # Add the edge to the graph
                G.add_edge(u, j)
                
                # Increment the counter
                i += 1
    
    # Return the generated graph
    return G

def random_1_from_distrib_incremental(n, distrib):
    """Generate a directed graph with a given number of nodes and a distribution of out-degrees, 
    but with nodes that can only connect to node already covered.
    
    Parameters
    ----------
    n : int
        The number of nodes in the graph.
    distrib : list
        A list of probabilities corresponding to the number of out-degrees.
        
    Returns
    -------
    networkx.DiGraph
        The generated directed graph.
    """
    # Initialize a directed graph
    G = nx.DiGraph()
    
    # Add the nodes to the graph
    G.add_nodes_from(range(n))
    
    # Loop through each node
    for u in range(n):
        # Sample a number of out-degrees from the distribution
        nb = random.choices(np.arange(len(distrib)), distrib)
        
        # Initialize a counter for the number of out-degrees
        i = 0
        
        # Loop until the desired number of out-degrees is reached
        while i < nb[0] and i<u:
            # Choose a random node to connect to
            j = random.randint(0, n - 1)
            
            # Check if the edge is valid (i.e., not self-loop and no duplicate edges)
            if j<u and (i == 0 or not G.has_edge(u, j)):
                # Add the edge to the graph
                G.add_edge(u, j)
                
                # Increment the counter
                i += 1
    
    # Return the generated graph
    return G


def random_1_from_lognormal(n, mean, std, scale):
    """Generate a directed graph with a given number of nodes and a distribution of out-degrees.
    
    Parameters
    ----------
    n : int
        The number of nodes in the graph.
    mean : float
        The mean of the log normal distribution.
    std : float
        The standard deviation of the log normal distribution.
    scale : float
        The scale of the log normal distribution.
        
    Returns
    -------
    networkx.DiGraph
        The generated directed graph.
    """
    # Set up the log normal distribution using the mean and std
    distribution = lognorm(mean, std, scale)
    
    # Initialize a directed graph
    G = nx.DiGraph()
    
    # Add the nodes to the graph
    G.add_nodes_from(range(n))
    
    # Loop through each node
    for u in range(n):
        # Generate a random number of out-degrees from the distribution
        nb = int(distribution.rvs()/5)
        print(nb)
        
        # Initialize a counter for the number of out-degrees
        i = 0
        
        # Loop until the desired number of out-degrees is reached
        while i != nb:
            # Choose a random node to connect to
            j = random.randint(0, n - 1)
            
            # Check if the edge is valid (i.e., not self-loop and no duplicate edges)
            if j != u and (i == 0 or not G.has_edge(u, j)):
                # Add the edge to the graph
                G.add_edge(u, j)
                
                # Increment the counter
                i += 1
    
    # Return the generated graph
    return G