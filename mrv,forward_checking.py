from copy import deepcopy
import numpy as np

#global variables
count = 0
#count of how many times backtracking was done


#solve function
def solve(board) :
    fixedval = [] #list of cells whose value has been fixed
    #elements = (r,c) 

    #create the remval list  #9x9 list
    remval = [[0 for x in range(9)] for y in range(9)]
    #remval[r][c] = list of values that can be filled in cell board[r][c]

    #initialise remval list
    #for each cell on board
    for row in range(0,9) :
        for col in range(0,9) :
            if board[row][col] == 0:
                #cell not filled
                remval[row][col] = [1,2,3,4,5,6,7,8,9]
            else: #cell already fixed
                remval[row][col] = []
                #add it to list of fixed cells
                fixedval.append((row,col))

    #for each fixed value, eliminate options
    for cell in fixedval :
        row = cell[0]
        col = cell[1]
        value = board[row][col]

        remval = eliminate( remval, row, col, value)

    #now solve the sudoku by backtracking    
    backtracking(board, remval)

    

#eliminate num from rem val list of all cells 
#in the same row, col, box
def eliminate(remval, row, col, num) :
    #board[row][col] = num
    #first clear rem val list of this cell
    remval[row][col] = []

    #entire row
    for r in range(0,9) :
        # if num is present in the rem val list of the cell
        if num in remval[r][col] :
            #remove num from list
            remval[r][col].remove(num)

            #now if remval list is now empty, raise error
            if len(remval[r][col]) == 0:
                return False

    #entire col
    for c in range(0,9) :
        if num in remval[row][c] :
            remval[row][c].remove(num)

            #now if remval list is now empty, raise error
            if len(remval[row][c]) == 0:
                return False


    #the entire box
    start_row = (row//3)*3
    end_row = start_row + 2

    start_col = (col//3)*3
    end_col = start_col + 2

    #for each cell in the box
    for r in range(start_row, end_row + 1) :
        for c in range(start_col , end_col + 1 ) :
            if num in remval[r][c] :
                remval[r][c].remove(num)

                #now if remval list is now empty, raise error
                if len(remval[r][c]) == 0:
                    return False
    
    #####################################################
    return remval



#solving by backtracking
def backtracking(board, remval) :
    global count

    #filling each empty cell priority wise
    while MRV(board, remval) != -1 :
        cell = MRV(board, remval)
        r = cell[0]
        c = cell[1]

        '''if len(remval[r][c]) == 0 : 
            print("cell has no remaining values", r,c)
            return
            #this cell accidently got high priority due to wrongly filled values'''

        #try filling each value from cell's remval list
        for num in remval[r][c] :
            #passing a deepcopy of remval for all functions so that the actual remval list remains unchanged
            #check if filling cell with num creates problems
            if eliminate(deepcopy(remval), r, c, num) == False :
                continue
            else: 
                board[r][c] = num

                #solve furthur
                #passing updated copy of remval list, where num has been eliminated from cells in the same row, col, box as (r,c)
                backtracking(board, eliminate(deepcopy(remval), r, c, num) )  #recursive call

                ######################################################
                #coming here means filling the cell with num created problems
                #so undo that
                board[r][c] = 0
                #only a copy of remval was changed in the eliminate() function, so actual remval remains unchanged
                #thus no need to do anything abt remval list

                #increment backtracking count
                count = count + 1

        return

    #coming here means all the cells have been filled
    #print the answer
    print("Number of times backtracking was done: ", count)
    print(board)
    print()



#function to return index of cell with min remaining value
#MRV = -1 means all cells are filled
def MRV(board, remval) :
    min = 10 #min 
    min_cell = ()

    for r in range(0,9) :
        for c in range(0,9) :
            if board[r][c] == 0 :
                if len(remval[r][c]) < min :
                    min = len(remval[r][c])
                    min_cell = (r,c)
    
    if min != 10 :
        return min_cell

    return -1



######################################################################
#driver code
board = np.array([[5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,0,1,9,0,0,5],
        [0,0,0,0,0,0,0,0,0]])
#26 cells filled


board2 = np.array([
        [8,0,0,0,0,0,0,0,0],
        [0,0,3,6,0,0,0,0,0],
        [0,7,0,0,9,0,2,0,0],
        [0,5,0,0,0,7,0,0,0],
        [0,0,0,0,4,5,7,0,0],
        [0,0,0,1,0,0,0,3,0],
        [0,0,1,0,0,0,0,6,8],
        [0,0,8,5,0,0,0,1,0],
        [0,9,0,0,0,0,4,0,0]])
#21 filled

print(board)
print()
solve(board)