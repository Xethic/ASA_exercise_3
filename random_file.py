import random
import string

s = ""

for i in range(5000001):
	s += random.choice("ACTG")
	
with open("random.txt", "w") as f:
	f.write(s)
