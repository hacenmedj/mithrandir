import networkx as nx

def build_people_graph(df):
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_node(row["name"], role=row["role"])
    return G
