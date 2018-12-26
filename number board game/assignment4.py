import sys


def scan_arg():
    try:
        input_file = sys.argv[1]
        try:
            file = open(input_file, "r")
            return file
        except FileNotFoundError:
            print("Error: There is no file named:", input_file)
            exit()
    except IndexError:
        print("Error: Enter the input file as an argument")
        exit()


def create_the_game_schema(file):
    game_schema = []
    for line in file:
        game_schema.append([line[numb] for numb in range(len(line) - 1) if line[numb] != " "])

    # If there are blank lines in input then remove them
    empty_line = []
    for i in range(len(game_schema)):
        if len(game_schema[i]) == 0:
            empty_line.append(i)
    for i in reversed(empty_line):
        del game_schema[i]

    for j in range(len(game_schema)):
        game_schema[j] = [" "] + game_schema[j]
        game_schema[j].append(" ")
    game_schema = [[" " for x in range(len(game_schema[0]))]] + game_schema
    game_schema.append([" " for x in range(len(game_schema[0]))])

    return game_schema


def game_turn(game_schema, score):
    print("\nYour score is:", score, "\n")
    try:
        row_column = (input("Please enter a row and column number: ").split(" "))
        row, column = int(row_column[0]), int(row_column[1])
        if len(row_column) > 2:
            print("Warning: Enter the row and column")
            return game_schema, False, score
    except ValueError:
        print("Warning: Enter the row and column as an integer!")
        return game_schema, False, score

    if row > len(game_schema)-2:
        print("Warning: Row out of bound!")
        return game_schema, False, score
    elif column > len(game_schema[row]):
        print("Warning: Column out of bound!")
        return game_schema, False, score

    if game_schema[row][column] != " ":
        number = game_schema[row][column]
        game_schema[row][column] = " "
        game_schema, counter = check_the_neighbors(number, row, column, game_schema, 1)
        if counter == 1:
            game_schema[row][column] = number
        else:
            score += int(number) * fibonacci_score(counter)
        game_schema, game_over = refresh_schema(game_schema)
        if game_over is True:
            game_schema = clean_the_empty(game_schema)
            return game_schema, True, score
        game_schema = clean_the_empty(game_schema)

    else:
        print("Please enter a correct size!")
    return game_schema, check_game_over(game_schema), score


def check_the_neighbors(number, row, column, game_schema, counter):
    # up
    if number == game_schema[row - 1][column]:
        game_schema[row - 1][column] = " "
        counter += 1
        game_schema, counter = check_the_neighbors(number, row - 1, column, game_schema, counter)

    # left
    if number == game_schema[row][column - 1]:
        game_schema[row][column - 1] = " "
        counter += 1
        game_schema, counter = check_the_neighbors(number, row, column - 1, game_schema, counter)

    # right
    if number == game_schema[row][column + 1]:
        game_schema[row][column + 1] = " "
        counter += 1
        game_schema, counter = check_the_neighbors(number, row, column + 1, game_schema, counter)

    # bottom
    if number == game_schema[row + 1][column]:
        game_schema[row + 1][column] = " "
        counter += 1
        game_schema, counter = check_the_neighbors(number, row + 1, column, game_schema, counter)
    return game_schema, counter


def refresh_schema(game_schema):
    for i in game_schema:
        for j in i:
            if j == " ":
                empty = True
            else:
                empty = False
                break
        if empty is False:
            break

    # If all cells are empty then no need for refresh because game is already over
    if empty is True:
        return game_schema, True

    else:

        # If there is just one row then no need for refresh
        if len(game_schema) == 3:
            return game_schema, False

        for i in range(1, len(game_schema) - 2):
            for j in range(1, len(game_schema[i]) - 1):
                if game_schema[i][j] != " " and game_schema[i+1][j] == " ":
                    done_schema = False
                    break
                else:
                    done_schema = True
            if done_schema is False:
                break

        if done_schema is True:
            return game_schema, False
        else:
            for m in range(1, len(game_schema) - 1):
                for n in range(1, len(game_schema[m]) - 1):
                    if game_schema[m][n] == " " and game_schema[m-1][n] != " ":
                        game_schema[m][n] = game_schema[m-1][n]
                        game_schema[m-1][n] = " "
            return refresh_schema(game_schema)


def clean_the_empty(game_schema):
    # clean row
    empty_rows = []
    for i in range(1, len(game_schema) - 1):
        for j in game_schema[i]:
            if j != " ":
                empty = False
                break
            else:
                empty = True
        if empty is True:
            empty_rows.append(i)
    for row in reversed(empty_rows):
        del game_schema[row]

    # clean column
    empty_columns = []
    for j in range(1, len(game_schema[1]) - 1):
        for i in range(1, len(game_schema) - 1):
            if game_schema[i][j] != " ":
                empty = False
                break
            else:
                empty = True
        if empty is True:
            empty_columns.append(j)
    for column in reversed(empty_columns):
        for i in range(1, len(game_schema) - 1):
            del game_schema[i][column]

    return game_schema


def check_game_over(game_schema):
    lis = []
    for i in range(len(game_schema)):
        lis.append([])
        for j in game_schema[i]:
            lis[i].append(j)
    for i in range(1, len(game_schema)-1):
        for j in range(1, len(game_schema[i])-1):
            if game_schema[i][j] != " ":
                if check_the_neighbors(game_schema[i][j], i, j, lis, 1)[0] != game_schema:
                    return False
    return True


def show_game_schema(game_schema):
    print("")
    for i in range(1, len(game_schema) - 1):
        print(" ".join(game_schema[i][1:]))


def fibonacci_score(counter):
    if counter == 1 or counter == 2:
        return 1
    else:
        return fibonacci_score(counter-1) + fibonacci_score(counter-2)


def main():
    game_schema = create_the_game_schema(scan_arg())
    score = 0
    game_over = False
    while game_over is False:
        show_game_schema(game_schema)
        game_schema, game_over, score = game_turn(game_schema, score)
    show_game_schema(game_schema)
    print("\nYour score:", score, "\n")
    print("Game over")


if __name__ == '__main__':
    main()
