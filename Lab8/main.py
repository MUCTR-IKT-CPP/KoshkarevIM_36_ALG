import time
import math
import matplotlib.pyplot as plt
import random
from collections import deque


class BinaryHeap:
    def __init__(self):
        self.heap = []

    def insert(self, key):
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[parent] <= self.heap[index]:
                break
            self.heap[parent], self.heap[index] = self.heap[index], self.heap[parent]
            index = parent

    def get_min(self):
        return self.heap[0] if self.heap else None

    def delete_min(self):
        if not self.heap:
            return None

        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        min_val = self.heap.pop()
        if self.heap:
            self._heapify_down(0)
        return min_val

    def _heapify_down(self, index):
        n = len(self.heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest == index:
                break

            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            index = smallest


class OptimizedFibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.num_nodes = 0
        self._iter_cache = []

    def insert(self, key):
        node = FibonacciHeapNode(key)
        self._add_to_root_list(node)
        if self.min_node is None or node.key < self.min_node.key:
            self.min_node = node
        self.num_nodes += 1
        return node

    def _add_to_root_list(self, node):
        if self.min_node is None:
            self.min_node = node
            node.left = node.right = node
        else:
            node.right = self.min_node.right
            node.left = self.min_node
            self.min_node.right.left = node
            self.min_node.right = node

    def minimum(self):
        return self.min_node.key if self.min_node else None

    def extract_min(self):
        if not self.min_node:
            return None

        min_node = self.min_node

        if min_node.child:
            self._iter_cache.clear()
            current = min_node.child
            while True:
                self._iter_cache.append(current)
                current = current.right
                if current == min_node.child:
                    break

            for child in self._iter_cache:
                self._add_to_root_list(child)
                child.parent = None

        self._remove_from_root_list(min_node)

        if min_node == min_node.right:
            self.min_node = None
        else:
            self.min_node = min_node.right
            self._consolidate()

        self.num_nodes -= 1
        return min_node

    def _remove_from_root_list(self, node):
        if node.right == node:
            self.min_node = None
        else:
            node.left.right = node.right
            node.right.left = node.left
            if node == self.min_node:
                self.min_node = node.right

    def _consolidate(self):
        if not self.min_node:
            return

        max_degree = math.floor(math.log2(self.num_nodes)) + 2
        degree_table = [None] * max_degree

        nodes = []
        current = self.min_node
        while True:
            nodes.append(current)
            current = current.right
            if current == self.min_node:
                break

        for node in nodes:
            degree = node.degree
            while degree_table[degree] is not None:
                other = degree_table[degree]
                if node.key > other.key:
                    node, other = other, node
                self._link(node, other)
                degree_table[degree] = None
                degree += 1
            degree_table[degree] = node

        self.min_node = None
        for node in degree_table:
            if node is not None:
                if self.min_node is None:
                    self.min_node = node
                    node.left = node.right = node
                else:
                    self._add_to_root_list(node)
                    if node.key < self.min_node.key:
                        self.min_node = node

    def _link(self, parent, child):
        self._remove_from_root_list(child)
        child.parent = parent
        child.mark = False

        if parent.child is None:
            parent.child = child
            child.left = child.right = child
        else:
            child.right = parent.child.right
            child.left = parent.child
            parent.child.right.left = child
            parent.child.right = child

        parent.degree += 1


class FibonacciHeapNode:
    __slots__ = ('key', 'degree', 'parent', 'child', 'mark', 'left', 'right')

    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.mark = False
        self.left = self
        self.right = self


def run_operations(heap, op_type, num_ops=1000):
    times = []

    if op_type == 'find_min':
        op = heap.minimum if isinstance(heap, OptimizedFibonacciHeap) else heap.get_min
    elif op_type == 'delete_min':
        op = heap.extract_min if isinstance(heap, OptimizedFibonacciHeap) else heap.delete_min
    elif op_type == 'insert':
        op = lambda: heap.insert(random.randint(1, 10 ** 6))

    for _ in range(num_ops):
        start = time.perf_counter()
        result = op()
        times.append(time.perf_counter() - start)
        if op_type == 'delete_min' and result is None:
            break

    avg_time = sum(times) / len(times) if times else 0
    max_time = max(times) if times else 0

    return avg_time, max_time


def benchmark():
    sizes = [10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6, 10 ** 7]
    heaps = {
        'BinaryHeap': BinaryHeap,
        'OptimizedFibonacciHeap': OptimizedFibonacciHeap
    }
    results = {name: {} for name in heaps}

    print("Начало тестирования производительности...")

    for size in sizes:
        print(f"\nРазмер кучи: {size}")
        data = [random.randint(1, 10 ** 6) for _ in range(size)]

        for name, heap_class in heaps.items():
            print(f"  Тестируем {name}...", end=' ', flush=True)

            # Создание и заполнение кучи
            start = time.perf_counter()
            heap = heap_class()
            for x in data:
                heap.insert(x)
            creation_time = time.perf_counter() - start

            # Тестирование операций
            avg_find, max_find = run_operations(heap, 'find_min')
            avg_del, max_del = run_operations(heap, 'delete_min')
            avg_insert, max_insert = run_operations(heap, 'insert')

            results[name][size] = {
                'find_min': {'avg': avg_find, 'max': max_find},
                'delete_min': {'avg': avg_del, 'max': max_del},
                'insert': {'avg': avg_insert, 'max': max_insert}
            }
            print("готово")

    # Построение графиков
    print("\nСоздание графиков...")
    operations = ['find_min', 'delete_min', 'insert']
    op_names = ['Поиск минимума', 'Удаление минимума', 'Вставка']

    fig, axes = plt.subplots(3, 2, figsize=(15, 15))

    for i, (op, op_name) in enumerate(zip(operations, op_names)):
        # Графики среднего времени
        ax_avg = axes[i, 0]
        for name in heaps:
            x = sizes
            y = [results[name][s][op]['avg'] for s in sizes]
            ax_avg.plot(x, y, marker='o', label=name)

        ax_avg.set_xscale('log')

        ax_avg.set_xlabel('Размер кучи')
        ax_avg.set_ylabel('Время (с)')
        ax_avg.set_title(f'Среднее время: {op_name}')
        ax_avg.legend()
        ax_avg.grid(True)

        # Графики максимального времени
        ax_max = axes[i, 1]
        for name in heaps:
            x = sizes
            y = [results[name][s][op]['max'] for s in sizes]
            ax_max.plot(x, y, marker='o', label=name)

        ax_max.set_xscale('log')

        ax_max.set_xlabel('Размер кучи')
        ax_max.set_ylabel('Время (с)')
        ax_max.set_title(f'Максимальное время: {op_name}')
        ax_max.legend()
        ax_max.grid(True)

    plt.tight_layout()
    plt.savefig('сравнение_производительности_операций.png')
    print("Графики сохранены в файл 'сравнение_производительности_операций.png'")


if __name__ == "__main__":
    benchmark()