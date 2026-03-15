fruits = ["apple", "banana", "pear", "tangerine"]
for i,v in enumerate(fruits):
    print(i+1,v,sep=":")

clubs = ["Real Madrid", "AC Milan", "Bayern Munich", "Barcelona"]
ucl = [15,7,6,5]
print(*list(zip(clubs,ucl)))



x = 10
print(type(x))
print(isinstance(x, int))

a = "5"
b = int(a)
print(b + 3)

nums = ["1", "2", "3"]
nums_int = list(map(int, nums))
print(nums_int)