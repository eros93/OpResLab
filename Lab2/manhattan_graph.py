import networkx as nx
import numpy as np
import matplotlib.pyplot as plt



#for i in range(0,100):
np.random.seed(3)
#print i

N=2
N_node = N*N
traffic_sort = []

# ************ Utility functions ************

# find "first" idle node in G (return False if no node is idle)
def find_idle_node(G):
	for ID_node in G.nodes():
		if G.node[ID_node]['alias'] == False:
			return ID_node
	return False

# find "first" idle neighbour in G for that nodex (if no neighbour is found try to take first idle node in the graph)
def find_idle_neighbour(G,ID_nodex):
	for neigh in G.node[ID_nodex]['neighbours']:
		#print neigh
		if G.node[neigh]['alias'] == False:
			return neigh
	return find_idle_node(G)

# check if this alias is already placed,(is yes return the ID_NODE, else False)
def is_placed(G, alias):
	for ID_node in G.nodes():
		if G.node[ID_node]['alias'] == alias:
			return ID_node
	return False

def add_costEdge(G, costEdges, path, traffic):
	length_path = len(path)
	for i in range(length_path -1):
		s_tmp = path[i]
		d_tmp = path[i+1]
		costEdges[int(G.node[s_tmp]['alias'])][int(G.node[d_tmp]['alias'])] += traffic


# ************ creation of the manhattan topology graph ************

G = nx.grid_2d_graph(N,N)

for i in range(0,N):
	G.add_edge((i,0),(i,N-1))
	G.add_edge((0,i),(N-1,i))
#print G.edges()

#alias attribute -> is the corrispondance in tsd nodes (is false if the node is not placed),
#neighbours attribute -> is the list of neighbour nodes

nx.set_node_attributes(G, 'alias', False)
for ID_node in G.nodes():
	G.node[ID_node]['neighbours'] = G.neighbors(ID_node)
	#print G.node[ID_node]['neighbours']


# ************ creation of traffic matrix ************

tsd = np.zeros((N_node, N_node))
for i in range(N_node):
	for j in range(N_node):
		if i != j:
			tsd[j, i] = np.random.random()
			tsd[i, j] = 0
#print tsd
tsd_routing = tsd.copy()

while True :
	MAX_tmp = tsd.max()
	if MAX_tmp == 0:
		break
	else:
		index_tuple = np.where(tsd == MAX_tmp)
		traffic_sort.append(tuple(zip(*index_tuple))[0])
		tsd[traffic_sort[-1][0], traffic_sort[-1][1]] = 0

print traffic_sort


# ************ placing the nodes ************

for edge in traffic_sort:
	print "Take node %r" %edge[0]
	if not is_placed(G, str(edge[0])):
		try:
			target_ID = find_idle_node(G)
			G.node[target_ID]['alias'] = str(edge[0])
			print "Node %r is placed in ID_node %r" %(edge[0],target_ID)
		except:
			print "It was not possible to placed node ", edge[0]
	else:
		print "Node %r is already placed" %edge[0]

	# print G.node[is_placed(G, str(edge[0]))]['alias']
	# print G.node[is_placed(G, str(edge[0]))]['neighbours']
	# print find_idle_neighbour(G, is_placed(G, str(edge[0])))

	print "Take node %r" % edge[1]
	if not is_placed(G, str(edge[1])):
		try:
			#print is_placed(G,str(edge[0]))
			#print find_idle_neighbour(G, is_placed(G, str(edge[0])))
			target_ID = find_idle_neighbour(G, is_placed(G, str(edge[0])))
			#print target_ID
			G.node[target_ID]['alias'] = str(edge[1])
			print "Node %r is placed (as neighbour of %r) in ID_node %r" % (edge[1], edge[0], target_ID)
		except:
			print "It was not possible to placed node %r as neighbour of %r" %(edge[1], edge[0])
	else:
		print "Node %r is already placed" %edge[1]

for ID_node in G.nodes():
	print "Node %r in ID_node %r" %(G.node[ID_node]['alias'], ID_node)

simple_paths = []
for path in nx.all_simple_paths(G,is_placed(G,'0'),is_placed(G,'1')):
	simple_paths.append(path)
#print "Simple paths ", simple_paths


# ************ routing cost edge ************

costEdges = np.zeros(shape=(N_node, N_node))

for s in range(N_node):
	for d in range(N_node):
		paths = []
		tot_edges = 0
		for path in nx.all_simple_paths(G, source=is_placed(G,str(s)), target=is_placed(G,str(d))):
			paths.append(path)
		for path in paths:
			add_costEdge(G, costEdges, path, tsd_routing[s][d] / len(paths))
#print costEdges


# ************ creation the dict for the labels ************

# round to 2 digits of cost edges
for i in range(len(costEdges)):
	costEdges[i] = np.round(costEdges[i], 2)

costEdges = np.triu(costEdges)
print costEdges

maxFlow = costEdges.max()
ii = np.where(costEdges == maxFlow)
print "the max edge flow is: ",maxFlow
max_flow_edge = []
max_flow_edge.append(tuple(zip(*ii))[0])
print max_flow_edge

labels = {}
label_maxFlow = {}
for edge in np.transpose(np.nonzero(costEdges)):
	labels[is_placed(G,str(edge[0])), is_placed(G,str(edge[1]))] = costEdges[edge[0]][edge[1]]
#print labels

label_maxFlow[tuple(zip(*ii))[0]] = maxFlow
print label_maxFlow

# ************ print of the manhattan topology graph ************

pos = nx.spring_layout(G, iterations=100) # positions for all nodes

nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightBlue', node_shape='o', alpha=1.0, cmap=None, vmin=None, vmax=None, ax=None, linewidths=None, label=None)
# nx.draw_networkx_edges(G,pos, edgelist=max_flow_edge, edge_color='r', width=3)
# nx.draw_networkx_edge_labels(G,pos,edge_labels=label_maxFlow, label_pos=0.6, font_size=15, font_color='r')
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

#plt.colorbar(edges)
plt.plot()
plt.show()