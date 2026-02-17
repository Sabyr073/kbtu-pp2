def fun(max):
    cnt = 0
    while cnt <= max:
        yield cnt
        cnt += 2

ctr = fun(int(input()))
for n in ctr:
    print(",".join(str(n) for n in ctr))