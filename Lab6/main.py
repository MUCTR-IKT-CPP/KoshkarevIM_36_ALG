import time
import random
import matplotlib.pyplot as plt
import sys
from statistics import mean

"""
Класс Node представляет узел дерева с ключом и указателями на левого/правого потомка.
Для AVL-дерева также хранится высота поддерева.
"""


class Node:
    def __init__(self, key):
        self.key = key  # Значение узла
        self.left = None  # Левый потомок
        self.right = None  # Правый потомок
        self.height = 1  # Высота поддерева (для AVL)


"""
Класс BST реализует бинарное дерево поиска с основными операциями:
- вставка (insert)
- поиск (search) 
- удаление (delete)
- обход (in_order)
"""


class BST:
    def __init__(self):
        self.root = None  # Корень дерева

    # Вставка нового ключа в дерево (итеративная реализация)
        # Вставка нового ключа в дерево (итеративная реализация)
    def insert(self, key):
        if not self.root:
            self.root = Node(key)
            return

        current = self.root
        while True:
            if key < current.key:  # Идем в левое поддерево
                if not current.left:
                    current.left = Node(key)
                    break
                else:
                    current = current.left
            else:  # Идем в правое поддерево
                if not current.right:
                    current.right = Node(key)
                    break
                else:
                    current = current.right

    # Рекурсивный поиск
    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None:
            return False

        if key == node.key:
            return True
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    # Рекурсивный обход (in-order)
    def in_order(self):
        elements = []
        self._in_order_recursive(self.root, elements)
        return elements

    def _in_order_recursive(self, node, elements):
        if node:
            self._in_order_recursive(node.left, elements)
            elements.append(node.key)
            self._in_order_recursive(node.right, elements)

    # Удаление ключа из дерева
    def delete(self, key):
        self.root = self._delete(self.root, key)

    # Вспомогательная рекурсивная функция для удаления
    def _delete(self, node, key):
        if node is None:
            return node

        if key < node.key:  # Ищем в левом поддереве
            node.left = self._delete(node.left, key)
        elif key > node.key:  # Ищем в правом поддереве
            node.right = self._delete(node.right, key)
        else:  # Нашли узел для удаления
            # Узел с одним потомком или без потомков
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Узел с двумя потомками - находим минимальный в правом поддереве
            temp = self._min_value_node(node.right)
            node.key = temp.key  # Копируем значение
            node.right = self._delete(node.right, temp.key)  # Удаляем дубликат

        return node

    # Поиск узла с минимальным значением в поддереве
    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current



"""
Класс AVL расширяет BST, добавляя балансировку для поддержания 
оптимальной высоты дерева после операций вставки и удаления.
"""


class AVL(BST):
    # Переопределяем вставку с балансировкой
    def insert(self, key):
        self.root = self._insert(self.root, key)

    # Рекурсивная вставка с обновлением высот и балансировкой
    def _insert(self, node, key):
        if not node:
            return Node(key)  # Базовый случай рекурсии

        # Обычная вставка как в BST
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        # Обновляем высоту текущего узла
        node.height = 1 + max(self._get_height(node.left),
                              self._get_height(node.right))

        # Проверяем баланс и выполняем повороты при необходимости
        balance = self._get_balance(node)

        # Левое-левое нарушение
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        # Правое-правое нарушение
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)

        # Левое-правое нарушение
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Правое-левое нарушение
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # Переопределяем удаление с балансировкой
    def delete(self, key):
        self.root = self._delete(self.root, key)

    # Расширенное удаление с балансировкой
    def _delete(self, node, key):
        # Сначала выполняем стандартное удаление BST
        node = super()._delete(node, key)

        if node is None:
            return node

        # Обновляем высоту текущего узла
        node.height = 1 + max(self._get_height(node.left),
                              self._get_height(node.right))

        # Проверяем баланс и выполняем повороты
        balance = self._get_balance(node)

        # Левое-левое
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)

        # Правое-правое
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)

        # Левое-правое
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Правое-левое
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # Левый поворот для балансировки
    def _left_rotate(self, z):
        if z is None or z.right is None:
            return z

        y = z.right
        T2 = y.left

        # Выполняем поворот
        y.left = z
        z.right = T2

        # Обновляем высоты
        z.height = 1 + max(self._get_height(z.left),
                           self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                           self._get_height(y.right))

        return y  # Новый корень поддерева

    # Правый поворот для балансировки
    def _right_rotate(self, z):
        if z is None or z.left is None:
            return z

        y = z.left
        T3 = y.right

        # Выполняем поворот
        y.right = z
        z.left = T3

        # Обновляем высоты
        z.height = 1 + max(self._get_height(z.left),
                           self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                           self._get_height(y.right))

        return y  # Новый корень поддерева

    # Получение высоты узла
    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    # Расчет баланс-фактора (разница высот поддеревьев)
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)


"""
Функции для генерации тестовых данных:
- generate_random_array - создает массив случайных чисел
- generate_sorted_array - создает отсортированный массив
"""


def generate_random_array(size):
    return [random.randint(0, 100000) for _ in range(size)]


