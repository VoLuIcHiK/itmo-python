import numpy as np

# Вспомогательный класс со стандартными арифметическими операциями
class ArithmeticMixin:
    
    def __add__(self, other):
        return self.__class__(self.data + other.data)

    def __sub__(self, other):
        return self.__class__(self.data - other.data)

    def __mul__(self, other):
        return self.__class__(self.data * other.data)

    def __matmul__(self, other):
        return self.__class__(self.data @ other.data)

    def __truediv__(self, other):
        return self.__class__(self.data / other.data)

# Вспомогательный класс для сохранения результата в файл
class FileSaveMixin:
    
    def save_to_file(self, filename):
        np.savetxt(filename, self.data, fmt='%d')

# Вспомогательный класс для красвого отображения в консоли
class PrettyOutputMixin:
    
    def __str__(self):
        return str(self.data)

# Вспомогательный класс с getter-ами и setter-ами для полей класса
class PropertyMixin:
    
    @property
    def data(self):
        return self._data
    
    @property
    def shape(self):
        return self._data.shape

    @data.setter
    def data(self, value):
        self._data = np.array(value)

class Matrix(ArithmeticMixin, FileSaveMixin, PrettyOutputMixin, PropertyMixin):
    
    def __init__(self, data):
        self.data = data  
        
if __name__ == '__main__':
    
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    result_add = matrix1 + matrix2
    result_mul = matrix1 * matrix2
    result_matmul = matrix1 @ matrix2

    result_add.save_to_file('hw3/artifacts/matrix+_task_2.txt')
    result_mul.save_to_file('hw3/artifacts/matrix*_task_2.txt')
    result_matmul.save_to_file('hw3/artifacts/matrix@_task_2.txt')

    print("Сложение матриц:")
    print(result_add)
    print("\nПокомпонентное умножение:")
    print(result_mul)
    print("\nМатричное умножение:")
    print(result_matmul)