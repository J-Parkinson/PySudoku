from pygame import sprite, draw, display, font, key, event, quit, mouse, Color, init, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_BACKSPACE, K_DELETE, K_SPACE
from os import environ, path
from pygame.locals import *
from math import ceil, floor
from random import sample
from copy import deepcopy
from time import time
from tkinter import *
from tkinter import filedialog, messagebox, ttk, colorchooser, simpledialog
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk
from io import BytesIO
from subprocess import Popen

global GlobIsGame
GlobIsGame = False

global GlobNew
GlobNew = False

#CREATE SUDOKU PAGE

def CreateSudokuPage(noSudokus, perPage, difficulty, filename, logo="", importGrid=[], gradeSet=[]):


    def CreateSudokus(perPage, sudokusLeft):
        pdf.rect(75, 760, 800, 36, fill=1)#Creates black bar at top
        pdf.setFillColorRGB(255, 255, 255)
        pdf.circle(75, 778, 35, stroke=1, fill=1)#Creates white circles
        if logo != "":
            pdf.drawInlineImage(logo, 51, 752, width=48, height=48)#Logo
        pdf.circle(75, 778, 35, stroke=1, fill=0)
        pdf.drawString(120, 774, "Sudoku Puzzles")
        pdf.setFillColorRGB(0,0,0)

        if perPage == 1:#Data to store different templates
            cellSize = 40
            xStart = 140
            yStart = 550
            spacing = 40
            fontSize = 20
        elif perPage == 2:#change
            cellSize = 30
            xStart = 175
            yStart = 675
            spacing = 50
            fontSize = 14
        elif perPage == 3:#change
            cellSize = 20
            xStart = 210
            yStart = 700
            spacing = 40
            fontSize = 10
        elif perPage == 4:
            cellSize = 25
            xStart = 200
            yStart = 675
            spacing = 50
            fontSize = 14
        elif perPage == 6:
            cellSize = 20
            xStart = 225
            yStart = 700
            spacing = 40
            fontSize = 10
        else:
            return

        pdf.setFontSize(fontSize)
        if perPage <= 3:#One column
            for noSudoku in range(min(perPage, sudokusLeft)):#Minimum allows pages to not be full when filling
                if importGrid == []:
                    sudoku, answer, grade, wordGrade, cells = SudokuSolveGen("generate", difficulty=difficulty) # 25 levels of difficulty
                else:
                    sudoku = importGrid
                    grade, wordGrade = gradeSet[0], gradeSet[1]
                for row in range(len(sudoku)):
                    for cell in range(len(sudoku[row])):
                        if sudoku[row][cell] != 0:
                            #pdf.drawString(100 + (cell * 20), 700 - (20 * row) - (220 * noSudoku), str(sudoku[row][cell]))
                            pdf.drawString(xStart + (cell * cellSize), yStart - (row * cellSize) - (((9 * cellSize) + spacing) * noSudoku), str(sudoku[row][cell]))
                    #pdf.line(93 + (row * 20), 717 - (220 * noSudoku), 93 + (row * 20), 537 - (220 * noSudoku))
                    if row % 3 == 0:
                        if perPage == 3:#Different lines for larger squares
                            pdf.setLineWidth(2)
                        else:
                            pdf.setLineWidth(3)
                    else:
                        pdf.setLineWidth(1)
                    pdf.line(xStart - (2 * cellSize / 5) + (row * cellSize), yStart + cellSize - (fontSize / 4) - (((9 * cellSize) + spacing) * noSudoku), xStart - (2 * cellSize / 5) + (row * cellSize), yStart + cellSize - (fontSize / 4) - (9 * cellSize) - (((9 * cellSize) + spacing) * noSudoku))
                    #pdf.line(93, 717 - (row * 20) - (220 * noSudoku), 273, 717 - (row * 20) - (220 * noSudoku))
                    pdf.line(xStart - (2 * cellSize / 5), yStart + cellSize - (fontSize / 4) - (row * cellSize) - (((9 * cellSize) + spacing) * noSudoku), xStart - (2 * cellSize / 5) + (9 * cellSize), yStart + cellSize - (fontSize / 4) - (row * cellSize) - (((9 * cellSize) + spacing) * noSudoku))
                pdf.setLineWidth(3)
                #pdf.line(273, 717 - (220 * noSudoku), 273, 537 - (220 * noSudoku))
                pdf.line(xStart - (2 * cellSize / 5) + (9 * cellSize), yStart + cellSize - (fontSize / 4) - (((9 * cellSize) + spacing) * noSudoku), xStart - (2 * cellSize / 5) + (9 * cellSize), yStart + cellSize - (fontSize / 4) - (((9 * cellSize) + spacing) * noSudoku) - (9 * cellSize))
                #pdf.line(93, 537 - (220 * noSudoku), 273, 537 - (220 * noSudoku))
                pdf.line(xStart - (2 * cellSize / 5), yStart + cellSize - (fontSize / 4) - (((9 * cellSize) + spacing) * noSudoku) - (9 * cellSize), xStart - (2 * cellSize / 5) + (9 * cellSize), yStart + cellSize - (fontSize / 4) - (((9 * cellSize) + spacing) * noSudoku) - (9 * cellSize))
                #pdf.drawString(100, 725 - (220 * noSudoku), "Grade: " + wordGrade + " (" + str(grade) + ")")
                pdf.drawString(xStart, yStart + cellSize - (((9 * cellSize) + spacing) * noSudoku), "Grade: " + wordGrade + " (" + str(grade) + ")")
            pdf.showPage()
        else:
            for noSudoku in range(min(perPage, sudokusLeft)):
                sudoku, answer, grade, wordGrade, cells = SudokuSolveGen("generate", difficulty=difficulty) # 25 levels of difficulty
                for row in range(len(sudoku)):
                    for cell in range(len(sudoku[row])):
                        if sudoku[row][cell] != 0:
                            #pdf.drawString(100 + (cell * 20), 700 - (20 * row) - (220 * noSudoku), str(sudoku[row][cell]))
                            pdf.drawString(xStart + (cell * cellSize) + ((9 * cellSize + (spacing / 2)) * (-1)**(noSudoku + 1) * 0.5), yStart - (row * cellSize) - (((9 * cellSize) + spacing) * floor(noSudoku / 2)), str(sudoku[row][cell]))
                    #pdf.line(93 + (row * 20), 717 - (220 * noSudoku), 93 + (row * 20), 537 - (220 * noSudoku))
                    if row % 3 == 0:
                        if perPage == 6:
                            pdf.setLineWidth(2)
                        else:
                            pdf.setLineWidth(3)
                    else:
                        pdf.setLineWidth(1)
                    pdf.line(xStart - (2 * cellSize / 5) + (row * cellSize) + ((9 * cellSize + (spacing / 2)) * (-1)**(noSudoku + 1) * 0.5), yStart + cellSize - (fontSize / 4) - (((9 * cellSize) + spacing) * floor(noSudoku / 2)), xStart - (2 * cellSize / 5) + (row * cellSize) + ((9 * cellSize + (spacing / 2)) * (-1)**(noSudoku + 1) * 0.5), yStart + cellSize - (fontSize / 4) - (9 * cellSize) - (((9 * cellSize) + spacing) * floor(noSudoku / 2)))
                    #pdf.line(93, 717 - (row * 20) - (220 * noSudoku), 273, 717 - (row * 20) - (220 * noSudoku))
                    pdf.line(xStart - (2 * cellSize / 5) + ((9 * cellSize + (spacing / 2)) * (-1)**(noSudoku + 1) * 0.5), yStart + cellSize - (fontSize / 4) - (row * cellSize) - (((9 * cellSize) + spacing) * floor(noSudoku / 2)), xStart - (2 * cellSize / 5) + (9 * cellSize) + ((9 * cellSize + (spacing / 2)) * (-1)**(noSudoku + 1) * 0.5), yStart + cellSize - (fontSize / 4) - (row * cellSize) - (((9 * cellSize) + spacing) * floor(noSudoku / 2)))
                pdf.setLineWidth(3)
                #pdf.line(273, 717 - (220 * noSudoku), 273, 537 - (220 * noSudoku))
                pdf.line(xStart - (2 * cellSize / 5) + (9 * cellSize) + ((9 * cellSize + (spacing / 2)) * (-1)**(noSudoku + 1) * 0.5), yStart + cellSize - (fontSize / 4) - (((9 * cellSize) + spacing) * floor(noSudoku / 2)), xStart - (2 * cellSize / 5) + (9 * cellSize) + ((9 * cellSize + (spacing / 2)) * (-1)**(noSudoku + 1) * 0.5), yStart + cellSize - (fontSize / 4) - (((9 * cellSize) + spacing) * floor(noSudoku / 2)) - (9 * cellSize))
                #pdf.line(93, 537 - (220 * noSudoku), 273, 537 - (220 * noSudoku))
                pdf.line(xStart - (2 * cellSize / 5) + ((9 * cellSize + (spacing / 2)) * (-1)**(noSudoku + 1) * 0.5), yStart + cellSize - (fontSize / 4) - (((9 * cellSize) + spacing) * floor(noSudoku / 2)) - (9 * cellSize), xStart - (2 * cellSize / 5) + (9 * cellSize) + ((9 * cellSize + (spacing / 2)) * (-1)**(noSudoku + 1) * 0.5), yStart + cellSize - (fontSize / 4) - (((9 * cellSize) + spacing) * floor(noSudoku / 2)) - (9 * cellSize))
                #pdf.drawString(100, 725 - (220 * noSudoku), "Grade: " + wordGrade + " (" + str(grade) + ")")
                pdf.drawString(xStart + ((9 * cellSize + (spacing / 2)) * (-1)**(noSudoku + 1) * 0.5), yStart + cellSize - (((9 * cellSize) + spacing) * floor(noSudoku / 2)), "Grade: " + wordGrade + " (" + str(grade) + ")")
            pdf.showPage()
        return

    pdf = canvas.Canvas(filename)#Creates PDF file
    sudokusLeft = noSudokus

    for iter in range(ceil(noSudokus / perPage)):#Non finished PDF page is still page
        CreateSudokus(perPage, sudokusLeft)
        sudokusLeft -= perPage#Ticks down number of sudokus left to print

    try:
        pdf.save()#Saves at end - checks if Sudoku opened between checks
    except:
        messagebox.showerror("Error", "Error 013: You must close the current PDF opened before you can save this PDF. Please try again.")
        return True
    return False

#SUDOKU GEN 4 ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def MainCheckSpace(sudoku, column, row, flag):
    # Checking cell algorithm - finds singles
    if sudoku[row][column] != 0 and flag != 2:# Breaks if that location already has a value
        return sudoku[row][column]
    elif sudoku[row][column] != 0 and flag == 2:# unless flag == 2
        sudoku[row][column] = 0
    nums = {1,2,3,4,5,6,7,8,9}# Set given all possible values
    nums = nums - set(sudoku[row])# Sets quicker than arrays
    for num in sudoku:
        nums = nums - set([num[column]])
    squareRow = (ceil((row + 1) / 3) * 3) - 3  # Finds first cell in row in square
    squareCol = (ceil((column + 1) / 3) * 3) - 3  # Finds first cell in column in square
    square = sudoku[squareRow][squareCol:squareCol + 3] + sudoku[squareRow + 1][squareCol:squareCol + 3] + sudoku[squareRow + 2][squareCol:squareCol + 3] # Sets list to numbers in square
    nums = nums - set(square)
    if flag == 1: # Flag used to return different values in different scenarios
        if len(nums) == 1:
            return list(nums)[0]
        else:
            return 0
    else:
        return list(nums)

