def read_lines(fname):
    with open(fname) as file:
        lines = [line.rstrip() for line in file]
    return lines
