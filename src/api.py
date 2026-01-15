from fastapi import FastAPI
from src.ingestion.load_data import load_csv
from src.graph.build_graph import build_people_graph
from src.graph.add_edges import add_relationships
from src.analysis.metrics import compute_metrics

app = FastAPI(title="Mithrandir API", version="1.0")

def build_graph():
    people_df = load_csv("data/people.csv")
    relations_df = load_csv("data/relations.csv")
    graph = build_people_graph(people_df)
    return add_relationships(graph, relations_df)

@app.get("/")
def root():
    return {"message": "Mithrandir API is running 👁️"}

@app.get("/nodes")
def get_nodes():
    graph = build_graph()
    return graph.nodes(data=True)

@app.get("/edges")
def get_edges():
    graph = build_graph()
    return graph.edges(data=True)

@app.get("/metrics")
def get_metrics():
    graph = build_graph()
    return compute_metrics(graph)
