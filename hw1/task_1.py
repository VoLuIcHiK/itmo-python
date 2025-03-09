import sys


def number_lines(input_file: str):
    """
    Функция для подсчета кол-ва строк в файле
    Args:
        input_file (str): название передаваемого файла
    """
    for i, line in enumerate(input_file, start=1):
        print(f"{i}\t{line}", end="")


def main():
    """
    Основная функция программы
    """
    if len(sys.argv) > 1:
        # Если передано файл - открываем файл
        with open(sys.argv[1], "r") as file:
            number_lines(file)
    else:
        # Если файл не передан - читаем из stdin
        number_lines(sys.stdin)


if __name__ == "__main__":
    main()
