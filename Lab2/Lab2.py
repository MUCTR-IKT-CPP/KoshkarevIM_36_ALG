import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Загрузка данных из файла
data = pd.read_csv("data.csv")

# Размеры массивов
array_sizes = data["ArraySize"]

# Время выполнения
avg_times = data["AvgTime"]
best_times = data["BestTime"]
worst_times = data["WorstTime"]

# Среднее количество памяти, вызовов и глубины
avg_mem = data["AvgMaxMemory"]
avg_cal = data["AvgTotalCalls"]
avg_deep = data["AvgMaxDepth"]


def O_N(n, c):
    return c * n * np.log(n)


# Подбор константы c для O(n log n)
def find_constant_c(array_sizes, worst_times):

    # Вычисляем c как максимальное значение (worst_time / (n * log2(n))) для n > 1000
    c_values = []
    for n, worst_time in zip(array_sizes, worst_times):
        if n > 1000:
            c_values.append(worst_time / (n * np.log2(n)))

    return max(c_values) * 1.1

c = find_constant_c(array_sizes,worst_times)
# Совмещённый график наихудшего времени и O(NlogN)
plt.figure(figsize=(10, 6))
plt.plot(array_sizes, worst_times, label="Наихудшее время", marker="o")
plt.plot(array_sizes, O_N(array_sizes, c), label=f"O(NlogN), c={c:.2e}", linestyle="--")
plt.xlabel("Размер массива")
plt.ylabel("Время (сек)")
plt.title("Совмещённый график наихудшего времени и O(NlogN)")
plt.legend()
plt.grid()
plt.show()

# Совмещённый график среднего, наилучшего и наихудшего времени
plt.figure(figsize=(10, 6))
plt.plot(array_sizes, avg_times, label="Среднее время", marker="o")
plt.plot(array_sizes, best_times, label="Наилучшее время", marker="o")
plt.plot(array_sizes, worst_times, label="Наихудшее время", marker="o")
plt.xlabel("Размер массива")
plt.ylabel("Время (сек)")
plt.title("Совмещённый график времени выполнения")
plt.legend()
plt.grid()
plt.show()

# График среднего количества вызовов
plt.figure(figsize=(10, 6))
plt.plot(array_sizes, avg_cal, label="Среднее количество вызовов рекурсии", marker="o", color="green")
plt.xlabel("Размер массива")
plt.ylabel("Количество вызовов")
plt.title("График среднего количества вызовов рекурсии")
plt.legend()
plt.grid()
plt.show()

# График среднего количества глубины
plt.figure(figsize=(10, 6))
plt.plot(array_sizes, avg_deep, label="Средняя глубина рекурсии", marker="o", color="purple")
plt.xlabel("Размер массива")
plt.ylabel("глубина рекурсии")
plt.title("График средней глубины рекурсии")
plt.legend()
plt.grid()
plt.show()

# График среднего количества памяти
plt.figure(figsize=(10, 6))
plt.plot(array_sizes, avg_mem, label="используется памяти", marker="o", color="purple")
plt.xlabel("Размер массива")
plt.ylabel("используемая память")
plt.title("График используемой памяти")
plt.legend()
plt.grid()
plt.show()

