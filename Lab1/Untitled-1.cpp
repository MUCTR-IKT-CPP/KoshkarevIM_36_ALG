#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <iomanip>
#include <fstream>
#include <algorithm> // для std::min_element и std::max_element

using namespace std;

// Функция сортировки выбором
void selectionSort(vector<double>& arr, int& passes, int& swaps) {
    int n = arr.size();
    passes = 0; // проходы по массиву
    swaps = 0;  // количество обменов

    for (int i = 0; i < n - 2; i++) {
        int min = i; // Индекс минимального элемента
        ++passes; // Считаем проходы

        // Находим минимальный элемент в оставшейся части массива
        for (int j = i + 1; j < n - 1; j++) {
            if (arr[j] < arr[min]) {
                min = j;
            }
        }

        swap(arr[i], arr[min]);
        ++swaps; // Считаем обмены
        
    }
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
    vector<int> passesList;
    vector<int> swapsList;

    for (int i = 0; i < seriesLen; ++i) {
        auto arr = genRandArr(arraySize);

        int passes = 0, swaps = 0;
        auto start = chrono::high_resolution_clock::now();
        selectionSort(arr, passes, swaps);
        auto end = chrono::high_resolution_clock::now();

        chrono::duration<double> period = end - start;
        times.push_back(period.count());
        passesList.push_back(passes);
        swapsList.push_back(swaps);

        cout << "Размер м: " << arraySize
             << ", Проходов: " << passes
             << ", Обменов: " << swaps
             << ", Время: " << period.count() << " сек\n";
    }

    // Вычисляем среднее, наилучшее и наихудшее время
    double avgTime = accumulate(times.begin(), times.end(), 0.0) / seriesLen;
    cout << "Среднее время для сортировки массива величиной " << arraySize << ": " << avgTime << " сек\n\n";
    double bestTime = *min_element(times.begin(), times.end());
    double worstTime = *max_element(times.begin(), times.end());

    // Вычисляем среднее количество проходов и обменов
    double avgPasses = accumulate(passesList.begin(), passesList.end(), 0.0) / seriesLen;
    double avgSwaps = accumulate(swapsList.begin(), swapsList.end(), 0.0) / seriesLen;

    // Записываем данные в файл
    outFile << arraySize << ","
            << avgTime << ","
            << bestTime << ","
            << worstTime << ","
            << avgPasses << ","
            << avgSwaps << "\n";
}

// Функция для записи данных в файл
void saveDataToFile(const vector<int>& arraySizes, int seriesLen) {
    ofstream outFile("sorting_data.csv");

    // Заголовок файла
    outFile << "ArraySize,AvgTime,BestTime,WorstTime,AvgPasses,AvgSwaps\n";

    for (int size : arraySizes) {
        cout << "Сортировка массивов величиной: " << size << "\n";
        runTestSeries(size, seriesLen, outFile);
    }

    outFile.close();
    cout << "Данные сохранены в файл sorting_data.csv\n";
}

int main() {
    vector<int> arraySizes = {1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000};
    int seriesLen = 20;

    // Сохраняем данные в файл
    saveDataToFile(arraySizes, seriesLen);

    return 0;
}