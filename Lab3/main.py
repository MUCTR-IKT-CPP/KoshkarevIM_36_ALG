import random
from datetime import datetime, timedelta
import time


# Узел двусвязного списка
class Node:
    def __init__(self, data):
        self.data = data  # Данные, которые хранятся в узле
        self.prev = None  # Ссылка на предыдущий узел
        self.next = None  # Ссылка на следующий узел


# Двусвязный список
class DoublyLinkedList:
    def __init__(self):
        self.head = None  # Ссылка на первый узел
        self.tail = None  # Ссылка на последний узел
        self._length = 0  # Количество элементов в списке

    def is_empty(self):
        #Проверяет, пуст ли список.
        return self._length == 0

    def __len__(self):
        #Возвращает количество элементов в списке.
        return self._length

    def append(self, data):
        #Добавляет элемент в конец списка.
        new_node = Node(data)
        if self.is_empty():  # Если список пуст
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._length += 1

    def prepend(self, data):
        #Добавляет элемент в начало списка.
        new_node = Node(data)
        if self.is_empty():  # Если список пуст
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._length += 1

    def insert_at(self, data, index):
        #Добавляет элемент в произвольное место по индексу.
        if index < 0:
            raise ValueError("Индекс не может быть отрицательным")

        if index == 0:  # Если вставляем в начало
            self.prepend(data)
            return
        elif index >= self._length:  # Если вставляем в конец
            self.append(data)
            return

        new_node = Node(data)
        current = self.head
        current_index = 0

        # Ищем узел, перед которым нужно вставить новый элемент
        while current and current_index < index:
            current = current.next
            current_index += 1

        # Вставляем новый узел между current.prev и current
        new_node.prev = current.prev
        new_node.next = current
        current.prev.next = new_node
        current.prev = new_node
        self._length += 1

    def delete_at(self, index):
        #Удаляет элемент по индексу.
        if self.is_empty():
            raise IndexError("Список пуст")

        if index < 0 or index >= self._length:
            raise IndexError("Индекс выходит за пределы списка")

        current = self.head
        current_index = 0

        # Ищем узел для удаления
        while current and current_index < index:
            current = current.next
            current_index += 1

        if current.prev:  # Если узел не является головой
            current.prev.next = current.next
        else:  # Если узел — это голова
            self.head = current.next

        if current.next:  # Если узел не является хвостом
            current.next.prev = current.prev
        else:  # Если узел — это хвост
            self.tail = current.prev

        self._length -= 1

    def __iter__(self):
        #Возвращает итератор для списка.
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __str__(self):
        #Возвращает строковое представление списка.
        return " <-> ".join(map(str, self)) + " <-> None"


# Структура для хранения данных о человеке
class Person:
    def __init__(self, last_name, first_name, patronymic, birth_date):
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.birth_date = birth_date

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic} ({self.birth_date.strftime('%d.%m.%Y')})"


# Генерация случайной даты
def generate_random_date(start, end):
    #Генерирует случайную дату между start и end.
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


# Тест 1: Заполнение контейнера 1000 целыми числами и подсчет суммы, среднего, минимального и максимального
def test_integer_operations():
    dll = DoublyLinkedList()  # Создаем двусвязный список
    numbers = [random.randint(-1000, 1000) for _ in range(1000)]  # Генерируем 1000 чисел

    # Заполняем список
    for number in numbers:
        dll.append(number)

    # Подсчет суммы, среднего, минимального и максимального
    total_sum = sum(dll)
    average = total_sum / len(dll)
    min_value = min(dll)
    max_value = max(dll)

    print(f"Сумма: {total_sum}")
    print(f"Среднее: {average}")
    print(f"Минимальное: {min_value}")
    print(f"Максимальное: {max_value}")