def generate_sorted_array(size):
    return [i for i in range(size)]


"""
Функция тестирования производительности дерева:
1. Вставка всех элементов массива
2. 1000 операций поиска случайных элементов
3. 1000 операций удаления/вставки (чтобы размер дерева не менялся)
Возвращает среднее время для каждой операции.
"""


def test_tree_performance(tree_class, array):
    # Тест вставки
    insert_time = time.time()
    tree = tree_class()
    for key in array:
        tree.insert(key)
    insert_time = time.time() - insert_time

    # Тест поиска (1000 операций)
    search_time = time.time()
    for _ in range(1000):
        key = random.choice(array)  # Выбираем случайный ключ из массива
        tree.search(key)
    search_time = (time.time() - search_time) / 1000  # Среднее время поиска

    # Тест удаления (1000 операций)
    delete_time = time.time()
    for _ in range(1000):
        key = random.choice(array)
        tree.delete(key)
        tree.insert(key)  # Восстанавливаем размер дерева
    delete_time = (time.time() - delete_time) / 1000  # Среднее время удаления

    return insert_time, search_time, delete_time


"""
Функция тестирования поиска в массиве:
Выполняет 1000 операций поиска и возвращает среднее время.
"""


def test_array_performance(array):
    search_time = time.time()
    for _ in range(1000):
        key = random.choice(array)
        key in array  # Оператор in для поиска в списке
    search_time = (time.time() - search_time) / 1000
    return search_time


"""
Основная функция тестирования:
1. Выполняет серии тестов для разных размеров массивов
2. Для каждого размера проводит 10 тестов со случайными данными 
   и 10 тестов с отсортированными данными
3. Сохраняет средние значения времени для каждой операции
"""


def run_test_series():
    # Структура для хранения результатов
    results = {
        'bst_random': {'insert': [], 'search': [], 'delete': []},
        'avl_random': {'insert': [], 'search': [], 'delete': []},
        'bst_sorted': {'insert': [], 'search': [], 'delete': []},
        'avl_sorted': {'insert': [], 'search': [], 'delete': []},
        'array_random': {'search': []},
        'array_sorted': {'search': []}
    }

    # 5 серий тестов для размеров 2^11 до 2^15
    for i in range(1, 6):
        size = 2 ** (10 + i)
        print(f"\nСерия {i}: Размер массива = {size}")

        # Списки для хранения временных результатов
        bst_random_insert, bst_random_search, bst_random_delete = [], [], []
        avl_random_insert, avl_random_search, avl_random_delete = [], [], []
        array_random_search = []

        bst_sorted_insert, bst_sorted_search, bst_sorted_delete = [], [], []
        avl_sorted_insert, avl_sorted_search, avl_sorted_delete = [], [], []
        array_sorted_search = []

        # 10 тестов со случайными данными
        print("  Тестируем случайные данные...")
        for _ in range(10):
            random_array = generate_random_array(size)

            # Тестируем BST
            ins, srch, dlt = test_tree_performance(BST, random_array)
            bst_random_insert.append(ins)
            bst_random_search.append(srch)
            bst_random_delete.append(dlt)

            # Тестируем AVL
            ins, srch, dlt = test_tree_performance(AVL, random_array)
            avl_random_insert.append(ins)
            avl_random_search.append(srch)
            avl_random_delete.append(dlt)

            # Тестируем массив
            array_random_search.append(test_array_performance(random_array))

        # 10 тестов с отсортированными данными
        print("  Тестируем отсортированные данные...")
        for _ in range(10):
            sorted_array = generate_sorted_array(size)

            # Тестируем BST
            ins, srch, dlt = test_tree_performance(BST, sorted_array)
            bst_sorted_insert.append(ins)
            bst_sorted_search.append(srch)
            bst_sorted_delete.append(dlt)

            # Тестируем AVL
            ins, srch, dlt = test_tree_performance(AVL, sorted_array)
            avl_sorted_insert.append(ins)
            avl_sorted_search.append(srch)
            avl_sorted_delete.append(dlt)

            # Тестируем массив
            array_sorted_search.append(test_array_performance(sorted_array))

        # Вычисляем средние значения и сохраняем результаты
        def avg(lst):
            return sum(lst) / len(lst)

        # Сохраняем результаты для случайных данных
        results['bst_random']['insert'].append(avg(bst_random_insert))
        results['bst_random']['search'].append(avg(bst_random_search))
        results['bst_random']['delete'].append(avg(bst_random_delete))

        results['avl_random']['insert'].append(avg(avl_random_insert))
        results['avl_random']['search'].append(avg(avl_random_search))
        results['avl_random']['delete'].append(avg(avl_random_delete))

        results['array_random']['search'].append(avg(array_random_search))

        # Сохраняем результаты для отсортированных данных
        results['bst_sorted']['insert'].append(avg(bst_sorted_insert))
        results['bst_sorted']['search'].append(avg(bst_sorted_search))
        results['bst_sorted']['delete'].append(avg(bst_sorted_delete))

        results['avl_sorted']['insert'].append(avg(avl_sorted_insert))
        results['avl_sorted']['search'].append(avg(avl_sorted_search))
        results['avl_sorted']['delete'].append(avg(avl_sorted_delete))

        results['array_sorted']['search'].append(avg(array_sorted_search))

        # Выводим результаты текущей серии
        print(
            f"  BST случайные: вставка={avg(bst_random_insert):.6f}, поиск={avg(bst_random_search):.6f}, удаление={avg(bst_random_delete):.6f}")
        print(
            f"  AVL случайные: вставка={avg(avl_random_insert):.6f}, поиск={avg(avl_random_search):.6f}, удаление={avg(avl_random_delete):.6f}")
        print(f"  Массив случайные: поиск={avg(array_random_search):.6f}")

        print(
            f"  BST отсорт.: вставка={avg(bst_sorted_insert):.6f}, поиск={avg(bst_sorted_search):.6f}, удаление={avg(bst_sorted_delete):.6f}")
        print(
            f"  AVL отсорт.: вставка={avg(avl_sorted_insert):.6f}, поиск={avg(avl_sorted_search):.6f}, удаление={avg(avl_sorted_delete):.6f}")
        print(f"  Массив отсорт.: поиск={avg(array_sorted_search):.6f}")

    return results


