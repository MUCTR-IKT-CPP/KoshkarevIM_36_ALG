import math
import struct
import random
import time
import matplotlib.pyplot as plt
from collections import defaultdict


def left_rotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF


def md5(message):
    # Инициализация переменных
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

    # Функции для раундов
    def F(X, Y, Z):
        return (X & Y) | (~X & Z)

    def G(X, Y, Z):
        return (X & Z) | (Y & ~Z)

    def H(X, Y, Z):
        return X ^ Y ^ Z

    def I(X, Y, Z):
        return Y ^ (X | ~Z)

    # Таблица констант
    T = [int(abs(math.sin(i + 1)) * 0x100000000) & 0xFFFFFFFF for i in range(64)]

    # Преобразование сообщения в байты
    orig_len = len(message)
    message = bytearray(message, 'utf-8')

    # Добавление бита '1' и выравнивание длины
    message.append(0x80)
    while (len(message) % 64) != 56:
        message.append(0)

    # Добавление длины сообщения (биты)
    message_len = (orig_len * 8) & 0xFFFFFFFFFFFFFFFF
    message += struct.pack('<Q', message_len)

    # Обработка блоков
    for block_start in range(0, len(message), 64):
        block = message[block_start:block_start + 64]
        M = struct.unpack('<16I', block)

        a, b, c, d = A, B, C, D

        # Раунды
        for i in range(64):
            if 0 <= i < 16:
                f = F(b, c, d)
                g = i
            elif 16 <= i < 32:
                f = G(b, c, d)
                g = (5 * i + 1) % 16
            elif 32 <= i < 48:
                f = H(b, c, d)
                g = (3 * i + 5) % 16
            else:
                f = I(b, c, d)
                g = (7 * i) % 16

            f = (f + a + T[i] + M[g]) & 0xFFFFFFFF
            a = d
            d = c
            c = b
            b = (b + left_rotate(f, [7, 12, 17, 22][i // 16])) & 0xFFFFFFFF

        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    # Формирование хеша
    hash_bytes = struct.pack('<4I', A, B, C, D)
    return ''.join(f'{b:02x}' for b in hash_bytes)


def generate_strings(length, num_diff):
    s1 = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))
    s2 = list(s1)
    indices = random.sample(range(length), num_diff)
    for i in indices:
        new_char = random.choice('abcdefghijklmnopqrstuvwxyz')
        while new_char == s2[i]:
            new_char = random.choice('abcdefghijklmnopqrstuvwxyz')
        s2[i] = new_char
    return s1, ''.join(s2)


def max_common_substring(s1, s2):
    max_len = 0
    for i in range(len(s1)):
        for j in range(len(s2)):
            current_len = 0
            while (i + current_len < len(s1) and j + current_len < len(s2) and s1[i + current_len] == s2[j + current_len]):
                current_len += 1
            if current_len > max_len:
                max_len = current_len
    return max_len


def test1():
    diff_counts = [1, 2, 4, 8, 16]
    results = {}
    for diff in diff_counts:
        max_lengths = []
        for _ in range(1000):
            s1, s2 = generate_strings(128, diff)
            h1 = md5(s1)
            h2 = md5(s2)
            max_len = max_common_substring(h1, h2)
            max_lengths.append(max_len)
        results[diff] = max(max_lengths)

    plt.figure(figsize=(10, 6))
    plt.plot(results.keys(), results.values(), marker='o')
    plt.xlabel('Количество отличий в символах')
    plt.ylabel('Максимальная длина совпадения в хеше')
    plt.title('Зависимость максимальной длины совпадения в хеше MD5\nот количества различий в исходных строках')
    plt.grid(True)
    plt.show()


def test2():
    results = []
    for i in range(2, 7):
        N = 10 ** i
        hashes = defaultdict(int)
        for _ in range(N):
            s = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=256))
            h = md5(s)
            hashes[h] += 1
        collisions = sum(count - 1 for count in hashes.values() if count > 1)
        results.append((N, collisions))

    print("\nРезультаты поиска коллизий:")
    print("+" + "-" * 25 + "+")
    print("| {:^12} | {:^10} |".format("Кол-во хешей", "Коллизии"))
    print("+" + "-" * 25 + "+")
    for n, c in results:
        print("| {:>12} | {:>10} |".format(n, c))
    print("+" + "-" * 25 + "+")


def test3():
    lengths = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
    avg_times = []
    for n in lengths:
        times = []
        for _ in range(1000):
            s = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=n))
            start = time.perf_counter()
            md5(s)
            end = time.perf_counter()
            times.append(end - start)
        avg = sum(times) / len(times)
        avg_times.append(avg)

    plt.figure(figsize=(10, 6))
    plt.plot(lengths, avg_times, marker='o')
    plt.xlabel('Длина входной строки (символы)')
    plt.ylabel('Среднее время вычисления (секунды)')
    plt.title('Зависимость времени вычисления MD5\nот длины входных данных')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    print("Запуск теста 1: Сравнение хешей для строк с различным числом отличий")
    test1()

    print("\nЗапуск теста 2: Поиск коллизий")
    test2()

    print("\nЗапуск теста 3: Замер времени выполнения")
    test3()