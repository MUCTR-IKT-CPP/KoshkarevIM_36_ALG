import time
import random
import matplotlib.pyplot as plt
from statistics import mean
import sys


class Node:
    """Узел дерева, используется как в Treap, так и в AVL"""
    def __init__(self, key, priority=None):
        self.key = key  # Ключ узла
        self.priority = priority if priority is not None else random.random()  # Приоритет для Treap
        self.left = None  # Левый потомок
        self.right = None  # Правый потомок
        self.height = 1  # Высота поддерева (для AVL)


class Treap:
    """Реализация структуры данных Treap (декартово дерево)"""
    def __init__(self):
        self.root = None  # Корень дерева

    def insert(self, key, priority=None):
        """Вставка ключа в Treap"""
        self.root = self._insert(self.root, key, priority)

    def _insert(self, node, key, priority=None):
        """Рекурсивная вставка ключа в поддерево"""
        if not node:
            return Node(key, priority)  # Создаем новый узел, если достигли пустого места

        if key < node.key:
            node.left = self._insert(node.left, key, priority)
            # Поддерживаем свойство кучи: если приоритет левого потомка больше
            if node.left.priority > node.priority:
                node = self._rotate_right(node)  # Правое вращение
        else:
            node.right = self._insert(node.right, key, priority)
            # Поддерживаем свойство кучи: если приоритет правого потомка больше
            if node.right.priority > node.priority:
                node = self._rotate_left(node)  # Левое вращение
        return node

    def _rotate_right(self, y):
        """Правое вращение вокруг узла y"""
        x = y.left
        y.left = x.right
        x.right = y
        return x

    def _rotate_left(self, x):
        """Левое вращение вокруг узла x"""
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def search(self, key):
        """Поиск ключа в дереве"""
        return self._search(self.root, key)

    def _search(self, node, key):
        """Рекурсивный поиск ключа в поддереве"""
        if not node:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def delete(self, key):
        """Удаление ключа из дерева"""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """Рекурсивное удаление ключа из поддерева"""
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Узел найден - выполняем удаление
            if not node.left:
                return node.right
            if not node.right:
                return node.left

            # Выбираем вращение в зависимости от приоритетов
            if node.left.priority > node.right.priority:
                node = self._rotate_right(node)
                node.right = self._delete(node.right, key)
            else:
                node = self._rotate_left(node)
                node.left = self._delete(node.left, key)
        return node

    def max_depth(self):
        """Вычисление максимальной глубины дерева"""
        return self._max_depth(self.root)

    def _max_depth(self, node):
        """Рекурсивное вычисление максимальной глубины поддерева"""
        if not node:
            return 0
        return 1 + max(self._max_depth(node.left), self._max_depth(node.right))

    def get_all_depths(self):
        """Получение глубин всех листьев дерева"""
        depths = []
        self._get_all_depths(self.root, 1, depths)
        return depths

    def _get_all_depths(self, node, current_depth, depths):
        """Рекурсивный сбор глубин листьев"""
        if not node:
            return
        if not node.left and not node.right:  # Если это лист
            depths.append(current_depth)
        self._get_all_depths(node.left, current_depth + 1, depths)
        self._get_all_depths(node.right, current_depth + 1, depths)


