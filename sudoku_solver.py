"""board= [
    [2,1,5,0,6,0,9,0,0],
    [7,0,0,0,0,9,1,0,0],
    [4,0,9,3,1,0,0,5,8],
    [0,0,1,0,0,5,0,4,0],
    [9,0,4,0,3,0,8,0,5],
    [0,5,0,2,0,0,6,0,0],
    [3,8,0,0,4,1,5,0,6],
    [0,0,6,7,0,0,0,0,2],
    [0,0,7,0,8,0,3,1,9]
]
board1= [
    [4, 0, 5, 0, 0, 0, 3, 0, 7],
    [0, 0, 0, 9, 0, 2, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 8, 0, 0, 0, 9, 0, 0],
    [0, 2, 6, 1, 0, 3, 4, 7, 0],
    [0, 0, 3, 0, 0, 0, 1, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 7, 0, 5, 0, 0, 0],
    [3, 0, 4, 0, 0, 0, 2, 0, 6]
]"""
def find_empty(board):
    for i in  range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==0:
                return (i,j)
    return None

def valid(board,num,pos):
    for i in range(len(board[0])):
        if board[pos[0]][i]==num and pos[1]!=i:
            return False
    for j in range(len(board)):
        if board[j][pos[1]]==num and pos[0]!=j:
            return False
    x=pos[1]//3
    y=pos[0]//3
    for i in range(y*3,y*3+3):
        for j in range(x*3,x*3+3):
            if board[i][j]==num and (i,j)!=pos:
                return False
    return True

def solve(board):
    find=find_empty(board)
    if not find:
        return True
    else:
        row,col=find
    for i in range(1,10):
        if valid(board,i,(row,col)):
            board[row][col]=i ## this would be set to zero if solve returns false
            if solve(board): ## if this is false
                return True
            board[row][col]=0 ## sets the previously entered cell to zero then loop will continue from the number ahead of what was initally entered(i)
    return False
