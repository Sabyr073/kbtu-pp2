# 1
# Functions can send data back to the code that called them using the return statement
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)

# 2
# Using the return value directly
def get_greeting():
  return "Hello from a function"

print(get_greeting())

# 3
# Function definitions cannot be empty.
# If you need to create a function placeholder without any code, use the pass statement
def my_function():
  pass