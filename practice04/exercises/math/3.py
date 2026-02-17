import math
sides = int(input("Input number of sides: "))
length = float(input("Input the length: "))

area = (sides * (length ** 2 ))/ (4 * math.tan(math.pi / sides))

print("The area is: ", int(area))