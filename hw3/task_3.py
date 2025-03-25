import numpy as np
from functools import lru_cache

# Вспомогательный класс с хэш-функцией
class HashMixin:
    def __hash__(self):
        """
        Упрощенная хэш-функция:
        1) Суммируются все элементы матрицы.
        2) Возвращается хэш от суммы.
        """
        return hash(int(np.sum(self.data)))

    def __eq__(self, other):
        """
        Сравнение двух матриц.
        """
        return np.array_equal(self.data, other.data)

# Вспомогательный класс для кэширования матричного умножения
class CacheMixin:
    @lru_cache(maxsize=None)
    def __matmul__(self, other):
        return self.__class__(self.data @ other.data)

# Основной класс матрицы
class Matrix(HashMixin, CacheMixin):
    
    def __init__(self, data):
        self.data = np.array(data)
        self.n_rows = self.data.shape[0]
        self.n_cols = self.data.shape[1]

    def __add__(self, other):
        if self.n_rows != other.n_rows or self.n_cols != other.n_cols:
            raise ValueError("Matrices must have the same dimensions to make addition.")
        return Matrix(self.data + other.data)

    def __mul__(self, other):
        if self.n_rows != other.n_rows or self.n_cols != other.n_cols:
            raise ValueError("Matrices must have the same dimensions to make component-wise multiplication.")
        return Matrix(self.data * other.data)

    def __matmul__(self, other):
        if self.n_cols != other.n_rows:
            raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix to make matrix multiplication.")
        return Matrix(self.data @ other.data)

    def __str__(self):
        return str(self.data)

    def save_to_file(self, filename):
        np.savetxt(filename, self.data, fmt='%d')
        
# Поиск коллизии
def find_collision():
    # Матрицы A и C с одинаковым хэшем, но разным содержимым
    A = Matrix([[1, 2], [3, 4]])
    C = Matrix([[4, 3], [2, 1]])  # hash(A) == hash(C), но A != C

    # Матрицы B и D одинаковые
    B = Matrix([[1, 0], [0, 1]])
    D = Matrix([[1, 0], [0, 1]])

    # Проверка условий
    assert (hash(A) == hash(C)) & (A != C)
    assert B == D
    assert (A @ B).data.tolist() != (C @ D).data.tolist()

    # Сохранение матриц в файлы
    A.save_to_file('hw3/artifacts/A.txt')
    B.save_to_file('hw3/artifacts/B.txt')
    C.save_to_file('hw3/artifacts/C.txt')
    D.save_to_file('hw3/artifacts/D.txt')

    # Результаты умножения
    AB = A @ B
    CD = C @ D
    AB.save_to_file('hw3/artifacts/AB.txt')
    CD.save_to_file('hw3/artifacts/CD.txt')

    # Сохранение хэшей
    with open('hw3/artifacts/hash.txt', 'w') as f:
        f.write(f"Hash of AB: {hash(AB)}\n")
        f.write(f"Hash of CD: {hash(CD)}\n")

    print("Коллизия найдена, результаты сохранены в файлы.")

if __name__ == '__main__':
    # Запуск поиска коллизии
    find_collision()