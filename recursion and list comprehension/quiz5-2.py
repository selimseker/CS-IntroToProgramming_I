import sys


try:
    number = int(sys.argv[1])
except ValueError:
    print("Error: Argument is not an integer!", sys.argv[1])
    exit()
except IndexError:
    print("Error: Enter the integer as an command line argument")
    exit()
if number < 0:
    print("Argument must be positive integer")
    exit()


def blank_star_number(number, actualnumber, char_type):
    if char_type == " ":
        return int((((2 * actualnumber) - 1) - ((2 * number) - 1)) / 2)
    else:
        return int((2 * number) - 1)


# List comprehension part
line = [(" " * blank_star_number(a, number, " "), "*" * blank_star_number(a, number, "*")) for a in range(0, number+1)]
for x in range(1, len(line)):
    print("".join(line[x]))
for x in range(len(line)-2, 0, -1):
    print("".join(line[x]))
