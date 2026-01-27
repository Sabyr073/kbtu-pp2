# 1
# With the continue statement we can stop the current iteration of the loop, and continue with the next
# Do not print banana
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

# 2
# To loop through a set of code a specified number of times, we can use the range() function

# Using the range() function
for x in range(6):
  print(x)

# 3
# Using the start parameter
for x in range(2, 6):
  print(x)
for x in range(2, 30, 3):
  print(x)

# 4
# The else keyword in a for loop specifies a block of code to be executed when the loop is finished

# Print all numbers from 0 to 5, and print a message when the loop has ended
for x in range(6):
  print(x)
else:
  print("Finally finished!")

# 5
# A nested loop is a loop inside a loop
# Print each adjective for every fruit
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]

for x in adj:
  for y in fruits:
    print(x, y)