class AVL:
    """Реализация структуры данных AVL-дерево"""
    def __init__(self):
        self.root = None  # Корень дерева

    def insert(self, key):
        """Вставка ключа в AVL-дерево"""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        """Рекурсивная вставка ключа в поддерево"""
        if not node:
            return Node(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        # Обновляем высоту текущего узла
        node.height = 1 + max(self._get_height(node.left),
                             self._get_height(node.right))

        # Проверяем баланс и выполняем балансировку
        balance = self._get_balance(node)

        # Левое поддерево перевешивает (LL-случай)
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        # Правое поддерево перевешивает (RR-случай)
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)

        # Левое-правое поддерево (LR-случай)
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Правое-левое поддерево (RL-случай)
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def delete(self, key):
        """Удаление ключа из AVL-дерева"""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """Рекурсивное удаление ключа из поддерева"""
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Узел найден - выполняем удаление
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Находим минимальный узел в правом поддереве
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        if node is None:
            return node

        # Обновляем высоту текущего узла
        node.height = 1 + max(self._get_height(node.left),
                             self._get_height(node.right))

        # Проверяем баланс и выполняем балансировку
        balance = self._get_balance(node)

        # Балансировка после удаления
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)

        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)

        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _left_rotate(self, z):
        """Левое вращение вокруг узла z"""
        if z is None or z.right is None:
            return z

        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left),
                          self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                          self._get_height(y.right))

        return y

    def _right_rotate(self, z):
        """Правое вращение вокруг узла z"""
        if z is None or z.left is None:
            return z

        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left),
                          self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                          self._get_height(y.right))

        return y

    def _get_height(self, node):
        """Получение высоты поддерева"""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """Вычисление баланса узла (разница высот поддеревьев)"""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _min_value_node(self, node):
        """Поиск узла с минимальным ключом в поддереве"""
        current = node
        while current.left:
            current = current.left
        return current

    def search(self, key):
        """Поиск ключа в дереве"""
        return self._search(self.root, key)

    def _search(self, node, key):
        """Рекурсивный поиск ключа в поддереве"""
        if not node:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def max_depth(self):
        """Вычисление максимальной глубины дерева"""
        return self._max_depth(self.root)

    def _max_depth(self, node):
        """Рекурсивное вычисление максимальной глубины поддерева"""
        if not node:
            return 0
        return 1 + max(self._max_depth(node.left), self._max_depth(node.right))

    def get_all_depths(self):
        """Получение глубин всех листьев дерева"""
        depths = []
        self._get_all_depths(self.root, 1, depths)
        return depths

    def _get_all_depths(self, node, current_depth, depths):
        """Рекурсивный сбор глубин листьев"""
        if not node:
            return
        if not node.left and not node.right:  # Если это лист
            depths.append(current_depth)
        self._get_all_depths(node.left, current_depth + 1, depths)
        self._get_all_depths(node.right, current_depth + 1, depths)


def generate_random_array(size):
    """Генерация массива случайных чисел"""
    return [random.randint(0, 10 * size) for _ in range(size)]


def run_comparison_tests():
    """Запуск тестов для сравнения Treap и AVL деревьев"""
    sizes = [2 ** i for i in range(10, 16)]  # Размеры массивов от 2^10 до 2^15
    num_repeats = 50  # Количество повторений для каждого размера

    # Словарь для хранения результатов
    results = {
        'Treap': {
            'insert_time': [],
            'delete_time': [],
            'search_time': [],
            'max_height': [],
            'avg_depth': [],  # Добавляем среднюю глубину веток
            'all_depths': []
        },
        'AVL': {
            'insert_time': [],
            'delete_time': [],
            'search_time': [],
            'max_height': [],
            'avg_depth': [],  # Добавляем среднюю глубину веток
            'all_depths': []
        }
    }

    for n in sizes:
        print(f"\nТестирование размера: {n}")
        treap_insert_times = []
        treap_delete_times = []
        treap_search_times = []
        treap_max_heights = []
        treap_avg_depths = []  # Средние глубины для каждого теста Treap
        treap_all_depths = []

        avl_insert_times = []
        avl_delete_times = []
        avl_search_times = []
        avl_max_heights = []
        avl_avg_depths = []  # Средние глубины для каждого теста AVL
        avl_all_depths = []

        for repeat in range(num_repeats):
            print(f"  Повтор {repeat + 1}/{num_repeats}", end="\r")
            data = generate_random_array(n)

            # Тестирование Treap
            start = time.time()
            treap = Treap()
            for key in data:
                treap.insert(key)
            treap_insert_times.append(time.time() - start)

            max_h = treap.max_depth()
            treap_max_heights.append(max_h)

            depths = treap.get_all_depths()
            treap_all_depths.extend(depths)
            avg_depth = mean(depths) if depths else 0
            treap_avg_depths.append(avg_depth)

            search_data = random.choices(data, k=100)
            start = time.time()
            for key in search_data:
                treap.search(key)
            treap_search_times.append((time.time() - start) / 100)

            delete_data = random.choices(data, k=100)
            start = time.time()
            for key in delete_data:
                treap.delete(key)
            treap_delete_times.append((time.time() - start) / 100)

            # Тестирование AVL
            start = time.time()
            avl = AVL()
            for key in data:
                avl.insert(key)
            avl_insert_times.append(time.time() - start)

            max_h = avl.max_depth()
            avl_max_heights.append(max_h)

            depths = avl.get_all_depths()
            avl_all_depths.extend(depths)
            avg_depth = mean(depths) if depths else 0
            avl_avg_depths.append(avg_depth)

            start = time.time()
            for key in search_data:
                avl.search(key)
            avl_search_times.append((time.time() - start) / 100)

            start = time.time()
            for key in delete_data:
                avl.delete(key)
            avl_delete_times.append((time.time() - start) / 100)

        # Сохранение средних результатов
        results['Treap']['insert_time'].append(mean(treap_insert_times))
        results['Treap']['delete_time'].append(mean(treap_delete_times))
        results['Treap']['search_time'].append(mean(treap_search_times))
        results['Treap']['max_height'].append(mean(treap_max_heights))
        results['Treap']['avg_depth'].append(mean(treap_avg_depths))
        results['Treap']['all_depths'].append(treap_all_depths)

        results['AVL']['insert_time'].append(mean(avl_insert_times))
        results['AVL']['delete_time'].append(mean(avl_delete_times))
        results['AVL']['search_time'].append(mean(avl_search_times))
        results['AVL']['max_height'].append(mean(avl_max_heights))
        results['AVL']['avg_depth'].append(mean(avl_avg_depths))
        results['AVL']['all_depths'].append(avl_all_depths)

        # Вывод статистики для текущего размера
        print("\nРезультаты для размера", n)
        print("Treap:")
        print(f"  Средняя максимальная глубина: {mean(treap_max_heights):.2f}")
        print(f"  Среднее время вставки: {mean(treap_insert_times):.6f} сек")
        print(f"  Среднее время удаления: {mean(treap_delete_times):.6f} сек")
        print(f"  Среднее время поиска: {mean(treap_search_times):.6f} сек")
        print(f"  Средняя глубина веток: {mean(treap_avg_depths):.2f}")

        print("\nAVL:")
        print(f"  Средняя максимальная глубина: {mean(avl_max_heights):.2f}")
        print(f"  Среднее время вставки: {mean(avl_insert_times):.6f} сек")
        print(f"  Среднее время удаления: {mean(avl_delete_times):.6f} сек")
        print(f"  Среднее время поиска: {mean(avl_search_times):.6f} сек")
        print(f"  Средняя глубина веток: {mean(avl_avg_depths):.2f}")
        print("----------------------------------------")

    return sizes, results


