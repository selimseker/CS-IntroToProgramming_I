import sys

halls = dict()

'''
    halls dictionary ->  { "key = hall_name" :  ["rowsxcolumns",
                                                [["ticket_owner", "ticket_type", ["seats"]]*selling process],
                                                [[student seats],[full seats]]}

'''

# This function reads the command line argument
def scan_arg():
    try:
        if len(sys.argv) < 2:
            write_to_out_file("Please enter the input file name")
            command_lines = None
            exit()
        elif len(sys.argv) > 2:
            write_to_out_file("Please enter only the input file")
            command_lines = None
            exit()
        else:
            input_file = sys.argv[1]
            command_lines = open(input_file, 'r')
            return command_lines
    except FileNotFoundError:
        write_to_out_file(("Error: There is no .txt file named "+input_file))
        exit()


# This function execute the commands in the input file line by line
def execute_commands(halls, command_lines):

    for line in command_lines:
        words_of_line = line.split()
        if len(words_of_line) != 0:
            if words_of_line[0] == "CREATEHALL":
                halls = createhall(words_of_line, halls)
            elif words_of_line[0] == "SELLTICKET":
                halls = sellticket(words_of_line, halls)
            elif words_of_line[0] == "CANCELTICKET":
                halls = cancelticket(words_of_line, halls)
            elif words_of_line[0] == "BALANCE":
                balance(words_of_line, halls)
            elif words_of_line[0] == "SHOWHALL":
                showhall(words_of_line, halls)
            else:
                write_to_out_file("Error: Invalid command")


def createhall(args, halls):

    if len(args) < 3:
        output = "Error: Not enough parameters for creating a hall!"
        write_to_out_file(output)
        return halls

    if len(args) > 3:
        output = "Error: Too much parameters for creating a hall!"
        write_to_out_file(output)
        return halls

    if args[1] in halls:
        output = "Warning: Cannot create the hall for the second time. The cinema has already " + args[1]
        write_to_out_file(output)
        return halls

    if len(args[2].split("x")) != 2:
        output = "Syntax Error: Second argument of the CREATEHALLL command must be like number_of_rowsxnumber_of_columns"
        write_to_out_file(output)
        return halls

    if int(args[2].split("x")[0]) > 26:
        output = "Error: Number of rows must be less then 27"
        write_to_out_file(output)
        return halls

    try:
        seat_numb = int(args[2].split("x")[0]) * int(args[2].split("x")[1])
    except ValueError:
        write_to_out_file(("Syntax Error: Wrong argument for row and column number "+args[2]))
        return halls
    halls[args[1]] = [args[2], [], [[], []]]
    output = "Hall '" + args[1] + "' having " + str(seat_numb) + " seats has been created"
    write_to_out_file(output)
    return halls


def sellticket(args, halls):

    ticket_owner = args[1]
    ticket_type = args[2]
    hall_name = args[3]
    seats_for_sale = [i for i in args[4:]]
    saled_seats = []

    # Checking the existence of hall
    if hall_name not in halls:
        write_to_out_file(("Warning: There is no hall named " + hall_name))
        return halls

    # Checking the arguments
    if len(args) < 5:
        output = "Error: Not enough parameters for buy a ticket!"
        write_to_out_file(output)
        return halls

    # Checking the ticket type
    ticket_types = ["student", "full"]
    if args[2] not in ticket_types:
        write_to_out_file("Error: Wrong ticket type")
        return halls

    # Checking the rows and columns
    lis = []
    lis.extend(seats_for_sale)
    for a in seats_for_sale:

        error_type = check_rowsxcolumns(halls, hall_name, a)
        if error_type == "column error":
            output = "Error: The hall "+hall_name+" has less column than the specified index "+a+"!"
            write_to_out_file(output)
            lis.remove(a)
        elif error_type == "row error":
            output = "Error: The hall "+hall_name+" has less raw than the specified index "+a+"!"
            write_to_out_file(output)
            lis.remove(a)
        elif error_type == "initial error":
            output = "Error: Initial seat is wrong at "+a+"!"
            write_to_out_file(output)
            lis.remove(a)
        elif error_type == "wrong seat":
            output = "Error: Wrong seat "+a+"!"
            write_to_out_file(output)
            lis.remove(a)
        seats_for_sale = []
        seats_for_sale.extend(lis)

    # Checking the seats that already sold
    for seat in seats_for_sale:
        if check_seat_in_hall(halls, hall_name, seat, saled_seats) is False:
            if "-" in seat:
                output = "Warning: The seats "+seat+" cannot be sold to "+ticket_owner+" due some of them have already been sold"
            else:
                output = "Warning: The seat "+seat+" cannot be sold to "+ticket_owner+" since it was already sold!"
        else:
            output = "Success: "+ticket_owner+" has bought "+seat+" at "+hall_name+""
            if "-" in seat:
                row_name = seat.split("-")[0][0]
                initial_seat = seat.split("-")[0][1:]
                final_seat = seat.split("-")[1]
                for a in range(int(initial_seat), (int(final_seat))):
                    seat = row_name + str(a)
                    saled_seats.append(seat)
            else:
                saled_seats.append(seat)

        write_to_out_file(output)

    # If there is at least one success selling then add them to halls data
    if len(saled_seats) != 0:
        halls[hall_name][1].append([ticket_owner, ticket_type, saled_seats])
        if ticket_type == "student":
            halls[hall_name][2][0].extend(saled_seats)
        else:
            halls[hall_name][2][1].extend(saled_seats)

    return halls


