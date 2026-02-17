def fun(a):
    while a >= 0:
        yield a
        a -= 1

a = fun(int(input()))
print(",".join(str(n) for n in a))