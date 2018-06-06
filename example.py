""""
What is Pythonic code?

The idea of writing idiomatic code that is most aligned with the language
features and ideals is a key concept in Pythons.

We call this idiomatic code Pythonic.
""""


################################# stringification #################################

name = 'Michael'
age = 43

# Create the string "Hi, I'm Michael and I'm 43 years old."

# crash: print("Hi, I'm " + name + " and I'm " + age + " years old.")

# works, but not pythonic
print("Hi, I'm " + name + " and I'm " + str(age) + " years old.")


# a little pythonic
print("Hi, I'm %s and I'm %d years old." % (name, age))

# pythonic
print("Hi, I'm {} and I'm {} years old.".format(name, age))
print("Hi, I'm {1} years old and my name is {0}, yeah {1}.".format(name, age))

data = {'day': 'Saturday', 'office': 'Home office', 'other': 'UNUSED'}
# print: On Saturday I was working in my Home office!
print("On {day} I was working in my {office}!".format(**data))

# In Python 3.6
print(f"Hi, I'm {name} and I'm {age+1} years old.")
# print: Hi, I'm Michael and I'm 44 years old.


################################# merging dictionaries #################################

# Overview:
# Often we have multiple dictionaries and want to combine
# them. For example, in Pyramid, we have separate dictionaries
# that hold query string data, route data, and POST data. Merging
# these makes access form data easier. That's just one example.

route = {'id': 271, 'title': 'Fast apps'}
query = {'id': 1, 'render_fast': True}
post = {'email': 'j@j.com', 'name': 'Jeff'}

print("Individual dictionaries: ")
print("route: {}".format(route))
print("query: {}".format(query))
print("post:  {}".format(post))

# Non-pythonic procedural way
m1 = {}
for k in query:
    m1[k] = query[k]
for k in post:
    m1[k] = post[k]
for k in route:
    m1[k] = route[k]

# Classic pythonic way:
m2 = query.copy()
m2.update(post)
m2.update(route)

# Via dictionary comprehensions:
m3 = {k: v for d in [query, post, route] for k, v in d.items()}

# Python 3.5+ pythonic way, warning crashes on Python <= 3.4:
m4 = {**query, **post, **route}

print(m1)
print(m2)
print(m3)
print(m4)

print("Are the same? " + 'yes' if m1 == m2 and m2 == m3 and m3 == m4 else 'no')


################################# safer calls with keywords #################################

def connect_v1(user, server, replicate, use_ssl):
    print("Connect v1, called with: ")
    print(f"User = {user}")
    print(f"Server = {server}")
    print(f"Replicate = {replicate}")
    print(f"Use SSL = {use_ssl}")
    print()


def connect_v2(*, user, server, replicate, use_ssl):
    print("Connect v2, called with: ")
    print(f"User = {user}")
    print(f"Server = {server}")
    print(f"Replicate = {replicate}")
    print(f"Use SSL = {use_ssl}")
    print()


print("******************* V1 *******************")
print("*")
connect_v1('mkennedy', 'db_svr', True, False)
connect_v1(user='mkennedy', server='db_svr', replicate=True, use_ssl=False)

print()
print("******************* V2 *******************")
print("*")
connect_v2(user='mkennedy', server='db_svr', replicate=True, use_ssl=False)
connect_v2('mkennedy', 'db_svr', True, False)

print("done")


################################# yield and generators #################################

# Fibonacci numbers:
# 1, 1, 2, 3, 5, 8, 13, 21, ...


def classic_fibonacci(limit):
    nums = []
    current, nxt = 0, 1

    while current < limit:
        current, nxt = nxt, nxt + current
        nums.append(current)

    return nums


# can we do better?
def generator_fibonacci():
    current, nxt = 0, 1

    while True:
        current, nxt = nxt, nxt + current
        yield current


# generator are composible:
def even_generator(numbers):
    for n in numbers:
        if n % 2 == 0:
            yield n


# consume both generators as a pipeline here
def even_fib():
    for n in even_generator(generator_fibonacci()):
        yield n


if __name__ == '__main__':

    print("Classic")
    for m in classic_fibonacci(100):
        print(m, end=', ')
    print()

    print("generator")
    for m in generator_fibonacci():
        print(m, end=', ')
        if m > 100:
            break
    print()

    print("composed")
    for m in even_fib():
        print(m, end=', ')
        if m > 1000000:
            break
    print()


