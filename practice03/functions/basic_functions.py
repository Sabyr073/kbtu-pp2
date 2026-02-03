# 1
# a function is a block of code that runs only when you call it
# In Python, a function is defined using the def keyword, followed by a function name and parentheses
def my_function():
  print("Hello from a function")

# 2
# To call a function, write its name followed by parentheses
def my_function():
  print("Hello from a function")

my_function()

# 3
# Without functions - repetitive code
# With functions - reusable code

def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))