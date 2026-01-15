from src.ingestion.load_data import load_csv
from src.graph.build_graph import build_people_graph
from src.graph.add_edges import add_relationships
from rich import print

# Chargement des données
people_df = load_csv("data/people.csv")
relations_df = load_csv("data/relations.csv")

# Construction du graph
graph = build_people_graph(people_df)
graph = add_relationships(graph, relations_df)

# Vision
print("[bold green]Mithrandir Vision activée 👁️[/bold green]")
print("\n[bold]Personnes :[/bold]")
print(graph.nodes(data=True))

print("\n[bold]Relations :[/bold]")
print(graph.edges(data=True))

from src.analysis.metrics import compute_metrics

metrics = compute_metrics(graph)

print("\n[bold]📊 Centralité (importance dans le réseau)[/bold]")
for person, score in metrics["degree_centrality"].items():
    print(f"{person}: {score:.2f}")

from src.analysis.visualize import visualize_graph

visualize_graph(graph)
