import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import json

inputfile = open("lab2_v2_random.json","w+")

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
output = {}
for delta in [2,3,4]:
	vector_fmax = []
	for N in range(5,15):
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



		string = "Random Graph with Nnodes = %d, Delta = %d" %(N,delta)
		fname = "N%d_delta%d_fmax%d_rand" %(N,delta,maxFlowSecondGraph)
		vector_fmax.append(maxFlowSecondGraph)

	output[str(delta)] = vector_fmax

inputfile.write(json.dumps(output))
inputfile.close()