def plot_results(sizes, results):
    """Построение графиков с результатами сравнения"""
    # 1. График времени вставки
    plt.figure(figsize=(12, 6))
    plt.plot(sizes, results['Treap']['insert_time'], 'o-', label='Treap')
    plt.plot(sizes, results['AVL']['insert_time'], 'o-', label='AVL')
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (секунды)')
    plt.title('Сравнение времени вставки')
    plt.legend()
    plt.grid(True)
    plt.show()

    # 2. График времени удаления
    plt.figure(figsize=(12, 6))
    plt.plot(sizes, results['Treap']['delete_time'], 'o-', label='Treap')
    plt.plot(sizes, results['AVL']['delete_time'], 'o-', label='AVL')
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (секунды)')
    plt.title('Сравнение времени удаления')
    plt.legend()
    plt.grid(True)
    plt.show()

    # 3. График времени поиска
    plt.figure(figsize=(12, 6))
    plt.plot(sizes, results['Treap']['search_time'], 'o-', label='Treap')
    plt.plot(sizes, results['AVL']['search_time'], 'o-', label='AVL')
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.xlabel('Количество элементов')
    plt.ylabel('Время (секунды)')
    plt.title('Сравнение времени поиска')
    plt.legend()
    plt.grid(True)
    plt.show()

    # 4. График максимальной высоты
    plt.figure(figsize=(12, 6))
    plt.plot(sizes, results['Treap']['max_height'], 'o-', label='Treap')
    plt.plot(sizes, results['AVL']['max_height'], 'o-', label='AVL')
    plt.xscale('log', base=2)
    plt.xlabel('Количество элементов')
    plt.ylabel('Максимальная высота')
    plt.title('Сравнение высоты деревьев')
    plt.legend()
    plt.grid(True)
    plt.show()

    # 5. Гистограмма распределения высот (N=2^15)
    plt.figure(figsize=(12, 6))
    plt.hist(results['Treap']['all_depths'][-1], bins=50, alpha=0.5, label='Treap')
    plt.hist(results['AVL']['all_depths'][-1], bins=50, alpha=0.5, label='AVL')
    plt.xlabel('Глубина')
    plt.ylabel('Частота')
    plt.title(f'Распределение глубин (N={sizes[-1]})')
    plt.legend()
    plt.grid(True)
    plt.show()

    # 6. Гистограмма средних максимальных высот
    plt.figure(figsize=(12, 6))
    plt.hist(results['Treap']['max_height'], bins=20, alpha=0.5, label='Treap')
    plt.hist(results['AVL']['max_height'], bins=20, alpha=0.5, label='AVL')
    plt.xlabel('Максимальная высота')
    plt.ylabel('Частота')
    plt.title('Распределение максимальных высот')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    sys.setrecursionlimit(1000000)  # Увеличиваем лимит рекурсии для больших деревьев
    print("Начало тестирования...")
    sizes, results = run_comparison_tests()
    print("\nТестирование завершено. Построение графиков...")
    plot_results(sizes, results)
    print("Готово!")