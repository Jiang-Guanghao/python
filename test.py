# /usr/bin/env python3
# -*- coding: utf-8 -*-

def maxof2(a, b):
    if a > b:
        return a
    else:
        return b

print(maxof2(10,100))

x = 7 ** 6
print (x)

for i in range(1,10,1):
    print(i)

a = 0
while a < 11:
    a = a + 1
    print(a)

print("--------test open file--------")
with open(".gitignore") as file:
    for line in file:
        print(line)

if __name__ == "__main__":
    print("hello.")