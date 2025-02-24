#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <fstream>
#include <algorithm>

using namespace std;

// Функция для слияния двух отсортированных половин
void merge(vector<double>& arr, int left, int mid, int right, size_t& current_memory_usage, size_t& max_memory_usage) {
    int n1 = mid - left;  // Размер левой половины
    int n2 = right - mid; // Размер правой половины

    // Временные массивы для левой и правой половин
    vector<double> L(n1), R(n2);

    // Копируем данные во временные массивы
    for (int i = 0; i < n1; i++)
        L[i] = arr[left + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[mid + j];

    // Обновляем текущее использование памяти
    current_memory_usage += n1 + n2;
    if (current_memory_usage > max_memory_usage)
        max_memory_usage = current_memory_usage;

    // Слияние временных массивов обратно
    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Копируем оставшиеся элементы L[], если они есть
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Копируем оставшиеся элементы R[], если они есть
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }

    // Освобождаем память, уменьшаем текущее использование памяти
    current_memory_usage -= n1 + n2;
}

// Рекурсивная функция для сортировки слиянием
void mergeSort(vector<double>& arr, int left, int right, int current_depth, size_t& current_memory_usage, size_t& max_memory_usage, size_t& max_recursion_depth, size_t& total_recursive_calls) {
    total_recursive_calls++;  // Увеличиваем счетчик рекурсивных вызовов

    // Обновляем максимальную глубину рекурсии
    if (current_depth > max_recursion_depth)
        max_recursion_depth = current_depth;

    // Базовый случай: если в подмассиве 1 элемент или меньше
    if (left + 1 >= right) {
        return;
    }

    int mid = left + (right - left) / 2; // Находим середину

    // Рекурсивно сортируем две половинки
    mergeSort(arr, left, mid, current_depth + 1, current_memory_usage, max_memory_usage, max_recursion_depth, total_recursive_calls);
    mergeSort(arr, mid, right, current_depth + 1, current_memory_usage, max_memory_usage, max_recursion_depth, total_recursive_calls);

    // Сливаем отсортированные половинки
    merge(arr, left, mid, right, current_memory_usage, max_memory_usage);
}

// Функция для запуска сортировки и сбора данных
void runMergeSort(vector<double>& arr, size_t& max_memory_usage, size_t& max_recursion_depth, size_t& total_recursive_calls) {
    size_t current_memory_usage = 0; 
    max_memory_usage = 0;            
    max_recursion_depth = 0;         
    total_recursive_calls = 0;       

    // Запускаем сортировку
    mergeSort(arr, 0, arr.size(), 0, current_memory_usage, max_memory_usage, max_recursion_depth, total_recursive_calls);
}

// Генерация массива случайных чисел
vector<double> genRandArr(int size) {
    vector<double> arr(size);

    // Инициализация генератора случайных чисел
    mt19937 engine(time(0));
    uniform_real_distribution<double> gen(-1.0, 1.0);

    // Заполняем массив случайными числами
    for (auto& el : arr) {
        el = gen(engine);
    }

    return arr;
}

// Запуск серии тестов
void runTestSeries(int arraySize, int seriesLen, ofstream& outFile) {
    vector<double> times;
    vector<size_t> maxMemoryList;
    vector<size_t> maxDepthList;
    vector<size_t> totalCallsList;

    // Начинаем тесты
    for (int i = 0; i < seriesLen; ++i) {
        // Создаем массив со случайными числами
        auto arr = genRandArr(arraySize);

        size_t max_memory = 0, max_depth = 0, total_calls = 0;

        // Засекаем время
        auto start = chrono::high_resolution_clock::now();

        // Сортировка и сбор метрик
        runMergeSort(arr, max_memory, max_depth, total_calls);

        // Останавливаем таймер
        auto end = chrono::high_resolution_clock::now();

        // Рассчитываем продолжительность
        chrono::duration<double> period = end - start;

        // Добавляем данные в массивы
        times.push_back(period.count());
        maxMemoryList.push_back(max_memory);
        maxDepthList.push_back(max_depth);
        totalCallsList.push_back(total_calls);

        cout << "Размер м: " << arraySize << ", Макс. память: " << max_memory
             << ", Глубина рекурсии: " << max_depth
             << ", Вызовы рекурсии: " << total_calls
             << ", Время: " << period.count() << " сек\n";
    }

    // Вычисляем среднее, наилучшее и наихудшее время
    double avgTime = accumulate(times.begin(), times.end(), 0.0) / seriesLen;
    double bestTime = *min_element(times.begin(), times.end());
    double worstTime = *max_element(times.begin(), times.end());

    // Вычисляем средние значения метрик
    size_t avgMaxMemory = accumulate(maxMemoryList.begin(), maxMemoryList.end(), 0) / seriesLen;
    size_t avgMaxDepth = accumulate(maxDepthList.begin(), maxDepthList.end(), 0) / seriesLen;
    size_t avgTotalCalls = accumulate(totalCallsList.begin(), totalCallsList.end(), 0) / seriesLen;

    // Записываем данные в файл
    outFile << arraySize << "," << avgTime << "," << bestTime << "," << worstTime << ","
            << avgMaxMemory << "," << avgMaxDepth << "," << avgTotalCalls << "\n";
}

// Функция для записи данных в файл
void saveDataToFile(const vector<int>& arraySizes, int seriesLen) {
    ofstream outFile("data.csv");

    // Заголовок файла
    outFile << "ArraySize,AvgTime,BestTime,WorstTime,AvgMaxMemory,AvgMaxDepth,AvgTotalCalls\n";

    for (int size : arraySizes) {
        cout << "Сортировка массивов величиной: " << size << "\n";
        runTestSeries(size, seriesLen, outFile);
    }

    outFile.close();
    cout << "Данные сохранены в файл data.csv\n";
}

int main() {
    vector<int> arraySizes = {1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000};
    int seriesLen = 20;

    // Сохраняем данные в файл
    saveDataToFile(arraySizes, seriesLen);

    return 0;
}