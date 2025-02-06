from collections import deque
from prettytable import PrettyTable

class FlowGraph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.capacity = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, start, end, cap):
        self.capacity[start][end] = cap

    def bfs(self, source, sink, parents):
        visited = [False] * self.num_vertices
        queue = deque([source])
        visited[source] = True

        while queue:
            current = queue.popleft()
            for neighbor, residual_cap in enumerate(self.capacity[current]):
                if not visited[neighbor] and residual_cap > 0:
                    queue.append(neighbor)
                    visited[neighbor] = True
                    parents[neighbor] = current
                    if neighbor == sink:
                        return True
        return False

    def max_flow(self, source, sink):
        parents = [-1] * self.num_vertices
        total_flow = 0
        flow_matrix = [[0] * self.num_vertices for _ in range(self.num_vertices)]

        while self.bfs(source, sink, parents):
            bottleneck_flow = float("inf")
            current = sink
            while current != source:
                prev = parents[current]
                bottleneck_flow = min(bottleneck_flow, self.capacity[prev][current])
                current = prev

            total_flow += bottleneck_flow
            current = sink
            while current != source:
                prev = parents[current]
                self.capacity[prev][current] -= bottleneck_flow
                self.capacity[current][prev] += bottleneck_flow
                flow_matrix[prev][current] += bottleneck_flow
                current = prev

        return total_flow, flow_matrix

if __name__ == "__main__":
    vertices = 22
    source = 0
    sink = vertices - 1

    graph = FlowGraph(vertices)
    
    graph.add_edge(source, 1, 25)
    graph.add_edge(source, 2, 20)
    graph.add_edge(source, 3, 15)
    graph.add_edge(source, 4, 15)
    graph.add_edge(source, 5, 30)
    graph.add_edge(source, 2, 10)
    
    graph.add_edge(1, 6, 15)
    graph.add_edge(1, 7, 10)
    graph.add_edge(1, 8, 20)
    graph.add_edge(2, 9, 15)
    graph.add_edge(2, 10, 10)
    graph.add_edge(2, 11, 25)
    graph.add_edge(3, 12, 20)
    graph.add_edge(3, 13, 15)
    graph.add_edge(3, 14, 10)
    graph.add_edge(4, 15, 20)
    graph.add_edge(4, 16, 10)
    graph.add_edge(4, 17, 15)
    graph.add_edge(4, 18, 5)
    graph.add_edge(4, 19, 10)
    
    graph.add_edge(6, sink, 15)
    graph.add_edge(7, sink, 10)
    graph.add_edge(8, sink, 20)
    graph.add_edge(9, sink, 15)
    graph.add_edge(10, sink, 10)
    graph.add_edge(11, sink, 25)
    graph.add_edge(12, sink, 20)
    graph.add_edge(13, sink, 15)
    graph.add_edge(14, sink, 10)
    graph.add_edge(15, sink, 20)
    graph.add_edge(16, sink, 10)
    graph.add_edge(17, sink, 15)
    graph.add_edge(18, sink, 5)
    graph.add_edge(19, sink, 10)
    
    max_flow, flows = graph.max_flow(source, sink)
    print(f"Максимальний потік: {max_flow}\n")
    
    table = PrettyTable()
    table.field_names = ["Термінал", "Магазин", "Потік (одиниць)"]
    
    for u in range(vertices):
        for v in range(vertices):
            if flows[u][v] > 0:
                terminal = None
                if u in {1, 2, 3}:
                    terminal = "Термінал 1"
                elif u in {4, 5}:
                    terminal = "Термінал 2"
                
                if terminal and 6 <= v <= 19:
                    store = f"Магазин {v - 5}"
                    table.add_row([terminal, store, flows[u][v]])
    
    print("Таблиця потоків:")
    print(table)
