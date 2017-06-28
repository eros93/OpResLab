import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def add_costEdge(costEdges, path, traffic):
	length_path = len(path)
	for i in range(length_path -1):
		s_tmp = path[i]
		d_tmp = path[i+1]
		costEdges[s_tmp][d_tmp] += traffic

def shift(vector,n):
	return vector[n:] + vector[:n]


# ************ creation of the Random graph ************
#N = 20
#delta = 1
p = 0.1
for delta in [2,3]:
	for N in [20]:

		np.random.seed(7)
		nodes = range(N)  # list of nodes
		degree = [delta for i in xrange(N)]
		G=nx.directed_havel_hakimi_graph(degree,degree)
		G=nx.DiGraph(G)

		# ************ creation of traffic matrix ************
		tsd = np.zeros((N, N))
		for i in range(N):
			for j in range(N):
				if i != j:
					coin = np.random.random()
					if coin < p:
						tsd[i, j] = 5 + np.random.random() * 10
					else:
						tsd[i, j] = 0.5 + np.random.random()

		#print tsd
		# ************ remove symmetric edges************

		edges = G.edges_iter()
		for (i,j) in list(edges):
			if G.has_edge(j,i) & G.has_edge(i,j):
				G.remove_edge(i,j)


		lis = [(u,v) for (u,v) in G.edges_iter() if G.has_edge(v,u)]
		#print lis


		# ************ routing cost edge ************
		costEdges = np.zeros(shape=(N, N))

		labels = {}
		for s in range(N):
			for d in range(N):
				paths = []
				tot_edges = 0
				for path in nx.all_simple_paths(G, source=s, target=d):
					# print path
					paths.append(path)
				# tot_edges += len(path)-1
				for path in paths:
					# traf = tsd[s][d]*((tot_edges-len(path)-1)/tot_edges)
					# print traf
					# add_costEdge(costEdges, path, traf)

					add_costEdge(costEdges, path, tsd[s][d] / len(paths))
					#print costEdges

		# round to 2 digits of cost edges
		for i in range(len(costEdges)):
			costEdges[i] = np.round(costEdges[i], 2)
		#print costEdges

		maxFlowSecondGraph = costEdges.max()

		print "the fmax of the graph is: ", maxFlowSecondGraph

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

		del labels[tuple(zip(*ii))[0]]

		plt.figure(num=None, figsize=(10, 10))

		pos=nx.random_layout(G) # positions for all nodes

		nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightBlue', node_shape='o', alpha=1.0, cmap=None, vmin=None, vmax=None, ax=None, linewidths=None, label=None)
		nx.draw_networkx_edges(G,pos, edgelist=weigther_edge, edge_color='r', width=3)
		nx.draw_networkx_edge_labels(G,pos,edge_labels=label_weightest, label_pos=0.6, font_size=15, font_color='r', )
		nx.draw_networkx_edges(G,pos)
		nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
		nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

		string = "Random Graph with Nnodes = %d, Delta = %d" %(N,delta)
		plt.title(string)

		#string = "the fmax of the Random Graph is: ", np.round(maxFlowSecondGraph,2)
		#plt.xlabel(string)
		#plt.colorbar(edges)
		fname = "HIghLowTraffic_N%d_delta%d_fmax%d_rand" %(N,delta,maxFlowSecondGraph)
		plt.plot()
		plt.savefig(fname)