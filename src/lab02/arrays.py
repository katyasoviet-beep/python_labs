def min_max(nums: list[float | int]) -> tuple[float | int]:
    if not nums:
        raise ValueError('Список не должен быть пустым')
    return (min(nums), max(nums))
def unique_sorted(nums: list[float | int]) -> list[float | int]:
    return sorted(set(nums))
def flatten(mat: list[list | tuple]) -> list:
    flat_list = []
    for element in mat:
        if not isinstance(element, (list, tuple)):
            raise TypeError('Строка не строка строк матрицы')
        else:
            flat_list.extend(element)
    return flat_list

#        Тест кейсы

print('min_max')
print(min_max([3, -1, 5, 5, 0]))
print(min_max([42]))
print(min_max([-5, -2, -9]))
try:
    print(min_max([]))
except ValueError as e:
    print(e)
print(min_max([1.5, 2, 2.0, -3.1]))

print('unique_sorted')
print(unique_sorted([3, 1, 2, 1, 3]))
print(unique_sorted([]))
print(unique_sorted([-1, -1, 0, 2, 2]))
print(unique_sorted([1.0, 1, 2.5, 0]))

print('flatten')
print(flatten([[1, 2], [3, 4]]))
print(flatten([[1, 2], (3, 4, 5)]))
print(flatten([[1], [], [2, 3]]))
try:
    print(flatten([[1, 2], 'ab']))
except TypeError as e:
    print(e)

#        Свои примеры

print('min_max')
print(min_max([4, -5, 10, 10, 3]))
print(min_max([52]))
print(min_max([-3, -8, -10]))
try:
    print(min_max([]))
except ValueError as e:
    print(e)
print(min_max([5.7, 3, 3.0, -5.3]))

print('unique_sorted')
print(unique_sorted([4, 5, 8, 4, 5]))
print(unique_sorted([]))
print(unique_sorted([-6, -6, 0, 4, 4]))
print(unique_sorted([4.0, 1.5, 6, 0]))

print('flatten')
print(flatten([[5, 4], [2, 7]]))
print(flatten([[3, 5], (4, 7, 8)]))
print(flatten([[3], [], [5, 8]]))
try:
    print(flatten([[5, 7], 'Грибочки']))
except TypeError as e:
    print(e)