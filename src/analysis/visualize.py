import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000,
        font_size=10
    )
    plt.show()
