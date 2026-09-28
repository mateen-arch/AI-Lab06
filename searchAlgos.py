"""Search algorithms + hospital graph (Use case: Emergency Supply Robot).
Imported by streamlit_app_solution_template2.py"""
import math
import heapq

locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6),
}

hospital_graph = {
    "Pharmacy": {"Main_Corridor": 2.2, "Patient_Wing": 4.1},
    "Main_Corridor": {"Nursing_Station": 2.2},
    "Patient_Wing": {"Laboratory": 5.0},
    "Nursing_Station": {"Laboratory": 3.2, "Emergency_Ward": 6.0},
    "Laboratory": {"Emergency_Ward": 3.2},
    "Emergency_Ward": {},
}


def heuristic(current, goal):
    """Euclidean (straight-line) distance from current to goal."""
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path


def path_cost(path, graph=hospital_graph):
    return sum(graph[a][b] for a, b in zip(path, path[1:]))


def gbfs(start, goal):
    """Greedy Best-First Search, f(n) = h(n).
    Returns (path, total_cost, expansion_order); path is None if no path."""
    counter = 0                                  # tie-breaker for equal priorities
    frontier = [(heuristic(start, goal), counter, start)]
    came_from = {start: None}
    explored, expansion_order = set(), []
    while frontier:
        _, _, node = heapq.heappop(frontier)
        if node in explored:
            continue
        explored.add(node)
        expansion_order.append(node)
        if node == goal:
            path = reconstruct_path(came_from, node)
            return path, path_cost(path), expansion_order
        for nb in hospital_graph[node]:
            if nb not in explored and nb not in came_from:
                came_from[nb] = node
                counter += 1
                heapq.heappush(frontier, (heuristic(nb, goal), counter, nb))
    return None, float("inf"), expansion_order


def a_star(start, goal):
    """A* Search, f(n) = g(n) + h(n).
    Returns (path, total_cost, expansion_order); path is None if no path."""
    counter = 0
    g_cost = {start: 0.0}
    came_from = {start: None}
    frontier = [(heuristic(start, goal), counter, start)]
    closed, expansion_order = set(), []
    while frontier:
        _, _, node = heapq.heappop(frontier)
        if node in closed:
            continue
        closed.add(node)
        expansion_order.append(node)
        if node == goal:
            path = reconstruct_path(came_from, node)
            return path, g_cost[node], expansion_order
        for nb, cost in hospital_graph[node].items():
            tentative_g = g_cost[node] + cost
            if nb not in g_cost or tentative_g < g_cost[nb]:
                g_cost[nb] = tentative_g
                came_from[nb] = node
                counter += 1
                heapq.heappush(frontier, (tentative_g + heuristic(nb, goal), counter, nb))
    return None, float("inf"), expansion_order
