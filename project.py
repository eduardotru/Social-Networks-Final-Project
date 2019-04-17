#! /bin/python
# Final project for CSCI4190 - Introduction to Social Networks Source Code
# Authors:
# Eduardo Enrique Trujillo Ramos - 1155128853
# Aubrey King - 1155128776

import snap

# Graph =  snap.LoadEdgeList(snap.PNEANet, "./soc-Epinions1.txt", 0, 1)
Graph = snap.GenRndGnm(snap.PNEANet, 10, 30)

infected = [1,2,3]

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
    string_node = str(nid) + ';0;' + str(state)
    labels[nid] = string_node

snap.DrawGViz(Graph, snap.gvlDot, "graph.png", "graph SIR", labels)
