# 1
# Python is an object oriented programming language
# Almost everything in Python is an object, with its properties and methods
# A Class is like an object constructor, or a "blueprint" for creating objects
# To create a class, use the keyword class
# Create a class named MyClass, with a property named x
class MyClass:
  x = 5

# 2
# Create an object named p1, and print the value of x
p1 = MyClass()
print(p1.x)

# 3
# Delete the p1 object
del p1

# 4 
# Create three objects from the MyClass class
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)

# 5 
# put in the pass statement to avoid getting an error
class Person:
  pass