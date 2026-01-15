import streamlit as st
import networkx as nx
import plotly.graph_objects as go

from src.ingestion.load_data import load_csv
from src.graph.build_graph import build_people_graph
from src.graph.add_edges import add_relationships
from src.analysis.metrics import compute_metrics
from src.ai import answer_question


# ================== CONFIG ==================
st.set_page_config(
    page_title="Mithrandir – Vision décisionnelle",
    page_icon="👁️",
    layout="wide"
)

#
st.markdown("""
<style>
/* Fond principal */
.stApp {
    background-color: #0f172a;
    color: #e5e7eb;
}

/* Titres */
h1, h2, h3 {
    color: #f8fafc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
}

/* Cartes KPI */
[data-testid="metric-container"] {
    background-color: #020617;
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid #1e293b;
}

/* Inputs */
input {
    background-color: #020617 !important;
    color: #e5e7eb !important;
}

/* Boutons */
button {
    background-color: #6366f1 !important;
    color: white !important;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

#
# ================== DATA ==================
try:
    people_df = load_csv("data/people.csv")
    relations_df = load_csv("data/relations.csv")

    graph = build_people_graph(people_df)
    graph = add_relationships(graph, relations_df)

except Exception as e:
    st.error(f"Erreur de chargement des données : {e}")
    st.stop()



# ================== SIDEBAR ==================
st.sidebar.markdown("## 👁️ Mithrandir")
st.sidebar.caption("Graph Intelligence Platform")

page = st.sidebar.radio(
    "Navigation",
    ["Accueil", "Graph", "Métriques", "IA"]
)



# ================== HEADER ==================
st.title("🧙‍♂️ Mithrandir")
st.markdown(
    "### Plateforme d’analyse relationnelle et décisionnelle\n"
    "Transformez vos données en **vision exploitable** grâce aux graphes."
)
st.markdown("---")


# ================== ACCUEIL ==================
if page == "Accueil":
    col1, col2, col3 = st.columns(3)

    col1.metric("👥 Entités", len(graph.nodes()))
    col2.metric("🔗 Relations", len(graph.edges()))
    col3.metric("📊 Indicateurs", len(compute_metrics(graph)))

    st.success(
    "Mithrandir transforme vos données en **vision relationnelle**.\n\n"
    "Explorez les **relations**, identifiez les **acteurs clés**, "
    "et interrogez le système en langage naturel."
)



# ================== GRAPH ==================
elif page == "Graph":
    st.header("👁️ Réseau relationnel")

    pos = nx.spring_layout(graph)

    edge_x, edge_y = [], []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=1, color="#888"),
        hoverinfo="none"
    )

    node_x, node_y, text = [], [], []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=text,
        textposition="bottom center",
        marker=dict(size=22, color="#636EFA")
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    st.caption("💡 Astuce : survolez les nœuds et zoomez pour explorer le réseau.")
    st.plotly_chart(fig, use_container_width=True)


# ================== METRICS ==================
elif page == "Métriques":
    st.header("📊 Indicateurs clés")

    metrics = compute_metrics(graph)
    cols = st.columns(len(metrics["degree_centrality"]))

    for col, (name, score) in zip(cols, metrics["degree_centrality"].items()):
        col.metric(label=name, value=f"{score:.2f}")


# ================== IA ==================
elif page == "IA":
    st.header("🤖 Interroger Mithrandir")

    question = st.text_input("Pose une question sur le réseau")
    if question:
        answer = answer_question(question, graph)
        st.success(answer)


# ================== FOOTER ==================
st.caption("© 2026 Mithrandir • Graph Intelligence Platform • Demo Version")

