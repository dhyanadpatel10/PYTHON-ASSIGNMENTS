from collections import defaultdict
import heapq

def resolve_dependencies(modules, imports):
    graph = defaultdict(list)
    indegree = {m: 0 for m in modules}

    # Build graph
    for a, b in imports:
        if b not in graph[a]:  # avoid duplicate edges
            graph[b].append(a)
            indegree[a] += 1

    # Min-heap for lexicographically smallest order
    heap = [m for m in modules if indegree[m] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        curr = heapq.heappop(heap)
        order.append(curr)
        for neighbor in graph[curr]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                heapq.heappush(heap, neighbor)

    # Detect cycle
    if len(order) != len(modules):
        cycle_nodes = [m for m in modules if indegree[m] > 0]
        print("CYCLE", cycle_nodes)
    else:
        print(" ".join(order))


# ---------------- SAMPLE INPUT ----------------
modules = ["alpha", "beta", "gamma", "delta", "epsilon"]
imports = [
    ("beta", "alpha"),   # beta imports alpha
    ("gamma", "beta"),   # gamma imports beta
    ("delta", "gamma"),  # delta imports gamma
    ("epsilon", "delta") # epsilon imports delta
]

resolve_dependencies(modules, imports)
