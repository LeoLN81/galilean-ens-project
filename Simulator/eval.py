import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from networkx.algorithms import community

def draw_edges_growth(method, args, start_size, max_size, step):
    """Plot the number of edges in a graph generated by a given method.
    
    Parameters
    ----------
    method : function
        The function used to generate the graph.
    args : tuple
        A tuple of arguments to be passed to the function.
    start_size : int
        The starting size of the graph (number of nodes).
    max_size : int
        The maximum size of the graph (number of nodes).
    step : int
        The size increment for each iteration (number of nodes).
        
    Returns
    -------
    None
        The function plots the graph and displays it.
    """
    # Initialize an empty list to store the number of edges
    n_edges = []
    
    # Loop through the desired size range
    for i in range(start_size, max_size, step):
        # Generate the graph with the given method and arguments
        graph = method(i, args)
        
        # Append the number of edges in the graph to the list
        n_edges.append(graph.number_of_edges())
    
    # Plot the number of edges against the size of the graph
    plt.plot(np.arange(start_size, max_size, step), n_edges)
    
    # Display the plot
    plt.show()

def detect_communities(G, threshold=0.5):
    """Detect communities in a graph using the Girvan-Newman algorithm.
    
    Parameters
    ----------
    G : networkx.Graph
        The graph to be analyzed.
    threshold : float, optional
        The modularity threshold for detecting communities. The default value is 0.5.
        
    Returns
    -------
    list of lists
        A list of lists, where each inner list contains the nodes in a community.
    """
    # Use the Girvan-Newman algorithm to detect communities
    communities = list(community.girvan_newman(G))
    
    # Extract the communities from the partition
    communities = [c for c in communities if community.modularity(G, c) > threshold]
    
    return communities


def calculate_modularity(G, communities):
    """Calculate the modularity of a graph.
    It measures the strength of division of a graph into communities. 
    It assigns higher values to graphs with high intra-community edge density and low inter-community 
    edge density.
    
    Parameters
    ----------
    G : networkx.Graph
        The graph for which to calculate the modularity.
    communities : list of lists
        A list of lists, where each inner list contains the nodes in a community.
    
    Returns
    -------
    float
        The modularity of the graph.
    """
    # Calculate the number of edges in the graph
    m = G.number_of_edges()
    
    # Initialize the modularity to 0
    modularity = 0
    
    # Loop through each community
    for community in communities:
        # Calculate the fraction of edges within the community
        e_in = sum([G.has_edge(u, v) for u in community for v in community]) / m
        
        # Calculate the fraction of edges between the community and the rest of the graph
        e_out = sum([G.has_edge(u, v) for u in community for v in G.nodes() if v not in community]) / m
        
        # Calculate the contribution to the modularity
        modularity += (e_in - (e_out**2))
    
    return modularity


def clustering():
    """"""