def SudokuSolveGen(mode, difficulty=12, imported=[]):

    def MainHiddenPrimes(sudoku, sudokuMoves, column, row):
        # Finds hidden singles - improves speed of code
        if sudoku[row][column] != 0:  # Breaks if the cell already has a value
            return sudoku[row][column]
        target = sudokuMoves[row][column]  # Sets a list to all current possible values of the cell
        for rw in range(9):
            if rw != row:
                if isinstance(sudokuMoves[rw][column], int):  # checks if only one possible value for that cell
                    target = set(target) - set([sudokuMoves[rw][column]])
                else:
                    target = set(target) - set(sudokuMoves[rw][column])
        if len(target) == 1:  # Stops needless calculation \/
            return list(target)[0]
        target = sudokuMoves[row][column]  # Resets list - hidden singles do not depend on row, column, square at once
        for cl in range(9):
            if cl != column:
                if isinstance(sudokuMoves[row][cl], int):
                    target = set(target) - set([sudokuMoves[row][cl]])
                else:
                    target = set(target) - set(sudokuMoves[row][cl])
        if len(target) == 1:  # Stops needless calculation \/
            return list(target)[0]
        target = sudokuMoves[row][column]
        squareRow = (ceil((row + 1) / 3) * 3) - 2  # Finds first cell in row in square
        squareCol = (ceil((column + 1) / 3) * 3) - 2  # Finds first cell in column in square
        for rw in range(squareRow - 1, squareRow + 2):
            for cl in range(squareCol - 1, squareCol + 2):
                if isinstance(sudokuMoves[rw][cl], int):
                    target = set(target) - set([sudokuMoves[rw][cl]])
                else:
                    target = set(target) - set(sudokuMoves[rw][cl])
        if len(target) == 1:
            return list(target)[0]
        return 0

    def MainQuickSolve(sudoku, cells, grade, difficulty):
        changed = False#Bool value used to detect changes in importGrid
        sudokuMoves = [[0 for iter in range(9)] for iter in range(9)]
        cells = sample([[n, m] for n in range(9) for m in range(9)], 81)#Shuffle cell list
        for cell in range(81):
            temp = sudoku[cells[cell][0]][cells[cell][1]]
            sudoku[cells[cell][0]][cells[cell][1]] = MainCheckSpace(sudoku, cells[cell][1], cells[cell][0], 1)# Try to solve cell using basic single cell algorithm
            if temp != sudoku[cells[cell][0]][cells[cell][1]]:
                changed = True#See if changed
                cells.append([cells[cell][0], cells[cell][1]])#Add solved cell to list
                if NumDiff(sudoku, difficulty):
                    grade += 4#Add value to score
            sudokuMoves[cells[cell][0]][cells[cell][1]] = MainCheckSpace(sudoku, cells[cell][1], cells[cell][0], 0)
        for cell in range(81):
            temp = sudoku[cells[cell][0]][cells[cell][1]]
            sudoku[cells[cell][0]][cells[cell][1]] = MainHiddenPrimes(sudoku, sudokuMoves, cells[cell][1], cells[cell][0])# Try to solve cell using hidden singles
            if temp != sudoku[cells[cell][0]][cells[cell][1]]:
                changed = True#See if changed
                cells.append([cells[cell][0], cells[cell][1]])
                if NumDiff(sudoku, difficulty):
                    grade += 10#Add score
        if changed:
            if NumDiff(sudoku, difficulty):
                grade += 10#Add score for every iteration needed
            sudoku, cells, grade = MainQuickSolve(sudoku, cells, grade, difficulty)#Recursion
        return sudoku, cells, grade

    def MainSolve(sudoku, grade, difficulty, cells=[]):
        sudoku, cells, grade = MainQuickSolve(sudoku, cells, grade, difficulty)# Solve grid to greatest ability
        flatSudoku = [item for subList in sudoku for item in subList]# Flat sudoku used to find 0's easily
        if 0 in flatSudoku:
            for cell in range(81):# Find first empty cell
                if sudoku[floor(cell / 9)][cell % 9] == 0:
                    row = floor(cell / 9)
                    column = cell % 9
                    break
            check = MainCheckSpace(sudoku, column, row, 0)# Find possible values
            check = sample(check, len(check))#Shuffles list so that grids are not predictable - does not affect solving
            if check == []:  # If grid is unsolveable
                return sudoku, cells, grade
            if NumDiff(sudoku, difficulty):#Since backtracking is needed add a heavy penalty for every number that need to be checked
                grade += (50*len(check))
            for possibility in check:
                testSudoku = deepcopy(sudoku) # Deepcopy used to copy grid by value not reference
                testSudoku[row][column] = possibility  # Guess the value of the cell
                cells.append([row,column])
                testSudoku, cells, grade = MainSolve(testSudoku, grade, difficulty, cells)# Try and solve guess grid
                if 0 not in [item for subList in testSudoku for item in subList]:# If the grid is solved
                    return testSudoku, cells, grade
                # otherwise try next value
            return sudoku, cells, grade  # Return incomplete grid
        else:
            return sudoku, cells, grade  # Return complete grid

    def NumDiff(sudoku, difficulty):
        difficulties = [81, 79, 77, 75, 73, 71, 69, 67, 65, 63, 61, 59, 57, 55, 53, 51, 49, 47, 45, 43, 41, 39, 37, 35, 33, 31, 29, 27, 25, 23, 21, 19, 17, 15]
        totalCells = 0
        for row in sudoku:
            for cell in row:
                if cell != 0:
                    totalCells += 1
        return difficulties[difficulty] <= totalCells

    #main function --------------------------------------------------------------------------------------------------------------------------
    if mode == "generate":
        grades = {"Very Easy": 250, "Easy": 550, "Medium": 850, "Hard": 1100, "Very Hard": 1600, "Super Hard": 2200, "Diabolical": 100000}
        grade = 0
        difficulties = [81, 79, 77, 75, 73, 71, 69, 67, 65, 63, 61, 59, 57, 55, 53, 51, 49, 47, 45, 43, 41, 39, 37, 35, 33, 31, 29, 27, 25, 23, 21, 19, 17, 15]
        answer = [[0 for x in range(9)] for y in range(9)]
        if str(difficulty).isnumeric():
            if 0 <= difficulty < len(difficulties):
                answer, cells, grade = MainSolve(answer, grade, difficulty)#Solve blank grid
                sudoku = [[0 for x in range(9)] for y in range(9)]
                for iter in range(difficulties[difficulty]):
                    sudoku[cells[0][0]][cells[0][1]] = answer[cells[0][0]][cells[0][1]]
                    cells.remove(cells[0])
                grade = ceil(grade * difficulty / 20)#Find whole number grade
                away = 100000#Must start large so even diabolical grids can affect the away score.
                wordGrade = ""
                for item in grades:
                    if grades[item] >= grade:
                        if grades[item] - grade < away:#Since it is not an ordered dict this algorithm finds the smallest value larger than the grade.
                            wordGrade = item
                            away = grades[item] - grade
                return sudoku, answer, grade, wordGrade, cells
        return [[0 for x in range(9)] for y in range(9)], [[0 for x in range(9)] for y in range(9)], 0, "", [[[] for x in range(9)] for y in range(9)]
    elif mode == "solve":
        answer, cells, grade = MainSolve(imported, 0, difficulty)
        return answer
    elif mode == "hint":
        answer, cells, grade = MainSolve(imported, 0, 1)
        return cells, answer
    elif mode == "grade":
        grades = {"Very Easy": 250, "Easy": 550, "Medium": 850, "Hard": 1100, "Very Hard": 1600, "Super Hard": 2200, "Diabolical": 100000}
        grade = 0
        difficulties = [81, 79, 77, 75, 73, 71, 69, 67, 65, 63, 61, 59, 57, 55, 53, 51, 49, 47, 45, 43, 41, 39, 37, 35, 33, 31, 29, 27, 25, 23, 21, 19, 17, 15]
        if str(difficulty).isnumeric():
            if 0 <= difficulty < len(difficulties):
                noNumbers = 81 - str(imported).count("0")
                if noNumbers in difficulties:
                    difficulty = difficulties.index(noNumbers)
                elif difficulty > 59:
                    difficulty = 1
                elif difficulty < 19:
                    difficulty = len(difficulties) - 1
                else:
                    difficulty += 1
                    difficulty = difficulties.index(noNumbers)
                answer, cells, grade = MainSolve(imported, grade, difficulty)
                grade = ceil(grade * difficulty / 20)#Find whole number grade
                away = 100000 #Must start large so even diabolical grids can affect the away score.
                wordGrade = ""
                for item in grades:
                    if grades[item] >= grade:
                        if grades[item] - grade < away:#Since it is not an ordered dict this algorithm finds the smallest value larger than the grade.
                            wordGrade = item
                            away = grades[item] - grade
                return imported, answer, grade, wordGrade, cells
        return [[0 for x in range(9)] for y in range(9)], [[0 for x in range(9)] for y in range(9)], 0, "", [[[] for x in range(9)] for y in range(9)]


#Game Code ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class SudokuGrid(sprite.Sprite):
    def _init_(self):
        sprite.Sprite._init_(self)

    def ChangeMark(self, value, row, column):
        if value not in self.mark[row][column]:
            self.mark[row][column].append(value)
        else:
            self.mark[row][column].remove(value)

    def ChangeValue(self, value, row, column):
        self.value[row][column] = value

    def EraseValues(self, row, column):
        self.value[row][column] = 0

    def EraseMarks(self, row, column):
        self.mark[row][column] = []

    def ResetGrid(self):
        self.value = [[0 for x in range(9)] for y in range(9)]
        self.initial = [[0 for x in range(9)] for y in range(9)]
        self.mark = [[[] for x in range(9)] for y in range(9)]
        self.errorPointer = []
        self.completed = [[0 for x in range(9)] for y in range(9)]
        self.startTime = time()
        self.grade = 0
        self.wordGrade = ""
        self.highlight = 0
        self.score = 0
        self.noHints = 0
        global GlobNew
        GlobNew = True

    def ImportValues(self, importGrid, unpack):#Enables load sudokus to be loaded by the load algorithm - values injected into SudokuGrid() based on input parameters of this function
        self.value = importGrid
        if unpack == "":
            a, answer, grade, wordGrade, cells = SudokuSolveGen("grade", imported=deepcopy(importGrid))
            self.initial = deepcopy(importGrid)
            self.mark = [[[] for x in range(9)] for y in range(9)]
            self.errorPointer = []
            self.completed = answer
            self.startTime = time()
            self.grade = grade
            self.wordGrade = wordGrade
            self.highlight = 0
            self.score = 5000
            self.noHints = 0
        else:
            self.initial = eval(unpack[1])
            self.mark = eval(unpack[2])
            self.errorPointer = eval(unpack[3])
            self.completed = eval(unpack[4])
            self.startTime = time() - float(unpack[5])
            self.grade = eval(unpack[6])
            self.wordGrade = unpack[7]
            self.highlight = 0
            self.score = round(float(unpack[8]))
            self.noHints = int(unpack[9])
        global GlobNew
        GlobNew = True

