import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

G = nx.path_graph(3)
bb = nx.betweenness_centrality(G)
nx.set_node_attributes(G, 'betweenness', bb)
print G.node[1]['h']
pos = nx.spring_layout(G, iterations=100) # positions for all nodes

nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightBlue', node_shape='o', alpha=1.0, cmap=None, vmin=None, vmax=None, ax=None, linewidths=None, label=None)
nx.draw_networkx_edges(G,pos)

string = "Manhattan street topology"
plt.title(string)
#plt.colorbar(edges)
plt.plot()
plt.show()