"""
Функция построения графиков:
Создает 6 графиков для визуализации результатов тестирования:
1. Вставка (случайные данные)
2. Поиск (случайные данные) с сравнением с массивом
3. Удаление (случайные данные)
4. Вставка (отсортированные данные)
5. Поиск (отсортированные данные) с сравнением с массивом
6. Удаление (отсортированные данные)
"""


def plot_results(results):
    x = [2 ** (10 + i) for i in range(1, 6)]  # Размеры массивов

    plt.figure(figsize=(18, 12))  # Создаем большое окно для графиков

    # График 1: Вставка (случайные данные)
    plt.subplot(2, 3, 1)
    plt.plot(x, results['bst_random']['insert'], 'o-', label='BST')
    plt.plot(x, results['avl_random']['insert'], 'o-', label='AVL')
    plt.xlabel('Размер массива')
    plt.ylabel('Время (сек)')
    plt.title('Вставка (случайные данные)')
    plt.legend()
    plt.grid(True)

    # График 2: Поиск (случайные данные)
    plt.subplot(2, 3, 2)
    plt.plot(x, results['bst_random']['search'], 'o-', label='BST')
    plt.plot(x, results['avl_random']['search'], 'o-', label='AVL')
    plt.plot(x, results['array_random']['search'], 'o-', label='Массив')
    plt.xlabel('Размер массива')
    plt.ylabel('Время (сек)')
    plt.title('Поиск (случайные данные)')
    plt.legend()
    plt.grid(True)

    # График 3: Удаление (случайные данные)
    plt.subplot(2, 3, 3)
    plt.plot(x, results['bst_random']['delete'], 'o-', label='BST')
    plt.plot(x, results['avl_random']['delete'], 'o-', label='AVL')
    plt.xlabel('Размер массива')
    plt.ylabel('Время (сек)')
    plt.title('Удаление (случайные данные)')
    plt.legend()
    plt.grid(True)

    # График 4: Вставка (отсортированные данные)
    plt.subplot(2, 3, 4)
    plt.plot(x, results['bst_sorted']['insert'], 'o-', label='BST')
    plt.plot(x, results['avl_sorted']['insert'], 'o-', label='AVL')
    plt.xlabel('Размер массива')
    plt.ylabel('Время (сек)')
    plt.title('Вставка (отсортированные данные)')
    plt.legend()
    plt.grid(True)

    # График 5: Поиск (отсортированные данные)
    plt.subplot(2, 3, 5)
    plt.plot(x, results['bst_sorted']['search'], 'o-', label='BST')
    plt.plot(x, results['avl_sorted']['search'], 'o-', label='AVL')
    plt.plot(x, results['array_sorted']['search'], 'o-', label='Массив')
    plt.xlabel('Размер массива')
    plt.ylabel('Время (сек)')
    plt.title('Поиск (отсортированные данные)')
    plt.legend()
    plt.grid(True)

    # График 6: Удаление (отсортированные данные)
    plt.subplot(2, 3, 6)
    plt.plot(x, results['bst_sorted']['delete'], 'o-', label='BST')
    plt.plot(x, results['avl_sorted']['delete'], 'o-', label='AVL')
    plt.xlabel('Размер массива')
    plt.ylabel('Время (сек)')
    plt.title('Удаление (отсортированные данные)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()  # Автоматическая настройка отступов
    plt.show()  # Показываем графики


"""
1. Устанавливаем увеличенный лимит рекурсии для работы с большими деревьями
2. Запускаем тестирование
3. Строим графики результатов
"""

sys.setrecursionlimit(1000000)  # Увеличиваем лимит рекурсии для больших деревьев
print("Начало тестирования...")
results = run_test_series()  # Запускаем тесты
plot_results(results)  # Строим графики
print("Тестирование завершено успешно!")
