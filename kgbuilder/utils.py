import rdflib
from rdflib import Graph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt

import requests
import json

class Endpoint:
    wikidata="https://query.wikidata.org/sparql"

def get_list_queer_germany_sparql(endpoint, size=10):

    # Define url and headers for the HTTP request
    endpoint_url = endpoint
    headers = { 'User-Agent': 'MyBot' }


    # SPARQL query to select a list of queer personalities in Germany from the Wikidata endpoint
    query='''SELECT DISTINCT ?item ?itemLabel WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
    {
        SELECT DISTINCT ?item WHERE {
        ?item p:P91 ?statement0.
        ?statement0 (ps:P91/(wdt:P279*)) ?instance.
        MINUS { ?item (p:P91/ps:P91) wd:Q1035954. }
        {
            ?item p:P19 ?statement1.
            ?statement1 (ps:P19/(wdt:P279*)) wd:Q183.
        }
        UNION
        {
            ?item p:P27 ?statement2.
            ?statement2 (ps:P27/(wdt:P279*)) wd:Q183.
        }
        }
        LIMIT'''+str(size)+'''
    }
    }'''

    # Define the payload for the GET request
    payload = {
        'query': query,
        'format': 'json'
    }
    # Make the GET request to the endpoint URL
    r = requests.get(endpoint_url, params=payload, headers=headers)
    results = r.json()

    # Extract the item labels and store in a list
    id_list=[item["itemLabel"]["value"] for item in results["results"]["bindings"]]

    return id_list

def get_list_queer_world_sparql(endpoint, size=10):
    endpoint_url = endpoint
    headers = { 'User-Agent': 'MyBot' }


    #request the list of queer personalities (in Germany)
    query='''SELECT DISTINCT ?item ?itemLabel WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
    {
        SELECT DISTINCT ?item WHERE {
            ?item p:P31 ?statement0.
            ?statement0 (ps:P31/(wdt:P279*)) wd:Q5.
            ?item p:P91 ?statement1.
            ?statement1 (ps:P91/(wdt:P279*)) ?instance.
            MINUS { ?item (p:P91/ps:P91) wd:Q1035954. }
        }
        LIMIT'''+str(size)+'''
    }
    }'''
    payload = {
        'query': query,
        'format': 'json'
    }
    r = requests.get(endpoint_url, params=payload, headers=headers)
    results = r.json()

    id_list=[item["itemLabel"]["value"] for item in results["results"]["bindings"]]

    return id_list

def create_merged_stars_graph(id_list, convert=True):
    # Create an empty RDF graph
    mgraph=Graph()
    # Iterate over the list of nodes (wikidata item ids)
    for node in id_list:
        # Parse the RDF data of the node from the wikidata entity URL in ntriples format
        mgraph.parse('https://www.wikidata.org/wiki/Special:EntityData/'+node+'.nt', format="nt")
    
    # If the convert parameter is True, the function will convert the RDF graph to a NetworkX multidigraph
    if convert:
        return rdflib_to_networkx_multidigraph(mgraph)
    else:
        return mgraph