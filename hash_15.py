def hash_string(s: str) -> int:
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val %= 256
    return val


with open("./hash_15.txt") as f:
    line = f.readline()

words = line.split(",")
print(sum([hash_string(w) for w in words]))
