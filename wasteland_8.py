import re
import functools
import math


left_map = dict()
right_map = dict()


PATH = ""
with open("./wasteland_8.txt") as file:
    for i, line in enumerate(file):
        if i == 0:
            PATH = line.rstrip()
        else:
            match = re.search(r"(\w*) = \((\w*), (\w*)\)", line)
            if match is not None:
                start, left, right = match.groups((1, 2, 3))
                left_map[start] = left
                right_map[start] = right


curr_node = "AAA"


def find_num_steps(curr_node):
    num_steps = 0
    found_end = False
    while not found_end:
        for step in PATH:
            if curr_node[-1] == "Z":
                print(curr_node)
                found_end = True
            num_steps += 1
            if step == "L":
                curr_node = left_map[curr_node]
            elif step == "R":
                curr_node = right_map[curr_node]
            else:
                assert False
    return num_steps

def find_loop_length(curr_node):
    start_node = curr_node
    num_steps = 0
    while num_steps == 0 or start_node != curr_node:
        for step in PATH:
            num_steps += 1
            if step == "L":
                curr_node = left_map[curr_node]
            elif step == "R":
                curr_node = right_map[curr_node]
            else:
                assert False
    return num_steps
    


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


start_nodes = [n for n in left_map if n[-1] == "A"]
num_steps = [find_num_steps(n) for n in start_nodes]

total_num_steps = functools.reduce(lcm, num_steps)
