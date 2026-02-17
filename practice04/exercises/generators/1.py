def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1

ctr = fun(int(input()))
for n in ctr:
    print(n**2)