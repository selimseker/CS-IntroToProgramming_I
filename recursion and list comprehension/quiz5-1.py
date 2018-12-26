import sys


def recursion_func(number, counter, actualnumber, minus_number):
    # Base case
    if number == minus_number+1:
        return None
    else:
        # Recursive case
        if counter == actualnumber:
            counter = -counter
        formula = (2 * abs(counter)) - 1
        outline = (" "*(int(((2 * actualnumber - 1) - formula)/2)) + ("*" * formula))
        print(outline)
        recursion_func(number-1, counter+1, actualnumber, minus_number)


try:
    number = int(sys.argv[1])
    if number == 0:
        exit()
except ValueError:
    print("Error: Argument is not an integer!", sys.argv[1])
    exit()
except IndexError:
    print("Error: Enter the integer as an command line argument")
    exit()
if number < 0:
    print("Argument must be positive integer")
    exit()
recursion_func(number, 1, number, -number)
