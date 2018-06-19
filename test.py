# /usr/bin/env python3
# -*- coding: utf-8 -*-

import struct
import os

f = open('test.txt', 'wb')
name = b'lily'
age = 17
sex = b'female'
job = b'teacher'

f.write(struct.pack('4si6s7s', name, age, sex, job))
f.flush()
f.close()

f = open('test.txt', 'rb')
print(struct.unpack('4si6s7s', f.read(21)))
f.close()

quit()

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