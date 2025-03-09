import sys


def tail_file(file: str, lines: int = 10, show_filename: bool = False) -> None:
    """
    Функция для вывода последних N линий в файле
    Args:
        file (str): имя файла
        lines (int): кол-во строк, которое необходимо вывести
        show_filename (bool): флаг вывода имя файла
    Returns:
        None
    """
    if show_filename:
        print(f"\n==> {file.name} <==")
    for line in file.readlines()[-lines:]:
        print(line, end="")


def main() -> None:
    """
    Основная функция программы
    """
    if len(sys.argv) > 1:
        # Если переданы файлы - обрабатываем каждый
        for filename in sys.argv[1:]:
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    # Если файлов больше одного - показываем имя файла
                    if len(sys.argv) > 2:
                        tail_file(file, lines=10, show_filename=True)
                    else:
                        tail_file(file, lines=10)
            except FileNotFoundError:
                print(
                    f"tail: cannot open '{filename}' for reading: No such file or directory",
                    file=sys.stderr,
                )
    else:
        # Если файлы не переданы - читаем последние 17 строк из stdin
        lines = sys.stdin.readlines()
        for line in lines[-17:]:
            print(line, end="")


if __name__ == "__main__":
    main()
