import networkx as nx
import matplotlib.pyplot as plt


savefile_counter = 0


#G = nx.karate_club_graph()
all_members = set(range(34))
club1 = {0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 16, 17, 19, 21}

G = nx.Graph()
G.add_nodes_from(all_members)
G.name = "Zachary's Karate Club"

with open('./zachary.dat','r') as inFile:
    row = 0
    for line in inFile:
        if row > 33:
            break
        member = line.split(" ")
        del member[0]
        member[len(member) -1] = (member[len(member) -1].split('\n'))[0]
        for col in range(0,len(member)):
            member[col] = int(member[col])
            if member[col] == 1:
                G.add_edge(row, col)
        row += 1

color_map = []
for node in G:
    if node in club1:
        color_map.append('green')
    else:
        color_map.append('red')

labeldict = {}
edgedict = []
for i in range (0,len(G)):
    labeldict[i] = i

for i in range (0,len(G.edges)):
    edgedict.append('black')

print(G.edges)

labeldict[0] = "JA"
labeldict[33] = "HI"


nx.draw(G, node_color = color_map, edge_color=edgedict, width=2, labels=labeldict, with_labels=True)
plt.show()
plt.savefig('./graph/karate%s.png' % savefile_counter)


graphs = list(nx.connected_component_subgraphs(G))
print(len(graphs))

while len(graphs) < 10:
    betweeness = nx.edge_betweenness(G, 34, normalized=True)
    sort = sorted(betweeness.items(), key=lambda x: x[1])

    leading_edge = sort[len(sort) - 1][0]

    edge_counter = 0
    for u, v in G.edges:
        if (u == leading_edge[0] and v == leading_edge[1]):
            edgedict[edge_counter] = 'blue'
            nx.draw(G, node_color=color_map, edge_color=edgedict, width=2, labels=labeldict, with_labels=True)
            plt.show()
            del edgedict[edge_counter]
            G.remove_edge(u, v)
            nx.draw(G, node_color=color_map, edge_color=edgedict, width=2, labels=labeldict, with_labels=True)
            plt.show()
            break
        else:
            pass
        edge_counter += 1
        # print("%s, %s : %s, %s" % (u, v,  leading_edge[0], leading_edge[1]))
    graphs = list(nx.connected_component_subgraphs(G))



