def add_relationships(G, df_relations):
    for _, row in df_relations.iterrows():
        G.add_edge(
            row["source"],
            row["target"],
            relation=row["relation"]
        )
    return G
