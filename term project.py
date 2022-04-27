import math, copy, random

from cmu_112_graphics import *
# lines 1 - 3 from previous homeworks

class Monster(): # leared how to create classes from week 8 notes
    def __init__(self, state, health, color, mProjectiles, x, y, radius, 
                 reloadSpeed, timePassed, timerDelay, num): 
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
        self.num = num

    def monsterStruck(self): 
        self.health -= 1

    def monsterDie(self): 
        self.state = False

    def monsterShoot(self, app, x, y): 
        a, b = self.x - app.cx, self.y - app.cy
        c = math.sqrt(a ** 2 + b ** 2)
        fiver = c // 5
        a, b = a // fiver, b // fiver
        self.mProjectiles = self.mProjectiles + [(self.x, self.y, a, b)]
    
    def checkHealth(self): 
        if self.health >= 14: 
            self.color = 'red'
        elif self.health < 14 and self.health > 7: 
            self.color = 'orange'
        elif self.health <= 7: 
            self.color = 'yellow'

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
        Monster.checkHealth(self)
        if self.health <= 0: 
            Monster.monsterDie(self)
        if self.state != True: 
            app.monsterList.remove(self)
        self.timePassed += self.timerDelay
        if self.timePassed >= self.reloadSpeed: 
            Monster.monsterShoot(self, app,  app.cx, app.cy)
            self.timePassed = 0
        if self.mProjectiles != [ ]: 
            for i in range(len(self.mProjectiles)): 
                (x, y, a, b) = self.mProjectiles[i]
                (row, col) = getCell(app, x, y)
                if row < 0 or row >= app.rows or col < 0 or col >= app.cols: 
                    self.mProjectiles[i] = (x - a, y - b, a, b)
                elif app.maze[row][col] == 1: 
                    app.maze[row][col] = 0
                    self.mProjectiles[i] = (x - a, y - b, a, b)
                else: 
                    self.mProjectiles[i] = (x - a, y - b, a, b)

def appStarted(app): 
    app.startMenu = True
    app.instructions = False
    app.hardMode = False
    app.timerDelay = 50
    app.radius = 20
    app.rows, app.cols, app.margin = 30, 35, 0
    app.color = 'green'
    app.maze = [([0] * app.cols) for row in range(app.rows)]
    app.maze = generateMaze(app)
    app.width, app.height = gameDimensions()
    app.cx, app.cy = findSpawn(app)
    app.health = 20
    app.projectilesList = [ ]
    app.keyRelease = 'z'
    app.monsterList = [ ] 
    for i in range(14): 
        (x, y) = findSpawn(app)
        newMonster = Monster(True, 20,'red', [ ], x, y, 20, 500, 0, 25, 0)
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

def spawnEnemies(app): 
    if app.hardMode: 
        app.monsterList = [ ] 
        for i in range(30): 
            (x, y) = findSpawn(app)
            newMonster = Monster(True, 20,'red', [ ], x, y, 20, 500, 0, 25, 0)
            app.monsterList.append(newMonster)
    else: 
        app.monsterList = [ ] 
        for i in range(14): 
            (x, y) = findSpawn(app)
            newMonster = Monster(True, 20,'red', [ ], x, y, 20, 500, 0, 25, 0)
            app.monsterList.append(newMonster)

def gameDimensions(): # from HW6
    return (1500, 900)

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
        app.maze[r2][c2] != 0 or r >= app.rows or r < 0 or c >= app.cols or 
        c < 0): 
        return False
    return True

def win(app): 
    if app.monsterList == [ ]: 
        return True
    return False

def lose(app): 
    if app.health <= 0: 
        return True
    return False

def checkHealth(app): 
    if app.health >= 14: 
        app.color = 'green'
    elif app.health < 14 and app.health > 7: 
        app.color = 'blue'
    elif app.health <= 7: 
        app.color = 'purple'

