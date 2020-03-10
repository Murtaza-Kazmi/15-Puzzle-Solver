from tkinter import *
import numpy as np
import sys

sys.setrecursionlimit(10000)

#window specs
window = Tk()
window.title("15-Puzzle Solver")
window.geometry("500x400")
window.configure(background='dark slate gray')
        
buttonfont =("Comic Sans MS", "11")

txt = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',' ']

#grid of 4 x 4
class grid4by4(Frame):
    def __init__(self, window):
        super().__init__(window)
        self.buttons = [None] * 16
        self.create_widgets()
        self.pack()
    def create_widgets(self):
        for r in range(4):  #row
            for c in range(4):  #column
                self.c_button(r * 4 + c, r, c)

    #Create the button and appends to buttons list
    def c_button(self, index, r, c):
        txttoplace = txt.pop(0)
        self.buttons[index] = Label(self,bg="dodger blue", borderwidth = 2, relief  = 'solid', text = txttoplace, justify = LEFT, font=buttonfont, width=3, height=1)
        self.buttons[index].grid(row=r, column=c)
        

grid = grid4by4(window)
alreadyvisitedstates = []
openlist = []
iterationnumber = 0
        
def randomize():
    arr = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',' ']
    np.random.shuffle(arr)
    ind = 0
    for i in grid.buttons:
        i.configure(text = str(arr[ind]))
        ind += 1
        
def customstating():
    inputtedtxt = entryofstate.get()
    ar = inputtedtxt.split(',')
    if len(ar) == 16 and len(ar) == len(set(ar)):
        flag = True
        for i in ar:
            if i != ' ':
                if int(i) > 15 or int(i) < 1:
                    flag = False
        if flag:
            index = 0
            for i in grid.buttons:
                i.configure(text = ar[index])
                index += 1
                #1,2,3,4,5,6,7,8,9,10,11,12,13,14, ,15
                #1,2,3,4,5,6, ,8,9,10,11,12,13,14,7,15
                #1,2,3,4,5,6,7,8, ,10,11,12,13,14,9,15
                # 1,2,3,4,5,6,7,8,9,10, ,12,13,14,11,15

def possiblemovesreturner2(curgrade, index_2d_of_empty_space):
    global openlist
    global alreadyvisitedstates
    i = index_2d_of_empty_space[0]
    j = index_2d_of_empty_space[1]
    if i <= 2:
        possiblestate = np.copy(curgrade)
        possiblestate[i][j] = possiblestate[i+1][j]
        possiblestate[i+1][j] = ' '
        if possiblestate.tolist() not in openlist and possiblestate.tolist() not in alreadyvisitedstates:
            openlist.append(possiblestate.tolist())
    if i >= 1:
        possiblestate = np.copy(curgrade)
        possiblestate[i][j] = possiblestate[i-1][j]
        possiblestate[i-1][j] = ' '
        if possiblestate.tolist() not in openlist and possiblestate.tolist() not in alreadyvisitedstates:
            openlist.append(possiblestate.tolist())
    if j <= 2:
        possiblestate = np.copy(curgrade)
        possiblestate[i][j] = possiblestate[i][j+1]
        possiblestate[i][j+1] = ' '
        if possiblestate.tolist() not in openlist and possiblestate.tolist() not in alreadyvisitedstates:
            openlist.append(possiblestate.tolist())
    if j >= 1:
        possiblestate = np.copy(curgrade)
        possiblestate[i][j] = possiblestate[i][j-1]
        possiblestate[i][j-1] = ' '
        if possiblestate.tolist() not in openlist and possiblestate.tolist() not in alreadyvisitedstates:
            openlist.append(possiblestate.tolist())

    return openlist


def least_heuristic_returner(nextpossiblestates):
    lst = []
    goal = np.array([np.array(['1','2','3','4']), np.array(['5','6','7','8']), np.array(['9','10','11','12']),np.array(['13','14','15',''])])
    index = 0
    for i in nextpossiblestates:
        if i.size != 0:
            booleans_of_comparison = []
            for j in range(4):
                for k in range(4):
                    if goal[j][k] != i[j][k]:
                        booleans_of_comparison.append(False)#meaning: at wrong place
            heuristic_value = booleans_of_comparison.count(False)#how many at wrong place
            lst.append((index,heuristic_value))
        index += 1
    least = 17
    ind = -1
    for i,j in lst:
        if j < least:
            least = j+0
            ind = i + 0

    return nextpossiblestates[ind]

