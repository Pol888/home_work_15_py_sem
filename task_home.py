import argparse
import logging


class MatrixError(Exception):
    pass


class AdditionOfMatricesError(MatrixError):

    def __init__(self, lens_matrix: list):
        self.lens_matrix: list = lens_matrix

    def __str__(self):
        if self.lens_matrix[0] != self.lens_matrix[2] and self.lens_matrix[1] != self.lens_matrix[3]:
            return f"Сторона A первой матрицы == {self.lens_matrix[0]} не ровна стороне A второй матрицы == " \
                   f"{self.lens_matrix[2]} и сторона B первой матрицы == {self.lens_matrix[1]} не ровна " \
                   f"стороне B второй матрицы == {self.lens_matrix[3]}. С такими параметрами матрицы не могут " \
                   f"быть суммированы."
        elif self.lens_matrix[0] != self.lens_matrix[2]:
            return f"Сторона A первой матрицы == {self.lens_matrix[0]} не ровна стороне A второй матрицы == " \
                   f"{self.lens_matrix[2]}. С такими параметрами матрицы не могут быть суммированы."
        else:
            return f"Сторона B первой матрицы == {self.lens_matrix[1]} не ровна стороне B второй матрицы == " \
                   f"{self.lens_matrix[3]}. С такими параметрами матрицы не могут быть суммированы."


class MultiplicationOfMatricesError(MatrixError):

    def __init__(self, lens_matrix: list):
        self.lens_matrix: list = lens_matrix

    def __str__(self):
        return f"Сторона B первой матрицы == {self.lens_matrix[0]} не ровна стороне A второй матрицы == " \
               f"{self.lens_matrix[1]}.\nС такими параметрами матрицы не могут " \
               f"быть перемножены.\nСторона B первой должна быть ровна стороне A второй."


class Matrix:
    """An instance of this class stores 1 matrix in memory, performs operations with other instances"""

    def __init__(self, matrix):
        """The matrix is initialized by a property of this class"""
        self.matrix = matrix

    def __str__(self):
        """Displays the string representation of the matrix"""
        string_representation = ''
        for i in self.matrix:
            string_representation += str(i) + '\n'
        return 'It`s matrix\n' + string_representation

    def __repr__(self):
        """String representation of the current instance"""
        return f'Matrix({str(self.matrix)})'

    def matrix_size(self):
        """Calculates the size of the matrix"""
        return len(self.matrix) * len(self.matrix[0])

    def __add__(self, other):
        """Performs matrix addition"""
        if len(self.matrix) == len(other.matrix) and len(self.matrix[0]) == len(other.matrix[0]):
            return Matrix([[self.matrix[i][j] + other.matrix[i][j] for j in
                            range(len(self.matrix[0]))] for i in range(len(self.matrix))])

        raise AdditionOfMatricesError([len(self.matrix), len(self.matrix[0]), len(other.matrix), len(other.matrix[0])])

    def __mul__(self, other):
        """Performs the product of matrices"""
        if len(self.matrix[0]) == len(other.matrix):
            new_mx = [[0 for _ in range(len(other.matrix[0]))] for _ in range(len(self.matrix))]
            for i in range(len(self.matrix)):
                for j in range(len(other.matrix[0])):
                    for y in range(len(self.matrix[0])):
                        new_mx[i][j] += self.matrix[i][y] * other.matrix[y][j]
            return Matrix(new_mx)

        raise MultiplicationOfMatricesError([len(self.matrix[0]), len(other.matrix)])

    def __eq__(self, o) -> bool:
        """Compares matrices (operator: ==)"""
        return self.matrix_size() == o.matrix_size()

    def __ne__(self, o) -> bool:
        """Compares matrices (operator: !=)"""
        return self.matrix_size() != o.matrix_size()

    def __gt__(self, o) -> bool:
        """Compares matrices (operator: >)"""
        return self.matrix_size() > o.matrix_size()

    def __ge__(self, o) -> bool:
        """Compares matrices (operator: <=)"""
        return self.matrix_size() <= o.matrix_size()

    def __lt__(self, o) -> bool:
        """Compares matrices (operator: <)"""
        return self.matrix_size() < o.matrix_size()

    def __le__(self, o) -> bool:
        """Compares matrices (operator: >=)"""
        return self.matrix_size() >= o.matrix_size()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="Matrix" + '_log_.log',
                        filemode='a', encoding='utf-8', format='{levelname} - {asctime} {msg}', style='{')
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('-m_1', metavar='matrix_1', nargs='*',
                        help='example: -m_1 1 2 3 . 3 2 1 . ==> [[1, 2, 3], [3, 2, 1]]', default=None)
    parser.add_argument('-m_2', metavar='matrix_2', nargs="*",
                        help='example: -m_2 1 2 3 . 3 2 1 . ==> [[1, 2, 3], [3, 2, 1]]', default=None)
    parser.add_argument('-add', metavar='m_1+m_2', help='Введите "True", для сложения матриц', default=None)
    parser.add_argument('-mul', metavar='m_1*m_2', help='Введите "True", для умножения матриц', default=None)
    args_input = parser.parse_args().__dict__
    matrix_1: list = [[1], [1]]
    matrix_2: list = [[1], [1]]
    try:
        if args_input['m_1'] is not None:
            matrix_1 = []
            matrix_1_line = []
            for i in args_input['m_1']:
                if i == '.':
                    matrix_1.append(matrix_1_line)
                    matrix_1_line = []
                else:
                    matrix_1_line.append(int(i))

        if args_input['m_2'] is not None:
            matrix_2 = []
            matrix_2_line = []
            for i in args_input['m_2']:
                if i == '.':
                    matrix_2.append(matrix_2_line)
                    matrix_2_line = []
                else:
                    matrix_2_line.append(int(i))

        logger.info(f'creation: matrix_1 - {Matrix(matrix_1).__repr__()}, matrix_2 - {Matrix(matrix_2).__repr__()}')
        print(f'matrix_1 - {Matrix(matrix_1).__repr__()}')
        print(f'matrix_2 - {Matrix(matrix_2).__repr__()}')
        if args_input['add'] == 'True':
            print(f"Результат сложения матриц: {Matrix(matrix_1) + Matrix(matrix_2)}")
            logger.warning(f'Результат сложения матриц: {(Matrix(matrix_1) + Matrix(matrix_2)).__repr__()}')
        if args_input['mul'] == 'True':
            print(f"Результат умножения матриц: {Matrix(matrix_1) * Matrix(matrix_2)}")
            logger.warning(f'Результат умножения матриц: {(Matrix(matrix_1) * Matrix(matrix_2)).__repr__()}')
    except AdditionOfMatricesError:
        logger.critical('Не удалось сложить матрицы')
        raise AdditionOfMatricesError([len(matrix_1), len(matrix_1[0]), len(matrix_2), len(matrix_2[0])])
    except MultiplicationOfMatricesError:
        logger.critical("'Не удалось перемножить матрицы'")
        raise MultiplicationOfMatricesError([len(matrix_1[0]), len(matrix_2)])
