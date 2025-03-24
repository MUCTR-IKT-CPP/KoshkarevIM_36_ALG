import random
import time
import matplotlib.pyplot as plt

# Класс графа
class Graph:
    def __init__(self, num_vert, edges):
        self.num_vert = num_vert
        self.edges = edges

    # Матрица смежности
    def adjacency_matrix(self):
        matrix = [[0] * self.num_vert for _ in range(self.num_vert)]
        for u, v, weight in self.edges:
            matrix[u][v] = weight
            matrix[v][u] = weight
        return matrix

    # Список смежности
    def adjacency_list(self):
        adj_list = {v: [] for v in range(self.num_vert)}
        for u, v, weight in self.edges:
            adj_list[u].append((v, weight))
            adj_list[v].append((u, weight))
        return adj_list

    # Список ребер
    def edge_list(self):
        return self.edges

    # Функция для поиска минимального остовного дерева (алгоритм Краскала)
    def kruskal(self):
        # Вспомогательная функция для нахождения корня множества
        def find(parent, i):
            if parent[i] == i:
                return i
            return find(parent, parent[i])

        # Вспомогательная функция для объединения двух множеств
        def union(parent, rank, x, y):
            xroot = find(parent, x)
            yroot = find(parent, y)

            # Присоединяем меньшее дерево к большему
            if rank[xroot] < rank[yroot]:
                parent[xroot] = yroot
            elif rank[xroot] > rank[yroot]:
                parent[yroot] = xroot
            else:
                parent[yroot] = xroot
                rank[xroot] += 1

        # Результирующее минимальное остовное дерево
        result = []

        # Индекс для сортированных рёбер
        i = 0
        # Индекс для результата
        e = 0

        # Шаг 1: Сортируем все рёбра по весу
        self.edges = sorted(self.edges, key=lambda item: item[2])

        parent = []
        rank = []

        # Создаём подмножества для каждой вершины
        for node in range(self.num_vert):
            parent.append(node)
            rank.append(0)

        # Шаг 2: Проходим по всем рёбрам и добавляем их в дерево, если они не образуют цикл
        while e < self.num_vert - 1:
            u, v, w = self.edges[i]
            i += 1
            x = find(parent, u)
            y = find(parent, v)

            # Если ребро не образует цикл, добавляем его в результат
            if x != y:
                e += 1
                result.append((u, v, w))
                union(parent, rank, x, y)

        return result


# Функция для создания связного взвешенного ненаправленного графа
def create_graph(num_vertices, min_edges, max_weight=20):
    edges = []  # Список рёбер

    # Создаём граф - цепь
    for i in range(1, num_vertices):
        weight = random.randint(1, max_weight)
        edges.append((i - 1, i, weight))

    # Добавляем к каждой вершине оставшиеся случайные рёбра
    for i in range(num_vertices):
        # Уже есть одно ребро в цепочке (кроме первой и последней вершины)
        remaining_edges = min_edges - 2 if i not in (0, num_vertices - 1) else min_edges - 1

        # Добавляем случайные рёбра
        while remaining_edges > 0:
            j = random.randint(0, num_vertices - 1)
            if j != i and (i, j) not in edges and (j, i) not in edges:  # Исключаем петли и дубликаты
                weight = random.randint(1, max_weight)
                edges.append((i, j, weight))
                remaining_edges -= 1

    return Graph(num_vertices, edges)


# Параметры для создания графов
num_vertices_list = [10, 20, 50, 100]  # Количество вершин
min_edges_list = [3, 4, 10, 20]  # Минимальное количество рёбер на вершину
max_weight = 20
num_tests = 10  # Количество тестов для каждого графа

graph = create_graph(10, 5, max_weight)
matrix = graph.adjacency_matrix()
for mat in matrix:
    print(mat)

# Выполнение тестов
for min_edges in min_edges_list:
    # Списки для хранения результатов
    average_execution_times = []
    sizes = []
    print(f"\nТестирование графа с минимум {min_edges} рёбрами:")
    for num_vertices in num_vertices_list:
        print(f"\nТестирование графа с {num_vertices} вершинами:")
        execution_times = []

        for test in range(num_tests):
            # Создаём граф
            graph = create_graph(num_vertices, min_edges, max_weight)

            # Замер времени выполнения алгоритма Краскала
            start_time = time.time()
            mst = graph.kruskal()
            end_time = time.time()

            execution_time = end_time - start_time
            execution_times.append(execution_time)

            print(f"Тест {test + 1}: Время выполнения = {execution_time:.6f} секунд")

        # Усредняем результаты
        average_time = sum(execution_times) / num_tests
        average_execution_times.append(average_time)
        sizes.append(num_vertices)

        print(f"Среднее время выполнения для {num_vertices} вершин: {average_time:.6f} секунд")

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, average_execution_times, marker='o', linestyle='-', color='b')
    plt.title(f"Зависимость времени выполнения алгоритма Краскала \nот количества вершин c минимум {min_edges} рёбер у каждой вершины")
    plt.xlabel("Количество вершин (N)")
    plt.ylabel("Среднее время выполнения (секунды)")
    plt.grid(True)
    plt.show()