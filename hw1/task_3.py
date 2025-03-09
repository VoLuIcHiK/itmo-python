#!/usr/bin/env python3

import sys


def count_stats(text: str) -> None:
    """
    Функция для подсчета кол-ва строк, слов и байт в тексте
    Args:
        text (str): текст для анализа
    Returns:
        None
    """
    lines = text.count("\n")
    words = len(text.split())
    bytes_count = len(text.encode("utf-8"))
    return lines, words, bytes_count


def print_stats(lines: int, words: int, bytes_count: int, filename=None) -> None:
    """
    Функция для вывода статистики в формате утилиты wc
    Args:
        lines (int): кол-во строк в файле
        words (int): кол-во слов в файле
        bytes_count (int): кол-во байт в файле"""
    if filename:
        print(f"{lines:8}{words:8}{bytes_count:8} {filename}")
    else:
        print(f"{lines:8}{words:8}{bytes_count:8}")


def main() -> None:
    """
    Основная функция программы
    """
    total_lines, total_words, total_bytes = 0, 0, 0
    if len(sys.argv) > 1:
        # Если переданы файлы - обрабатываем каждый
        for filename in sys.argv[1:]:
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    text = file.read()
                    lines, words, bytes_count = count_stats(text)
                    print_stats(lines, words, bytes_count, filename)
                    # Суммируем статистику для total
                    total_lines += lines
                    total_words += words
                    total_bytes += bytes_count
            except FileNotFoundError:
                print(f"wc: {filename}: No such file or directory", file=sys.stderr)
                sys.exit(1)

        # Если файлов больше одного - выводим суммарную статистику (total)
        if len(sys.argv) > 2:
            print_stats(total_lines, total_words, total_bytes, "total")
    else:
        # Если файлы не переданы - читаем из stdin
        text = sys.stdin.read()
        lines, words, bytes_count = count_stats(text)
        print_stats(lines, words, bytes_count)


if __name__ == "__main__":
    main()
