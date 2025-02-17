import numpy as np
from matrix import Matrix

if __name__ == '__main__':
    one = Matrix(list(np.array(np.random.randint(0, 10, (3, 3))).tolist()))
    two = Matrix(list(np.array(np.random.randint(0, 10, (3, 3))).tolist()))

    add = one + two
    mul = one * two
    matmul = one @ two
    file_add = open('artifacts/3.1/matrix+.txt', 'w')
    file_mul = open('artifacts/3.1/matrix*.txt', 'w')
    file_matmul = open('artifacts/3.1/matrix@.txt', 'w')
    assets = [(file_add, add), (file_mul, mul), (file_matmul, matmul)]

    for (file_descr, matrix) in assets:
        file_descr.write(f'Left matrix: \n')
        file_descr.writelines(str(one))
        file_descr.write('\n')
        file_descr.write(f'Right matrix: \n')
        file_descr.writelines(str(two))
        file_descr.write('\n')
        file_descr.write(f'Result: \n')
        file_descr.writelines(str(matrix))