def display_n_change_state(arr2d):
    arr1d = arr2d.flatten()
    ind = 0
    for i in grid.buttons:
        i.configure(text = str(arr1d[ind]))
        ind += 1
    window.update()

    #1,2,3,4,5,6,7,8,9,10,11,12,13,14, ,15
                #1,2,3,4,5,6, ,8,9,10,11,12,13,14,7,15
                #1,2,3,4,5,6,7,8, ,10,11,12,13,14,9,15
                # 1,2,3,4,5,6,7,8,9,10, ,12,13,14,11,15
def bestfirstsearch():
    goal = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',' ']
    index = 0
    curgrid = []
    flag = True
    
    global alreadyvisitedstates
    global openlist
    
    for i in grid.buttons:
        curgrid.append(i['text'])
        if goal[index] != i['text']:
            flag = False
        index += 1
    if not flag:    
        ar1 = np.array(curgrid[0:4])
        ar2 = np.array(curgrid[4:8])
        ar3 = np.array(curgrid[8:12])
        ar4 = np.array(curgrid[12:])
        curgrid = np.array([ar1, ar2,ar3, ar4])
        #calculate next states
        #choose the one with least heuristics
        
        #found empty spot:
        solutions = np.argwhere(curgrid == ' ')
        openlist = possiblemovesreturner2(curgrid, solutions[0])
        #above calculates possible new states and then adds them to the set of all states
        #provided they are not in openlist or thevisitedlist
        nextstate = least_heuristic_returner(np.array(openlist))
        alreadyvisitedstates.append(nextstate.tolist())
        openlist.remove(nextstate.tolist())
        display_n_change_state(nextstate)
        
        bestfirstsearch()
        
        return
    
    alreadyvisitedstates = []
    openlist = []
    return

def possiblemovesreturnerAstar(curgrade, curgridlevel, index_2d_of_empty_space):
    global openlist
    global alreadyvisitedstates
    
    i = index_2d_of_empty_space[0]
    j = index_2d_of_empty_space[1]
    
    if i <= 2:
        possiblestate = np.copy(curgrade)
        possiblestate[i][j] = possiblestate[i+1][j]
        possiblestate[i+1][j] = ' '
        if possiblestate.tolist() not in [x for x,y in openlist] and possiblestate.tolist() not in alreadyvisitedstates:
            openlist.append((possiblestate.tolist(), curgridlevel+1))
    if i >= 1:
        possiblestate = np.copy(curgrade)
        possiblestate[i][j] = possiblestate[i-1][j]
        possiblestate[i-1][j] = ' '
        if possiblestate.tolist() not in [x for x,y in openlist] and possiblestate.tolist() not in alreadyvisitedstates:
            openlist.append((possiblestate.tolist(), curgridlevel+1))
    if j <= 2:
        possiblestate = np.copy(curgrade)
        possiblestate[i][j] = possiblestate[i][j+1]
        possiblestate[i][j+1] = ' '
        if possiblestate.tolist() not in [x for x,y in openlist] and possiblestate.tolist() not in alreadyvisitedstates:
            openlist.append((possiblestate.tolist(), curgridlevel+1))
    if j >= 1:
        possiblestate = np.copy(curgrade)
        possiblestate[i][j] = possiblestate[i][j-1]
        possiblestate[i][j-1] = ' '
        if possiblestate.tolist() not in [x for x,y in openlist] and possiblestate.tolist() not in alreadyvisitedstates:
            openlist.append((possiblestate.tolist(), curgridlevel+1))

    return openlist

