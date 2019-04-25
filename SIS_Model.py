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


labels = snap.TIntStrH()

for index in range(0,4):
    Graph = graphList[index]
    print("Next Graph to plot: SIS Model for " + graphNameList[index])
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
        string_node = str(nid) + ';0;' + str(state)
        labels[nid] = string_node

    #snap.DrawGViz(Graph, snap.gvlDot, "graph.png", "graph SIR", labels)

    number_S = number_node - len(init_infected)
    number_I = len(init_infected)
    number_echo = 0

    infected_list = []
    susceptible_list = []

    infected_list.append(number_I)
    susceptible_list.append(number_S)

    while (number_S != number_node) & (number_echo < 100):
        for NI in Graph.Nodes():
            nid = NI.GetId()
            nodeState = Graph.GetIntAttrDatN(nid, "state")
            # if it's infectious, it will infect its neighbors.
            if nodeState == 1:
                for nid1 in NI.GetOutEdges():
                    neighborState = Graph.GetIntAttrDatN(nid1, "state")

                    # with probability of p=0.2, a susceptible node will be infected.
                    if (random.uniform(0,1) <= p) and (neighborState == 0):
                        # The state 3 is temporary in order to avoid repeated infection.
                        Graph.AddIntAttrDatN(nid1, 3, "state")

                # update the step of infection.
                step_this = Graph.GetIntAttrDatN(nid, "step")
                step_this += 1
                if step_this == time_infected:
                    # The state 4 is temporary in order to avoid repeated infection.
                    Graph.AddIntAttrDatN(nid, 4, "state")
                    Graph.AddIntAttrDatN(nid, 0, "step")

        # Count the number of susceptible or removed nodes.
        number_S_temp = 0
        for NI in Graph.Nodes():
            nid = NI.GetId()
            nodeState = Graph.GetIntAttrDatN(nid, "state")
            if nodeState == 3: # The nodes should be updated as infectious now.
                Graph.AddIntAttrDatN(nid, 1, "state")
                nodeState = 1
            elif nodeState == 4:
                Graph.AddIntAttrDatN(nid, 0, "state")
                nodeState = 0

            # update the label for each node for visualization.
            step_number = Graph.GetIntAttrDatN(nid, "step")
            string_node = str(NI.GetId()) + ';' + str(step_number) + ';' + str(nodeState)
            labels[NI.GetId()] = string_node
            #snap.DrawGViz(G, snap.gvlDot, "temp_graph%d.png" % number_echo, "graph %d" % number_echo, labels)

            if nodeState == 0:
                number_S_temp += 1



        number_S = number_S_temp
        number_I = number_node - number_S
        number_echo += 1
        infected_list.append(number_I)
        susceptible_list.append(number_S)
        # print("Infected nodes: " + str(number_I) + " At loop: " + str(number_echo))


    graph_name = graphNameList[index]
    title = 'SIS %s with p=%f, # of init_infected=%d, time_infected=%d' % (graph_name, p, len(init_infected), time_infected)
    png_name = 'SIS_%s_p=%f_init=%d_timeinf=%d.png' % (graph_name, p, len(init_infected), time_infected)
    plt.title(title)
    plt.plot(susceptible_list, 'g-', label='Susceptible')
    plt.plot(infected_list, 'r-', label='Infected')
    plt.legend(loc='best')
    plt.savefig(png_name)


#for NI in Graph.Nodes():
    #nid = NI.GetId()
    #nodeState = Graph.GetIntAttrDatN(nid, "state")
    #step_number = Graph.GetIntAttrDatN(nid, "step")
    #print(nodeState, step_number)