def StartGame(isNew, importGrid=[], unpack=[]):


    def ToTuple(value): #Substitutes return value of getColour with Tkinter style tuple
        value = value.replace("#", "")
        tuple = (int(value[:2], 16), int(value[2:4], 16), int(value[4:6], 16))
        return tuple

    def ShowSudokuScreen(screenSize, cursor, isNew, currentCell=[-1, -1]):#Updates screen based on input parameters and values of SudokuGrid class

        def CreateGrid(screenSize, cursor, isNew, currentCell=[-1, -1]):#Draws grid

            maxSize, smallest, difference = GetDimensions(screenSize)#Finds size of grid

            boxSize = (maxSize - 42) / 9

            #Put values into grid

            if isNew:#If the grid is new
                sudoku, answer, grade, wordGrade, cells = SudokuSolveGen("generate", difficulty=int(difficulty.get()))

                Grid.value = sudoku
                Grid.initial = deepcopy(sudoku)
                Grid.completed = answer
                Grid.mark = [[[] for x in range(9)] for y in range(9)]
                try: #Has a game been started out of scope?
                    difficultyLabel.configure(text="Difficulty: " + wordGrade + " (" + str(grade) + ")")
                except:
                    return

                Grid.grade = grade
                Grid.wordGrade = wordGrade
                Grid.errors = False
                Grid.errorPointer = []
                Grid.highlight = 0
                Grid.score = 5000
                Grid.noHints = 0

                Grid.startTime = time()

            else:
                sudoku = Grid.value#Ensures sudoku still has a value equal to the current - using 'sudoku' variable makes the below code more universal

            initial = Grid.initial
            mark = Grid.mark


            def FindColour(cell): #Converts cell along with variables currentCell and settings colours to return the correct colour tuple
                if (sudoku[cell//9][cell%9] not in MainCheckSpace(deepcopy(sudoku), cell%9, cell//9, 2) and sudoku[cell//9][cell%9] != 0 and alerts.get() == True) or (cell//9, cell%9) in Grid.errorPointer:
                    return ToTuple(colourHLWrong.get())
                elif [cell // 9, cell % 9] == currentCell:
                    return ToTuple(colourHLSelect.get())
                elif (sudoku[cell//9][cell%9] == Grid.highlight and Grid.highlight != 0 and highlights.get() == True):
                    return ToTuple(colourHLOther.get())
                elif [cell // 9, cell % 9] == cursor:
                    return ToTuple(colourHLCursor.get())
                else:
                    return ToTuple(colourCell.get())


            if smallest == "width":#Draws central to window
                draw.rect(screen, ToTuple(colourLines.get()), (15, 15 + (difference / 2), (maxSize), (maxSize)))
                for cell in range(81):
                    draw.rect(screen, FindColour(cell), (21 + ((boxSize + 3) * (cell%9)) + (3 *((cell%9)//3)), (difference/2) + 21 + ((boxSize + 3) * (cell//9)) + (3 *((cell//9)//3)), boxSize, boxSize))#If statements did allow for different coloured cells - now done with FindColour
            else:
                draw.rect(screen, ToTuple(colourLines.get()), (15 + (difference / 2), 15, (maxSize), (maxSize)))
                for cell in range(81):
                    draw.rect(screen, FindColour(cell), ((difference/2) + 21 + ((boxSize + 3) * (cell%9)) + (3 *((cell%9)//3)), 21 + ((boxSize + 3) * (cell//9)) + (3 *((cell//9)//3)), boxSize, boxSize))

            for row in range(len(sudoku)):
                for column in range(len(sudoku[row])):
                    if sudoku[row][column] != 0: #Does not draw 0's
                        textSurf = mainFont.render(str(sudoku[row][column]), True, ToTuple(colourValues.get()) if sudoku[row][column] == initial[row][column] else ToTuple(colourFont.get()))#If statement changes colour based on if it was user-inputted or not - colourFont.get() used in Settings to change colour
                        textRect = textSurf.get_rect()#Find current location
                        if smallest == "height":
                            textRect.center = (15 + difference/2 + (maxSize * column /9) + (maxSize/18), 15 + ((maxSize - 7) * row /9) + (maxSize/12))#Move text
                        else:
                            textRect.center = (15 + (maxSize * column /9) + (maxSize/18), 15 + difference/2 + ((maxSize - 7) * row /9) + (maxSize/18))
                        screen.blit(textSurf, textRect)#Project render on screen at proper location
                    if mark[row][column] != []:#Does not bother drawing blank marks
                        for item in mark[row][column]:
                            textSurf = markFont.render(str(item), True, ToTuple(colourMark.get()))
                            textRect = textSurf.get_rect()
                            if item != 0:
                                if smallest == "height":
                                    textRect.center = (9 + difference/2 + (maxSize * column /9) + (maxSize*item / 90) + (9-column), 28 + ((maxSize - 7) * row /9))#5*item moves the mark along in the cell
                                else:
                                    textRect.center = (9 + (maxSize * column /9) + (maxSize*item / 90) + (9-column), 28 + difference/2 + ((maxSize - 7) * row /9))
                            screen.blit(textSurf, textRect)

            return

        screen = display.set_mode((screenSize[0], screenSize[1]))#Sets window to this size
        screen.fill((240, 240, 240))
        mainFont = font.Font("freesansbold.ttf", int(min(screenSize) / 17))
        markFont = font.Font("freesansbold.ttf", int(min(screenSize) / 51))

        CreateGrid(screenSize, cursor, isNew, currentCell)

        display.update()
        try: #To ensure that only one Sudoku grid is loaded
            gameWindow.update()
        except:
            messagebox.showerror("Error", "Error 001: Please check your settings, close all other programs and try again."
                                          "")
            return
        return

    def GetDimensions(screenSize):#Inputs screenSize tuple, returns size of grid, plus smallest size
        maxSize = min(screenSize) - 30

        if screenSize[0] >= screenSize[1]:
            smallest = "height"
            difference = screenSize[0] - screenSize[1]
        else:
            smallest = "width"
            difference = screenSize[1] - screenSize[0]

        return maxSize, smallest, difference

    def CheckForEvents(currentCell, screenSize, isErase, isMark):#Checks keyboard and mouse inputs

        def CheckForErrors():
            Grid.errorPointer = []
            for row in range(len(Grid.completed)):
                for cell in range(len(Grid.completed[row])):
                    if Grid.value[row][cell] != 0 and (Grid.value[row][cell] not in MainCheckSpace(deepcopy(Grid.value), cell, row, 2)): #Is it not a possible value for this cell?
                        Grid.errorPointer.append((row, cell))
            return


        def IsCompleted(Grid):
            if 0 not in [item for subList in Grid.value for item in subList]:

                CheckForErrors()

                if len(Grid.errorPointer) == 0:
                    return True
            return False

        def GetButtons():#Returns pressed-down keys (which are accepted by the system)
            buttons = []
            if key.get_pressed()[K_0] != 0 or key.get_pressed()[K_KP0] != 0 or key.get_pressed()[K_BACKSPACE] != 0 or key.get_pressed()[K_DELETE] != 0 or key.get_pressed()[K_SPACE] != 0:#Equivalent to erase Button
                buttons.append(0)
            if key.get_pressed()[K_1] != 0 or key.get_pressed()[K_KP1] != 0:
                buttons.append(1)
            if key.get_pressed()[K_2] != 0 or key.get_pressed()[K_KP2] != 0:
                buttons.append(2)
            if key.get_pressed()[K_3] != 0 or key.get_pressed()[K_KP3] != 0:
                buttons.append(3)
            if key.get_pressed()[K_4] != 0 or key.get_pressed()[K_KP4] != 0:
                buttons.append(4)
            if key.get_pressed()[K_5] != 0 or key.get_pressed()[K_KP5] != 0:
                buttons.append(5)
            if key.get_pressed()[K_6] != 0 or key.get_pressed()[K_KP6] != 0:
                buttons.append(6)
            if key.get_pressed()[K_7] != 0 or key.get_pressed()[K_KP7] != 0:
                buttons.append(7)
            if key.get_pressed()[K_8] != 0 or key.get_pressed()[K_KP8] != 0:
                buttons.append(8)
            if key.get_pressed()[K_9] != 0 or key.get_pressed()[K_KP9] != 0:
                buttons.append(9)

            if len(buttons) != 1:
                return False, []
            else:
                return True, buttons

        def CoordsToCell(x, y):#Converts location of cursor into a cell location on the Sudoku grid
            maxSize, smallest, difference = GetDimensions(screenSize)

            if smallest == "width":
                column = (x - 15) // (maxSize / 9)
                row = (y - 15 - difference/2) // (maxSize / 9)
            else:
                column = (x - 15 - difference/2) // (maxSize / 9)
                row = (y - 15) // (maxSize / 9)

            if column > 8 or column < 0 or row > 8 or row < 0:# Returns bool to say if the cursor is on the grid or not
                return False, int(row), int(column)
            return True, int(row), int(column)



        coordX, coordY = mouse.get_pos()  # Location of cursor
        onGrid, row, column = CoordsToCell(coordX, coordY)


        if not IsCompleted(Grid):
            for input in event.get():
                if input.type == QUIT:
                    SafeDestroy()
                elif input.type == MOUSEBUTTONUP:#Mouse up used so the user can move their cursor to cancel an input
                    currentCell = [row, column]
                    if isErase.get() == 1 and -1 < currentCell[0] < 9 and -1 < currentCell[1] < 9 and Grid.initial[currentCell[0]][currentCell[1]] == 0:#Removes value from clicked cell
                        Grid.EraseValues(currentCell[0], currentCell[1])
                        Grid.EraseMarks(currentCell[0], currentCell[1])
                        Grid.highlight = 0
                    CheckForErrors()
                    ShowSudokuScreen(screenSize, currentCell, False, currentCell)
                elif input.type == MOUSEMOTION:
                    if [row, column] != currentCell:
                        ShowSudokuScreen(screenSize, [row, column], False, currentCell)#Change cell

            global GlobNew
            if GlobNew: #Makes new grids appear
                ShowSudokuScreen(screenSize, currentCell, False, currentCell)
                GlobNew = False

            if key.get_focused():#Is there an input at all?
                unique, buttons = GetButtons()#Return all recognised key presses
                if unique == True:# One key press
                    currentNumber = buttons[0]
                    if isMark.get() == 1 and -1 < currentCell[0] < 9 and -1 < currentCell[1] < 9 and Grid.initial[currentCell[0]][currentCell[1]] == 0:# Change mark
                        Grid.ChangeMark(currentNumber, currentCell[0], currentCell[1])
                        Grid.highlight = currentNumber
                        CheckForErrors()
                        ShowSudokuScreen(screenSize, currentCell, False, currentCell)
                    elif -1 < currentCell[0] < 9 and -1 < currentCell[1] < 9 and Grid.initial[currentCell[0]][currentCell[1]] == 0:#Change cell
                        Grid.ChangeValue(currentNumber, currentCell[0], currentCell[1])
                        Grid.highlight = currentNumber
                        CheckForErrors()
                        ShowSudokuScreen(screenSize, currentCell, False, currentCell)
            else:
                Grid.highlight = 0

        #Goes here to be after currentTime is updated but before currentTime is manipulated for label
        if NoZeroes(Grid.initial) == 0:
            pass
        elif NoZeroes(Grid.value) == 0:
            if IsCompleted(Grid):
                draw.rect(screen, (0, 0, 0), (30, screenSize[1] * (3/8), screenSize[0] - 60, screenSize[1] * (1/4)), 4)
                draw.rect(screen, (255, 255, 255), (30, screenSize[1] * (3/8), screenSize[0] - 60, screenSize[1] * (1/4)))

                winFont = font.Font("freesansbold.ttf", int(min(screenSize) / 20))
                winSurf = winFont.render("Congrats, you've finished the grid!", True, (0, 0, 0))
                winRect = winSurf.get_rect()
                winRect.center = (screenSize[0] / 2, (screenSize[1] - 40) / 2)
                screen.blit(winSurf, winRect)

                scoreSurf = winFont.render("Score: " + str(ceil(Grid.score)), True, (0, 0, 0))
                scoreRect = scoreSurf.get_rect()
                scoreRect.center = (screenSize[0] / 2, (screenSize[1] + 40) / 2)
                screen.blit(scoreSurf, scoreRect)
        else:
            currentTime = time() - Grid.startTime
            if Grid.score > 0:
                Grid.score = (5000 - (2000 * currentTime /  Grid.grade) - (((500 * Grid.grade / (450 * NoZeroes(Grid.initial)))) * Grid.noHints)) * Grid.grade / 100 #Uses function to find the absolute current value of the score, using difficulty, hints, time and other factors
            elif Grid.score < 0:
                Grid.score = 0

            if currentTime > 60.0:# Formats the decimal no of seconds since 1970 into a recognisable format since the game started (mins, secs, hours, etc)
                if currentTime // 60 < 10:
                    if currentTime % 60.0 < 10.0:
                        timeLabelText = "0" + str(currentTime // 60)[0] + ":0" + str(currentTime % 60)[:4]
                    else:
                        timeLabelText = "0" + str(currentTime // 60)[0] + ":" + str(currentTime % 60)[:5]
                else:
                    if currentTime % 60.0 < 10.0:
                        timeLabelText = str(currentTime // 60)[:2] + ":0" + str(currentTime % 60)[:4]
                    else:
                        timeLabelText = str(currentTime // 60)[:2] + ":" + str(currentTime % 60)[:5]
            elif currentTime < 10.0:
                timeLabelText = "00:0" + str(currentTime)[:4]
            else:
                timeLabelText = "00:" + str(currentTime)[:5]
            timeLabelText = timeLabelText.replace(".", ":")

            timerLabel['text'] = ("Timer: " + timeLabelText)#Change UI label

        scoreLabel.configure(text=("Score: " + str(ceil(Grid.score))))
        difficultyLabel.configure(text="Difficulty: " + Grid.wordGrade + " (" + str(Grid.grade) + ")")

        return currentCell

    def GetHint():
        if Grid.completed == None: #If it has not yet been needed / imported for some reason - occasional error
            Grid.completed = SudokuSolveGen("solve", 0, Grid.initial)

        for row in range(len(Grid.completed)):
            for cell in range(len(Grid.completed[row])):
                if Grid.value[row][cell] != 0 and (Grid.value[row][cell] not in MainCheckSpace(deepcopy(Grid.value), cell, row, 2)): #Is it not a possible value for this cell?
                    Grid.errorPointer.append((row, cell))
                else:
                    if (row, cell) in Grid.errorPointer:
                        Grid.errorPointer.remove((row, cell)) #Remove any corrected errors from the error list

        if Grid.errorPointer == []: #No errors? Give a hint
            cells, answer = SudokuSolveGen("hint", difficulty=Grid.grade, imported=deepcopy(Grid.value)) #Solve current grid - find cells
            if 0 in [item for subList in answer for item in subList]: # Flat sudoku used to find 0's easily
                for row in range(len(answer)): #Solves error where wrong value entered which does not directly impact grid - shows the user there is an error
                    for cell in range(len(answer[row])):
                        if Grid.completed[row][cell] != Grid.value[row][cell] and Grid.value[row][cell] != 0:
                            Grid.errorPointer.append((row, cell))
                ShowSudokuScreen(screenSize, (-1, -1), False)
            else:
                for cell in range(81):
                    position = cells[cell]
                    if Grid.value[position[0]][position[1]] == 0:
                        break
                Grid.value[position[0]][position[1]] = answer[position[0]][position[1]] #Give them a cell
                ShowSudokuScreen(screenSize, position, False) #Show
        else:
            ShowSudokuScreen(screenSize, (-1, -1), False)

        Grid.noHints += 1
        return

    def AutoSolve():
        answer = messagebox.askokcancel("PySudoku", "Are you sure you want to AutoSolve? This will set your score to zero!") #Warns user
        if not answer:
            return
        if Grid.completed == [[0 for x in range(9)] for y in range(9)]:
            a, Grid.completed, Grid.grade, Grid.wordGrade, b = SudokuSolveGen("grade", imported=Grid.value)
        Grid.value = Grid.completed
        Grid.initial = Grid.completed #Cannot edit grid and solve it themselves using remembering
        Grid.score = 0
        ShowSudokuScreen(screenSize, [-1, -1], False)
        return

    def NoZeroes(importGrid): #Returns number of blanks in grid
        no = 0
        for row in importGrid:
            for cell in row:
                if cell == 0:
                    no += 1
        return no

    def SafeDestroy(): #Destroys game window whilst trying to avoid any errors whatsoever
        try:
            global GlobIsGame
            GlobIsGame = False
            display.quit()
            gameWindow.destroy()
        except:
            return
        return


    global GlobIsGame #GlobIsGame used to stop two windows error
    GlobIsGame = True

    currentCell = [-1, -1]
    screenSize = [500, 500]

    gameWindow = Toplevel(root)

    if isNew:

        isErase = IntVar()#Easier to manage buttons with two variables rather than one
        isErase.set(1)

        isMark = IntVar()
        isMark.set(0)

        #Menu
        gameBar = Menu(gameWindow)

        newMenu = Menu(gameBar, tearoff=0)
        newMenu.add_command(label="Game", command=lambda: ShowSudokuScreen(screenSize, [-1, -1], True), font=("Arial", sizeSet.get()))
        newMenu.add_command(label="Blank grid", command=lambda: LoadSudoku("blank"), font=("Arial", sizeSet.get()))
        gameBar.add_cascade(label="New..", menu=newMenu, font=("Arial", sizeSet.get()))

        loadMenu = Menu(gameBar, tearoff=0)
        loadMenu.add_command(label="From save game..", command=lambda: LoadSudoku("save"), font=("Arial", sizeSet.get()))
        loadMenu.add_command(label="From string..", command=lambda: LoadSudoku("string"), font=("Arial", sizeSet.get()))
        gameBar.add_cascade(label="Load..", menu=loadMenu, font=("Arial", sizeSet.get()))

        saveMenu = Menu(gameBar, tearoff=0)
        saveMenu.add_command(label="Game as save game", command=lambda: SaveSudoku("save", Grid, time()), font=("Arial", sizeSet.get()))
        saveMenu.add_command(label="Current position as string", command=lambda: SaveSudoku("stringcurrent", Grid, time()), font=("Arial", sizeSet.get()))
        saveMenu.add_command(label="Initial grid as string", command=lambda: SaveSudoku("stringinitial", Grid, time()), font=("Arial", sizeSet.get()))
        gameBar.add_cascade(label="Save..", menu=saveMenu, font=("Arial", sizeSet.get()))

        printMenu = Menu(gameBar, tearoff=0)
        printMenu.add_command(label="Current Sudoku grid", command=lambda: CreateSudoku(1, 1, 0, "", importGrid=Grid.initial, grade=[Grid.grade, Grid.wordGrade]), font=("Arial", sizeSet.get()))
        printMenu.add_command(label="Multiple Sudoku grids as PDF", command=PrintSudoku, font=("Arial", sizeSet.get()))
        gameBar.add_cascade(label="Print..", menu=printMenu, font=("Arial", sizeSet.get()))

        gameBar.add_command(label="Settings", command=Settings, font=("Arial", sizeSet.get()))

        helpMenu = Menu(gameBar, tearoff=0)
        helpMenu.add_command(label="Instructions", command=InstHelp, font=("Arial", sizeSet.get()))
        helpMenu.add_separator()
        helpMenu.add_command(label="About", command=AboutHelp, font=("Arial", sizeSet.get()))
        gameBar.add_cascade(label="Help", menu=helpMenu, font=("Arial", sizeSet.get()))

        gameBar.add_command(label="Exit", command=SafeDestroy, font=("Arial", sizeSet.get()))

        gameWindow.config(menu=gameBar)

        embed = Frame(gameWindow, width=screenSize[0], height=screenSize[1]) #creates embed frame for pygame window
        embed.grid(row=0, column=0, rowspan=6) # Adds grid
        environ['SDL_WINDOWID'] = str(embed.winfo_id())#Embeds frame in Tkinter window using driver trickery - copied from stackoverflow (mentioned in writeup)
        environ['SDL_VIDEODRIVER'] = 'windib'
        screen = display.set_mode(tuple(screenSize))
        screen.fill(Color(255,255,255))
        init()
        display.update()
        gap = Label(gameWindow, text="").grid(row=0, column=1, columnspan=2)#Creates gap above difficulty label
        difficultyLabel = Label(gameWindow, text="Difficulty:", font=("Arial", sizeSet.get() + 2))
        difficultyLabel.grid(row=1, column=1, columnspan=2)
        timerLabel = Label(gameWindow, text="Timer:", font=("Arial", sizeSet.get() + 3))
        timerLabel.grid(row=2, column=1, columnspan=2)

        scoreLabel = Label(gameWindow, text="Score:", font=("Arial", sizeSet.get() + 3))
        scoreLabel.grid(row=3, column=1, columnspan=2)

        eraseImage = PhotoImage(file="pics/change.gif")
        eraseCell = Checkbutton(gameWindow, image=eraseImage, indicatoron=0, variable=isErase, command=lambda: isMark.set(0))
        eraseCell.image = eraseImage
        eraseCell.grid(row=4, column=1)

        markImage = PhotoImage(file="pics/mark.gif")
        markCell = Checkbutton(gameWindow, image=markImage, indicatoron=0, variable=isMark, command=lambda: isErase.set(0))
        markCell.image = eraseImage
        markCell.grid(row=4, column=2)

        hint = Button(gameWindow, text="Hint", command=GetHint, font=("Arial", sizeSet.get()))
        hint.grid(row=5, column=1)
        autoSolve = Button(gameWindow, text="Autosolve", command=AutoSolve, font=("Arial", sizeSet.get()))
        autoSolve.grid(row=5, column=2)

    global Grid #Grid can be referenced anywhere now
    Grid = SudokuGrid()


    if importGrid == "blank":
        Grid.ResetGrid()#Creates blank grid
    elif unpack != []:
        Grid.ImportValues(importGrid, unpack) #Imports save game
    elif importGrid != []:
        Grid.ImportValues(importGrid, "")
    else:
        Grid.initial = [[0 for x in range(9)] for y in range(9)]


    ShowSudokuScreen(screenSize, [-1, -1], True if importGrid == [] else False)
    gameWindow.iconbitmap("pics/thumbnail2.ico")#Adds PySudoku logo to top (rather than Tkinter logo)
    i = 0
    while True:
        try:
            display.update()  # Update what has been on the screen
            gameWindow.update()  # Update tkinter window
            currentCell = CheckForEvents(currentCell, screenSize, isErase, isMark)  # Check inputs - leads to printing screen if needed
        except:
            SafeDestroy()
            if i == 0: #Iterator counts if it errors in the first loop - hence not closing program error, rather a two window error
                messagebox.showerror("Error", "Error 001: Please close all currently running games and try again.")
            return
        i += 1

def LoadSudoku(referral):
    if referral == "save":
        filename = filedialog.askopenfilename(defaultextension=".SUDOKU")
        if filename == "": #Filename not selected
            messagebox.showerror("Error", "Error 002: You must select a filename to save to. Please try again.")
            return
        with open(filename, "rb") as sudokugrid:
            file, ext = path.splitext(filename)
            if ext != ".sudoku": #Not right file type of file
                messagebox.showerror("Error", "Error 004: You must select a .sudoku file to load from.")
                return
            try:
                sudokugrid = sudokugrid.read().decode('utf-8')
            except: #Corrupt file or from older version of program which was not compatible?
                messagebox.showerror("Error", "Error 006: This is not a valid file. Please try again.")
                return
            sudoku = sudokugrid.split("\n")
            newGrid = eval(sudoku[0])
        if GlobIsGame:
            Grid.ImportValues(newGrid, sudoku) #Files now handled loading, either replacing current or making new using GlobIsGame global
        else:
            StartGame(True, newGrid, sudoku)
    elif referral == "string":
        string = simpledialog.askstring("PySudoku", "Please enter/paste the Sudoku grid into the entry box below:")  # Simpledialog provides basic input window (without extra programming)
        if string == None:
            return
        else:
            string = string.replace(".", "0").replace("-", "0").replace(" ", "0") #Removes need for delimiter
        if len(string) == 81 and ("0" in string or "1" in string):
            temp = [string[row:row + 9] for row in range(0, len(string), 9)]
            sudoku = []
            for row in range(9):
                sudoku.append([])
                for column in range(9):
                    sudoku[row].append(int(temp[row][column])) #Makes list
        else:
            messagebox.showerror("Error", "Error 007: You must enter a 81 cell Sudoku grid, with blank cells being either '.', '-'. ' ' or '0'.")
            return
        if GlobIsGame:
            Grid.ImportValues(sudoku, "")
        else:
            StartGame(True, sudoku)
    elif referral == "blank":
        if GlobIsGame:
            Grid.ResetGrid()
        else:
            StartGame(True, "blank")
    else:
        if GlobIsGame:
            Grid.ResetGrid()
            sudoku, answer, grade, wordGrade, cells = SudokuSolveGen("generate", difficulty=int(difficulty.get()))

            Grid.value = sudoku
            Grid.initial = deepcopy(sudoku)
            Grid.completed = answer
            Grid.mark = [[[] for x in range(9)] for y in range(9)]
            Grid.grade = grade
            Grid.wordGrade = wordGrade
        else:
            StartGame(True)
    return



def SaveSudoku(referral, Grid, time):

    def ToString(sudoku): #Turns nested list into PySudoku compatible string
        string = ""
        for row in sudoku:
            for cell in item:
                if cell == 0 or cell == "":
                    string += "."
                else:
                    string += str(cell)
        return string

    if referral[:6] == "string":
        if referral == "stringinitial":
            string = ToString(Grid.initial)
        else:
            string = ToString(Grid.value)
        value = Toplevel(root)
        value.iconbitmap("pics/thumbnail2.ico") # Removes tkinter branding
        stringDialog = Label(value, text="Copy the following string to reload progress, or transfer this grid to another program.")
        stringDialog.grid(row=0, column=0)
        stringBox = Entry(value, state='normal', width=60) #To allow entry to be written to
        stringBox.grid(row=1, column=0)
        stringBox.insert(0, string)
        stringBox.configure(state='readonly') #To only allow copy/paste
        stringClose = Button(value, text="Close", command=value.destroy)
        stringClose.grid(row=2, column=0)
    else:
        string = ""
        for item in [str(Grid.value), str(Grid.initial), str(Grid.mark), str(Grid.errorPointer), str(Grid.completed), str(time - Grid.startTime), str(Grid.grade), Grid.wordGrade, str(Grid.score), str(Grid.noHints)]: #Write each of these to the file
            string += item #Make writeable string
            string += "\n"
        string = string[:-1]
        string = bytes(string, 'utf-8') #Turn into bytes so it can be written using binary - more secure, harder to read/edit
        filename = filedialog.asksaveasfilename(defaultextension=".SUDOKU")
        if filename == "": #File dialog exited / no file selected
            messagebox.showerror("Error", "Error 002: You must select a filename to save to. Please try again.")
            return
        file, ext = path.splitext(filename)
        if ext != ".sudoku": #Force to type .sudoku (if just filename given without suffix then this works else makes double suffix - imo better than error for no reason)
            filename = file + ".sudoku"
        with open(filename, "wb") as text: #write binary
            text.write(string)
        return
    return

def CreateSudoku(noSudoku, perPage, difficulty, filename, importGrid=[], grade=[], pic=""):
    if importGrid != []: #Single pdf sudoku
        filename = filedialog.asksaveasfilename(defaultextension=".pdf")

    if noSudoku == None or noSudoku == "": #Already been checked for integer - just checking for no value
        messagebox.showerror("Error", "Error 008: You must enter a valid number of Sudokus.")
        return
    elif perPage == None or perPage == "":#Already been checked for integer - just checking for no value
        messagebox.showerror("Error", "Error 009: You must enter a valid number of Sudokus per page.")
        return
    elif difficulty == None or difficulty == "":#Already been checked for integer - just checking for no value
        messagebox.showerror("Error", "Error 010: You must enter a valid difficulty.")
        return
    else:
         noSudoku, perPage, difficulty = int(noSudoku), int(perPage), int(difficulty)

    if filename=="":
        messagebox.showerror("Error", "Error 002: You must select a filename to save to. Please try again.")
        return

    if importGrid != []: #Single grid
        error = CreateSudokuPage(1, 1, 0, filename, importGrid=importGrid, gradeSet=grade)
    else:
        if pic != "No file selected..":
            error = CreateSudokuPage(noSudoku, perPage, difficulty, filename, logo=pic)
        else:
            error = CreateSudokuPage(noSudoku, perPage, difficulty, filename)
    if not error:
        messagebox.showinfo("Finished generation", "Your Sudoku PDF has been created.")#Removed progressbar as it froze, causing the window to not respond - I felt this was better than no feedback but users have told me they would be worried if the program 'crashed' hence I have changed this
    Popen(filename, shell=True)
    return

def PrintSudoku():

    def ClearLogo():
        logoFilename.configure(state="normal")  # Allows data to be transferred to the Entry widget despite it being read-only
        logoFilename.delete(0, END)
        logoFilename.insert(0, "No file selected..")  # Change text
        logoFilename.configure(state="readonly")
        logo = PhotoImage(file="pics/images.thumbnail")
        logoLabel.configure(image=logo)
        logoLabel.image = logo  # Reference ensures photo appears
        return

    def SelectLogoFile():
        filename = filedialog.askopenfilename()
        if filename == "":
            messagebox.showerror("Error", "Error 002: You must select a filename to save to. Please try again.")
            return
        raw, error = CreateThumbnail(filename)  # Makes thumbnail-sized image of selected image
        if not error:
            logoFilename.configure(state="normal")
            logoFilename.delete(0, END)
            logoFilename.insert(0, filename)
            logoFilename.configure(state="readonly")
            logo = ImageTk.PhotoImage(Image.open(raw))  # Turns BytesIO into an image, then into a Tk compatible image
            logoLabel.configure(image=logo)
            logoLabel.image = logo
        return

    def CreateThumbnail(filename): #main code copied from http://pillow.readthedocs.io/en/3.4.x/reference/Image.html
        size = 50, 50
        photo = BytesIO()  # Converts into RAM stored BytesIO object - removes the need to store in the user's PC
        try:
            image = Image.open(filename)  # Takes image
            image.thumbnail(size)  # Shrinks
            image.save(photo, "GIF")
            error = False
        except:
            messagebox.showerror("Error", "Error 005: You must use a picture file type as an image (for example, PNG, JPG, GIF, BMP).")
            error = True
        return photo, error

    def ChangePreview(a,b,c):
        noSudoku, perPage, page = noSudokuValue.get(), perPageValue.get(), imageNo.get()
        if noSudoku == None: #Try/except replaced with simple-ish if statement
            messagebox.showerror("Error", "Error 008: You must enter a valid number of Sudokus.")
            return
        elif perPage == None:
            messagebox.showerror("Error", "Error 009: You must enter a valid number of Sudokus per page.")
            return
        elif page == None:
            messagebox.showerror("Error", "Error 011: The page number does not seem to be correct. Close this window and try again")
            return

        if str(noSudoku).isnumeric() and str(perPage).isnumeric() and str(page).isnumeric():
            #If the user just changes page make it just change page
            # otherwise generate list and then set image
            preview.configure(image="", text="Please check your inputs.")  # If perPage, noSudoku or page are not valid this code will still have been executed
            pages = [str(perPage) + str(perPage) + ("b-1" if newPage % 2 == 0 else "-1") for newPage in range(int(noSudoku) // int(perPage))]  # Creates list which contains filenames of corresponding images to spoof a print preview
            if int(noSudoku) % int(perPage) != 0:  # Is there an incomplete page at the end?
                pages += [str(perPage) + str(int(noSudoku) % int(perPage)) + "-1"]  # Add it in
            if int(page) >= int(ceil(int(noSudoku) / int(perPage))):
                page = int(ceil(int(noSudoku) / int(perPage))) - 1
            logo2 = PhotoImage(file="pics/" + pages[page] + ".gif")
            preview.configure(image=logo2)
            preview.image = logo2

            imageNo.set(0)
            labelText.set("Page " + str(imageNo.get() + 1))
            leftArrow.configure(state=DISABLED)
            if len(pages) == 1:
                rightArrow.configure(state=DISABLED)
            else:
                rightArrow.configure(state=NORMAL)
        return

    def ChangePage(val, noSudoku, perPage, page):
        if noSudoku == None or noSudoku == "":
            messagebox.showerror("Error", "Error 008: You must enter a valid number of Sudokus.")
            return
        elif perPage == None or perPage == "":
            messagebox.showerror("Error", "Error 009: You must enter a valid number of Sudokus per page.")
            return
        elif page == None or page == "":
            messagebox.showerror("Error", "Error 011: The page number does not seem to be correct. Close this window and try again")
            return

        if str(noSudoku).isnumeric() and str(perPage).isnumeric() and str(page).isnumeric():
            imageNo.set(imageNo.get() + val)#Change page up/down same algorithm different parameter
            noSudoku, perPage, page = noSudokuValue.get(), perPageValue.get(), imageNo.get()#Same as ChangePreview algorithm
            pages = [str(perPage) + str(perPage) + ("b-1" if newPage % 2 == 0 else "-1") for newPage in range(int(noSudoku) // int(perPage))]
            sys.stdout.write(str(pages))
            if int(noSudoku)%int(perPage) != 0:
                pages += [str(perPage) + str(int(noSudoku)%int(perPage)) + "-1"]
            if int(page) >= int(ceil(int(noSudoku) / int(perPage))):
                page = int(ceil(int(noSudoku) / int(perPage))) - 1
            logo2 = PhotoImage(file="pics/" + pages[page] + ".gif")
            preview.configure(image=logo2)
            preview.image = logo2
            labelText.set("Page " + str(imageNo.get() + 1))
            if page < 1:
                leftArrow.configure(state=DISABLED)
            else:
                leftArrow.configure(state=NORMAL)
            if len(pages) == page + 1:
                rightArrow.configure(state=DISABLED)
            else:
                rightArrow.configure(state=NORMAL)
        return

    def DiffCheck(a,b,c): #3 variables cos that's what trace does
        if not difficultyValue.get().isnumeric() and difficultyValue.get() != "":
            difficultyValue.set("12")
            messagebox.showerror("Error", "Error 003: This is not a valid integer. Please enter a number between 1-33.")
        elif difficultyValue.get().isnumeric():
            if int(difficultyValue.get()) < 1 or int(difficultyValue.get()) > 33:
                difficultyValue.set("12")
                messagebox.showerror("Error", "Error 003: This is not a valid integer. Please enter a number between 1-33.")
        return

    def NoSudokuCheck(a,b,c): #3 variables cos that's what trace does
        if not noSudokuValue.get().isnumeric() and noSudokuValue.get() != "":
            noSudokuValue.set("12")
            messagebox.showerror("Error", "Error 003: This is not a valid integer. Please enter a number between 1 and 10000.")
        elif noSudokuValue.get().isnumeric():
            if int(noSudokuValue.get()) < 1 or int(noSudokuValue.get()) > 10000:
                noSudokuValue.set("12")
                messagebox.showerror("Error", "Error 003: This is not a valid integer. Please enter a number between 1 and 10000.")
        a = b = c = 0  # a,b,c do not matter – using variable noSudokuValue.get() since this is in scope
        ChangePreview(a, b, c)  # Call original function
        return

    imageNo = IntVar()
    imageNo.set(0)
    labelText = StringVar()
    labelText.set("Page 1")

    pages = ["44b-1", "44-1"]

    printSet = Toplevel(root)
    printSet.iconbitmap("pics/thumbnail2.ico")
    noSudokuValue = StringVar()#Since it is an Entry widget, Stringvar ensures no errors if the user enters a random set of characters
    noSudokuValue.set("8")
    noSudokuValue.trace_variable("w", NoSudokuCheck)#Any changes automatically lead to this function being called (hence using IntVar / StringVar for this functionality)
    perPageValue = IntVar()
    perPageValue.set(4)
    perPageValue.trace_variable("w", ChangePreview)
    difficultyValue = StringVar()
    difficultyValue.set("12")
    difficultyValue.trace_variable("w", DiffCheck)
    printLabel = Label(printSet, text="Create PDF", font=("Arial", sizeSet.get() + 3)).grid(row=0, column=0, columnspan=7)

    page = PhotoImage(file="pics/" + pages[0] + ".gif")#Print preview
    preview = Label(printSet, image=page)
    preview.image = page
    preview.grid(row=1, column=0, rowspan=4, columnspan=3)#Both references needed for some reason to show

    noSudokuLabel = Label(printSet, text="Total number of Sudoku grids:", font=("Arial", sizeSet.get())).grid(row=1, column=3)
    noSudoku = Entry(printSet, textvariable=noSudokuValue, font=("Arial", sizeSet.get())).grid(row=1, column=4, columnspan=3)
    perPageLabel = Label(printSet, text="Number of Sudoku grids per page:", font=("Arial", sizeSet.get())).grid(row=2, column=3)
    perPage = OptionMenu(printSet, perPageValue, 1, 2, 3, 4, 6).grid(row=2, column=4, columnspan=3)
    difficultyLabel = Label(printSet, text="Difficulty (1-33):", font=("Arial", sizeSet.get())).grid(row=3, column=3)
    difficulty = Entry(printSet, textvariable=difficultyValue, font=("Arial", sizeSet.get())).grid(row=3, column=4, columnspan=3)

    logoDesc = Label(printSet, text="Logo used in top corner:", font=("Arial", sizeSet.get())).grid(row=4, column=3)
    logoFilename = Entry(printSet)
    logoFilename.insert(0,"No file selected..")
    logoFilename.configure(state="readonly")#User cannot change contents
    logoFilename.grid(row=4, column=4)
    browse = Button(printSet, text="Browse..", command=SelectLogoFile, font=("Arial", sizeSet.get())).grid(row=4, column=5)
    logo = PhotoImage(file="pics/images.thumbnail")
    clear = Button(printSet, text="Clear logo", command=ClearLogo, font=("Arial", sizeSet.get())).grid(row=4, column=6)
    logoLabel = Label(printSet, image=logo)
    logoLabel.image = logo
    logoLabel.grid(row=4, column=7)

    leftArrow = Button(printSet, text="<", command=lambda: ChangePage(-1, noSudokuValue.get(), perPageValue.get(), imageNo.get()), state=DISABLED, font=("Arial", sizeSet.get()))
    leftArrow.grid(row=5, column=0)
    pageLabel = Label(printSet, textvariable=labelText, width=15, font=("Arial", sizeSet.get()))
    pageLabel.grid(row=5, column=1)
    rightArrow = Button(printSet, text=">", command=lambda: ChangePage(1, noSudokuValue.get(), perPageValue.get(), imageNo.get()), state=NORMAL, font=("Arial", sizeSet.get()))
    rightArrow.grid(row=5, column=2)

    cancelButton = Button(printSet, text="Cancel", command=printSet.destroy, font=("Arial", sizeSet.get())).grid(row=5, column=3)#Closes window
    createButton = Button(printSet, text="Create", command=lambda: CreateSudoku(noSudokuValue.get(), perPageValue.get(), difficultyValue.get(), filedialog.asksaveasfilename(defaultextension=".pdf"), pic=logoFilename.get()), font=("Arial", sizeSet.get())).grid(row=5, column=4, columnspan=3)#Calls CreateSudoku function with parameters in widgets
    return

def Settings():

    global GlobChanges#Changes variable stores all changes made to settings whilst the window is open - global to stop constant passing of data.
    GlobChanges = []

    settings = Toplevel(root)
    settings.iconbitmap("pics/thumbnail2.ico")
    notebook = ttk.Notebook(settings)#Notebook used to create tab-based GUI - simpler to code as deletion and addition of widgets handled by notebook
    notebook.grid(row=0, column=0, columnspan=3)

    okButton = Button(settings, text="OK", command=lambda: Reset(True), font=("Arial", sizeSet.get()))#Applies settings and quits
    okButton.grid(row=1, column=0)

    cancelButton = Button(settings, text="Cancel", command=settings.destroy, font=("Arial", sizeSet.get()))#Quits without applying settings
    cancelButton.grid(row=1, column=1)

    applyButton = Button(settings, text="Apply", state=DISABLED, command=lambda: Reset(False), font=("Arial", sizeSet.get()))#Applies settings
    applyButton.grid(row=1, column=2)

    def RemoveAll(value):
        global GlobChanges
        for item in GlobChanges:
            if item == value:
                GlobChanges.remove(value)
        if value in GlobChanges: # Weird error where difficulty delete fails
            GlobChanges.remove(value)
        return

    def ChangeApply():
        global GlobChanges
        if len(GlobChanges) > 0:
            applyButton.configure(state=NORMAL)#Makes apply Button clickable if changes have been made
        else:
            applyButton.configure(state=DISABLED)
        return

    def Reset(destroy):
        global GlobChanges
        GlobChanges = []
        if difficultyTemp.get() == "" or (not difficultyTemp.get().isnumeric()) or (difficultyTemp.get().isnumeric() and not 1<=int(difficultyTemp.get())<=40): #Empty difficulty box allowed (for entering numbers) but will cause error otherwise - this catches this
            messagebox.showerror("Error", "Error 012: You must select an integer difficulty between 1 and 33.")
            difficultyTemp.set("12")
            return
        ChangeApply()
        # Set variables to new values
        difficulty.set(difficultyTemp.get())
        alerts.set(alertsTemp.get())
        highlights.set(highlightsTemp.get())
        colourCell.set(colourCellTemp.get())
        colourHLCursor.set(colourHLCursorTemp.get())
        colourHLWrong.set(colourHLWrongTemp.get())
        colourHLSelect.set(colourHLSelectTemp.get())
        colourHLOther.set(colourHLOtherTemp.get())
        colourLines.set(colourLinesTemp.get())
        sizeSet.set(sizeSetTemp.get())
        colourValues.set(colourValuesTemp.get())
        colourMark.set(colourMarkTemp.get())
        colourFont.set(colourFont.get())
        if destroy:
            settings.destroy()
        return

    def PickColour(variable, current):
        colour = colorchooser.askcolor(current)
        if colour == (None, None):#removes try / except
            return
        #format colour
        colour = "#" + str(colour).split("#")[1][:6]
        if variable == "colourCell":
            old = colourCell.get()#old variable used to check for changes
            colourCellTemp.set(colour)
            colourCellButton.configure(bg=colour)
        elif variable == "colourHLCursor":
            old = colourHLCursor.get()
            colourHLCursorTemp.set(colour)
            colourHLCursorButton.configure(bg=colour)
        elif variable == "colourHLSelect":
            old = colourHLSelect.get()
            colourHLSelectTemp.set(colour)
            colourHLSelectButton.configure(bg=colour)
        elif variable == "colourHLWrong":
            old = colourHLWrong.get()
            colourHLWrongTemp.set(colour)
            colourHLWrongButton.configure(bg=colour)
        elif variable == "colourHLOther":
            old = colourHLOther.get()
            colourHLOtherTemp.set(colour)
            colourHLOtherButton.configure(bg=colour)
        elif variable == "colourLines":
            old = colourLines.get()
            colourLinesTemp.set(colour)
            colourLinesButton.configure(bg=colour)
        elif variable == "colourMark":
            old = colourMark.get()
            colourMarkTemp.set(colour)
            colourMarkButton.configure(bg=colour)
        elif variable == "colourValues":
            old = colourValues.get()
            colourValuesTemp.set(colour)
            colourValuesButton.configure(bg=colour)
        elif variable == "colourFont":
            old = colourFont.get()
            colourFonttemp.set(colour)
            colourFontButton.configure(bg=colour)
        global GlobChanges
        if old != colour:#Has change been made?
            GlobChanges.append(variable)
        else:
            RemoveAll(variable)
        ChangeApply()

        return

    def BoolToDisabled(value):
        if value == 0:
            return DISABLED
        else:
            return NORMAL

    def StateChange(value, button):
        if value == True:#Set corresponding colour labels to read only or normal
            if button == "alerts":
                colourHLWrongLabel.configure(state=NORMAL)
                colourHLWrongButton.configure(state=NORMAL)
            else:
                colourHLOtherLabel.configure(state=NORMAL)
                colourHLOtherButton.configure(state=NORMAL)
        else:
            if button == "alerts":
                colourHLWrongLabel.configure(state=DISABLED)
                colourHLWrongButton.configure(state=DISABLED)
            else:
                colourHLOtherLabel.configure(state=DISABLED)
                colourHLOtherButton.configure(state=DISABLED)
        global GlobChanges
        if button == "alerts":
            if alerts.get() != value:#Change made?
                GlobChanges.append(button)
            else:
                RemoveAll(button)#Remove from GlobChanges if change not made overall
        else:
            if highlights.get() != value:
                GlobChanges.append(button)
            else:
                RemoveAll(button)
        ChangeApply()
        return

    def DiffCheck(a,b,c): #3 variables cos that's what trace does
        if difficulty.get() != difficultyTemp.get():#Removes or appends to GlobChanges if change made, validates difficulty entered
            if not difficultyTemp.get().isnumeric() and difficultyTemp.get() != "":
                difficultyTemp.set("12")
                messagebox.showerror("Error", "Error 003: This is not a valid integer. Please enter a number between 1-33.")
                if difficultyTemp.get() == difficulty.get():
                    RemoveAll("difficulty")
                else:
                    GlobChanges.append("difficulty")
            elif difficultyTemp.get().isnumeric():
                if int(difficultyTemp.get()) < 1 or int(difficultyTemp.get()) > 33:
                    difficultyTemp.set("12")
                    messagebox.showerror("Error", "Error 003: This is not a valid integer. Please enter a number between 1-33.")
                    if difficultyTemp.get() == difficulty.get():
                        RemoveAll("difficulty")
                    else:
                        GlobChanges.append("difficulty")
            else:
                GlobChanges.append("difficulty")
        else:
            RemoveAll("difficulty")
        ChangeApply()
        return


    def SizeCheck(a,b,c):#Applies changes for control scheme
        if sizeSet.get() == sizeSetTemp.get():
            RemoveAll("size")
        else:
            GlobChanges.append("size")
        ChangeApply()
        return

    puzzle = Frame(notebook)
    puzzle.pack()


    difficultyTemp = StringVar()#Using Stringvar, Intvar and Boolvar for all temp variables so they can be traced easily
    difficultyTemp.set(difficulty.get())
    difficultyTemp.trace("w", DiffCheck)

    difficultyLabel = Label(puzzle, text="Difficulty (1-33)", font=("Arial", sizeSet.get()))
    difficultyLabel.grid(row=0, column=0)
    difficultyEnter = Entry(puzzle, textvariable=difficultyTemp, font=("Arial", sizeSet.get()))
    difficultyEnter.grid(row=0, column=1)


    alertsTemp = BooleanVar()
    alertsTemp.set(alerts.get())


    alertsLabel = Label(puzzle, text="Wrong number alerts", font=("Arial", sizeSet.get()))
    alertsLabel.grid(row=1, column=0)
    alertsButton = Checkbutton(puzzle, variable=alertsTemp, command=lambda: StateChange(alertsTemp.get(), "alerts"), font=("Arial", sizeSet.get()))
    alertsButton.grid(row=1, column=1)


    highlightsTemp = BooleanVar()
    highlightsTemp.set(highlights.get())

    highlightsLabel = Label(puzzle, text="Highlight when number entered", font=("Arial", sizeSet.get()))
    highlightsLabel.grid(row=2, column=0)
    highlightsButton = Checkbutton(puzzle, variable=highlightsTemp, command=lambda: StateChange(highlightsTemp.get(), "highlights"), font=("Arial", sizeSet.get()))
    highlightsButton.grid(row=2, column=1)


    appearance = Frame(notebook)#New tab
    appearance.pack()


    colourCellTemp = StringVar()
    colourCellTemp.set(colourCell.get())

    colourCellLabel = Label(appearance, text="Colour of cells", font=("Arial", sizeSet.get())).grid(row=0, column=0)
    colourCellButton = Button(appearance, bg=colourCellTemp.get(), width=3, relief=GROOVE, command=lambda: PickColour("colourCell", colourCellTemp.get()), font=("Arial", sizeSet.get()))
    colourCellButton.grid(row=0, column=1)


    colourHLCursorTemp = StringVar()
    colourHLCursorTemp.set(colourHLCursor.get())

    colourHLCursorLabel = Label(appearance, text="Colour of cursor highlight", font=("Arial", sizeSet.get())).grid(row=1, column=0)
    colourHLCursorButton = Button(appearance, bg=colourHLCursorTemp.get(), width=3, relief=GROOVE,command=lambda: PickColour("colourHLCursor", colourHLCursorTemp.get()), font=("Arial", sizeSet.get()))
    colourHLCursorButton.grid(row=1, column=1)


    colourHLSelectTemp = StringVar()
    colourHLSelectTemp.set(colourHLSelect.get())

    colourHLSelectLabel = Label(appearance, text="Colour of selection highlight", font=("Arial", sizeSet.get())).grid(row=2, column=0)
    colourHLSelectButton = Button(appearance, bg=colourHLSelectTemp.get(), width=3, relief=GROOVE, command=lambda: PickColour("colourHLSelect", colourHLSelectTemp.get()), font=("Arial", sizeSet.get()))
    colourHLSelectButton.grid(row=2, column=1)


    colourHLWrongTemp = StringVar()
    colourHLWrongTemp.set(colourHLWrong.get())

    colourHLWrongLabel = Label(appearance, text="Colour of wrong number highlight", state=BoolToDisabled(alertsTemp.get()), font=("Arial", sizeSet.get()))#State uses DISABLED, boolean uses True/False so BoolToDisabled converts between
    colourHLWrongLabel.grid(row=3, column=0)
    colourHLWrongButton = Button(appearance, bg=colourHLWrongTemp.get(), width=3, relief=GROOVE, state=BoolToDisabled(alertsTemp.get()), command=lambda: PickColour("colourHLWrong", colourHLWrongTemp.get()), font=("Arial", sizeSet.get()))
    colourHLWrongButton.grid(row=3, column=1)


    colourHLOtherTemp = StringVar()
    colourHLOtherTemp.set(colourHLOther.get())

    colourHLOtherLabel = Label(appearance, text="Colour of same number highlight", state=BoolToDisabled(highlightsTemp.get()), font=("Arial", sizeSet.get()))
    colourHLOtherLabel.grid(row=4, column=0)
    colourHLOtherButton = Button(appearance, bg=colourHLOtherTemp.get(), width=3, relief=GROOVE, state=BoolToDisabled(highlightsTemp.get()), command=lambda: PickColour("colourHLOther", colourHLOtherTemp.get()), font=("Arial", sizeSet.get()))
    colourHLOtherButton.grid(row=4, column=1)


    colourLinesTemp = StringVar()
    colourLinesTemp.set(colourLines.get())

    colourLinesLabel = Label(appearance, text="Colour of lines", font=("Arial", sizeSet.get())).grid(row=5, column=0)
    colourLinesButton = Button(appearance, bg=colourLinesTemp.get(), width=3, relief=GROOVE,command=lambda: PickColour("colourLines", colourLinesTemp.get()), font=("Arial", sizeSet.get()))
    colourLinesButton.grid(row=5, column=1)

    colourFonttemp = StringVar()
    colourFonttemp.set(colourFont.get())

    colourFontLabel = Label(appearance, text="Font colour of user entered values", font=("Arial", sizeSet.get())).grid(row=6, column=0)
    colourFontButton = Button(appearance, bg=colourFonttemp.get(), width=3, relief=GROOVE,command=lambda: PickColour("colourFont", colourFonttemp.get()), font=("Arial", sizeSet.get()))
    colourFontButton.grid(row=6, column=1)

    colourValuesTemp = StringVar()
    colourValuesTemp.set(colourValues.get())


    colourValuesLabel = Label(appearance, text="Font colour of locked Sudoku values", font=("Arial", sizeSet.get())).grid(row=7, column=0)
    colourValuesButton = Button(appearance, bg=colourValuesTemp.get(), width=3, relief=GROOVE,command=lambda: PickColour("colourValues", colourValuesTemp.get()), font=("Arial", sizeSet.get()))
    colourValuesButton.grid(row=7, column=1)

    colourMarkTemp = StringVar()
    colourMarkTemp.set(colourMark.get())

    colourMarkLabel = Label(appearance, text="Font colour of marks", font=("Arial", sizeSet.get())).grid(row=8, column=0)
    colourMarkButton = Button(appearance, bg=colourMarkTemp.get(), width=3, relief=GROOVE,command=lambda: PickColour("colourMark", colourMarkTemp.get()), font=("Arial", sizeSet.get()))
    colourMarkButton.grid(row=8, column=1)

    sizeSetTemp = IntVar()
    sizeSetTemp.set(sizeSet.get())
    sizeSetTemp.trace("w", SizeCheck)

    sizeLabel = Label(appearance, text="Font size for user interface:", font=("Arial", sizeSet.get())).grid(row=9, column=0)
    sizeSelection = OptionMenu(appearance, sizeSetTemp, 8,9)#Drop down
    sizeSelection.grid(row=9, column=1)


    notebook.add(puzzle, text="Puzzle", state="normal")#Adding frames to notebook
    notebook.add(appearance, text="Appearance", state="normal")

    return

def InstHelp():
    instructions = Toplevel(root)
    instructions.iconbitmap("pics/thumbnail2.ico") #Replaces tkinter logo

    pages = ttk.Notebook(instructions, width=200) #Notebook same as settings
    pages.grid(row=0, column=0)

    splash = Frame(pages)
    splash.pack()

    splashImage = PhotoImage(file="pics/inst1.gif")
    splashLabel = Label(splash, image=splashImage)
    splashLabel.image = splashImage #Reference makes photo appear
    splashLabel.grid(row=0, column=0)

    splashText = Label(splash, #Text used to show user how to use program
                       text="When starting PySudoku, a splash screen will\nappear while background processes run; these\nare mainly to show the speed of your PC, since\na longer load time corresponds to a slower PC.\nWe recommend only PC's capable of loading\nthe splash screen in 3 or less seconds are\nsuitable for running this program.",
                       font=("Arial", sizeSet.get()))
    splashText.grid(row=1, column=0)

    main = Frame(pages)
    main.pack()

    mainImage = PhotoImage(file="pics/inst2.gif")
    mainLabel = Label(main, image=mainImage)
    mainLabel.image = mainImage
    mainLabel.grid(row=0, column=0)

    mainText = Label(main, #Tried to use wrapping but did not work - manual wrapping
                       text="When PySudoku has loaded, a root window\nwill appear, allowing you to access most\nparts of the program from a centralised\nlocation. These parts are the following:\n• New Sudoku Button - starts new game\n• Load Sudoku Button - loads game from save\ngame/string\n• Print PDF Sudokus Button - prints Sudoku PDFs\n• Instructions Button - shows these instructions\n• File menubar - allows for new blank grids, exiting,\nand loading/new games.\n• Settings menu - loads settings window, to\nchange appearance/function\n• Help menu - allows the user to view instructions,\nor about the programmers.",
                       font=("Arial", sizeSet.get()))
    mainText.grid(row=1, column=0)

    game = Frame(pages)
    game.pack()

    gameImage = PhotoImage(file="pics/inst3.gif")
    gameLabel = Label(game, image=gameImage)
    gameLabel.image = gameImage
    gameLabel.grid(row=0, column=0)

    gameText = Label(game,
                     text="When a game loads, the above window appears.\nIt has the following features:\n• Game window - allows the user to enter\nvalues using the rubber icon to enter values,\nfirst by clicking then by pressing a number,\nand to delete all values in a cell by clicking;\nand using the mark Button to enter small 'mark'\nnumbers at the top of the cell, allowing the user\nto work out values.\n• Difficulty - shows difficulty and estimated 'grade'\n• Timer - shows how long the user has played for\n• Score - shows the user their progress/success.\n• Rubber/mark buttons (respectively) - Allow data to\nbe entered in the game window\n• Hint Button - Gives the value of the next cell, or\n(if errors) shows what values are incorrect.\n• Autosolve Button - Completes the grid for\nthe user, and resets score to 0.\n• New.. menubar - Creates new generated/blank\ngrids\n• Save.. menubar - Allows the current game to be\nsaved\nas either a save game or a string.\n• Print.. menubar - Allows the current grid to be\nprinted or for PDFs to be generated.\n• Exit menubar - Closes game window.\n(Loading games must be done from the main\n'root' window to avoid the program from\ncrashing.",
                     font=("Arial", sizeSet.get()))
    gameText.grid(row=1, column=0)

    print = Frame(pages)
    print.pack()

    printImage = PhotoImage(file="pics/inst5.gif")
    printLabel = Label(print, image=printImage)
    printLabel.image = printImage
    printLabel.grid(row=0, column=0)

    printText = Label(print,
                     text="When printing multiple grids, this window appears.\nFrom here, the number of grids, number of grids\nper page, difficulty and upper corner logo\ncan all be changed. The latter is done\nthrough 'browsing' for a picture, after which a\nthumbnail will appear in the window.\nFinally, a print preview is provided which allows\nthe user to scroll between the pages of their\ndocument, and visualise what the final product\nwill be like.",
                     font=("Arial", sizeSet.get()))
    printText.grid(row=1, column=0)

    settings = Frame(pages)
    settings.pack()

    settingsImage = PhotoImage(file="pics/inst4.gif")
    settingsLabel = Label(settings, image=settingsImage)
    settingsLabel.image = settingsImage
    settingsLabel.grid(row=0, column=0)

    settingsText = Label(settings,
                      text="When the 'Settings' buttons are pressed, this\nwindow appears. From here, multiple settings,\nsuch as showing errors, highlights, changing\ndifficulty changing the colour of the game\nwindow and changing the font size. This is done\nby:\n• entering a valid number for difficulty\n• checking boxes for errors/highlights\n• clicking the coloured buttons then selecting a\ncolour for changing highlight colours\n• selecting one of the font sizes from the drop down\nlist.\nThese settings are then finalised with the 'Apply'\nButton, or cancelled with the 'Cancel' Button.",
                      font=("Arial", sizeSet.get()))
    settingsText.grid(row=1, column=0)

    pages.add(splash, text="Splash screen", state="normal")
    pages.add(main, text="Main menu", state="normal")
    pages.add(game, text="Game window", state="normal")
    pages.add(print, text="Print window", state="normal")
    pages.add(settings, text="Settings window", state="normal")

    close = Button(instructions, text="Close window", command=instructions.destroy, font=("Arial", sizeSet.get()))
    close.grid(row=1, column=0)
    return

def AboutHelp():

    about = Toplevel()

    about.iconbitmap("pics/thumbnail2.ico")

    aboutInfo = Label(about, text="Created by Jack Parkinson as part of\nY13 Computer Science Unit 3 Coursework.\nAll rights reserved (2017)", font=("Arial", sizeSet.get()))#Translations omitted
    aboutInfo.grid(row=0, column=0)

    aboutClose = Button(about, text="Close", command=about.destroy, font=("Arial", sizeSet.get()))
    aboutClose.grid(row=1, column=0)

    return

def PreLoadSudoku():

    preLoad = Toplevel(root)
    preLoad.iconbitmap("pics/thumbnail2.ico")

    printSave = Button(preLoad, text="From save game..", command=lambda: LoadSudoku("save"), font=("Arial", sizeSet.get()))
    printSave.grid(row=0, column=0)
    printString = Button(preLoad, text="From string..", command=lambda: LoadSudoku("string"), font=("Arial", sizeSet.get()))
    printString.grid(row=1, column=0)
    return






#MAIN PROGRAM INIT.------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def CloseRoot():
    if messagebox.askokcancel("PySudoku", "Do you want to close PySudoku? This will close all currently open games, print windows and will stop PDF generation."):
        root.destroy()




#Splashscreen used from stack overflow with variable changes/changes to layout
root = Tk()

# get screen width and height
ws = 700
hs = 300
# calculate position x, y
wp = (root.winfo_screenwidth() - 700) / 2
hp = (root.winfo_screenheight() - 300) / 2
root.geometry('%dx%d+%d+%d' % (ws, hs, wp, hp))

root.overrideredirect(True) #Makes window non-closeable and borderless
logoSplash = PhotoImage(file="pics/logo.gif") #Main splash menu has larger logo
photoSplash = Label(root, image=logoSplash)
photoSplash.image = logoSplash
photoSplash.grid(row=0, column=0, columnspan=4)

root.config(bg="#F0F0F0")#Logo background same as generic Windows basic background colour

labelSplash = Label(root, text="Designed by Jack Parkinson.\nFree and open source. All rights reserved (2017)", justify=RIGHT, fg="gray60")#Makes program look more professional
labelSplash.grid(row=1, column=3)

for iter in range(50000):#Gives the program a wait period equivalent to speed of computer - threading makes this window not have any purpose but visual since no loading is done in background
    root.update()
    root.update_idletasks()
    root.lift()#Bring to top of open windows

root.withdraw()#Root disappears
root.geometry("")
root.overrideredirect(False)#Reset normal layout of Tkinter window for root
root.resizable(0,0)

for widget in root.grid_slaves():
    widget.grid_forget()#Remove all current widgets in root





root.title("PySudoku")#Removes 'tkinter' branding from top of window

#Settings variable setup
difficulty = StringVar() #Stringvar to avoid invalid literal for int() with base 10: ''
difficulty.set("12")

alerts = BooleanVar()
alerts.set(TRUE)

highlights = BooleanVar()
highlights.set(TRUE)

colourCell = StringVar()
colourCell.set("#ffffff")

colourHLCursor = StringVar()
colourHLCursor.set("#bebeff")

colourHLSelect = StringVar()
colourHLSelect.set("#beffff")

colourHLWrong = StringVar()
colourHLWrong.set("#ffbebe")

colourHLOther = StringVar()
colourHLOther.set("#ffffbe")

colourLines = StringVar()
colourLines.set("#000000")

colourFont = StringVar()
colourFont.set("#000000")

colourValues = StringVar()
colourValues.set("#4A4A5A")

colourMark = StringVar()
colourMark.set("#FF0000")

sizeSet = IntVar()
sizeSet.set(9)

#Menu
mainBar = Menu(root)

fileMenu = Menu(mainBar, tearoff=0)#Within file menu \/

newMenu = Menu(fileMenu, tearoff=0)
newMenu.add_command(label="Game..", command=lambda: LoadSudoku("new"), font=("Arial", sizeSet.get()))#Within new game submenu \/
newMenu.add_command(label="Blank grid..", command=lambda: LoadSudoku("blank"), font=("Arial", sizeSet.get()))
fileMenu.add_cascade(label="New..", menu=newMenu, font=("Arial", sizeSet.get()))

loadMenu = Menu(fileMenu, tearoff=0)
loadMenu.add_command(label="From save game..", command=lambda: LoadSudoku("save"), font=("Arial", sizeSet.get()))#Within load submenu \/
loadMenu.add_command(label="From string..", command=lambda: LoadSudoku("string"), font=("Arial", sizeSet.get()))
fileMenu.add_cascade(label="Load..", menu=loadMenu, font=("Arial", sizeSet.get()))
fileMenu.add_separator()
fileMenu.add_command(label="Print PDF", command = PrintSudoku, font=("Arial", sizeSet.get()))
fileMenu.add_command(label="Exit", command=CloseRoot, font=("Arial", sizeSet.get()))
mainBar.add_cascade(label="File", menu=fileMenu, font=("Arial", sizeSet.get()))

mainBar.add_command(label="Settings", command=Settings, font=("Arial", sizeSet.get()))#One settings menu used

helpMenu = Menu(mainBar, tearoff=0)
helpMenu.add_command(label="Instructions", command=InstHelp, font=("Arial", sizeSet.get()))#Within help menu \/
helpMenu.add_separator()
helpMenu.add_command(label="About", command=AboutHelp, font=("Arial", sizeSet.get()))
mainBar.add_cascade(label="Help", menu=helpMenu, font=("Arial", sizeSet.get()))

root.config(menu=mainBar)#Reference makes menu appear

#GUI layout
logo = PhotoImage(file="pics/logosmall.gif")#Logo
photo = Label(root, image=logo)
photo.image = logo#Reference makes photo appear
photo.grid(row=0, column=0, columnspan=2)

#Graphical user interface

new = Button(root, text="New Sudoku", command=lambda: LoadSudoku("new"), width=15, font=("Arial", sizeSet.get())).grid(row=1, column=0, pady=2, padx=2)
load = Button(root, text="Load Sudoku", command=PreLoadSudoku, width=15, font=("Arial", sizeSet.get())).grid(row=1, column=1, pady=2, padx=2)
print = Button(root, text="Print PDF Sudokus", command=PrintSudoku, width=15, font=("Arial", sizeSet.get())).grid(row=2, column=0, pady=2, padx=2)
help = Button(root, text="Instructions", command=InstHelp, width=15, font=("Arial", sizeSet.get())).grid(row=2, column=1, pady=2, padx=2)

root.protocol("WM_DELETE_WINDOW", CloseRoot)
root.deiconify() #Makes root appear
root.iconbitmap("pics/thumbnail2.ico") #Sets icon as logo rather than tkinter logo

mainloop()
