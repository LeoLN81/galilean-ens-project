from kgbuilder.utils import *

l=get_list_people_sparql(Endpoint.wikidata, size=10)
G=create_merged_stars_graph(l)

print(nx.info(G))