def least_heuristic_returner_aStar(openlist):
    lst = []
    goal = np.array([np.array(['1','2','3','4']), np.array(['5','6','7','8']), np.array(['9','10','11','12']),np.array(['13','14','15',''])])
    index = 0
    for i,l in openlist:
        x = np.array(i)
        if x.size != 0:
            booleans_of_comparison = []
            for j in range(4):
                for k in range(4):
                    if goal[j][k] != x[j][k]:
                        booleans_of_comparison.append(False)#meaning: at wrong place
            heuristic_value = booleans_of_comparison.count(False)+ l
            #how many at wrong place i.e. heuristic value + level
            lst.append((index,heuristic_value))
        index += 1
    least = 50
    ind = -1
    for i,j in lst:
        if j < least:
            least = j+0
            ind = i + 0

    return openlist[ind][0]

def display_n_change_state_aStar(arr2d):
    arr1d = arr2d.flatten()
    ind = 0
    print(arr1d)
    for i in grid.buttons:
        i.configure(text = str(arr1d[ind]))
        ind += 1
    window.update()

    if len(entryofiterationlimit.get()) != 0:
        global iterationnumber
        iterationnumber += 1
        if str(iterationnumber) == entryofiterationlimit.get():
            exit(1)
    
def A_star_search(level = 0):
    goal = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',' ']
    index = 0
    curgrid = []
    flag = True
    global openlist
    global alreadyvisitedstates
    
    for i in grid.buttons:
        curgrid.append(i['text'])
        if goal[index] != i['text']:
            flag = False
        index += 1
    if flag:
        openlist = []
        alreadyvisitedstates = []
        return
    ar1 = np.array(curgrid[0:4])
    ar2 = np.array(curgrid[4:8])
    ar3 = np.array(curgrid[8:12])
    ar4 = np.array(curgrid[12:])
    curgrid = np.array([ar1, ar2,ar3, ar4])

    #found empty spot:
    solutions = np.argwhere(curgrid == ' ')
    openlist = possiblemovesreturnerAstar(curgrid, level, solutions[0])
    #above calculates possible new states and then adds them to the set of all states
    #provided they are not in openlist or thevisitedlist
    nextstate = least_heuristic_returner_aStar(np.array(openlist))
    
    alreadyvisitedstates.append(nextstate)
    for i in openlist:
        if i[0] == nextstate:
            level = i[1]
            openlist.remove(i)
            break
    display_n_change_state_aStar(np.array(nextstate))
    level += 1
    #take level from the ordered pair
    A_star_search(level)
    
    return
    
def searchalgos():
    if w['text'] == 'Best-First':
        bestfirstsearch()
    elif w['text'] == 'A*':
        A_star_search()
    
        
fontformaintext = ("Comic Sans MS", "32")
#main text
Label(text="~15 puzzle solver~",bg = 'dark slate gray', fg = 'white', font = fontformaintext).pack()
#buttons
randombutton = Button(text = "Randomize", fg = "black",bg = "slate gray", command = randomize)
randombutton.config(width = 20)
randombutton.pack()
customstatebutton = Button(text = "Enter custom state: ", bg = "slate gray",fg = "black", command = customstating)
customstatebutton.config(width = 20)
customstatebutton.pack()
entryofstate = Entry()
entryofstate.config(width = 25)
entryofstate.pack()

#drop down
variable = StringVar(window)
variable.set("Select an algorithm") # default value
w = OptionMenu(window, variable, "A*", "Best-First")
w.config(bg = "slate gray", fg = "black")
w.pack()

searchbutton = Button(text = 'Search',command = searchalgos, fg = 'white', bg = 'slate gray')
searchbutton.config(width = 20)
searchbutton.pack()

setiterationlabel = Label(text = "Set Iteration Limit:", fg = "white",bg = "dark slate gray", width = 20)
setiterationlabel.pack()
entryofiterationlimit = Entry()
entryofiterationlimit.config(width = 25)
entryofiterationlimit.pack()

setrecursionlabel = Label(text = "Set Recursion Limit:", fg = "white",bg = "dark slate gray", width = 20)
setrecursionlabel.pack()
entryofrecursionlimit = Entry()
entryofrecursionlimit.config(width = 25)
entryofrecursionlimit.pack()

if len(entryofrecursionlimit.get()) != 0:
    sys.setrecursionlimit(int(entryofrecursionlimit.get()))
    
window.mainloop()
