def transpose(mat: list[list[float | int]]) -> list[list[float | int]]:
    if not mat:
        return []
    num_rows = len(mat)
    num_cols = len(mat[0])
    for row in mat:
        if len(row) != num_cols:
            raise ValueError('Рваная')

    transposed_mat = [[mat[i][j] for i in range(num_rows)] for j in range(num_cols)]
    return transposed_mat

def row_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []
    num_cols = len(mat[0])
    for row in mat:
        if len(row) != num_cols:
            raise ValueError("Рваная")
    return [sum(row) for row in mat]

def col_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []
    num_cols = len(mat[0])
    for row in mat:
        if len(row) != num_cols:
            raise ValueError("Рваная")
    return [sum(mat[i][j] for i in range(len(mat))) for j in range(num_cols)]


#     Тест кейсы

print('transpose')
print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
try:
    print(transpose([[1, 2], [3]]))
except ValueError as e:
    print(e)

print('row_sums')
print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0, 0], [0, 0]]))
try:
    print(row_sums([[1, 2], [3]]))
except ValueError as e:
    print(e)

print('col_sums')
print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
try:
    print(col_sums([[1, 2], [3]]))
except ValueError as e:
    print(e)

#     Свои примеры

print('transpose')
print(transpose([[4, 6, 1]]))
print(transpose([[5], [3], [7]]))
print(transpose([[5, 3], [6, 1]]))
print(transpose([]))
try:
    print(transpose([[2, 7], [4]]))
except ValueError as e:
    print(e)

print('row_sums')
print(row_sums([[2, 1, 4], [5, 4, 1]]))
print(row_sums([[-5, 5], [17, -17]]))
print(row_sums([[0, 0], [0, 0]]))
try:
    print(row_sums([[7, 3], [5]]))
except ValueError as e:
    print(e)

print('col_sums')
print(col_sums([[5, 7, 2], [4, 3, 10]]))
print(col_sums([[-3, 3], [14, -14]]))
print(col_sums([[0, 0], [0, 0]]))
try:
    print(col_sums([[7, 3], [5]]))
except ValueError as e:
    print(e)