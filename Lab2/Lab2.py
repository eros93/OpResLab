import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def printGraph(G):
	nx.draw_networkx(G,arrows=True,with_labels=True)
	plt.show()


def add_costEdge(costEdges, path, tsd):
	length_path = len(path)
	for i in range(length_path -1):
		s = path[i]
		d = path[i+1]
		costEdges[s] += tsd[s, d]


# ************ creation of the empty graph ************
N = 6
delta = 3
nodes = range(N)  # list of nodes
flagNodes = []  # create an array that give the information of the taken nodes (0 if not take, 1 if already take)
for i in range(N):
	flagNodes.append(0)

print "Nodes = ", nodes
G = nx.DiGraph()
G.add_nodes_from(nodes)


# ************ creation of traffic matrix ************
tsd = np.zeros((N, N))
for i in range(N):
	for j in range(N):
		if i != j:
			tsd[i, j] = 0.5 + np.random.random()

print tsd

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

flowNodes = []
flowNodes.append(max_x)
flowNodes.append(max_y)

costEdges = np.zeros(N)
for i in range(N-1):
	for j in range(N):
		flagNodes[s] = 1
		d = np.argmax(tsd_tmp[s])   # this is the next node index

		if flagNodes[d] == 0:
			G.add_edge(s, d)
			flowNodes.append(d)
			tsd_tmp[s, d] = 0
			flagNodes[d] = 1
			s = d
			break
		else:
			tsd_tmp[s, d] = 0

G.add_edge(s, firstNode)

# ************ routing cost edge ************

print "flowNodes ",flowNodes

labels = {}
for s in range(N):
	for d in range(N):
		for path in nx.all_simple_paths(G, source=s, target=d):
			print path
			add_costEdge(costEdges, path, tsd)



int_costEdges = []


for item in costEdges:
	int_costEdges.append(int(item))

print "costEdges: ", int_costEdges

# ************ creation the dict for the labels ************

firstNode = flowNodes[0]
for i in range(N-1):
	labels[(flowNodes[i],flowNodes[i + 1])] = int_costEdges[i]

lastNode = flowNodes[N-1]

labels[(lastNode, firstNode)] = int_costEdges[lastNode]
print labels

costEdges = hash(tuple(np.array(costEdges)))

pos=nx.spring_layout(G) # positions for all nodes

colors = range(N)


# ************ print the initial ring graph ************

# print(nx.shortest_path(G,source=0,target=4))
#
# fig, ax = plt.subplots(nrows=2,ncols=1)
#
# plt.subplot(2,1,1)
# nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightBlue', node_shape='o', alpha=1.0, cmap=None, vmin=None, vmax=None, ax=None, linewidths=None, label=None)
# #nx.draw_networkx_edges(G,pos)
# nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
# nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
# edges = nx.draw_networkx_edges(G,pos,edge_color=colors,width=3,edge_cmap=plt.cm.Blues)
# plt.colorbar(edges)
# plt.plot()
# plt.subplot(2,1,2)

# ************ print the initial ring graph ************

print(nx.shortest_path(G,source=0,target=4))

fig, ax = plt.subplots(nrows=2,ncols=1)

plt.subplot(2,1,1)
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightBlue', node_shape='o', alpha=1.0, cmap=None, vmin=None, vmax=None, ax=None, linewidths=None, label=None)
#nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
edges = nx.draw_networkx_edges(G,pos)
#plt.colorbar(edges)
plt.plot()
plt.subplot(2,1,2)

#print nx.shortest_path(G,flowNodes[0],flowNodes[-1])

# ************ start with the algorithm ************

#print(nx.shortest_path(G,source=0,target=4))

# divide the graph delta times for add new path

partial_flowNode = (len(flowNodes)) // (delta -1)
print "partial_flowNode", partial_flowNode

chunks = [flowNodes[i:i+partial_flowNode] for i in xrange(0, len(flowNodes), partial_flowNode)]
print "chunks", chunks
for chunk in chunks:
	try :
		s = chunks[0][0]
		d = chunk[-1]
		print "s ", s
		print "d ", d
		if G.has_edge(d,s) == False:
			G.add_edge(chunks[0][0], chunk[-1])
		else:
			G.add_edge(chunks[0][0], chunk[-2])
	except:
		pass


pos=nx.spring_layout(G) # positions for all nodes

nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightBlue', node_shape='o', alpha=1.0, cmap=None, vmin=None, vmax=None, ax=None, linewidths=None, label=None)
nx.draw_networkx_edges(G,pos)
nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
edges = nx.draw_networkx_edges(G,pos)

labels = {}
for s in range(N):
	for d in range(N):
		for path in nx.all_simple_paths(G, source=s, target=d):
			print path


#plt.colorbar(edges)
plt.plot()
plt.show()