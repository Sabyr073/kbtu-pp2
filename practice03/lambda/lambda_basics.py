# 1
# A lambda function is a small anonymous function
# Add 10 to argument a, and return the result
x = lambda a : a + 10
print(x(5))

# 2
# Multiply argument a with argument b and return the result
x = lambda a, b : a * b
print(x(5, 6))

# 3
# Summarize argument a, b, and c and return the result
x = lambda a, b, c : a + b + c
print(x(5, 6, 2))

# 4 
# The power of lambda is better shown when you use them as an anonymous function inside another function
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))

# 5
# Use the same function definition to make both functions, in the same program
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))