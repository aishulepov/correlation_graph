# https://stackoverflow.com/questions/59598019/how-to-plot-large-networks-clearly
# https://stackoverflow.com/questions/58881266/how-to-have-different-edge-weights-but-same-edge-length-in-network-diagram
# https://gist.github.com/maciejkos/e3bc958aac9e7a245dddff8d86058e17
# https://js.cytoscape.org/demos/2ebdc40f1c2540de6cf0/
import pandas as pd
import networkx as nx
from pyvis.network import Network



df = pd.read_csv('./input_data/Корреляция_регионы_tab.csv', sep='\t')
df["value"] = df.value.str.replace(",", ".").astype(float)

df = df[df["to"]!=df["from"]]
df = df[df.value>df.value.quantile(0.96)]
df["value"] = df.value

G = nx.from_pandas_edgelist(df, 'from', 'to', edge_attr=True, create_using=nx.Graph())


edges = G.edges()
weights = list(df.value)
#weights = [G[u][v]['weight'] for u,v in edges]
pos = nx.spring_layout(G, weight='weight')
nc = nx.draw_networkx(G, pos, with_labels=True, node_color='yellow')


nt = Network()
nt.from_nx(G)
'''for k, v in pos.items():
    nt.add_node(k, title=k, x = v[0]*10000, y=v[1]*10000, label=k, physics=False, color='#FF0000', font='90px arial blue')

for src,tgt in edges:
    nt.add_edge(src,tgt, title=G[src][tgt]["value"])'''
nt.show('nx.html')