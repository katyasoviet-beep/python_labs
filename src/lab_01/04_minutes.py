m = int(input("Введите минуты:"))
h = m // 60
m1 = m % 60
if h >= 24:
    d = h // 24
    h1 = h % 24
    print(m)
    print(d, h1, m1, sep=":")
else:
    print(m)
    print(h, m1, sep=":")
