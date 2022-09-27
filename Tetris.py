import math, copy, random
from cmu_112_graphics import *

def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

def playTetris():
    rows, cols, cellSize, margin = gameDimensions()
    x = margin * 2 + cellSize * cols
    y = margin * 2 + cellSize * rows
    runApp(width = x, height = y)

def appStarted(app):
    app.label = 'Tetris!'
    app.color = 'orange'
    app.size = 0

    app.pause = False

    rows, cols, cellSize, margin = gameDimensions()
    app.rows = rows
    app.cols = cols
    app.cellSize = cellSize
    app.margin = margin

    app.emptyColor = 'blue'
    app.board = [ ([app.emptyColor] * cols) for c in range(rows) ]
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, 
                        sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", 
                             "cyan", "green", "orange" ]
    
    #index, startRow, startCol, piece
    app.nextPiece = [0, 0, 3, app.tetrisPieces[0]]
    app.isGameOver = False
    app.score = 0
    #app.timerDelay = 250

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col,
                     app.board[row][col])

def getCellCounds(app, row, col):
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    x0 = app.margin + gridWidth * col / app.cols
    x1 = app.margin + gridWidth * (col+1) / app.cols
    y0 = app.margin + gridHeight * row / app.rows
    y1 = app.margin + gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

def drawCell(app, canvas, row, col, color):
    x0, y0, x1, y1 = getCellCounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, width = 3,
                            fill = color, outline = 'black')

def newFallingPiece(app):
    import random
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    pieceLen = len((app.tetrisPieces[randomIndex])[0])
    startCol = app.cols // 2 - pieceLen // 2
    app.nextPiece = [randomIndex, 0, startCol, 
                     app.tetrisPieces[randomIndex]]

def drawFallingPiece(app, canvas):
    index = app.nextPiece[0]
    startRow = app.nextPiece[1]
    startCol = app.nextPiece[2]
    p = app.nextPiece[3]
    for i in range(len(p)):
        for j in range(len(p[0])):
            if(p[i][j]):
                drawCell(app, canvas, startRow + i, startCol + j,
                         app.tetrisPieceColors[index])

def moveFallingPiece(app, drow, dcol):
    index = app.nextPiece[0]
    cr = app.nextPiece[1]
    cc = app.nextPiece[2]
    piece = app.nextPiece[3]
    app.nextPiece = (index, cr + drow, cc + dcol, piece)
    if(fallingPieceIsLegal(app, piece, cr + drow, cc + dcol)):
        app.nextPiece = [index, cr + drow, cc + dcol, piece]
        return True
    else:
        app.nextPiece = [index, cr, cc, piece]
        return False

def fallingPieceIsLegal(app, piece, row, col):
    pieceHeight = len(piece)
    pieceWidth = len(piece[0])
    if(col < 0): return False
    if(row < 0 or col < 0 or row + pieceHeight > app.rows
       or col + pieceWidth > app.cols):
       return False
    for i in range(pieceHeight):
        for j in range(pieceWidth):
            if(piece[i][j]):
                if(app.board[row + i][col + j] != app.emptyColor):
                    return False
    return True

def rotateFallingPiece(app):
    index = app.nextPiece[0]
    r = app.nextPiece[1]
    c = app.nextPiece[2]
    piece = app.nextPiece[3]
    pieceRow = len(piece)
    pieceCol = len(piece[0])
    newPiece = [ ([None] * pieceRow) for col in range(pieceCol) ]
    l = []
    for i in range(pieceRow):
        for j in range(pieceCol):
            l.append(piece[i][j])
    count = 0
    for j in range(pieceRow):
        for i in range(pieceCol - 1, -1, -1):
            newPiece[i][j] = l[count]
            count += 1
    if(index == 0):
        if(len(newPiece) == 4):
            nr = r - 2
            nc = c + 2
        else:
            nr = r + 2
            nc = c -2
    else:
        nr = r
        nc = c
    if(fallingPieceIsLegal(app, newPiece, nr, nc)):
        app.nextPiece = [index, nr, nc, newPiece]
    else:
        app.nextPiece = [index, r, c, piece]

def placeFallingPiece(app):
    piece = app.nextPiece[3]
    r = app.nextPiece[1]
    c = app.nextPiece[2]
    color = app.tetrisPieceColors[app.nextPiece[0]]
    pieceRow = len(piece)
    pieceCol = len(piece[0])
    for i in range(pieceRow):
        for j in range(pieceCol):
            if(piece[i][j]):
                app.board[r + i][c + j] = color
    newFallingPiece(app)
    removeFullRows(app)

def initTetris(app):
    app.board = [ ([app.emptyColor] * app.cols) for c in range(app.rows) ]
    app.nextPiece = [0, 0, 3, app.tetrisPieces[0]]
    app.isGameOver = False
    app.score = 1

def drawGameOver(app, canvas):
    if(app.isGameOver):
        canvas.create_rectangle(app.margin, app.margin + app.cellSize,
                                app.margin + app.cellSize * app.cols,
                                app.margin + app.cellSize * 3, fill = 'black')
        canvas.create_text(app.width / 2, app.margin + 2 * app.cellSize,
                           text = 'Game Over!', font = 'Arial 17 bold', 
                           fill = 'yellow')

def clearRow(app, row):
    while(row > 0):
        row -= 1
        tmp = copy.copy(app.board[row])
        app.board[row + 1] = tmp
    for c in app.board[0]:
        c = app.emptyColor

def removeFullRows(app):
    count = 0
    for r in range(len(app.board)):
        if(app.emptyColor not in app.board[r]):
            count += 1
            clearRow(app, r)
    app.score += count**2

def drawScore(app, canvas):
    canvas.create_text(app.width / 2, app.margin / 2, 
                       text = f'Score: {app.score}',
                       font = 'Arial 12 bold', fill = 'blue')

def hardDrop(app):
    while(moveFallingPiece(app, +1, 0)):
        continue

def keyPressed(app, event):
    if(app.isGameOver == False):
        if(event.key == 'Up'): rotateFallingPiece(app)
        elif (event.key == 'Down'): moveFallingPiece(app, 1, 0)
        elif (event.key == 'Left'): moveFallingPiece(app, 0, -1)
        elif (event.key == 'Right'): moveFallingPiece(app, 0, +1)
        elif (event.key == 'Space'): hardDrop(app)
    if(event.key == 'r'):
        initTetris(app)

def timerFired(app):
    if(app.isGameOver == False):
        if(not moveFallingPiece(app, +1, 0)):
            placeFallingPiece(app)
            piece = app.nextPiece[3]
            row = app.nextPiece[1]
            col = app.nextPiece[2]
            if(not fallingPieceIsLegal(app, piece, row, col)):
                app.isGameOver = True

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='orange')
    drawBoard(app, canvas)
    drawFallingPiece(app, canvas)
    drawGameOver(app, canvas)
    drawScore(app, canvas)

playTetris()