def cancelticket(args, halls):
    hall_name = args[1]
    seats_for_cancel = [i for i in args[2:]]

    # Checking the existence of hall
    if hall_name not in halls:
        write_to_out_file(("Warning: There is no hall named " + hall_name))
        return halls

    # Checking the arguments
    if len(args) < 3:
        write_to_out_file("Not enough parameters for cancel a ticket!")
        return halls

    # Checking the rows and columns
    lis = []
    lis.extend(seats_for_cancel)
    for a in seats_for_cancel:
        error_type = check_rowsxcolumns(halls, hall_name, a)
        if error_type == "column error":
            output = "Error: The hall " + hall_name + " has less column than the specified index " + a + "!"
            write_to_out_file(output)
            lis.remove(a)
        elif error_type == "row error":
            output = "Error: The hall " + hall_name + " has less raw than the specified index " + a + "!"
            write_to_out_file(output)
            lis.remove(a)
        elif error_type == "initial error":
            output = "Error: Initial seat is wrong at " + a + "!"
            write_to_out_file(output)
            lis.remove(a)
        elif error_type == "wrong seat":
            output = "Error: Wrong seat "+a+"!"
            write_to_out_file(output)
            lis.remove(a)
        seats_for_cancel = []
        seats_for_cancel.extend(lis)

    # Checking the seats that cant cancel
    for seat in seats_for_cancel:

        if "-" in seat:
            row_name = seat.split("-")[0][0]
            initial_seat = seat.split("-")[0][1:]
            final_seat = seat.split("-")[1]
            cancel_counter = 0
            noncancel_counter = 0
            output = []
            for a in range(int(initial_seat), (int(final_seat))):
                one_seat = row_name + str(a)
                if check_seat_in_hall(halls, hall_name, one_seat, None) is False:
                    output.append("Success: The seat " + one_seat + " at " + hall_name + " has been canceled and now ready to sell again")
                    cancel_counter += 1
                    number_of_persons = len(halls[hall_name][1])
                    for x in range(number_of_persons):
                        if one_seat in halls[hall_name][1][x][2]:
                            halls[hall_name][1][x][2].remove(one_seat)
                            if len(halls[hall_name][1][x][2]) == 0:
                                del halls[hall_name][1][x]
                                break

                    try:
                        halls[hall_name][2][0].remove(one_seat)
                    except ValueError:
                        halls[hall_name][2][1].remove(one_seat)

                else:
                    output.append("Error: The seat " + one_seat + " at " + hall_name + " has already been free! Nothing to cancel")
                    noncancel_counter += 1

            if cancel_counter == (int(final_seat) - int(initial_seat)):
                output = "Success: The seat "+seat+" at "+hall_name+" has been canceled and now ready to sell again"
                write_to_out_file(output)
            elif noncancel_counter == (int(final_seat) - int(initial_seat)):
                output = "Error: The seat " + seat + " at " + hall_name + " has already been free! Nothing to cancel"
                write_to_out_file(output)
            else:
                write_to_out_file("\n".join(output))
        else:
            if check_seat_in_hall(halls, hall_name, seat, None) is False:
                output = "Success: The seat " + seat + " at " + hall_name + " has been canceled and now ready to sell again"
                length_of_persons = len(halls[hall_name][1])

                for x in range(length_of_persons):
                    if seat in halls[hall_name][1][x][2]:
                        halls[hall_name][1][x][2].remove(seat)

                        if len(halls[hall_name][1][x][2]) == 0:
                            del halls[hall_name][1][x]
                            break
                try:
                    halls[hall_name][2][0].remove(seat)
                except ValueError:
                    halls[hall_name][2][1].remove(seat)
                write_to_out_file(output)

            else:
                output = "Error: The seat " + seat + " at " + hall_name + " has already been free! Nothing to cancel"
                write_to_out_file(output)

    return halls


