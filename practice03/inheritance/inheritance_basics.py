# 1
# Inheritance allows us to define a class that inherits all the methods and properties from another class
# Parent class is the class being inherited from, also called base class
# Child class is the class that inherits from another class, also called derived class
# Create a class named Person, with firstname and lastname properties, and a printname method
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()

# 2
# Create a class named Student, which will inherit the properties and methods from the Person class
class Student(Person):
  pass
#Use the Student class to create an object, and then execute the printname method
x = Student("Mike", "Olsen")
x.printname()

# 3
# Add the __init__() function to the Student class
class Student(Person):
  def __init__(self, fname, lname):
    #add properties etc.

# 4
# Python also has a super() function that will make the child class inherit all the methods and properties from its parent
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)

# 5
# Add a property called graduationyear to the Student class
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)
    self.graduationyear = 2019