def keyPressed(app, event): 
    if event.key == 'w': 
        app.wKey = True
    elif event.key == 'a': 
        app.aKey = True
    elif event.key == 's': 
        app.sKey = True
    elif event.key == 'd': 
        app.dKey = True
    if event.key == "r": 
        appStarted(app)
    if event.key == 'e': 
        app.startMenu = False
    if app.startMenu: 
        if event.key == 'i': 
            if app.instructions: 
                app.instructions = False
            else: 
                app.instructions = True
        if event.key == 'h': 
            if app.hardMode: 
                app.hardMode = False
                app.monsterList = []
                spawnEnemies(app)
            else: 
                app.hardMode = True
                app.monsterList = []
                spawnEnemies(app)

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
    if app.startMenu == False:
        checkHealth(app)
        if win(app) == False and lose(app) == False: 
            for i in range(len(app.projectilesList)): 
                (x, y, a, b) = app.projectilesList[i]
                (row, col) = getCell(app, x, y)
                r = app.radius // 2
                for monster in app.monsterList: 
                    mLeft = monster.x - monster.radius
                    mTop = monster.y - monster.radius
                    mRight = monster.x + monster.radius
                    mBottom = monster.y + monster.radius
                    bLeft = x - r
                    bTop = y - r
                    bRight = x + r
                    bBottom = y + r
                    if (bBottom < mBottom and bBottom > mTop and bRight > mLeft 
                    and bRight < mRight): 
                        Monster.monsterStruck(monster)
                    elif (bBottom < mBottom and bBottom > mTop and bLeft > mLeft 
                    and bLeft < mRight): 
                        Monster.monsterStruck(monster)
                    elif (bTop > mTop and bTop < mBottom and bRight > mLeft and 
                        bRight < mRight): 
                        Monster.monsterStruck(monster)
                    elif (bTop > mTop and bTop < mBottom and bLeft > mLeft and 
                        bLeft < mRight): 
                        Monster.monsterStruck(monster)
                if row < 0 or row >= app.rows or col < 0 or col >= app.cols: 
                    app.projectilesList[i]
                elif app.maze[row][col] == 1: 
                    app.projectilesList[i]
                else: 
                    app.projectilesList[i] = (x + a * 3, 
                                            y + b * 3, a, b)
            for monster in app.monsterList: 
                for i in range(len(monster.mProjectiles)): 
                    r = app.radius // 2
                    (x, y, a, b) = monster.mProjectiles[i]
                    pLeft = app.cx - app.radius
                    pTop = app.cy - app.radius
                    pRight = app.cx + app.radius
                    pBottom = app.cy + app.radius
                    buLeft = x - r
                    buTop = y - r
                    buRight = x + r
                    buBottom = y + r
                    if (buBottom < pBottom and buBottom > pTop and buRight > 
                    pLeft and buRight < pRight): 
                        app.health -= 1
                    elif (buBottom < pBottom and buBottom > pTop and buLeft > 
                    pLeft and buLeft < pRight): 
                        app.health -= 1
                    elif (buTop > pTop and buTop < pBottom and buRight > pLeft 
                    and buRight < pRight): 
                        app.health -= 1
                    elif (buTop > pTop and buTop < pBottom and buLeft > pLeft 
                    and buLeft < pRight): 
                        app.health -= 1
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
            if app.maze[r][c] == 1: 
                canvas.create_rectangle(x0, y0, x1, y1, fill='black')

def drawProjectiles(app, canvas): 
    r = app.radius // 2
    for i in range(len(app.projectilesList)): 
        (x, y, a, b) = app.projectilesList[i]
        canvas.create_oval(x - r, y + r, x + r, y - r, fill = "black")

def drawPlayerCharacter(app, canvas): # draws the player
    r = app.radius
    cx, cy = app.cx, app.cy
    canvas.create_oval(cx - r, cy + r, cx + r, cy - r, fill = app.color)

def drawHealthBar(app, canvas): 
    for r in range(1): 
        for c in range(app.health): 
            (x0, y0, x1, y1) = getCellBounds(app, r, c)
            x0 = 50
            y0 = 800
            x1 = 20 * app.health
            y1 = 850
            canvas.create_rectangle(x0, y0, x1, y1, fill='red', width = 5)
            canvas.create_text((x0 + x1) // 2, 825, text = str(app.health), 
                                fill = 'black', font = 'Arial 20 bold')

def drawWin(app, canvas): 
    canvas.create_rectangle(0, 350, app.width, 550, fill='black')
    canvas.create_text(app.width // 2, app.height // 2 - 20, 
                        text='You win!',fill='white', font='Arial 40 bold')
    canvas.create_text(app.width // 2, app.height // 2 + 20, 
    text='press r to try again',fill='white', font='Arial 20')

def drawFail(app, canvas): 
    canvas.create_rectangle(0, 350, app.width, 550, fill='black')
    canvas.create_text(app.width // 2, app.height // 2 - 20, 
                        text='You lose!',fill='white', font='Arial 40 bold')
    canvas.create_text(app.width // 2, app.height // 2 + 20, 
    text='press r to try again',fill='white', font='Arial 20')

''' font research for drawStartMenu comes from ->
https://docs.huihoo.com/tkinter/an-introduction-to-tkinter-1999/x444-fonts.
htm#:~:text=Font%20descriptors,-Starting%20with%20Tk&text=Arial%20(corresponds%
20to%20Helvetica)%2C,the%20tuple%20syntax%20described%20above.
'''

''' for information on how to create arcs -> 
https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_arc.html
'''