def balance(args, halls):

    # Checking the arguments
    if len(args) < 2:
        write_to_out_file("Not enough parameters!")

    # Checking the existence of hall
    for hall in args[1:]:
        if hall not in halls:
            output = ("Warning: There is no hall named " + hall)
        else:
            sum_of_std = 5 * len(halls[hall][2][0])
            sum_of_full = 10 * len(halls[hall][2][1])
            overall = sum_of_full + sum_of_std
            output = """Hall report of '"""+hall+"""'
-------------------------
Sum of students = """+str(sum_of_std)+""", Sum of full fares = """+str(sum_of_full)+""", Overall = """+str(overall)+""""""
        write_to_out_file(output)


def showhall(args, halls):
    # Checking the arguments
    if len(args) < 2:
        write_to_out_file("Not enough parameters!")

    ascii_uppercase = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for hall in args[1:]:

        if hall not in halls:
            write_to_out_file(("Warning: There is no hall named " + args[1]))
        else:
            row = int(halls[hall][0].split("x")[0])
            column = int(halls[hall][0].split("x")[1])
            write_to_out_file("Printing hall layout of "+hall)
            for i in range(row, -1, -1):
                line = []
                letter = ascii_uppercase[i]
                for j in range(column, -1, -1):
                    if i == 0:

                        if j-1 >= 10:
                            line.append(str(j-1))
                        elif j == 0:
                            line.append(" ")
                        else:
                            line.append(" " + str(j-1))

                    elif j == 0:
                        line.append(letter)

                    else:
                        seat = letter + str(j-1)
                        if seat in halls[hall][2][0]:
                            line.append(" S")
                        elif seat in halls[hall][2][1]:
                            line.append(" F")
                        else:
                            line.append(" X")
                reversedline = list(reversed(line))
                write_to_out_file((reversedline[0] + " ".join(reversedline[1:])))


# This function output the results of the operations to both console and a text file.
def write_to_out_file(out_line):
    out = open("out.txt", "a")
    out.write(out_line + "\n")
    print(out_line)
    out.close()


def check_rowsxcolumns(halls, hall_name, seat):
    ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    halls_column = int(halls[hall_name][0].split("x")[1])
    halls_row = int(halls[hall_name][0].split("x")[0])

    try:
        if "-" in seat:
            int(seat.split("-")[0][1:])
            int(seat.split("-")[1])
        else:
            int(seat[1:])
    except ValueError:
        return "wrong seat"

    if seat[0] not in ascii_uppercase:
        return "wrong seat"

    if "-" in seat:
        row = ascii_uppercase.index(seat.split("-")[0][0]) + 1
        column = int(seat.split("-")[1])
        column_initial = int(seat.split("-")[0][1:])
        if column_initial < 0 or column_initial > halls_column:
            return "initial error"
        elif column > halls_column:
            return "column error"
    else:
        row = ascii_uppercase.index(seat[0])
        column = int(seat[1])
        if column > (halls_column - 1):
            return "column error"

    if row > halls_row:
        return "row error"
    else:
        return "correct"


def check_seat_in_hall(halls, hall_name, seat, executed_seats):
    if "-" not in seat:
        if executed_seats is None:
            if seat in halls[hall_name][2][0] or seat in halls[hall_name][2][1]:
                return False
        else:
            if seat in halls[hall_name][2][0] or seat in halls[hall_name][2][1] or seat in executed_seats:
                return False

    else:
        row_name = seat.split("-")[0][0]
        initial_seat = seat.split("-")[0][1:]
        final_seat = seat.split("-")[1]
        for a in range(int(initial_seat), (int(final_seat))):
            seat = row_name + str(a)
            return check_seat_in_hall(halls, hall_name, seat, executed_seats)


command_lines = scan_arg()
open('out.txt', 'w').close()
execute_commands(halls, command_lines)
