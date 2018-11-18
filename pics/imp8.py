def f(x):
    for i in range(x, x+4):
        v=i
        for j in range(1, v):
            v *= i
        print(v)
    return

f(4)