def drawStartMenu(app, canvas):  
    cx1, cy1 = app. width // 5 - 50, app.height // 2 + app.height // 4 - 50
    cx2, cy2 = (app.width // 5) * 4 + 50, app.height // 2 + app.height // 4 - 50
    cRadius = 200
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'black')
    canvas.create_text(app.width // 2, app.height // 4, 
    text = 'Cave Crusader!', font = 'MS 80', fill = 'white')
    canvas.create_text(app.width // 2, app.height // 2.5, 
    text = 'You, the green circle, must vanquish your foes,', 
    font = 'MS 40', fill = 'white')
    canvas.create_text(app.width // 2, app.height // 2.5 + 65, 
    text = 'the red circles!', 
    font = 'MS 40', fill = 'white')
    canvas.create_text(app.width // 2, app.height // 2 + 50, 
    text = 'Press i to view the instructions', 
    font = 'MS 30', fill = 'white')
    canvas.create_text(app.width // 2, app.height // 2 + 200, 
    text = 'Press e to begin', 
    font = 'MS 30', fill = 'white')
    canvas.create_text(app.width // 2, app.height // 2 + 100, 
    text = 'Press h for hard mode', 
    font = 'MS 30', fill = 'white')
    canvas.create_text(app.width // 2, app.height // 2 + 150, 
    text = 'Hard mode = ', 
    font = 'MS 30', fill = 'white')
    if app.hardMode:
        canvas.create_text(app.width // 2 + 145, app.height // 2 + 150, 
        text = 'on', 
        font = 'MS 30', fill = 'red')
    else: 
        canvas.create_text(app.width // 2 + 145, app.height // 2 + 150, 
        text = 'off', 
        font = 'MS 30', fill = 'green')
    canvas.create_oval(cx1 - cRadius, cy1 + cRadius, cx1 + cRadius, 
                    cy1 - cRadius, fill = 'green')
    canvas.create_oval(cx1 - 40 - 60, cy1 + 40 - 60, cx1 + 40 - 60, 
                    cy1 - 40 - 60, fill = 'black')
    canvas.create_oval(cx1 - 40 + 60, cy1 + 40 - 60, cx1 + 40 + 60, 
                    cy1 - 40 - 60, fill = 'black')
    canvas.create_oval(cx2 - cRadius, cy2 + cRadius, cx2 + cRadius, 
                    cy2 - cRadius, fill = 'red')
    canvas.create_oval(cx2 - 40 - 60, cy2 + 40 - 60, cx2 + 40 - 60, 
                    cy2 - 40 - 60, fill = 'black')
    canvas.create_oval(cx2 - 40 + 60, cy2 + 40 - 60, cx2 + 40 + 60, 
                    cy2 - 40 - 60, fill = 'black')
    canvas.create_arc(cx1 - 70, cy1 + 50, cx1 + 70, cy1 + 100, fill = 'black', 
                      style = ARC, extent = -180, width = 10)
    canvas.create_arc(cx2 - 70, cy2 + 50, cx2 + 70, cy2 + 100, fill = 'black', 
                      style = ARC, extent = 180, width = 10)

def drawInstructions(app, canvas): 
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'white')
    canvas.create_text(app.width // 4, app.height // 4, 
    text = 'Use WASD to move up, left, down and right respectively', 
    font = 'MS 20', fill = 'black')
    canvas.create_text(app.width // 4, app.height // 4 + 50, 
    text = 'Use left mouseclick to shoot a projectile in that direction', 
    font = 'MS 20', fill = 'black')
    canvas.create_text(app.width // 4 + 50, app.height // 4 + 100, 
    text = 'Your healthbar in the bottom left shows how much health you have', 
    font = 'MS 20', fill = 'black')
    canvas.create_text(app.width // 4, app.height // 4 + 150, 
    text = 'Dodge enemy projectiles or take damage', 
    font = 'MS 20', fill = 'black')
    canvas.create_text(app.width // 4, app.height // 4 + 200, 
    text = 'Defeat all the enemy circles to win!', 
    font = 'MS 20', fill = 'black')
    canvas.create_text(app.width // 2, (app.height // 5) * 4, 
    text = 'Press i to close the instructions', 
    font = 'MS 20', fill = 'black')

def redrawAll(app, canvas):
    drawCells(app, canvas)
    drawPlayerCharacter(app, canvas)
    for monster in app.monsterList: 
        monster.drawMonster(app, canvas)
    drawProjectiles(app, canvas)
    for monster in app.monsterList: 
        monster.drawMProjectiles(app, canvas)
    drawHealthBar(app, canvas)
    if win(app): 
        drawWin(app, canvas)
    if lose(app): 
        drawFail(app, canvas)
    if app.startMenu: 
        drawStartMenu(app, canvas)
    if app.instructions: 
        drawInstructions(app, canvas)

def playGame(): 
    width, height = gameDimensions()
    runApp(width=width, height=height)

def main(): 
    playGame()

if __name__ == '__main__': # from previous homeworks
    main()