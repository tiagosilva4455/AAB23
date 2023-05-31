from MyGraph import MyGraph


class WeightedGraph(MyGraph):
    def __init__(self, g):
        super().__init__(g)

    def shortest_path_with_weights(graph, start, end): #caminho com pesos
        distances = {start: 0}
        predecessors = {start: None}
        queue = [(start, 0)]
        while queue:
            node, dist = queue.pop(0)
            if node == end:
                path = []
                while node is not None:
                    path.insert(0, node)
                    node = predecessors[node]
                return path
            for destination, weight in graph[node]:
                new_dist = dist + weight
                if destination not in distances or new_dist < distances[destination]:
                    distances[destination] = new_dist
                    predecessors[destination] = node
                    queue.append((destination, new_dist))
        return []

    def distance_with_weights(graph, start, end):
        distances = {start: 0}
        queue = [(start, 0)]
        while queue:
            node, dist = queue.pop(0)
            if node == end:
                return dist
            for destination, weight in graph[node]:
                new_dist = dist + weight
                if destination not in distances or new_dist < distances[destination]:
                    distances[destination] = new_dist
                    queue.append((destination, new_dist))
        return float("inf")

    def shortest_path_with_weights(graph, start, end):
        distances = {start: 0}
        predecessors = {start: None}
        queue = [(start, 0)]
        while queue:
            node, dist = queue.pop(0)
            if node == end:
                path = []
                while node is not None:
                    path.insert(0, node)
                    node = predecessors[node]
                return path
            for destination, weight in graph[node]:
                new_dist = dist + weight
                if destination not in distances or new_dist < distances[destination]:
                    distances[destination] = new_dist
                    predecessors[destination] = node
                    queue.append((destination, new_dist))
        return []