#! /bin/python
# Final project for CSCI4190 - Introduction to Social Networks Source Code
# Authors:
# Eduardo Enrique Trujillo Ramos - 1155128853
# Aubrey King - 1155128776

import snap
import random
import matplotlib.pyplot as plt
import sys

if len(sys.argv) < 4:
    print('Incorrect number of arguments. Way of usage:')
    print('python ' + sys.argv[0] + ' <p of infection> <# of initial infected> <time infected>')
    exit(1)

MainGraph =  snap.LoadEdgeList(snap.PNEANet, "./soc-Epinions1.txt", 0, 1)

#creation of various graphs
#Low Clustering Coefficient
LowClusterGraph = snap.GenRndGnm(snap.PNEANet, 1000, 3000)

#High Clustering Coefficient
HighClusterGraph = snap.GenFull(snap.PNEANet, 1000)

#Random subgraph
NIdV = snap.TIntV()
rangList = random.sample(range(MainGraph.GetNodes()), 7000)

for i in range(1, 7000):
    NIdV.Add(rangList[i])

subGraph = snap.GetSubGraph(MainGraph, NIdV)


graphList = []
graphList.append(MainGraph)
graphList.append(subGraph)
graphList.append(LowClusterGraph)
graphList.append(HighClusterGraph)

graphNameList = []
graphNameList.append("Main Real World Graph")
graphNameList.append("Subset of Real World Graph")
graphNameList.append("Low Cluster Graph")
graphNameList.append("High Cluster Graph")
# Susceptible = 0
# Infectious = 1
# Removed = 2

labels = snap.TIntStrH()



for index in range(0,4):

    Graph = graphList[index]
    print("Next Graph to plot: SIR Model for " + graphNameList[index])
    number_node = Graph.GetNodes()
    init_infected = random.sample(range(1, Graph.GetNodes()+1), int(sys.argv[2]))
    p = float(sys.argv[1])
    time_infected = int(sys.argv[3])

    for Node in Graph.Nodes():
        nid = Node.GetId()
        state = 0
        if nid in init_infected:
            Graph.AddIntAttrDatN(nid, 1, "state")
            state = 1
        else:
            Graph.AddIntAttrDatN(nid, 0, "state")
            state = 0
        Graph.AddIntAttrDatN(nid, 0, "step")

        # Labels
        # string_node = str(nid) + ';0;' + str(state)
        # labels[nid] = string_node

    # snap.DrawGViz(Graph, snap.gvlDot, "graph.png", "graph SIR", labels)

    number_nodes = Graph.GetNodes()
    number_removed = 0
    number_infected = len(init_infected)
    number_susceptible = number_nodes - len(init_infected)

    removed = [number_removed]
    infected = [number_infected]
    susceptible = [number_susceptible]

    iterations = 0
    while number_removed + number_susceptible < number_nodes:
        for Node in Graph.Nodes():
            nid = Node.GetId()
            state = Graph.GetIntAttrDatN(nid, "state")
            # If infectious it'll infect it's neighbos with probability p
            if state == 1:
                for neighbor in Node.GetOutEdges():
                    neighbor_state = Graph.GetIntAttrDatN(neighbor, "state")

                    # with probability of p, a susceptible node will be infected.
                    if (random.uniform(0,1) <= p) and (neighbor_state == 0):
                        # The state 3 is temporary in order to avoid repeated infection.
                        Graph.AddIntAttrDatN(neighbor, 3, "state")

                # update the step of infection.
                step = Graph.GetIntAttrDatN(nid, "step")
                step += 1
                Graph.AddIntAttrDatN(nid, step, "step")
                # We will remove the node once it has been infected during time_infected time
                if step == time_infected:
                    Graph.AddIntAttrDatN(nid, 2, "state")

        # Count the number of each type of node
        number_removed = 0
        number_susceptible = 0
        number_infected = 0
        for Node in Graph.Nodes():
            nid = Node.GetId()
            state = Graph.GetIntAttrDatN(nid, "state")
            if state == 3: # The nodes should be updated as infectious now.
                Graph.AddIntAttrDatN(nid, 1, "state")
                state = 1

            # update the label for each node for visualization.
            # step = Graph.GetIntAttrDatN(nid, "step")
            # string_node = str(NI.GetId()) + ';' + str(step_number) + ';' + str(ival)
            # labels[NI.GetId()] = string_node

            if state == 2:
                number_removed += 1
            elif state == 0:
                number_susceptible += 1
            else:
                number_infected += 1

        removed.append(number_removed)
        susceptible.append(number_susceptible)
        infected.append(number_infected)

        iterations += 1

    graph_name = graphNameList[index]
    title = 'SIR %s with p=%f, # of init_infected=%d, time_infected=%d' % (graph_name, p, len(init_infected), time_infected)
    png_name = 'SIR_%s_p=%f_init=%d_timeinf=%d.png' % (graph_name, p, len(init_infected), time_infected)
    plt.title(title)
    plt.plot(susceptible, 'g-', label='Susceptible')
    plt.plot(infected, 'r-', label='Infected')
    plt.plot(removed, '-', label='Removed')
    plt.legend(loc='best')
    plt.savefig(png_name)

# for NI in G.Nodes():
#     nid = NI.GetId()
#     ival = G.GetIntAttrDatN(nid, "state")
#     step_number = G.GetIntAttrDatN(nid, "step")
#     print(ival, step_number)