# Тест 2: Проверка операций вставки и удаления на коллекции из 10 строковых элементов
def test_string_operations():
    dll = DoublyLinkedList()  # Создаем двусвязный список
    strings = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon"]

    # Заполняем список
    for s in strings:
        dll.append(s)

    # Вставляем элемент в середину
    dll.insert_at("mango", 5)  # Вставляем "mango" на позицию 5

    # Удаляем элемент по индексу
    dll.delete_at(2)  # Удаляем "cherry"

    # Выводим результат
    print("Список после операций:")
    print(dll)


# Тест 3: Заполнение контейнера 100 структур (ФИО и дата рождения) и фильтрация
def test_person_filter():
    dll = DoublyLinkedList()  # Создаем двусвязный список
    last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов"]
    first_names = ["Алексей", "Дмитрий", "Ольга", "Екатерина", "Иван"]
    patronymics = ["Иванович", "Дмитриевич", "Олеговна", "Егоровна", "Алексеевич"]

    # Генерируем 100 случайных людей
    start_date = datetime(1980, 1, 1)
    end_date = datetime(2020, 1, 1)
    for _ in range(100):
        last_name = random.choice(last_names)
        first_name = random.choice(first_names)
        patronymic = random.choice(patronymics)
        birth_date = generate_random_date(start_date, end_date)
        person = Person(last_name, first_name, patronymic, birth_date)
        dll.append(person)

    # Фильтрация: люди младше 20 и старше 30 лет
    young_people = DoublyLinkedList()
    old_people = DoublyLinkedList()
    current_date = datetime.now()

    for person in dll:
        age = (current_date - person.birth_date).days // 365
        if age < 20:
            young_people.append(person)
        elif age > 30:
            old_people.append(person)

    # Проверка правильности фильтрации
    print(f"Людей младше 20 лет: {len(young_people)}")
    print(f"Людей старше 30 лет: {len(old_people)}")


# Тест 4: Сортировка выбором на двусвязном списке
def selection_sort(dll):
    current = dll.head
    while current:
        min_node = current
        next_node = current.next
        while next_node:
            if next_node.data < min_node.data:
                min_node = next_node
            next_node = next_node.next
        if current != min_node:
            current.data, min_node.data = min_node.data, current.data
        current = current.next


def test_selection_sort():
    #Создает и сортирует 20 списков разного размера, измеряя время выполнения.
    sizes = [1000, 2000, 4000, 8000, 16000]
    num_tests = 20
    for size in sizes:
        total_time = 0
        for _ in range(num_tests):
            dll = DoublyLinkedList()
            for _ in range(size):
                dll.append(random.randint(-10000, 10000))
            start_time = time.time()
            selection_sort(dll)
            end_time = time.time()
            total_time += (end_time - start_time)
        avg_time = total_time / num_tests
        print(f"Среднее время сортировки списка размером {size}: {avg_time:.5f} секунд")


# Тест 5: Перемешивание элементов списка
def shuffle_list(dll):
    nodes = []
    current = dll.head
    while current:
        nodes.append(current)
        current = current.next

    random.shuffle(nodes)

    # Восстанавливаем связи
    dll.head = nodes[0]
    dll.tail = nodes[-1]
    dll.head.prev = None
    dll.tail.next = None

    for i in range(len(nodes)):
        if i > 0:
            nodes[i].prev = nodes[i - 1]
        if i < len(nodes) - 1:
            nodes[i].next = nodes[i + 1]


def test_shuffle():
    dll = DoublyLinkedList()  # Создаем двусвязный список
    numbers = [random.randint(-1000, 1000) for _ in range(10)]  # Генерируем 10 чисел

    # Заполняем список
    for number in numbers:
        dll.append(number)

    print("До перемешивания:")
    print(dll)

    # Перемешиваем список
    shuffle_list(dll)

    print("После перемешивания:")
    print(dll)


# Запуск всех тестов
if __name__ == "__main__":
    print("Тест 1: Список с числами")
    test_integer_operations()

    print("\nТест 2: Список со строками")
    test_string_operations()

    print("\nТест 3: Фильтрация людей")
    test_person_filter()

    print("\nТест 4: Сортировка выбором")
    test_selection_sort()

    print("\nТест 5: Перемешивание элементов")
    test_shuffle()