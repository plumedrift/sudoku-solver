import numpy as np

solution2 = np.array([[0, 0, 4, 0, 0, 6, 0, 7, 9],
                      [0, 0, 0, 0, 0, 0, 6, 0, 2],
                      [0, 5, 6, 0, 9, 2, 3, 0, 0],

                      [0, 7, 8, 0, 6, 1, 0, 3, 0],
                      [5, 0, 9, 0, 0, 0, 4, 0, 6],
                      [0, 2, 0, 5, 4, 0, 8, 9, 0],

                      [0, 0, 7, 4, 1, 0, 9, 2, 0],
                      [1, 0, 5, 0, 0, 0, 0, 0, 0],
                      [8, 4, 0, 6, 0, 0, 1, 0, 0]])

solution = np.array([[6, 0, 7, 0, 0, 9, 3, 0, 1],
                     [0, 2, 0, 3, 0, 0, 5, 0, 6],
                     [0, 0, 0, 7, 6, 0, 0, 4, 0],

                     [0, 9, 3, 0, 0, 2, 0, 0, 0],
                     [2, 0, 0, 0, 0, 0, 0, 0, 7],
                     [0, 0, 0, 5, 0, 0, 6, 2, 0],

                     [0, 5, 0, 0, 7, 3, 0, 0, 0],
                     [3, 0, 8, 0, 0, 6, 0, 5, 0],
                     [9, 0, 2, 8, 0, 0, 7, 0, 3]])

potential = [np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9)),
             np.ones((9, 9))]


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
            if solution[row][col] > 0:
                clear(solution[row][col], row, col)


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
                        solution[index][col] = map + 1
                        clear(map + 1, index, col)

                        return True

            # found solution in a column
            if np.sum(potential[map], axis=0)[index] == 1:
                for row in range(0, 9):
                    if potential[map][row][index] == 1:
                        solution[row][index] = map + 1
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

                solution[actualRow][actualCol] = map + 1
                clear(map + 1, actualRow, actualCol)

                return True
    return False

# returns actual coordinates for where the solution is
def returnCoords(miniSquare, i, j):
    for row in range(0, 3):
        for col in range(0, 3):
            if miniSquare[row][col] == 1:
                return [3 * i + row, 3 * j + col]


while not isComplete(solution):
    refillPotentials()
    if not searchSolution():
        print("Didn't find a solution")
        break

if isComplete(solution):
    print("We found a solution")

# todo
# - upload to github
# - intake puzzle easier/quicker
# - print solution
#
