#########################################################
# NAME: Matt Stokes
# COURSE: ICS4U
# FILE: Minesweeper_MattStokes.py
# DESCRIPTION: Minesweeper with I/O, custom dimensions, left and right click, and more!
#########################################################
from tkinter import *
from tkinter import messagebox #For error messages
from pathlib import Path #To check to see if the file exists
from random import randint #Random number generator
import time #For timer

class application:
    highscore = [] #First spot is score, second is name
    maxNum = 25 #Max number of rows and columns for custom option
    numRows = 9
    numColumns = 9
    curName = "" #Name of current user
    numBombs = 5
    l = [] #List with numbers for game grid
    d = [] #List to keep track on how close the user is to winning
    b = [] #List with all the bomb locations
    f = [] #List with all the frames in the game grid
    timer = 0
    run = "" #Keep track of the .after for the timer
    ending = 0 #Win or lose ending
    numZeros = 0
    #########################################################
    # FCN NAME: __init__
    # DESCRIPTION: Bring in all previous highscores
    # INPUTS: self - the class variables
    # OUTPUTS: none
    # ALGORITHM:
    #   IF there is a 'highscore.txt' file
    #       Append all highscores to class list 'highscore'
    #   CALL self.options()
    ########################################################
    def __init__(self):
        #Bring in all previous high scores
        theFile = Path("highscore.txt")
        if theFile.is_file():
            numScores = sum(1 for line in open('highscore.txt'))//2 #Number of previous highscores
            with open("highscore.txt", "r") as inFile:
                for a in range(numScores):
                    self.highscore.append([])
                    c = 0
                    for b in inFile:
                        self.highscore[a].append(b.strip())
                        if(c == 0):
                            self.highscore[a][c] = int(self.highscore[a][c])
                        c+=1
                        if(c == 2):
                            break
        self.options()
    #########################################################
    # FCN NAME: options
    # DESCRIPTION: To provide the user with the setup options
    # INPUTS: self -
    # OUTPUTS: none
    # ALGORITHM:
    #   CREATE first window
    #   BIND enter key to the same function as the start buttons
    #   CREATE widgets for various options
    #   CREATE buttons to either start the game or quit
    ########################################################
    def options(self):
        #########################################################
        # FCN NAME: entered
        # DESCRIPTION: To allow the user to press the enter key to continue
        # INPUTS: event - the event (enter key)
        # OUTPUTS: none
        # ALGORITHM:
        #   CALL testStart()
        ########################################################
        def entered(event):
            testStart()
        #########################################################
        # FCN NAME: testStart
        # DESCRIPTION: To test the inputted values
        # INPUTS: none
        # OUTPUTS: none
        # ALGORITHM:
        #   TRY
        #       IF the mode is custom
        #           TEST number of rows, number of columns, number of bombs
        #       IF TEST name
        #           ERRORBOX
        #       ELSE
        #           SET number of columns, rows, bombs, name
        #       DESTROY window
        #       CALL createGame()
        #   EXCEPT
        #       ERRORBOX
        ########################################################
        def testStart():
            bad = False
            try:
                rows = int(numRows.get())
                columns = int(numColumns.get())
                bombs = int(numBombs.get())
                if(modeNum.get() == 4):
                    if(rows > self.maxNum or columns > self.maxNum): #Cannot exceed max dimensions
                        bad = True
                        messagebox.showerror("Invalid Number", "There is a maximum of %d rows and %d columns." % (self.maxNum, self.maxNum))
                    elif(rows < 2 or columns < 2): #Must have at least 2x2 dimensions
                        bad = True
                        messagebox.showerror("Invalid Number", "There is a minimum of 2 rows and 2 columns.")
                    elif(bombs >= rows * columns or bombs < 1): #Validate number of bombs
                        bad = True
                        messagebox.showerror("Invalid Number", "There must be between 1 and %d bombs" % (rows * columns - 1))
                if(curName.get() == ""): #Validate a name
                    messagebox.showerror("Invalid Name", "Please enter your name.")
                elif(bad == False): #If no errors
                    #set the right values to the class variables
                    if(modeNum.get() == 0):
                        self.numRows = 9
                        self.numColumns = 9
                        self.numBombs = 9
                    elif(modeNum.get() == 1):
                        self.numRows = 12
                        self.numColumns = 12
                        self.numBombs = 20
                    elif(modeNum.get() == 2):
                        self.numRows = 15
                        self.numColumns = 15
                        self.numBombs = 40
                    elif(modeNum.get() == 3):
                        self.numRows = 15
                        self.numColumns = 15
                        self.numBombs = 224
                    else:
                        self.numRows = rows
                        self.numColumns = columns
                        self.numBombs = bombs

                    first.destroy()
                    self.curName = curName.get()
                    self.createGame()
            except: #The user entered non-integer values
                messagebox.showerror("Invalid Entry", "Please enter integer values under the custom options")
        #########################################################
        # FCN NAME: newOptions
        # DESCRIPTION: toggle the customizable entries
        # INPUTS: none
        # OUTPUTS: none
        # ALGORITHM:
        #   IF user chose custom
        #       PACK all widgets
        #   ELSE
        #       FORGET all widgets
        ########################################################
        def newOptions():
            if(modeNum.get() == 4):
                #Show custom options
                rowL.pack(side = LEFT)
                rowO.pack(side = LEFT)
                columnL.pack(side = LEFT)
                columnO.pack(side = LEFT)
                bombL.pack(side = LEFT)
                bombE.pack(side = LEFT)
            else:
                #Hide custom options
                rowL.pack_forget()
                rowO.pack_forget()
                columnL.pack_forget()
                columnO.pack_forget()
                bombL.pack_forget()
                bombE.pack_forget()
        first = Tk()
        first.title('Game Setup')
        first.bind("<Return>", entered) #Allow the user to press enter to start
        first.geometry("235x250") #Window dimensions

        modeF = Frame(first)
        modeF.pack()
        modeNum = IntVar(modeF)
        modeNum.set(0)
        modeR = []
        #Game modes
        for x in range(5):
            modeR.append(Radiobutton(modeF, variable = modeNum, value = x, command = newOptions))
            modeR[x].pack()
        modeR[0].configure(text = "Easy")
        modeR[1].configure(text = "Intermediate")
        modeR[2].configure(text = "Expert")
        modeR[3].configure(text = "Impossible")
        modeR[4].configure(text = "Custom")
        #Rows
        rowF = Frame(first)
        rowF.pack()
        rowL = Label(rowF, text = "Number of rows")
        numRows = IntVar(rowF)
        numRows.set(self.numRows)
        rowO = Entry(rowF, textvariable = numRows, width = 8)
        #Columns
        columnF = Frame(first)
        columnF.pack()
        columnL = Label(columnF, text = "Number of columns")
        numColumns = IntVar(columnF)
        numColumns.set(self.numColumns)
        columnO = Entry(columnF, textvariable = numColumns, width = 7)
        #Number of bombs
        bombF = Frame(first)
        bombF.pack()
        bombL = Label(bombF, text = "Number of bombs")
        numBombs = IntVar(bombF)
        numBombs.set(self.numBombs)
        bombE = Entry(bombF, textvariable = numBombs, width = 8)
        #Name
        nameF = Frame(first)
        nameF.pack()
        nameL = Label(nameF, text = "Name")
        nameL.pack(side = LEFT)
        curName = StringVar(nameF)
        nameE = Entry(nameF, textvariable = curName)
        nameE.pack(side = LEFT)
        nameE.focus_set()
        #Start and quit
        buttonF = Frame(first)
        buttonF.pack()
        buttonS = Button(buttonF, text = "Start", command = testStart)
        buttonS.pack(side = LEFT)
        buttonI = Button(buttonF, text = "Instructions", command = self.Rules)
        buttonI.pack(side = LEFT)
        buttonQ = Button(buttonF, text = "Quit", command = lambda: first.destroy())
        buttonQ.pack(side = RIGHT)

        first.mainloop()
    #########################################################
    # FCN NAME: createGame
    # DESCRIPTION: create and calculate all values needed for the game
    # INPUTS: self
    # OUTPUTS: none
    # ALGORITHM:
    #   APPEND 0 to all spots in l list
    #   APPEND coordinates of each point to d list
    #   FOR q in numBombs
    #       CREATE two random numbers and APPEND to b list
    #       IF that spot already has a bomb, POP b then CONTINUE
    #       SET the coordinate in l list to 9 and INCREMENT all adjacent spots in the list
    #   SORT b - so that it can be compared to d, to see if the user wins
    #   INCREMENT self.numZeros for each zero in self.l
    #   CALL game()
    ########################################################
    def createGame(self):
        #Start all numbers in the grid at 0 bombs adjacent to its location
        for x in range(self.numRows):
            self.l.append([])
            for y in range(self.numColumns):
                self.l[x].append(0)
                self.d.append([x, y])
        q = 0
        while q < self.numBombs:
            bad = False #Reset variable
            #Generate two random coordinates for the bomb
            self.b.append([randint(0, self.numRows-1), randint(0, self.numColumns-1)])
            #Check to see if the coordinate is already in the list of bomb locations
            for y in range(q):
                if(self.b[y][0] == self.b[q][0] and self.b[y][1] == self.b[q][1]):
                    bad = True
                    break #If found, break
            if(bad == True):
                self.b.pop() #Pop it from the list if it is already there
                continue #Skip everything else in the loop
            self.l[self.b[q][0]][self.b[q][1]] = 9 #Set the bomb location to 9
            #Make sure the program doesn't crash if the bomb is near a border of the grid
            if(self.b[q][0] - 1 > 0):
                firstF = self.b[q][0] - 1
            else:
                firstF = 0
            if(self.b[q][1] - 1 > 0):
                firstS = self.b[q][1] - 1
            else:
                firstS = 0
            if(self.b[q][0] + 2 <= self.numRows):
                secondF = self.b[q][0] + 2
            else:
                secondF = self.numRows
            if(self.b[q][1] + 2 <= self.numColumns):
                secondS = self.b[q][1] + 2
            else:
                secondS = self.numColumns
            #Increment all adjacent spots to the bomb's location
            for m in range(firstF, secondF):
                for n in range(firstS, secondS):
                    if(self.l[m][n] != 9):
                        self.l[m][n]+=1
            q+=1 #Increment q
        self.b.sort(key = lambda l: (l[0], l[1])) #Sort the bomb locations to be comparable to self.d
        #Find the number of zeros for scoring purposes
        for x in range(len(self.l)):
            for y in range(len(self.l[x])):
                if(self.l[x][y] == 0):
                    self.numZeros+=1
        self.game()
    #########################################################
    # FCN NAME: Rules
    # DESCRIPTION: show instructions and rules
    # INPUTS: none
    # OUTPUTS: none
    # ALGORITHM:
    #   ruleText EQUALS rules
    #   CREATE top window
    #   FOCUS on top window
    #   CREATE widgets, including button to close
    ########################################################
    def Rules(self):
        ruleText = """Minesweeper Instructions and Help

How to play
        Goal of the game
                The goal of the game is to click on all of the buttons that don't contain bombs. Left-clicking a bomb will result in a Game Over.
                If all buttons except for those containing bombs are clicked, a new window screen will appear, giving you your score as well as
                all of the high scores.

        What the game looks like
                Uniform buttons fill up the dimensions of the grid.
                When you left-click on a button one of three things will happen:
                        1. A number will appear in place of the button, representing the number of bombs in the adjacent spots (including diagonals).
                        2. A blank spot will appear, showing that there are no bombs in surrounding buttons. All adjacent blank spots, and all
                           adjacent numbers to the blank spots, will be revealed.
                        3. A capital 'B' will appear, representing a bomb. This is a GAME OVER.
                When you right-click on a button one of two things will happen:
                        1. A capital 'D' will appear, showing that you have defused a bomb.
                        2. A number or blank spot will appear. This is a GAME OVER.

        Score System
                100 points are awarded for each bomb present in the current game.
                The amount of time it takes to win is subtracted from the total points.
                You only get points if you successfully left-click on all buttons that don't contain bombs.

        Setup
                In easy mode, it is a 9x9 grid with 9 bombs.
                In intermediate mode, it is a 12x12 grid with 20 bombs.
                In expert mode, it is a 15x15 grid with 40 bombs.
                In impossible mode, it is a 15x15 grid with 224 bombs.
                In custom mode, you get to choose how many rows, columns, and bombs.
                        The maximum number of rows and columns is 25 each.
                        The minimum number of rows and columns is 2 each.
                        The maximum number of bombs is the total number of buttons in the grid minus one. There must be some way for you to win!
                        The minimum number of bombs is 1."""
        top = Tk()
        top.focus_force()
        instructionsT = Label(top, text = ruleText, justify = LEFT)
        instructionsT.pack()
        quitB = Button(top, text = "Close", command = lambda: top.destroy())
        quitB.pack()
        top.mainloop()
    #########################################################
    # FCN NAME: game
    # DESCRIPTION: The gui of the game
    # INPUTS: self -
    # OUTPUTS: none
    # ALGORITHM:
    #   CREATE root window
    #   FOCUS on root window
    #   CREATE widgets for timer, instructions, and quit
    #   FOR x in RANGE numRows
    #       APPEND g, d, f for 2d list
    #       FOR y in RANGE numRows[x]
    #           APPEND frame to f, GRID and GRID PROPOGATE it
    #           APPEND button to g and PACK it
    #           BIND left click and right click to the button
    #   CALL updateTimer()
    ########################################################
    def game(self):
        #########################################################
        # FCN NAME: scoreW
        # DESCRIPTION: the highscore window
        # INPUTS: none
        # OUTPUTS: none
        # ALGORITHM:
        #   CREATE score window
        #   CREATE widgets to show title and subtitles
        #   CREATE labels for the top 5 highscores
        #   CREATE buttons for various options
        #   CREATE label for the user's score
        ########################################################
        def scoreW():
            #########################################################
            # FCN NAME: clearIt
            # DESCRIPTION: reset the variables
            # INPUTS: num - the function to go to after clearing values
            # OUTPUTS: none
            # ALGORITHM:
            #   DESTROY windows
            #   CLEAR lists, timer, run
            #   IF num EQUALS 0 then reset game with the same values
            #   ELSE go back to options screen
            ########################################################
            def clearIt(num):
                #If the user already closed one of the windows then just pass
                try:
                    self.root.destroy()
                except:
                    pass
                try:
                    score.destroy()
                except:
                    pass
                #Reset all needed variables
                self.l = []
                self.d = []
                self. b = []
                self.f = []
                self.timer = 0
                self.run = ""
                if(num == 0): #Play again
                    self.createGame()
                else: #Setup game
                    self.options()
            #########################################################
            # FCN NAME: done
            # DESCRIPTION: destroy all windows
            # INPUTS: none
            # OUTPUTS: none
            # ALGORITHM:
            #   DESTROY windows
            ########################################################
            def done():
                #If the user already closed one of the windows then just pass
                try:
                    self.root.destroy()
                except:
                    pass
                try:
                    score.destroy()
                except:
                    pass
            score = Tk()
            score.focus_force()
            score.title('Highscores')
            score.geometry("400x300") #Set dimensions
            if(self.ending == 0):
                words = "Game over!"
            else:
                words = "You win!"
            #Title
            label = Label(score, text = words, font = "Verdana 18")
            label.pack()
            labelS = Label(score, text = "Highscores", font = "Verdana 14")
            labelS.pack()
            scoreF = Frame(score)
            scoreF.pack()
            #Subtitles
            titleN = Label(scoreF, text = "Number", font = "Verdana 12 bold", bd = 4)
            titleN.grid(row = 0, column = 0)
            titleL = Label(scoreF, text = "Player name", font = "Verdana 12 bold", bd = 4)
            titleL.grid(row = 0, column = 1)
            titleR = Label(scoreF, text = "Score", font = "Verdana 12 bold", bd = 4)
            titleR.grid(row = 0, column = 2)
            h = []
            #Top 5 highscores, or less if there are less than 5 previous scores.
            for x in range(len(self.highscore)):
                h.append([])
                for y in range(len(self.highscore[x]) + 1):
                    if(y == 0):
                        tText = x + 1 #First column is position on scoreboard
                    elif(y == 1):
                        tText = self.highscore[x][y] #Second is name
                    else:
                        tText = self.highscore[x][y - 2] #Third is score
                    h[x].append(Label(scoreF, text = tText, font = "Verdana 12"))
                    h[x][y].grid(row = x + 1, column = y)
                    #If the name is the same as the current user make it red and bold
                    if(self.highscore[x][y - 1] == self.curName):
                        for z in range(len(h[x])):
                            h[x][z].configure(fg = "red", font = "Verdana 12 bold")
                if(x == 4):
                    #Break to only show top 5
                    break
            #Button options
            buttonF = Frame(score)
            buttonF.pack(side = BOTTOM)
            buttonA = Button(buttonF, text = "Play again", command = lambda : clearIt(0))
            buttonA.pack(side = LEFT)
            buttonS = Button(buttonF, text = "Setup game", command = lambda: clearIt(1))
            buttonS.pack(side = LEFT)
            global app
            buttonQ = Button(buttonF, text = "Quit", command = done)
            buttonQ.pack(side = LEFT)
            #If the user won, show their score too.
            if(self.ending == 1):
                youF = Frame(score)
                youF.pack(side = BOTTOM)
                youL = Label(youF, text = "You", fg = "red", font = "Verdana 12 bold", bd = 4)
                youL.pack(side = LEFT)
                youS = Label(youF, text = self.numBombs * 100 - self.timer - self.numZeros, fg = "red", font = "Verdana 12 bold", bd = 4)
                youS.pack(side = LEFT)
            score.mainloop()
        #########################################################
        # FCN NAME: click
        # DESCRIPTION: test values after user clicks a button in the game
        # INPUTS:   event - the event(clicking)
        #           r - the row clicked
        #           c - the column clicked
        #           num - the button clicked (left or right)
        # OUTPUTS: none
        # ALGORITHM:
        #   IF bombs is clicked
        #       DESTROY button
        #       IF left click
        #           SET color and show all numbers and bombs
        #           STOP timer
        #           ending EQUALS 0
        #           CALL scoreW()
        #       ELSE
        #           CREATE button with the letter D
        #   ELSE
        #       IF left click
        #           IF the number isn't 0
        #               Set the color according to the number
        #               DESTROY button and CREATE label with appropriate number
        #               TRY to remove coordinate from d, then update the list
        #               EXCEPT PASS
        #           ELSE - number is 0
        #               CLEAR all adjacent 0s and numbers adjacent to each 0
        #               CREATE label with appropriate number and color
        #           CALL updateList()
        #           IF the buttons remaining are all bombs
        #               IF highscore LESS THAN 0
        #                   highscore EQUALS 0
        #               APPEND highscore and name to listItems
        #               CALL win()
        #       ELSE
        #           SET color and show all numbers and bombs
        #           STOP timer
        #           ending EQUALS 0
        #           CALL scoreW()
        ########################################################
        def click(event, r, c, num):
            def win():
                #Disable all remaining bomb buttons
                for x in range(len(self.b)):
                    y, z = self.b[x][0], self.b[x][1]
                    g[y][z].configure(state = DISABLED, text = "B")
                self.root.after_cancel(self.run) #Stop timer
                self.ending = 1
                #Output user name and score to the file
                with open("highscore.txt", mode = 'wt', encoding = 'utf-8') as outFile:
                    for a in self.highscore:
                        for b in a:
                            outFile.write(str(b) + '\n')
                scoreW()
            def updateList():
                #Clear all empty lists within the 2d list
                newD = [x for x in self.d if x != []]
                self.d = newD
            if(self.l[r][c] == 9): #If a bomb is clicked
                if(num == 1): #If it is a left click
                    #User loses, show all numbers and bombs
                    for a in range(len(self.l)):
                        for b in range(len(self.l[a])):
                            #Colors for each number
                            if(self.l[a][b] == 1):
                                color = "#0000FF"
                            elif(self.l[a][b] == 2):
                                color = "#00FF00"
                            elif(self.l[a][b] == 3):
                                color = "#FF0000"
                            elif(self.l[a][b] == 4):
                                color = "#000099"
                            elif(self.l[a][b] == 5):
                                color = "#8C001A"
                            elif(self.l[a][b] == 6):
                                color = "#00FFFF"
                            elif(self.l[a][b] == 7):
                                color = "#000000"
                            elif(self.l[a][b] == 8):
                                color = "#FFD700"
                            else:
                                color = "#808080"
                                tText = "B"
                            g[a][b].destroy()
                            if(self.l[a][b] == 0):
                                tText = " "
                            elif(self.l[a][b] != 9):
                                tText = self.l[a][b]
                            g[a][b] = Label(self.f[a][b], text = tText, padx = 7, pady = 3.2, fg = color)
                            g[a][b].pack()
                    self.root.after_cancel(self.run) #Stop timer
                    self.ending = 0
                    scoreW()
                else: #If right click
                    '''
                    Create a button with D, bomb defused. Kept as a button
                    because, when testing, it is easier to forget about defused
                    bombs when they turn into labels.
                    '''
                    g[r][c].destroy()
                    g[r][c] = Button(self.f[r][c], text = "D", fg = "orange", width = 2, height = 1)
                    g[r][c].pack()
            else: #Button clicked is not a bomb
                if(num == 1): #If left click
                    if(self.l[r][c] != 0): #If the number is not 0
                        #Set color
                        if(self.l[r][c] == 1):
                            color = "#0000FF"
                        elif(self.l[r][c] == 2):
                            color = "#00FF00"
                        elif(self.l[r][c] == 3):
                            color = "#FF0000"
                        elif(self.l[r][c] == 4):
                            color = "#000099"
                        elif(self.l[r][c] == 5):
                            color = "#8C001A"
                        elif(self.l[r][c] == 6):
                            color = "#00FFFF"
                        elif(self.l[r][c] == 7):
                            color = "#000000"
                        else:
                            color = "#808080"
                        #Create a label with the appropriate number
                        g[r][c].destroy()
                        g[r][c] = Label(self.f[r][c], text = self.l[r][c], padx = 7, pady = 3.2, fg = color)
                        g[r][c].pack()
                        #Try to remove, if it doesn't work then it was already removed.
                        try:
                            self.d.remove([r, c])
                            updateList()
                        except:
                            pass
                    else: #If the number is 0
                        spot = [[r, c]] #List for all zeros found, start with current
                        done = [] #List for all coordinates cleared
                        while(len(spot) > 0): #Until there are no more zeros to clear adjacent spots
                            #To avoid crashing if zero is near a border of the grid
                            if(spot[0][0] - 1 > 0):
                                r1 = spot[0][0] - 1
                            else:
                                r1 = 0
                            if(spot[0][1] - 1 > 0):
                                c1 = spot[0][1] - 1
                            else:
                                c1 = 0
                            if(spot[0][0] + 2 <= self.numRows):
                                r2 = spot[0][0] + 2
                            else:
                                r2 = self.numRows
                            if(spot[0][1] + 2 <= self.numColumns):
                                c2 = spot[0][1] + 2
                            else:
                                c2 = self.numColumns
                            #Clear all adjacent spots (including diagonals)
                            for m in range(r1, r2):
                                for n in range(c1, c2):
                                    stop = False
                                    for x in range(len(done)):
                                        #If that zero was already found, skip.
                                        #Otherwise, it could be an infinite loop.
                                        if(done[x] == [m, n]):
                                            stop = True
                                            break
                                    if(stop == True):
                                        #Skip the rest of the loop
                                        continue
                                    elif(self.l[m][n] == 0):
                                        #Add the zero to the list of spots to clear adjacent ones
                                        spot.append([m, n])
                                        self.l[m][n] = "  "
                                    done.append([m, n])
                                    g[m][n].destroy()
                                    #Set color
                                    if(self.l[m][n] == 1):
                                        color = "#0000FF"
                                    elif(self.l[m][n] == 2):
                                        color = "#00FF00"
                                    elif(self.l[m][n] == 3):
                                        color = "#FF0000"
                                    elif(self.l[m][n] == 4):
                                        color = "#000099"
                                    elif(self.l[m][n] == 5):
                                        color = "#8C001A"
                                    elif(self.l[m][n] == 6):
                                        color = "#00FFFF"
                                    elif(self.l[m][n] == 7):
                                        color = "#000000"
                                    else:
                                        color = "#808080"
                                    g[m][n] = Label(self.f[m][n], text = self.l[m][n], padx = 7, pady = 3, fg = color)
                                    g[m][n].pack()
                                    g[m][n].grid_propagate(0)
                            spot.pop(0) #Pop the current zero from the list because it is done
                        for x in done:
                            try:
                                '''Remove all cleared numbers from the d list.
                                The purpose of the d list is so that when all buttons
                                except for the bombs are clicked, the d list will be
                                the same as the list of bombs, making the statement a
                                few lines down true.
                                '''
                                self.d.remove(x)
                            except:
                                #Skip the rest of the loop
                                continue
                        #Clear the lists
                        del spot
                        del done
                    updateList()
                    if(self.d == self.b): #User wins
                        #Add the user to the highscore list
                        scoreNum = self.numBombs * 100 - self.timer - self.numZeros
                        if(scoreNum < 0):
                            scoreNum = 0
                        self.highscore.append([scoreNum, self.curName])
                        #Sort it by score, reversed so that the largest is first
                        self.highscore.sort(key = lambda l:l[0], reverse=True)
                        win()
                else: #If right click
                    #Show all numbers and bombs
                    for a in range(len(self.l)):
                        for b in range(len(self.l[a])):
                            if(self.l[a][b] == 1):
                                color = "#0000FF"
                            elif(self.l[a][b] == 2):
                                color = "#00FF00"
                            elif(self.l[a][b] == 3):
                                color = "#FF0000"
                            elif(self.l[a][b] == 4):
                                color = "#000099"
                            elif(self.l[a][b] == 5):
                                color = "#8C001A"
                            elif(self.l[a][b] == 6):
                                color = "#00FFFF"
                            elif(self.l[a][b] == 7):
                                color = "#000000"
                            elif(self.l[a][b] == 8):
                                color = "#FFD700"
                            else:
                                color = "#808080"
                                tText = "B"
                            g[a][b].destroy()
                            if(self.l[a][b] == 0):
                                tText = " "
                            elif(self.l[a][b] != 9):
                                tText = self.l[a][b]
                            g[a][b] = Label(self.f[a][b], text = tText, padx = 7, pady = 3.2, fg = color)
                            g[a][b].pack()
                    self.root.after_cancel(self.run) #Stop timer
                    self.ending = 0
                    scoreW()
        #########################################################
        # FCN NAME: updateTimer
        # DESCRIPTION: update the timer
        # INPUTS: none
        # OUTPUTS: none
        # ALGORITHM:
        #   INCREMENT timer
        #   update timer text
        #   Re-CALL this function after one second
        ########################################################
        def updateTimer():
            #Add to the timer every second and update the text in the widget
            self.timer+= 1
            timerL.configure(text = self.timer)
            self.run = self.root.after(1000, updateTimer)
        self.root = Tk()
        self.root.title('Minesweeper')
        self.root.focus_force() #Focus on this window

        otherF = Frame(self.root)
        otherF.pack(side = LEFT)
        oNameF = Frame(otherF)
        oNameF.pack(side = TOP)
        nameL = Label(oNameF, text = "Name: ")
        nameL.pack(side = LEFT)
        nameR = Label(oNameF, text = self.curName)
        nameR.pack(side = LEFT)
        timerL = Label(otherF, text = self.timer)
        timerL.pack(anchor = N)
        instructionsB = Button(otherF, text = "Instructions", command = self.Rules)
        instructionsB.pack()
        quitB = Button(otherF, text = "Quit", command = lambda: self.root.destroy())
        quitB.pack()

        gameF = Frame(self.root)
        gameF.pack(side = LEFT)
        g = []
        for x in range(self.numRows):
            g.append([])
            self.d.append([])
            self.f.append([])
            for y in range(self.numColumns):
                self.f[x].append(Frame(gameF, height = 50, width = 50))
                self.f[x][y].grid(row = x, column = y)
                self.f[x][y].grid_propagate(0)
                g[x].append(Button(self.f[x][y], text = " ", width = 2, height = 1))
                g[x][y].pack()
                g[x][y].bind("<Button-3>", lambda event, x=x, y=y: click(event, x, y, 3))
                g[x][y].bind("<Button-1>", lambda event, x=x, y=y: click(event, x, y, 1))
        updateTimer()
        self.root.mainloop()
app = application()
