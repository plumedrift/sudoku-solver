import numpy as np
# 607009301
# 020300506
# 000760040

# 093002000
# 200000007
# 000500620

# 050073000
# 308006050
# 902800703


# check if solution is filled
def isComplete(solution):
    for element in solution.flatten():
        if element == 0:
            return False
    return True


# Fill out potential maps based on starting board
def refillPotentials():
    for row in range(0, 9):
        for col in range(0, 9):
            if input_puzzle[row][col] > 0:
                clear(input_puzzle[row][col], row, col)


# clear the row in the same-value potential map
def clear(value, row, col):
    potential[value - 1][row] = np.zeros((1, 9))

    # clear the column in the same-value potential map
    for x in range(0, 9):
        potential[value - 1][x][col] = 0

    # clear the square in the same-value potential map
    clearSquare(potential[value - 1], row // 3, col // 3)

    # clear the same squares in other potential maps
    for x in range(0, 9):
        potential[x][row][col] = 0


# clear the mini-square in the same-value potential map
def clearSquare(potentialMap, megaRow, megaCol):
    for i in range(0, 3):
        for j in range(0, 3):
            potentialMap[megaRow * 3 + i][megaCol * 3 + j] = 0


# looks for a solution across all potential maps, returns true if found
def searchSolution():
    # search all potential rows/cols for a single '1', meaning there is a solution
    for map in range(0, 9):
        for index in range(0, 9):

            # found a solution in a row
            if np.sum(potential[map][index]) == 1:
                for col in range(0, 9):
                    if potential[map][index][col] == 1:
                        input_puzzle[index][col] = map + 1
                        clear(map + 1, index, col)

                        return True

            # found solution in a column
            if np.sum(potential[map], axis=0)[index] == 1:
                for row in range(0, 9):
                    if potential[map][row][index] == 1:
                        input_puzzle[row][index] = map + 1
                        clear(map + 1, row, index)

                        return True

        # found solution in a square
        if squareSolutionFound(map):
            return True

    return False


# checks all nine mini-squares across all potential maps for a solution, returns true after editing the solution matrix
def squareSolutionFound(map):
    for row in range(0, 3):
        for col in range(0, 3):
            target = potential[map][row * 3:row * 3 + 3, col * 3:col * 3 + 3]
            if np.sum(target) == 1:
                actualCoords = returnCoords(target, row, col)
                actualRow = actualCoords[0]
                actualCol = actualCoords[1]

                input_puzzle[actualRow][actualCol] = map + 1
                clear(map + 1, actualRow, actualCol)

                return True
    return False


# returns actual coordinates for where the solution is
def returnCoords(miniSquare, i, j):
    for row in range(0, 3):
        for col in range(0, 3):
            if miniSquare[row][col] == 1:
                return [3 * i + row, 3 * j + col]


def print_solution(solution):
    print()
    print()
    print("One solution is as follows:")
    print("===========================")
    print()

    for row in solution:
        for col in row:
            print(str(col) + ' ', end='')
        print()


potential = [np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9))]

input_puzzle = list()
for row in range(9):
    temp = list()

    submitted = input("Please enter one row of nine numbers, with no spaces, and hit enter:")

    while len(submitted) != 9:
        print("Entry is not nine numbers, please resubmit the last row:")
        submitted = input()

    for char in submitted:
        temp.append(int(char))

    input_puzzle.append(temp)

input_puzzle = np.array(input_puzzle)

while not isComplete(input_puzzle):
    refillPotentials()
    if not searchSolution():
        print("Didn't find a solution")
        break

if isComplete(input_puzzle):
    print_solution(input_puzzle)