################################# recursive generators all the way down #################################


import os


def main():
    root_dir = '/Users/mkennedy/github/talk-python/courses/jumpstart/jumpstart-demos/transcripts'

    files = get_files(root_dir)
    print("Found these files")
    for f in files:
        print(f)
    print('done')


def get_files(folder):
    for item in os.listdir(folder):

        full_item = os.path.join(folder, item)
        # print(full_item)
        if os.path.isfile(full_item):
            yield full_item
        elif os.path.isdir(full_item):
            # for f in get_files(full_item):
            #     yield f
            yield from get_files(full_item)


################################# counting iterables #################################

import collections
import uuid

Measurement = collections.namedtuple('Measurement', 'id x y value')

measurements = [
    Measurement(str(uuid.uuid4()), 1, 1, 72),
    Measurement(str(uuid.uuid4()), 2, 1, 40),
    Measurement(str(uuid.uuid4()), 3, 1, 11),
    Measurement(str(uuid.uuid4()), 2, 1, 90),
    Measurement(str(uuid.uuid4()), 2, 2, 60),
    Measurement(str(uuid.uuid4()), 2, 3, 73),
    Measurement(str(uuid.uuid4()), 3, 1, 40),
    Measurement(str(uuid.uuid4()), 3, 2, 44),
    Measurement(str(uuid.uuid4()), 3, 3, 90)
]

# generator expression
high_values = (
    m.value
    for m in measurements
    if m.value >= 70
)

# crash! no len()
# print(len(high_values))

# could use a list, but expensive!
# lst = list(high_values)
# print(len(lst))

# pythonic counting!
count = sum(1 for _ in high_values)
print(count)


################################# slicing infinity #################################

import itertools


def list_fibonacci(limit):
    nums = []
    current, nxt = 0, 1

    for _ in range(0, limit):
        current, nxt = nxt, nxt + current
        nums.append(current)

    return nums


def generator_fibonacci():
    current, nxt = 0, 1

    while True:
        current, nxt = nxt, nxt + current
        yield current


print(list_fibonacci(100)[:5])
# ERROR: print(generator_fibonacci()[:5])

print(list(itertools.islice(generator_fibonacci(), 5)))


################################# slots for improved memory usage #################################


# Overview:
# Custom types store their data in individualized, dynamic dictionaries
# via self.__dict__. Using __slots__ to limit available attribute names
# and move the name/key storage outside the instance to a type level
# can significantly improve memory usage. See EOF for perf numbers.
#

import collections
import datetime

ImmutableThingTuple = collections.namedtuple("ImmutableThingTuple", "a b c d")


class MutableThing:
    def __init__(self, a, b, c, d):
        self.variable_a = a
        self.variable_b = b
        self.variable_c = c
        self.variable_d = d


class ImmutableThing:
    __slots__ = ['a', 'b', 'c', 'd']

    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d


print("Uncomment just 1 of these 4 loops below")
print("after the program pauses on input, check the process memory")

count = 1000000
data = []

t0 = datetime.datetime.now()

# Loop 1: Tuples
print("tuple")
for n in range(count):
    data.append((1 + n, 2 + n, 3 + n, 4 + n))

# # Loop 2: Named tuple
# print("named tuple")
# for n in range(count):
#     data.append(ImmutableThingTuple(1 + n, 2 + n, 3 + n, 4 + n))
#
# # Loop 3: Standard mutable class
# print("standard class")
# for n in range(count):
#     data.append(MutableThing(1 + n, 2 + n, 3 + n, 4 + n))
#
# # Loop 4: Slot based immutable class
# print("slot based class")
# for n in range(count):
#   data.append(ImmutableThing(1 + n, 2 + n, 3 + n, 4 + n))

t1 = datetime.datetime.now()

input("Finished, waiting... done in {:,} s".format((t1 - t0).total_seconds()))

# Sample output on OS X + Python 3
# Hardware: Macbook Pro 2013 edition

# straight tuple:  207 MB, 0.528455 s
# named tuple:     215 MB, 1.519358 s
# class (dynamic): 370 MB, 1.680248 s
# slot class:      120 MB, 1.438989 s

# And on Windows 10 + Python 3, same hardware (memory is "working set")
# tuple: 153 MB
# named: 153 MB
# class: 248 MB
# slots: 145 MB

# Interesting real-world story of benefits of slots:
# http://tech.oyster.com/save-ram-with-python-slots/
