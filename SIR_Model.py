#! /bin/python
# Final project for CSCI4190 - Introduction to Social Networks Source Code
# Authors:
# Eduardo Enrique Trujillo Ramos - 1155128853
# Aubrey King - 1155128776

import snap
import random
import matplotlib.pyplot as plt

Graph =  snap.LoadEdgeList(snap.PNEANet, "./soc-Epinions1.txt", 0, 1)
# Graph = snap.GenRndGnm(snap.PNEANet, 10, 30)

# Initial parameters of the model
infected = [1,2,3]
p = 0.5
time_infected = 2

# Susceptible = 0
# Infectious = 1
# Removed = 2

labels = snap.TIntStrH()
for Node in Graph.Nodes():
    nid = Node.GetId()
    state = 0
    if nid in infected:
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
number_infected = len(infected)
number_susceptible = number_nodes - len(infected)

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

plt.plot(susceptible, 'g-')
plt.plot(infected, 'r-')
plt.plot(removed, '-')
plt.show()

# for NI in G.Nodes():
#     nid = NI.GetId()
#     ival = G.GetIntAttrDatN(nid, "state")
#     step_number = G.GetIntAttrDatN(nid, "step")
#     print(ival, step_number)
