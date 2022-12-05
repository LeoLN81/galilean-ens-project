import rdflib
from rdflib import Graph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt

import requests
import json

class Endpoint:
    wikidata="https://query.wikidata.org/sparql"

def get_list_people_sparql(endpoint, size=10):
    endpoint_url = endpoint
    headers = { 'User-Agent': 'MyBot' }


    #request the list of queer personalities (in Germany)
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
    payload = {
        'query': query,
        'format': 'json'
    }
    r = requests.get(endpoint_url, params=payload, headers=headers)
    results = r.json()

    id_list=[item["itemLabel"]["value"] for item in results["results"]["bindings"]]

    return id_list

def create_merged_stars_graph(id_list):
    mgraph=Graph()
    for node in id_list:
        mgraph.parse('https://www.wikidata.org/wiki/Special:EntityData/'+node+'.nt', format="nt")
    
    G = rdflib_to_networkx_multidigraph(mgraph)
    return G