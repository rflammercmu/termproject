import math, copy, random

from cmu_112_graphics import *
# lines 1 - 3 from previous homeworks

def appStarted(app): 
    app.radius = 20
    app.rows, app.cols, app.margin = 50, 50, 0
    app.maze = [([0] * app.cols) for row in range(app.rows)]
    app.maze = generateMaze(app)
    app.width, app.height = 1500, 900
    app.cx, app.cy = app.width // 2, app.height // 2
    app.x, app.y = app.cx, app.cy
    # app.scrollX, app.scrollY = 0, 0
    app.projectilesList = [ ]
    app.keyRelease = 'z'
    app.wKey, app.aKey, app.sKey, app.dKey = False, False, False, False

# pointInGrid, getCell, drawCell and getCellBounds from Animations Part 2: Case 
# Studies
def pointInGrid(app, x, y): 
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))

def getCell(app, x, y):
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)
    return (row, col)

def getCellBounds(app, row, col):
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

# def findSpawn(app): 
#     for x in range(100): 
#         randomX = random.randint(100, app.width - 100)
#         randomY = random.randint(100, app.height - 100)
#         row, col = getCell(app, randomX, randomY)
#         if app.maze[row][col] == 0: 
#             return (randomX, randomY)

def isLegal(app, vertical, horizontal, flag): 
    if flag == 'up': 
        r, c = getCell(app, app.x, app.y + vertical - app.radius)
        r1, c1 = getCell(app, app.x - app.radius + 1, 
                         app.y + vertical - app.radius)
        r2, c2 = getCell(app, app.x + app.radius - 1, 
                         app.y + vertical - app.radius)
    elif flag == 'left': 
        r, c = getCell(app, app.x + horizontal - app.radius, app.y)
        r1, c1 = getCell(app, app.x + horizontal - app.radius, 
                         app.y - app.radius + 1)
        r2, c2 = getCell(app, app.x + horizontal - app.radius, 
                         app.y + app.radius - 1)
    elif flag == 'down': 
        r, c = getCell(app, app.x, app.y + vertical + app.radius - 1)
        r1, c1 = getCell(app, app.x - app.radius,
                         app.y + vertical + app.radius - 1)
        r2, c2 = getCell(app, app.x + app.radius - 1, 
                         app.y + vertical + app.radius - 1)
    elif flag == 'right': 
        r, c = getCell(app, app.x + horizontal + app.radius - 1, app.y)
        r1, c1 = getCell(app, app.x + horizontal + app.radius - 1, 
                         app.y - app.radius + 1)
        r2, c2 = getCell(app, app.x + horizontal + app.radius - 1, 
                         app.y + app.radius - 1)
    if (app.maze[r][c] != 0 or app.maze[r1][c1] != 0 or
        app.maze[r2][c2] != 0): 
        print (r, c)
        return False
    return True

def keyPressed(app, event): 
    if event.key == 'w': 
        app.wKey = True
    elif event.key == 'a': 
        app.aKey = True
    elif event.key == 's': 
        app.sKey = True
    elif event.key == 'd': 
        app.dKey = True

def keyReleased(app, event): 
    if event.key == 'w': 
        app.wKey = False
    elif event.key == 'a': 
        app.aKey = False
    elif event.key == 's': 
        app.sKey = False
    elif event.key == 'd': 
        app.dKey = False

def mousePressed(app, event): # mouseclick to shoot projectiles
    shoot(app, event.x, event.y)
 
def timerFired(app): 
    for i in range(len(app.projectilesList)): 
        (x, y, a, b) = app.projectilesList[i]
        app.projectilesList[i] = (x + a * 3, 
                                  y + b * 3, a, b)
    if app.wKey: 
        if isLegal(app, -5, 0, 'up'): 
            app.cy -= 10
    if app.aKey: 
        if isLegal(app, 0, -5, 'left'): 
            app.scrollX += 10
            app.x -= 10
    if app.sKey: 
        if isLegal(app, 5, 0, 'down'): 
            app.scrollY -= 10
            app.y += 10
    if app.dKey: 
        if isLegal(app, 0, 5, 'right'): 
            app.scrollX -= 10
            app.x += 10
    
def shoot(app, x, y): # when mouse is pressed, a projectile is created
    a, b = x - app.cx, y - app.cy
    c = math.sqrt(a ** 2 + b ** 2)
    fiver = c // 5
    a, b = a // fiver, b // fiver
    app.projectilesList = app.projectilesList + [(app.cx, app.cy, a, b)]

def isMazeLegal(app, r, c, nearR, nearC): 
    if (r + nearR < 0 or r + nearR >= app.rows or c + nearC < 0 or 
        c + nearC >= app.cols): 
        return False
    return True

def generateMaze(app): # guide form Terrain.pdf 15-112 course notes
    randomMaze = app.maze
    for r in range(app.rows): 
        for c in range(app.cols): 
            randomMaze[r][c] = random.randint(0, 1)
    for i in range(7): 
        for r in range(app.rows): 
            for c in range(app.cols): 
                passageSum = 0
                for nearR in [-1, 0, 1]: 
                    for nearC in [-1, 0, 1]: 
                        if isMazeLegal(app, r, c, nearR, nearC):
                            if randomMaze[r + nearR][c + nearC] == 1: 
                                passageSum += 1
                if passageSum >= 5: 
                    randomMaze[r][c] = 1
                else: 
                    randomMaze[r][c] = 0
    # for r in range(app.rows): 
    #         for c in range(app.cols): 
    #             if randomMaze[r][c] == 1: 
    #                 randomMaze[r][c] = 0 
    #             else: 
    #                 randomMaze[r][c] = 1 
    for r in range(app.rows // 2 - 2, app.rows // 2 + 2): 
        for c in range(app.cols // 2 - 2, app.rows // 2 + 2): 
            randomMaze[r][c] = 0
    return randomMaze

def drawCells(app, canvas): 
    for r in range(app.rows): 
        for c in range(app.cols): 
            (x0, y0, x1, y1) = getCellBounds(app, r, c)
            if app.maze[r][c] == 0: 
                # canvas.create_rectangle(x0 + app.scrollX, y0 + app.scrollY, 
                # x1 + app.scrollX, y1 + app.scrollY, fill='white')
                pass
            else: 
                canvas.create_rectangle(x0 + app.scrollX, y0 + app.scrollY, 
                x1 + app.scrollX, y1 + app.scrollY, fill='black')

def drawProjectiles(app, canvas): 
    r = app.radius // 2
    for i in range(len(app.projectilesList)): 
        (x, y, a, b) = app.projectilesList[i]
        canvas.create_oval(x - r, y + r, x + r, y - r, fill = "green")

def drawPlayerCharacter(app, canvas): # draws the player
    r = app.radius
    cx, cy = app.cx, app.cy
    canvas.create_oval(cx - r, cy + r, cx + r, cy - r, fill = "red")

def redrawAll(app, canvas):
    drawCells(app, canvas)
    drawPlayerCharacter(app, canvas)
    drawProjectiles(app, canvas)

def playGame(): 
    runApp(width=1500, height=900)

def main(): 
    playGame()

if __name__ == '__main__': # from previous homeworks
    main()