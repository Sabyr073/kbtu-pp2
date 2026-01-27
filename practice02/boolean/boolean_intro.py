# 1
# Booleans represent one of two values: True or False
print(10 > 9)
print(10 == 9)
print(10 < 9)

# 2
# Evaluate a string and a number

print(bool("Hello"))
print(bool(15))

# 3
# Almost any value is evaluated to True if it has some sort of content
# The following will return True

bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

# 4 
# an object that is made from a class with a __len__ function that returns 0 or False:

class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))

# 5

def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")
