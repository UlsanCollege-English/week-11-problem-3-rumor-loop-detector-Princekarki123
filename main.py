"""
HW03 — Rumor Loop Detector (Cycle in Undirected Graph)

Implement:
- has_cycle(graph)
- find_cycle(graph)
"""

def has_cycle(graph):
    """Return True if the undirected graph has any cycle; else False."""
    result = find_cycle(graph)
    return result is not None


def find_cycle(graph):
    """Return a list of nodes forming a simple cycle where first == last.
    If no cycle, return None.

    Note:
    - Use DFS and a parent map.
    - Self-loop counts: return [u, u].
    """

    visited = set()
    parent = {}

    # Check self-loops first
    for u in graph:
        for v in graph[u]:
            if u == v:  # self-loop
                return [u, u]

    # DFS helper
    def dfs(node):
        visited.add(node)

        for nbr in graph[node]:
            # neighbor not visited → explore deeper
            if nbr not in visited:
                parent[nbr] = node
                result = dfs(nbr)
                if result is not None:
                    return result

            # neighbor is visited BUT not parent → cycle!
            elif parent.get(node) != nbr:
                # reconstruct cycle from node → nbr
                return reconstruct_cycle(node, nbr)

        return None

    def reconstruct_cycle(x, y):
        """Reconstruct cycle when edge x-y completes a loop."""
        path_x = [x]
        path_y = [y]

        # Move up from x
        px = parent.get(x)
        while px is not None:
            path_x.append(px)
            px = parent.get(px)

        # Move up from y
        py = parent.get(y)
        while py is not None:
            path_y.append(py)
            py = parent.get(py)

        # Find first common ancestor
        set_y = set(path_y)
        meet = None
        for node in path_x:
            if node in set_y:
                meet = node
                break

        # Build the actual cycle
        cycle = []

        # from x → meet
        cur = x
        while cur != meet:
            cycle.append(cur)
            cur = parent[cur]
        cycle.append(meet)

        # from meet → y (reverse direction)
        temp = []
        cur = y
        while cur != meet:
            temp.append(cur)
            cur = parent[cur]

        cycle += reversed(temp)

        cycle.append(x)  # close the cycle
        return cycle

    # Run DFS from each unvisited node (graph may be disconnected)
    for node in graph:
        if node not in visited:
            parent[node] = None
            result = dfs(node)
            if result is not None:
                return result

    return None
