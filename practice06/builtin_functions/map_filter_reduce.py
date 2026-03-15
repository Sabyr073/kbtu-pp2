a = [1,2,3,4,5,6]
b = list(map(lambda x: x * 2 ,a))
c = list(filter(lambda x: x % 3 == 0,a))
print(b)
print(c)

from functools import reduce
result = reduce(lambda x,y:x*y,a)
print(result)