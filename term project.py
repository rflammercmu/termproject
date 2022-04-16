import math, copy, random

from cmu_112_graphics import *
# lines 1 - 3 from previous homeworks

class Monster(): 
    def __init__(self, state, health, color, mProjectiles, x, y, radius, 
                 reloadSpeed, timePassed, timerDelay, speed): 
        self.state = state
        self.health = health
        self.color = color
        self.mProjectiles = mProjectiles
        self.x = x
        self.y = y
        self.radius = radius
        self.reloadSpeed = reloadSpeed
        self.timePassed = timePassed
        self.timerDelay = timerDelay

    def monsterStruck(self): 
        self.health -= 1

    def monsterDie(self): 
        self.state = False

    def monsterAliveOrNot(self, app): 
        return self.state

    def monsterShoot(self, app, x, y): 
        print (x, y, app.cx, app.cy)
        a, b = self.x - app.cx, self.y - app.cy
        c = math.sqrt(a ** 2 + b ** 2)
        fiver = c // 5
        a, b = a // fiver, b // fiver
        self.mProjectiles = self.mProjectiles + [(self.x, self.y, a, b)]

    def drawMonster(self, app, canvas): 
        canvas.create_oval(self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius,
                           fill=self.color)

    def drawMProjectiles(self, app, canvas): 
        radius = self.radius // 2
        for i in range(len(self.mProjectiles)): 
            (x, y, a, b) = self.mProjectiles[i]
            canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                               fill = self.color)

    def timerFired(self, app): 
        self.timePassed += self.timerDelay
        if self.timePassed >= self.reloadSpeed: 
            Monster.monsterShoot(self, app,  app.cx, app.cy)
            self.timePassed = 0
        if self.mProjectiles != [ ]: 
            for i in range(len(self.mProjectiles)): 
                (x, y, a, b) = self.mProjectiles[i]
                self.mProjectiles[i] = (x - a, y - b, a, b)

class Runner(Monster): 
    def __init__(self, state, health, color, mProjectiles, x, y, radius, 
                 reloadSpeed, timePassed, timerDelay, speed): 
        self.x, self.y = x, y
        self.health = health
        self.speed = speed
        self.radius = radius
        self.state = state
        self.color = color
        self.timePassed = timePassed
        self.timerDelay = timerDelay

def appStarted(app): 
    app.timerDelay = 50
    app.radius = 20
    app.rows, app.cols, app.margin = 30, 30, 0
    app.maze = [([0] * app.cols) for row in range(app.rows)]
    app.maze = generateMaze(app)
    app.width, app.height = 1500, 900
    app.cx, app.cy = findSpawn(app)
    app.projectilesList = [ ]
    app.keyRelease = 'z'
    app.monsterList = [ ]
    (x, y) = findSpawn(app)
    newMonster = Monster(True, 10,'Yellow', [ ], x, y, 20, 1000, 0, 25, 10)
    app.monsterList.append(newMonster)
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

def findSpawn(app): 
    for x in range(100): 
        randomX = random.randint(100, app.width - 100)
        randomY = random.randint(100, app.height - 100)
        row, col = getCell(app, randomX, randomY)
        if app.maze[row][col] == 0: 
            return (randomX, randomY)

def isLegal(app, vertical, horizontal, flag): 
    if flag == 'up': 
        r, c = getCell(app, app.cx, app.cy + vertical - app.radius)
        r1, c1 = getCell(app, app.cx - app.radius + 1, 
                         app.cy + vertical - app.radius)
        r2, c2 = getCell(app, app.cx + app.radius - 1, 
                         app.cy + vertical - app.radius)
    elif flag == 'left': 
        r, c = getCell(app, app.cx + horizontal - app.radius, app.cy)
        r1, c1 = getCell(app, app.cx + horizontal - app.radius, 
                         app.cy - app.radius + 1)
        r2, c2 = getCell(app, app.cx + horizontal - app.radius, 
                         app.cy + app.radius - 1)
    elif flag == 'down': 
        r, c = getCell(app, app.cx, app.cy + vertical + app.radius - 1)
        r1, c1 = getCell(app, app.cx - app.radius,
                         app.cy + vertical + app.radius - 1)
        r2, c2 = getCell(app, app.cx + app.radius - 1, 
                         app.cy + vertical + app.radius - 1)
    elif flag == 'right': 
        r, c = getCell(app, app.cx + horizontal + app.radius - 1, app.cy)
        r1, c1 = getCell(app, app.cx + horizontal + app.radius - 1, 
                         app.cy - app.radius + 1)
        r2, c2 = getCell(app, app.cx + horizontal + app.radius - 1, 
                         app.cy + app.radius - 1)
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
        (row, col) = getCell(app, x, y)
        if app.maze[row][col] == 1: 
            app.projectilesList[i]
        else: 
            app.projectilesList[i] = (x + a * 3, 
                                    y + b * 3, a, b)
    for monster in app.monsterList: 
        monster.timerFired(app)
    if app.wKey: 
        if isLegal(app, -5, 0, 'up'): 
            app.cy -= 10
    if app.aKey: 
        if isLegal(app, 0, -5, 'left'): 
            app.cx -= 10
    if app.sKey: 
        if isLegal(app, 5, 0, 'down'): 
            app.cy += 10
    if app.dKey: 
        if isLegal(app, 0, 5, 'right'): 
            app.cx += 10
    
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
    return randomMaze

def drawCells(app, canvas): 
    for r in range(app.rows): 
        for c in range(app.cols): 
            (x0, y0, x1, y1) = getCellBounds(app, r, c)
            if app.maze[r][c] == 0: 
                # canvas.create_rectangle(x0, y0, x1, y1, fill='white')
                pass
            else: 
                canvas.create_rectangle(x0, y0, x1, y1, fill='black')

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
    for monster in app.monsterList: 
        monster.drawMonster(app, canvas)
    drawProjectiles(app, canvas)
    for monster in app.monsterList: 
        monster.drawMProjectiles(app, canvas)

def playGame(): 
    runApp(width=1500, height=900)

def main(): 
    playGame()

if __name__ == '__main__': # from previous homeworks
    main()