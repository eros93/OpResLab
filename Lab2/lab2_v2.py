import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def printGraph(G):
	nx.draw_networkx(G,arrows=True,with_labels=True)
	plt.show()


def add_costEdge(costEdges, path, traffic):
	length_path = len(path)
	for i in range(length_path -1):
		s_tmp = path[i]
		d_tmp = path[i+1]
		costEdges[s_tmp][d_tmp] += traffic

def shift(vector,n):
	return vector[n:] + vector[:n]


# ************ creation of the empty graph ************
N = 15
delta = 3
np.random.seed(7)
nodes = range(N)  # list of nodes
flagNodes = []  # create an array that give the information of the taken nodes (0 if not take, 1 if already take)
for i in range(N):
	flagNodes.append(0)

#print "Nodes = ", nodes
G = nx.DiGraph()
G.add_nodes_from(nodes)


# ************ creation of traffic matrix ************
tsd = np.zeros((N, N))
for i in range(N):
	for j in range(N):
		if i != j:
			tsd[i, j] = 0.5 + np.random.random()

#print tsd

# ************ creation of the ring ************
# i is the source, j is the destination

tsd_tmp = tsd.copy()
MAX = tsd.max()

for i in range(N):
	for j in range(N):
		if tsd[i, j] == MAX:
			max_x = i
			max_y = j
			break

#print "i = ", max_x , "j = ", max_y

# create the arc (i,j)
G.add_edge(max_x, max_y)
flagNodes[max_x] = 1
flagNodes[max_y] = 1

firstNode = max_x

s = max_y

flowNodesRing = []
flowNodesRing.append(max_x)
flowNodesRing.append(max_y)

for i in range(N-1):
	for j in range(N):
		flagNodes[s] = 1
		d = np.argmax(tsd_tmp[s])   # this is the next node index

		if flagNodes[d] == 0:
			G.add_edge(s, d)
			flowNodesRing.append(d)
			tsd_tmp[s, d] = 0
			flagNodes[d] = 1
			s = d
			break
		else:
			tsd_tmp[s, d] = 0

G.add_edge(s, firstNode)

# ************ routing cost edge ************

costEdges = np.zeros(shape=(N,N))

#print "flowNodesRing ",flowNodesRing

labels = {}
for s in range(N):
	for d in range(N):
		for path in nx.all_simple_paths(G, source=s, target=d):
			#print path
			add_costEdge(costEdges, path, tsd[s][d])
			#print costEdges


# round to 2 digits of cost edges
for i in range(len(costEdges)):
	costEdges[i] = np.round(costEdges[i], 2)
maxFlowFirstGraph = costEdges.max()


# ************ creation the dict for the labels ************

for edge in np.transpose(np.nonzero(costEdges)):
	labels[(edge[0], edge[1])] = costEdges[edge[0]][edge[1]]


#pos=nx.shell_layout(G) # positions for all nodes

#colors = range(N)


# ************ print the initial ring graph ************


# fig, ax = plt.subplots(nrows=2,ncols=1)
#
# plt.subplot(2,1,1)
# nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightBlue', node_shape='o', alpha=1.0, cmap=None, vmin=None, vmax=None, ax=None, linewidths=None, label=None)
# #nx.draw_networkx_edges(G,pos)
# nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
# nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
# edges = nx.draw_networkx_edges(G,pos)
# #plt.colorbar(edges)
# plt.plot()
# plt.subplot(2,1,2)

#print nx.shortest_path(G,flowNodesRing[0],flowNodesRing[-1])

# ************ start with the algorithm ************

#print(nx.shortest_path(G,source=0,target=4))

# divide the graph delta times for add new path

partial_flowNode = (len(flowNodesRing)) // (delta -1)
#print "partial_flowNode", partial_flowNode

for step in range(N):
	flowNodesRingAlg = shift(flowNodesRing, step)
	chunks = [flowNodesRingAlg[i:i+partial_flowNode] for i in xrange(0, len(flowNodesRingAlg), partial_flowNode)]
	#print "chunks", chunks
	for chunk in chunks:
		try :
			s = chunks[0][0]
			d = chunk[-1]
			#print "s ", s
			#print "d ", d
			if G.has_edge(d,s) == False:
				G.add_edge(chunks[0][0], chunk[-1])
			else:
				G.add_edge(chunks[0][0], chunk[-2])
		except:
			pass


	# ************ routing cost edge ************

	costEdges = np.zeros(shape=(N,N))

	labels = {}
	for s in range(N):
		for d in range(N):
			paths = []
			tot_edges=0
			for path in nx.all_simple_paths(G, source=s, target=d):
				#print path
				paths.append(path)
				#tot_edges += len(path)-1
			for path in paths:
				# traf = tsd[s][d]*((tot_edges-len(path)-1)/tot_edges)
				# print traf
				# add_costEdge(costEdges, path, traf)

				add_costEdge(costEdges, path, tsd[s][d]/len(paths))
				#print costEdges


	# round to 2 digits of cost edges
	for i in range(len(costEdges)):
		costEdges[i] = np.round(costEdges[i], 2)
	#print costEdges

maxFlowSecondGraph = costEdges.max()

print "the fmax of the first graph is %f\n the fmax of the second graph is %f" %(maxFlowFirstGraph,maxFlowSecondGraph)


ii= np.where(costEdges==maxFlowSecondGraph)
print "the fmax of the graph is: ", maxFlowSecondGraph
#print G.edges()
weigther_edge=[]
weigther_edge.append(tuple(zip(*ii))[0])

numberOfEdges = G.number_of_edges()
print "the number of edges is: ", numberOfEdges
# ************ creation the dict for the labels ************

del labels
labels = {}
label_weightest={}
for edge in np.transpose(np.nonzero(costEdges)):
	labels[(edge[0], edge[1])] = costEdges[edge[0]][edge[1]]

label_weightest[tuple(zip(*ii))[0]] = maxFlowSecondGraph

#print labels



pos = nx.shell_layout(G) # positions for all nodes

nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightBlue', node_shape='o', alpha=1.0, cmap=None, vmin=None, vmax=None, ax=None, linewidths=None, label=None)
nx.draw_networkx_edges(G,pos, edgelist=weigther_edge, edge_color='r', width=3)
nx.draw_networkx_edge_labels(G,pos,edge_labels=label_weightest, label_pos=0.6, font_size=15, font_color='r', )
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

string = "Greedy Heuristic Graph with Nnodes = %d, Nedges = %d" %(N,numberOfEdges)
plt.title(string)
#plt.colorbar(edges)
plt.plot()
plt.show()