import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def printGraph(G):
    nx.draw_networkx(G,arrows=True,with_labels=True)
    plt.show()


# creation of the empty graph
N = 5
nodes = range(N)  #list of nodes
flagNodes = [] #create an array that give the information of the taken nodes (0 if not take, 1 if already take)
for i in range(N):
    flagNodes.append(0)

print "Nodes = ", nodes
G = nx.DiGraph()
G.add_nodes_from(nodes)

#create the dictionay for labels

# pos = {}
# for i in range(N):
#     pos[i] = str(i)
# print pos

# creation of traffic matrix
tsd = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        if (i != j):
            tsd[i, j] = 0.5 + np.random.random()

print tsd

#nx.draw(G)
#plt.show()

# creation of the ring
# i is the source, j is the destination
MAX = tsd.max()
for i in range(N):
	for j in range(N):
		if tsd[i, j] == MAX:
			max_x = i
			max_y = j
			break
print "i = ", max_x, "j = ", max_y
#create the arc (i,j)
G.add_edge(max_x,max_y)
flagNodes[max_x] = 1
flagNodes[max_y] = 1

firstNode= max_x

s = max_y
# TODO i need to delete the nodes already taken node
for i in range(N-1):
    for j in range(N):
        flagNodes[s] = 1
        d = np.argmax(tsd[s]) #this is the next node index
        if flagNodes[d] == 0:
            G.add_edge(s,d)
            tsd[s] = 0
            print tsd
            flagNodes[d] = 1
            s = d

            break
        else :
            tsd[d] = 0


printGraph(G)


