import numpy as np

class Matrix:
    
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
        
if __name__ == '__main__':
    
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    result_add = matrix1 + matrix2
    result_mul = matrix1 * matrix2
    result_matmul = matrix1 @ matrix2

    result_add.save_to_file('hw3/artifacts/matrix+_task_1.txt')
    result_mul.save_to_file('hw3/artifacts/matrix*_task_1.txt')
    result_matmul.save_to_file('hw3/artifacts/matrix@_task_1.txt')

    print("Сложение матриц:")
    print(result_add)
    print("\nПокомпонентное умножение:")
    print(result_mul)
    print("\nМатричное умножение:")
    print(result_matmul)