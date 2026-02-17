# 1
# An iterator is an object that contains a countable number of values
# An iterator is an object that can be iterated upon, meaning that you can traverse through all the values
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))

# 2 
# Iterate the values of a tuple
mytuple = ("apple", "banana", "cherry")

for x in mytuple:
  print(x)

# 3
# Create an iterator that returns numbers, starting with 1, and each sequence will increase by one
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))

# 4
# Stop after 20 iterations
# To prevent the iteration from going on forever, we can use the StopIteration statement
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)

for x in myiter:
  print(x)

# 5
# A generator function is a special type of function that returns an iterator object
def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1

ctr = fun(5)
for n in ctr:
    print(n)