import pandas as pd
import matplotlib.pyplot as plt


# Загрузка данных из файла
data = pd.read_csv("sorting_data.csv")

# Размеры массивов
array_sizes = data["ArraySize"]

# Времена выполнения
avg_times = data["AvgTime"]
best_times = data["BestTime"]
worst_times = data["WorstTime"]

# Среднее количество обменов и проходов
avg_swaps = data["AvgSwaps"]
avg_passes = data["AvgPasses"]

# Функция для вычисления O(N^2) с подобранной константой c
def O_N(n, c):
    return c * n**2

# Подбор константы c для O(N^2)
# Найдем такое c, чтобы график O(N^2) был выше графика наихудшего времени при N > 1000
c = max(worst_times / (array_sizes**2))

# Совмещённый график наихудшего времени и O(N^2)
plt.figure(figsize=(10, 6))
plt.plot(array_sizes, worst_times, label="Наихудшее время", marker="o")
plt.plot(array_sizes, O_N(array_sizes, c), label=f"O(N^2), c={c:.2e}", linestyle="--")
plt.xlabel("Размер массива")
plt.ylabel("Время (сек)")
plt.title("Совмещённый график наихудшего времени и O(N^2)")
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

# График среднего количества обменов
plt.figure(figsize=(10, 6))
plt.plot(array_sizes, avg_swaps, label="Среднее количество обменов", marker="o", color="green")
plt.xlabel("Размер массива")
plt.ylabel("Количество обменов")
plt.title("График среднего количества обменов")
plt.legend()
plt.grid()
plt.show()

# График среднего количества проходов
plt.figure(figsize=(10, 6))
plt.plot(array_sizes, avg_passes, label="Среднее количество проходов", marker="o", color="purple")
plt.xlabel("Размер массива")
plt.ylabel("Количество проходов")
plt.title("График среднего количества проходов")
plt.legend()
plt.grid()
plt.show()

