# 1
# If you do not know how many arguments will be passed into your function, add a * before the parameter name
def my_function(*kids):
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus")

# 2
# The *args parameter allows a function to accept any number of positional arguments
def my_function(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function("Emil", "Tobias", "Linus")

# 3
# The **kwargs parameter allows a function to accept any number of keyword arguments
def my_function(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function(name = "Tobias", age = 30, city = "Bergen")

# 4
# You can use both *args and **kwargs in the same function
# The order must be:
# regular parameters
# *args
# **kwargs
def my_function(title, *args, **kwargs):
  print("Title:", title)
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)

my_function("User Info", "Emil", "Tobias", age = 25, city = "Oslo")

# 5 
# If you have values stored in a list, you can use * to unpack them into individual arguments
def my_function(a, b, c):
  return a + b + c

numbers = [1, 2, 3]
result = my_function(*numbers) # Same as: my_function(1, 2, 3)
print(result)