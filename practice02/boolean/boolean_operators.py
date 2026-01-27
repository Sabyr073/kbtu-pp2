# 1
# The is operator returns True if both variables point to the same object
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y)
# 2
# The is not operator returns True if both variables do not point to the same object
x = ["apple", "banana"]
y = ["apple", "banana"]

print(x is not y)

# 3
# Check if "banana" is present in a list
fruits = ["apple", "banana", "cherry"]

print("banana" in fruits)

# 4 
text = "Hello World"

print("H" in text)
print("hello" in text)
print("z" not in text)

# 5 
a = 6      # binary: 110
b = 3      # binary: 011

print(a & b) # 010  → 2
print(a | b) # 111  → 7
print(a ^ b) # 101  → 5