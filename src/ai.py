def answer_question(question: str, graph):
    q = question.lower()

    if "manager" in q:
        return [
            node
            for node, data in graph.nodes(data=True)
            if data.get("role") == "Manager"
        ]

    if "relation" in q:
        return list(graph.edges(data=True))

    if "personne" in q or "personnes" in q:
        return list(graph.nodes())

    return "Je n’ai pas encore la réponse à cette question."
