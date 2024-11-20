from itertools import repeat
from typing import List, Any, Tuple

class Matrix:
    def __init__(self, array: List[List[Any]]):
        if len(array) == 0:
            raise ValueError("Matrix should have at least 1 row")
        lengths = list(map(len, array))
        if lengths.count(lengths[0]) != len(lengths) or lengths[0] == 0:
            raise ValueError("All rows of the matrix should have equal length of at least 1 element")
        self.__array : List[List[Any]] = array
        self.__dimensions : Tuple[int, int] = (len(array), lengths[0])

    def __getitem__(self, item : Tuple[int, int]):
        row, col = item
        if row >= self.__dimensions[0] or col >= self.__dimensions[1]:
            raise ValueError("Specified index was outside of the matrix")
        return self.__array[row][col]

    def __add__(self, other : "Matrix") -> 'Matrix':
        if self.__dimensions != other.__dimensions:
            raise ValueError(f'Matrices have incompatible dimensions: {self.__dimensions} on left, {other.__dimensions} on right')

        result = []
        for row in range(self.__dimensions[0]):
            current = []
            for col in range(self.__dimensions[1]):
                current.append(self[(row, col)] + other[(row, col)])
            result.append(current)
        return Matrix(result)

    def __mul__(self, other : "Matrix") -> 'Matrix':
        if self.__dimensions != other.__dimensions:
            raise ValueError(f'Matrices have incompatible dimensions: {self.__dimensions} on left, {other.__dimensions} on right')

        result = []
        for row in range(self.__dimensions[0]):
            current = []
            for col in range(self.__dimensions[1]):
                current.append(self[(row, col)] * other[(row, col)])
            result.append(current)
        return Matrix(result)

    def __matmul__(self, other : "Matrix") -> 'Matrix':
        rows_left, cols_left = self.__dimensions
        rows_right, cols_right  = other.__dimensions
        if cols_left != rows_right:
            raise ValueError(f'Matrices have incompatible dimensions: {self.__dimensions} on left, {other.__dimensions} on right')

        common_side = cols_left
        result_rows = rows_left
        result_cols = cols_right

        result = []
        for r in range(result_rows):
            result.append(list(repeat(0, result_cols)))

        for row in range(result_rows):
            for col in range(result_cols):
                for i in range(common_side):
                    result[row][col] += self.__array[row][i] * other.__array[i][col]

        return Matrix(result)

    def __str__(self):
        strings = [list(map(str, line)) for line in self.__array]
        max_length = max([max(map(len, line)) for line in strings])
        fancy_lines = '\n '.join(map(lambda line: f'[{" ".join(map(lambda element: element.rjust(max_length), line))}]', strings))
        return f'[{fancy_lines}]'