def fun(max):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())
print(",".join(str(x) for x in fun(n)))