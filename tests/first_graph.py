# -*- coding: utf-8 -*-
"""first_graph.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NuzFHDb1LhjPO8Lnf2oVJqzJB7dP4mcn
"""

!pip install rdflib
import rdflib
from rdflib import Graph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt

import requests
import json

endpoint_url = "https://query.wikidata.org/sparql"
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
    LIMIT 10
  }
}'''
payload = {
    'query': query,
    'format': 'json'
}
r = requests.get(endpoint_url, params=payload, headers=headers)
results = r.json()

#print(results["results"]["bindings"])

#extract id from json list
node_ids=[item["itemLabel"]["value"] for item in results["results"]["bindings"]]
print(node_ids)
print(len(node_ids))

#get all nt graph files

#graphs = [Graph() for n in node_ids]
#for i,n in enumerate(node_ids):
#  graphs[i].parse('https://www.wikidata.org/wiki/Special:EntityData/'+n+'.nt', format="nt")

mgraph=Graph()
for n in node_ids:
  mgraph.parse('https://www.wikidata.org/wiki/Special:EntityData/'+n+'.nt', format="nt")

## Transform to networkx and plot
G = rdflib_to_networkx_multidigraph(mgraph)

# Plot Networkx instance of RDF Graph
'''pos = nx.spring_layout(G, scale=2)
edge_labels = nx.get_edge_attributes(G, 'r')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw(G, with_labels=False)

print(nx.info(G))

#if not in interactive mode for 
plt.show()'''

to_suppr=[]

for node in G.nodes:
  if not (node.startswith('http://www.wikidata.org/entity/Q') or node.startswith('http://www.wikidata.org/entity/P')):
    to_suppr.append(node)

for node in to_suppr:
  G.remove_node(node)

print(G.nodes())

out_deg = G.degree()

to_suppr=[]

for node in G.nodes:
  if G.in_degree(node)==0 and G.out_degree(node)==0:
    to_suppr.append(node)

for node in to_suppr:
  G.remove_node(node)

print(out_deg)

labels = {}
mapping = {}

for node in G.nodes():
  if node.split('/')[-1] in node_ids:
    #mapping[node]='person'
    labels[node]=node.split('/')[-1]
    print(node)
  if node.startswith('http://www.wikidata.org/entity/'):
    labels[node]=node[31:]

#G = nx.relabel_nodes(G, mapping)

import warnings
warnings.filterwarnings('ignore')
pos = nx.spring_layout(G)
node_color = ['yellow' if v.startswith("httpd") else 'blue' for v in G]
node_size =  [1000 if v.startswith("httpd") else 35 for v in G]
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 15)
plt.axis('off')

nx.draw_networkx(G, pos, with_labels = False, node_color=node_color,node_size=node_size)
nx.draw_networkx_labels(G,pos,labels,font_size=10,font_color='r')
plt.show()

nodes=list(G)
nodes.sort(key=G.out_degree)
print(nodes)

B_1=[]

for node in G.nodes():
  if node.split('/')[-1] in node_ids:
    B_1.append(node)

nx.draw_networkx(G,pos=nx.drawing.layout.bipartite_layout(G, B_1), with_labels = False)

plt.show()