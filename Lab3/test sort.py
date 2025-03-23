import time
import random

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def generate_random_array(size):
    return [random.randint(0, 10000) for _ in range(size)]

def test_sorting(algorithm, array_size, num_tests=20):
    total_time = 0
    for _ in range(num_tests):
        arr = generate_random_array(array_size)
        start_time = time.time()
        algorithm(arr)
        end_time = time.time()
        total_time += (end_time - start_time)
    return total_time / num_tests

# Размеры массивов для тестирования
array_sizes = [1000, 2000, 4000, 8000, 16000]

# Проведение тестов для каждого размера массива
for size in array_sizes:
    avg_time = test_sorting(selection_sort, size)
    print(f"Среднее время сортировки массива размером {size}: {avg_time:.6f} секунд")