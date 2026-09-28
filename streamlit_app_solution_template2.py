import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
# import the necessary functions and variables from searchAlgos.py
from searchAlgos import hospital_graph, locations, gbfs, a_star

# ------------------------------------------------------------------
# Streamlit GUI
# ------------------------------------------------------------------
st.set_page_config(page_title="Informed Search Visualizer", page_icon="🤖", layout="wide")

st.title("🤖 Emergency Supply Robot – Informed Search Visualizer")
st.write(
    "A hospital robot must deliver an emergency medical supply. Pick a start node, "
    "a goal node and a search algorithm (**Greedy Best-First Search** or **A\\***). "
    "The app runs the algorithm on the hospital corridor graph and highlights the "
    "solution path. Heuristic: Euclidean distance to the goal."
)

# define the nodes
nodes = list(hospital_graph.keys())

col1, col2, col3 = st.columns(3)
with col1:
    start = st.selectbox("Select Initial Node", nodes, index=nodes.index("Pharmacy"))
with col2:
    goal = st.selectbox("Select Goal Node", nodes, index=nodes.index("Emergency_Ward"))
with col3:
    algorithm = st.selectbox("Select Search Algorithm", ["GBFS", "A*"])


def draw_graph(path):
    G = nx.DiGraph()
    for node in hospital_graph:
        G.add_node(node)
    for node, neighbors in hospital_graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)
    pos = locations
    path_edges = list(zip(path, path[1:])) if path else []

    fig, ax = plt.subplots(figsize=(10, 6))
    node_colors = [
        "limegreen" if n == start else "tomato" if n == goal
        else "orange" if path and n in path else "lightblue"
        for n in G.nodes()
    ]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2200, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
    other_edges = [e for e in G.edges() if e not in path_edges]
    nx.draw_networkx_edges(G, pos, edgelist=other_edges, edge_color="gray",
                           arrows=True, arrowsize=18, node_size=2200, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=3.5,
                           arrows=True, arrowsize=22, node_size=2200, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"),
                                 font_size=8, ax=ax)
    ax.set_title(f"{algorithm} Solution Path")
    ax.axis("off")
    return fig


if st.button("Run Search"):
    if start == goal:
        st.warning("Start and goal are the same node - the path is trivial.")

    if algorithm == "GBFS":
        path, cost, expansion_order = gbfs(start, goal)
    else:
        path, cost, expansion_order = a_star(start, goal)

    if path is None:
        st.error(f"No path found from {start} to {goal}. "
                 "(The corridor graph is directed - edges only go one way.)")
        st.pyplot(draw_graph(None))
    else:
        # graph first, results below it
        st.pyplot(draw_graph(path))

        st.subheader("Search Result")
        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")
        st.write(f"**Node Expansion Order:** {' → '.join(expansion_order)}")
