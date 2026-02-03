# 1
# A function with one argument
def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")

# 2 
# A parameter is the variable listed inside the parentheses in the function definition
# An argument is the actual value that is sent to the function when it is called

def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an argument

# 3 
# You can assign default values to parameters.
# If the function is called without an argument, it uses the default value
def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

# 4 
# You can send arguments with the key = value syntax
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(animal = "dog", name = "Buddy")

# 5 
# You can mix positional and keyword arguments in a function call
def my_function(animal, name, age):
  print("I have a", age, "year old", animal, "named", name)

my_function("dog", name = "Buddy", age = 5)