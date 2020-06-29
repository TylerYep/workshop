import re
import sys


def regex(filename, regexp):
    with open(filename, "r") as f:
        matches = []
        regex = re.compile(regexp)
        for line in f:
            if regex.search(line):
                matches.append(line[:-1])
        for m in matches:
            print(m)


def regex_str(line, regexp):
    matches = []
    regex = re.compile(regexp)
    matches.append(regex.findall(line))
    for m in matches:
        print(m)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2:
        regex(args[0], args[1])
    else:
        line = "1 5 71 13"
        regex_str(line, args[0])
