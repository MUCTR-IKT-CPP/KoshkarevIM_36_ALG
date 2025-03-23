import random
from collections import deque
import time
import matplotlib.pyplot as plt

# Класс графа
class Graph:
    def __init__(self, num_vert, edges, directed=False):
        self.num_vert = num_vert
        self.edges = edges
        self.directed = directed

    # Матрица смежности
    def adjacency_matrix(self):
        matrix = [[0] * self.num_vert for _ in range(self.num_vert)]
        for u, v in self.edges:
            matrix[u][v] = 1
            if not self.directed:
                matrix[v][u] = 1
        return matrix

    # Матрица инцидентности
    def incidence_matrix(self):
        matrix = [[0] * len(self.edges) for _ in range(self.num_vert)]
        for i, (u, v) in enumerate(self.edges):
            matrix[u][i] = 1
            if self.directed:
                matrix[v][i] = -1
            else:
                matrix[v][i] = 1
        return matrix

    # Список смежности
    def adjacency_list(self):
        adj_list = {v: [] for v in range(self.num_vert)}
        for u, v in self.edges:
            adj_list[u].append(v)
            if not self.directed:
                adj_list[v].append(u)
        return adj_list

    # Список ребер
    def edge_list(self):
        return self.edges


# Генератор случайных графов
def generate_random_graph(min_vert, max_vert, min_edges, max_edges, max_degree, directed=False,
                          max_in_degree=None, max_out_degree=None):
    num_vert = random.randint(min_vert, max_vert)
    num_edges = random.randint(min_edges, max_edges)

    edges = []
    degree = [0] * num_vert

    for i in range(num_edges):
        u = random.randint(0, num_vert - 1)
        v = random.randint(0, num_vert - 1)

        if u == v:
            i = i - 1
            continue

        if directed:
            if max_out_degree and degree[u] >= max_out_degree:
                i = i - 1
                continue
            if max_in_degree and degree[v] >= max_in_degree:
                i = i - 1
                continue
        else:
            if degree[u] >= max_degree or degree[v] >= max_degree:
                i = i - 1
                continue

        edges.append((u, v))
        degree[u] += 1
        degree[v] += 1

    return Graph(num_vert, edges, directed)


# Поиск в ширину (BFS)
def bfs(graph, start, end):
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.adjacency_list()[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None


# Поиск в глубину (DFS)
def dfs(graph, start, end, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path = path + [start]

    if start == end:
        return path

    for neighbor in graph.adjacency_list()[start]:
        if neighbor not in visited:
            new_path = dfs(graph, neighbor, end, visited, path)
            if new_path:
                return new_path
    return None


# Параметры для генерации графов
min_ver = 10
max_ver = 100
min_edge = 20
max_edge = 200
max_degree = 5
directed = True

# Демонстрация работы методов класса

# Генерация графа
graph = generate_random_graph(min_ver, max_ver, min_edge, max_edge, max_degree, directed)

# Вывод информации о графе
print("Матрица смежности:")
for row in graph.adjacency_matrix():
    print(row)

print("\nМатрица инцидентности:")
for row in graph.incidence_matrix():
    print(row)

print("\nСписок смежности:")
for key, value in graph.adjacency_list().items():
    print(f"{key}: {value}")

print("\nСписок ребер:")
print(graph.edge_list())

# Списки для хранения результатов
bfs_times = []
dfs_times = []
sizes = []

# Генерация 10 графов с возрастающим количеством вершин и ребер
for i in range(10):
    num_ver = 100 + i * 200
    num_edge = 100 + i * 400
    graph = generate_random_graph(num_ver, num_ver, num_edge, num_edge, max_degree, directed)
    sizes.append(num_ver)

    # Выбор случайных вершин для поиска пути
    start = random.randint(0, num_ver - 1)
    end = random.randint(0, num_ver - 1)

    # Замер времени выполнения BFS
    start_time = time.time()
    bfs_path = bfs(graph, start, end)
    bfs_time = time.time() - start_time
    bfs_times.append(bfs_time)

    # Замер времени выполнения DFS
    start_time = time.time()
    dfs_path = dfs(graph, start, end)
    dfs_time = time.time() - start_time
    dfs_times.append(dfs_time)

    # Вывод информации о графе и путях
    print(f"Граф {i + 1}:")
    print(f"Количество вершин: {num_ver}, Количество ребер: {num_edge}")
    print("-" * 50)

# Построение графика
plt.plot(sizes, bfs_times, label='BFS', marker='o')
plt.plot(sizes, dfs_times, label='DFS', marker='o')
plt.xlabel('Количество вершин')
plt.ylabel('Время (секунды)')
plt.title('Сравнение времени выполнения BFS и DFS')
plt.legend()
plt.grid(True)
plt.show()