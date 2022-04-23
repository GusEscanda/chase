
import random
import time

try:
    import browser
    from browser import document, svg, alert, timer, window, html
    # I'm running in a web browser => use Brython to manage the GUI (https://brython.info/)
    BROWSER = True
except:
    # Brython isn't available so use standard python text based interfase
    import os
    BROWSER = False

class BoardObject:
    # Mother class for all the board objects, implements the standard behavior and atributes of them.
    
    # Priority to remain in a cell of the grid when two BoardObject run into each other.
    PRIO_LOWER     = 0
    PRIO_HERO      = 10
    PRIO_FOE       = 50
    PRIO_FIRE      = 80
    PRIO_DEAD_HERO = 90

    # Types of tools that the Hero can find in the Board
    TOOL_SMALL_BOMB      = 'v'
    TOOL_BIG_BOMB        = 'b'
    TOOL_TELEPORT        = 't'
    TOOL_SAFE_TELEPORT   = 's'
    TOOL_GUIDED_TELEPORT = '\u0398'
    
    idCount = 0

    def __init__(self, board, row, col):
        self.alive = True
        self.board = board
        self.gui = board.gui
        self.row = row
        self.col = col
        self.priority = BoardObject.PRIO_LOWER
        self.tool = None
        self.char = ' ' # character to display in the board, only in testing mode
        BoardObject.idCount += 1
        self.id = f'BObj_{BoardObject.idCount}' # asign a unique id (used in the GUI as the id in the browser object svgRoot)
        self.draw      = self.gui.drawNothing # replace this function in each subclass
        self.translate = self.gui.translate
        self.delete    = self.gui.delete

    def step( self, *args, **kwargs ):
        """ by default the BoardObject doesn't move and, if possible, copies itself to the updated grid """
        if not self.alive:
            return
        if self.board.grid[ self.row ][ self.col ] == None: # if the cell is empty copy the BoardObject to the current grid
            self.board.grid[ self.row ][ self.col ] = self
        else:
            # if my place was taken fill the cell based on priority
            if self.board.grid[ self.row ][ self.col ] == self: # It's taken by my self!! I'm already on the grid, do nothing
                return
            # So the cell have an occupant that's not me. Who of us will stay on the grid?
            if self.priority <= self.board.grid[ self.row ][ self.col ].priority:
                self.die( killer = self.board.grid[ self.row ][ self.col ] )  # He has priority, so I die
            else:
                self.board.grid[ self.row ][ self.col ].die( killer = self )  # I have priority, kill him and take his place
                self.board.grid[ self.row ][ self.col ] = self

    def die(self, killer=None):
        if not self.alive:
            return
        if self.tool != None and isinstance(killer,Hero): # if it's the Hero stepping on a tool, take the tool off the board and increase the stock of that tool.
            self.board.tool( self.tool, +1 )
        self.alive = False
        self.delete( boardObj = self )
        if self.board.grid[ self.row ][ self.col ] == self: # if THIS BoardObject is on the grid, take it off
           self.board.grid[ self.row ][ self.col ] = None

class Fire( BoardObject ):
    def __init__(self, board, row, col):
        BoardObject.__init__(self, board, row, col)
        self.priority = BoardObject.PRIO_FIRE
        self.char = '\u039E'
        self.draw = self.gui.drawFire

class SmallBomb( BoardObject ):
    def __init__(self, board, row, col):
        BoardObject.__init__(self, board, row, col)
        self.priority = BoardObject.PRIO_LOWER
        self.tool = BoardObject.TOOL_SMALL_BOMB
        self.char = 'v'
        self.draw = self.gui.drawSmallBomb

class BigBomb( BoardObject ):
    def __init__(self, board, row, col):
        BoardObject.__init__(self, board, row, col)
        self.priority = BoardObject.PRIO_LOWER
        self.tool = BoardObject.TOOL_BIG_BOMB
        self.char = 'b'
        self.draw = self.gui.drawBigBomb

class SafeTeleport( BoardObject ):
    def __init__(self, board, row, col):
        BoardObject.__init__(self, board, row, col)
        self.priority = BoardObject.PRIO_LOWER
        self.tool = BoardObject.TOOL_SAFE_TELEPORT
        self.char = 's'
        self.draw = self.gui.drawSafeTeleport

class GuidedTeleport( BoardObject ):
    def __init__(self, board, row, col):
        BoardObject.__init__(self, board, row, col)
        self.priority = BoardObject.PRIO_LOWER
        self.tool = BoardObject.TOOL_GUIDED_TELEPORT
        self.char = '\u0398'
        self.draw = self.gui.drawGuidedTeleport

class DeadHero( BoardObject ):
    def __init__(self, board, row, col):
        BoardObject.__init__(self, board, row, col)
        self.priority = BoardObject.PRIO_DEAD_HERO
        self.char = 'g'
        self.draw = self.gui.drawDeadHero

class Foe( BoardObject ):
    def __init__(self, board, row, col):
        BoardObject.__init__(self, board, row, col)
        self.priority = BoardObject.PRIO_FOE
        self.char = '\u03A9'
        self.draw = self.gui.drawFoe

    def step(self, heroR, heroC):
        if not self.alive:
            return

        if heroR > self.row: # update row, go towards the Hero!!
            self.row += 1
        elif heroR < self.row:
            self.row -= 1

        if heroC > self.col: # update column, go towards the Hero!!
            self.col += 1
        elif heroC < self.col:
            self.col -= 1
        
        self.translate( boardObj = self )

        if isinstance( self.board.grid[ self.row ][ self.col ], Foe ): # Two Foes collide, they kill each other, a Fire takes their place
            self.die( killer = self.board.grid[ self.row ][ self.col ] )
            self.board.grid[ self.row ][ self.col ].die( killer = self )
            self.board.placeBoardObjects( Fire, coords = (self.row, self.col) )
        else:
            BoardObject.step(self)

    def die(self, killer=None):
        BoardObject.die(self, killer=killer)
        self.board.foeCount -= 1
        if killer is not None:
            self.board.score += 1
            self.board.highScore = max( self.board.score, self.board.highScore )


class Hero( BoardObject ):
    def __init__(self, board, row, col):
        BoardObject.__init__(self, board, row, col)
        self.priority = BoardObject.PRIO_HERO
        self.char = '\u00B7'
        self.draw = self.gui.drawHero

    def step(self, deltaR, deltaC):
        if not self.alive:
            return

        self.row += deltaR
        self.col += deltaC

        if self.row < 0 or self.row >= self.board.maxR or self.col < 0 or self.col >= self.board.maxC:
            # if fell off the grid, undo the movement to stay right on the edge
            self.row -= deltaR
            self.col -= deltaC
            if self.board.dieBeyondEdges:
                self.die()  # if fell off the board, die
        if self.alive:
            self.translate( boardObj = self )
            BoardObject.step(self)


class Board:

    def __init__(self, maxR, maxC, gui = None):
        # Set the height and width of the board
        self.maxR = maxR
        self.maxC = maxC

        # Store a reference to the GUI object
        self.gui = gui

        self.hero = None
        self.level = 0 # Counts the level so each one will be more challenging

        # Create a grid that will contain the objects in the board
        self.grid = self.emptyGrid()

        # metrics that will determine how difficult the game will be to play
        self.initFoeCount = 0
        self.incrementFoeCountByLevel = 5
        self.dropToolMu = 0
        self.dropToolSigma = 1
        self.inicToolStock = {
            BoardObject.TOOL_TELEPORT: -1,
            BoardObject.TOOL_SAFE_TELEPORT: 1,
            BoardObject.TOOL_GUIDED_TELEPORT: 1,
            BoardObject.TOOL_SMALL_BOMB: 1,
            BoardObject.TOOL_BIG_BOMB: 1,            
        }
        self.dieBeyondEdges = False

        self.foeCount = 0
        self.score = 0
        self.highScore = 0
        self.toolStock = {}

        self.repeat = False
        self.guided = False

        # Create a list that will contain all the objects that must do something in each cicle of the game
        self.boardObjectList = []


    def emptyGrid(self):
        # using regular python lists because brython doesn't support numpy, I hope will not have performance issues...
        return [ [ None for _ in range(self.maxC) ] for _ in range(self.maxR) ]

    def cleanBoard(self):
        for bObj in self.boardObjectList:
            bObj.die()
        self.boardObjectList = []
        self.grid = self.emptyGrid()
        self.foeCount = 0

    def newLevel(self):
        self.level += 1
        self.cleanBoard()
        self.placeBoardObjects( Hero )
        self.hero = self.boardObjectList[0]
        self.placeBoardObjects( Foe, self.initFoeCount + self.incrementFoeCountByLevel * self.level )
        
        toolDrop = lambda : max(0, int( random.normalvariate( self.dropToolMu, self.dropToolSigma ) ))
        self.placeBoardObjects( SmallBomb, toolDrop() )
        self.placeBoardObjects( BigBomb, toolDrop() )
        self.placeBoardObjects( SafeTeleport, toolDrop() )
        self.placeBoardObjects( GuidedTeleport, toolDrop() )
        
        self.setRepeat('off')  # reset the repeat mode
        self.setGuided('off')  # reset the guided mode

        self.gui.textDisplayBoard(board = self)
        self.gui.refreshScores()
        
    def newGame(self):
        if self.hero is not None:
            if not self.gui.askNewGame():
                return
        self.level = 0
        self.score = 0
        self.newLevel()
        for tool in self.inicToolStock:
            self.toolStock[tool] = self.inicToolStock[tool]
        self.gui.refreshButtons()

    def collectTools(self):
        for _ in range(len(self.boardObjectList)): # for all the tools that remain in the board
            bObj = self.boardObjectList.pop(0)
            if bObj.tool is not None:
                bObj.die( killer = self.hero )
            else:
                self.boardObjectList.append( bObj )


    def tool(self, tool, qty=0):
        # Updates the tool stock based on qty. Returns the current stock of the tool 
        if self.toolStock[tool] < 0:
            self.toolStock[tool] = -1 # tool quantity < 0 means infinite use => don't update it, keep it at -1
        else:
            self.toolStock[tool] += qty
        if qty != 0:
            self.gui.refreshButtons(tool) # if the stock has changed, refresh the button
        return self.toolStock[tool]

    def placeBoardObjects(self, boardObjectClass, qty=1, coords=None):
        added = 0
        while added < qty:
            if coords is None:
                row = random.randrange(self.maxR)
                col = random.randrange(self.maxC)
                if self.grid[row][col] != None:
                    continue
            else:
                row, col = coords
            boardObject = boardObjectClass( board = self, row = row, col = col ) # create the BoardObject
            self.grid[row][col] = boardObject # put it in the grid
            self.boardObjectList.append( boardObject ) # put it in the object list
            boardObject.draw( boardObj = boardObject ) # draw it
            if isinstance(boardObject, Foe):
                self.foeCount += 1
            added += 1

    def setRepeat(self, mode='toggle'):
        """ mode: 'on' set repeat mode on, 'off' set repeat mode off, 'toggle' toggles repeat mode"""
        if self.checkNewGame():
            return
        if mode == 'toggle':
            value = not self.repeat
        else:
            value = (mode.lower() == 'on')
        self.repeat = value
        self.gui.refreshRepeat(self.repeat)
        return self.repeat

    def setGuided(self, mode='toggle'):
        """ mode: 'on' set guided mode on, 'off' set guided mode off, 'toggle' toggles guided mode"""
        if self.checkNewGame():
            return
        if mode == 'toggle':
            value = not self.guided
        else:
            value = (mode.lower() == 'on')
        self.guided = value and ( self.tool(BoardObject.TOOL_GUIDED_TELEPORT) != 0 )
        self.gui.refreshGuided(self.guided)
        return self.guided


    def move(self, deltaR, deltaC):
        if self.checkNewGame():
            return
        # Take one or more steps in the (deltaR, deltaC) direction.
        while self.hero.alive and self.foeCount > 0:

            newR = self.hero.row + deltaR
            newC = self.hero.col + deltaC

            # If the mode is 'repeat', keep going until reaches a border, an obstacle or a non safe cell (near a Foe). 
            # So the 'repeat' mode is safe...
            if self.repeat and ( self.notSafe(newR,newC) or self.notEmpty(newR,newC) ):
                break

            # clear the grid and start to generate the updated one
            self.grid = self.emptyGrid()
            
            # take a single step
            self.hero.step(deltaR,deltaC)

            if not self.hero.alive:
                break

            # move all the Foes towards the hero
            for _ in range(len(self.boardObjectList)): # for all the live BoardObjects other than the Hero, make a step
                bObj = self.boardObjectList.pop(0)
                if bObj.alive and not isinstance(bObj, Hero):
                    bObj.step( self.hero.row, self.hero.col )
                if bObj.alive:
                    self.boardObjectList.append( bObj )

            # if the mode is 'repeat', keep going
            if not self.repeat:
                break

            self.gui.textDisplayBoard(board = self)

            if self.repeat:
                self.gui.repeatDelay()


        if not self.hero.alive:
            self.placeBoardObjects( DeadHero, coords = (self.hero.row, self.hero.col) )

        self.setRepeat('off')  # reset the repeat mode
        self.setGuided('off')  # reset the guided mode
        self.gui.textDisplayBoard(board = self)
        self.gui.refreshScores()

        if self.foeCount == 0:
            self.collectTools()
            self.newLevel()

    def notEmpty(self, row, col):
        if row < 0 or row >= self.maxR or col < 0 or col >= self.maxC: # for this funcion off limits is considered not empty
            return True
        # This cell is considered 'empty' if it's content is None or 
        # if the hero is on it (need this to handle correctly the step(0,0) in repeat mode)
        return ( self.grid[row][col] != None ) and ( self.grid[row][col] != self.hero )
 
    def notSafe(self, row, col):
        """ Return True if it's not safe for the Hero to move to the cell row, col (there are foes nearby) """
        if row < 0 or row >= self.maxR or col < 0 or col >= self.maxC: # going beyond board limits is not safe...
            return True
        if self.grid[row][col] != None:
            if self.hero.priority < self.grid[row][col].priority: # landing in a Foe or a Fire, is not safe...
                return True
        for deltaR in range(-1, 2, 1):
            if row + deltaR < 0 or row + deltaR >= self.maxR: # if row + deltaR is out of boundaries, don't check here
                continue
            for deltaC in range(-1, 2, 1):
                if col + deltaC < 0 or col + deltaC >= self.maxC: # if col + deltaC is out of boundaries, don't check here
                    continue
                if deltaR == 0 and deltaC == 0: # check only neighbor cells 
                    continue
                if isinstance( self.grid[ row + deltaR ][ col + deltaC ], Foe ): # there is a Foe nearby
                    return True
        return False

    def teleport(self, safe=False, guided=False, coords=(0,0)):
        if self.checkNewGame():
            return
        # Check if you have the tool
        if safe and self.tool(BoardObject.TOOL_SAFE_TELEPORT) == 0:
            return
        if guided and self.tool(BoardObject.TOOL_GUIDED_TELEPORT) == 0:
            return
        if not safe and not guided and self.tool(BoardObject.TOOL_TELEPORT) == 0:
            return

        if guided:
            row, col = coords
        else:
            row = random.randrange(self.maxR)
            col = random.randrange(self.maxC)
            while safe and self.notSafe(row,col):
                row = random.randrange(self.maxR)
                col = random.randrange(self.maxC)
        
        if safe:
            self.tool(BoardObject.TOOL_SAFE_TELEPORT, -1)
        if guided:
            self.tool(BoardObject.TOOL_GUIDED_TELEPORT, -1)
        if not safe and not guided:
            self.tool(BoardObject.TOOL_TELEPORT, -1)

        self.hero.row = row
        self.hero.col = col
        self.hero.translate( boardObj = self.hero )
        self.setRepeat('off')
        self.move(0,0)
        self.gui.textDisplayBoard(board = self)

    def bomb(self, big=False):
        if self.checkNewGame():
            return
        bombType = BoardObject.TOOL_BIG_BOMB if big else BoardObject.TOOL_SMALL_BOMB
        if self.tool( bombType ) == 0:
            return

        self.tool( bombType, -1 )
        row = self.hero.row
        col = self.hero.col
        for deltaR in range(-1, 2, 1):
            if row + deltaR < 0 or row + deltaR >= self.maxR: # if row + deltaR is out of boundaries, don't work here
                continue
            for deltaC in range(-1, 2, 1):
                if col + deltaC < 0 or col + deltaC >= self.maxC: # if row + deltaR is out of boundaries, don't work here
                    continue
                if deltaR == 0 and deltaC == 0: # work only on the neighbor cells 
                    continue
                if self.grid[ row + deltaR ][ col + deltaC ] is None:
                    pass
                elif isinstance( self.grid[ row + deltaR ][ col + deltaC ], Foe ): # there is a Foe nearby
                    self.grid[ row + deltaR ][ col + deltaC ].die(killer=self.hero)
                    if big:
                        self.placeBoardObjects( Fire, coords = (row + deltaR, col + deltaC) )
                elif not isinstance( self.grid[ row + deltaR ][ col + deltaC ], Fire ):
                    self.grid[ row + deltaR ][ col + deltaC ].die(killer=None)
        self.setRepeat('off')
        self.move(0,0)
        self.gui.textDisplayBoard(board = self)

    def checkNewGame(self):
        if self.hero.alive:
            return False
        else:
            self.newGame()
            return True

class UI:

    nullFunction = lambda *args, **kwargs: None

    # override all or any of these functions depending on the type of interfase, text (standard os console) or graphic (via Brython)
    drawHero = nullFunction
    drawDeadHero = nullFunction
    drawFoe = nullFunction
    drawFire = nullFunction
    drawSmallBomb = nullFunction
    drawBigBomb = nullFunction
    drawSafeTeleport = nullFunction
    drawGuidedTeleport = nullFunction
    drawNothing = nullFunction

    translate = nullFunction
    delete = nullFunction
    
    refreshScores = nullFunction
    refreshButtons = nullFunction
    refreshRepeat = nullFunction
    refreshGuided = nullFunction

    repeatDelay = nullFunction

    askNewGame = nullFunction

    textDisplayBoard = nullFunction


class NoGui(UI):
    # when testing the game in text mode (no graphics available) use this class instead to manage the user interfase

    def repeatDelay(self):
        time.sleep(0.25)  # sleep 250ms

    def askNewGame(self):
        again = ' '
        while again not in 'yns':
            again = input('Play again (y/n)? ').lower()
        return again in 'ys'

    def textDisplayBoard(self, board):

        os.system('cls')
        print()
        print('Foes left', board.foeCount, ' '*20, 'Score:', board.score, ' '*20, 'High Score:', board.highScore)
        print()
        print('  ' + ('. 1 2 3 4 5 6 7 8 9 ' * 20)[ : board.maxC*2 ] + '  ' )
        for row in range(board.maxR):
            print( (str(row%10) if row%10 != 0 else '.') + ' ', end='')
            for col in range(board.maxC):
                if board.grid[row][col] != None:
                    print(board.grid[row][col].char+' ', end='')
                else:
                    print('  ', end='')
            print( (str(row%10) if row%10 != 0 else '.') )
        print('  ' + ('. 1 2 3 4 5 6 7 8 9 ' * 20)[ : board.maxC*2 ] + '  ' )
        print()
        for t in board.toolStock:
            print( t + ' ' + str(board.toolStock[t] if board.toolStock[t] >= 0 else ''), end='   ' )
        print( '   ', '[r]' if board.repeat else ' r ', end='   ' )
        print()
        print()


class GUI(UI):
    # class to manage all the Graphical User Interfase based on Brython and the browser objects

    SMALL_MOVE = 1
    BIG_MOVE = 15
    FAST_MOVE = 250  # milliseconds between clicks in a double click

    def __init__(self, board):
        
        self.svgRoot = browser.document["svg_root"]
        
        self.width = self.svgRoot.clientWidth
        self.height = self.svgRoot.clientHeight

        self.board = board
        
        self.cellSize = min( self.width // (self.board.maxC+2), self.height // (self.board.maxR+2) )
        self.relativeTop  = self.cellSize
        self.relativeLeft = self.cellSize
        self.absoluteTop  = self.svgRoot.abs_top  + self.relativeTop
        self.absoluteLeft = self.svgRoot.abs_left + self.relativeLeft


        self.mouseDownRow = None
        self.mouseDownCol = None 
        self.mouseUpRow = None
        self.mouseUpCol = None
        self.lastPointerMoveTimeStamp = 0

        self.svgRoot.bind("mousedown", self.pointerStart)
        self.svgRoot.bind("mousemove", self.pointerMove)
        self.svgRoot.bind("mouseup", self.pointerEnd)

        self.svgRoot.bind('touchstart', self.pointerStart)
        self.svgRoot.bind('touchmove', self.pointerMove)
        self.svgRoot.bind('touchend', self.pointerEnd)

        window.bind('keydown', self.keyPressed)
        window.bind('keyup', self.keyPressed)
        self.keydownArrows = {'ArrowUp':False, 'ArrowDown':False, 'ArrowLeft':False, 'ArrowRight':False}

        browser.document[BoardObject.TOOL_TELEPORT].bind( 'click', lambda evt: self.board.teleport() )
        browser.document['repeat'].bind( 'click', lambda evt: self.board.setRepeat('toggle') )

        browser.document[BoardObject.TOOL_SAFE_TELEPORT].bind( 'click', lambda evt: self.board.teleport(safe=True) )
        browser.document[BoardObject.TOOL_GUIDED_TELEPORT].bind( 'click', lambda evt: self.board.setGuided('toggle') )
        browser.document[BoardObject.TOOL_SMALL_BOMB].bind( 'click', lambda evt: self.board.bomb(big=False) )
        browser.document[BoardObject.TOOL_BIG_BOMB].bind( 'click', lambda evt: self.board.bomb(big=True) )

        browser.document['new'].bind( 'click', lambda evt: self.board.newGame() )

        browser.document['moveNW'].bind( 'click', lambda evt: self.board.move(-1,-1) )
        browser.document['moveN'].bind( 'click', lambda evt: self.board.move(-1, 0) )
        browser.document['moveNE'].bind( 'click', lambda evt: self.board.move(-1, 1) )
        browser.document['moveW'].bind( 'click', lambda evt: self.board.move(0, -1) )
        browser.document['moveStay'].bind( 'click', lambda evt: self.board.move(0, 0) )
        browser.document['moveE'].bind( 'click', lambda evt: self.board.move(0, 1) )
        browser.document['moveSW'].bind( 'click', lambda evt: self.board.move(1, -1) )
        browser.document['moveS'].bind( 'click', lambda evt: self.board.move(1, 0) )
        browser.document['moveSE'].bind( 'click', lambda evt: self.board.move(1, 1) )
 
    def rowcol2coords(self, row, col, relative=True):
        top  = self.relativeTop  if relative else self.absoluteTop
        left = self.relativeLeft if relative else self.absoluteLeft
        return ( left + col * self.cellSize, top + row * self.cellSize )

    def coords2rowcol(self, x, y, relative=False):
        top  = self.relativeTop  if relative else self.absoluteTop
        left = self.relativeLeft if relative else self.absoluteLeft
        return ( round((y - top) / self.cellSize), round((x - left) / self.cellSize) )

    def repeatDelay(self):
        # todo: 
        # Hacer esta funcion. No funcionó nada de lo que intenté desde Python.
        # Por ahi hay que hacerla en javascript...
        pass

    def drawHero(self, boardObj):
        print(f'drawHero, id={boardObj.id} en {boardObj.row}, {boardObj.col}')
        cx, cy = self.rowcol2coords( boardObj.row, boardObj.col )
        svgShape = svg.circle(
            id = boardObj.id,
            cx = cx, 
            cy = cy,
            r  = self.cellSize / 2,
            style = {"fill": '#334BFF'})
#        svgShape = html.OBJECT(
#            id = boardObj.id,
#            type = "image/svg+xml", 
#            data = 'fire.svg', 
#            width = self.cellSize,
#            height = self.cellSize,
#            cx = cx, 
#            cy = cy
#        )
        self.svgRoot <= svgShape

        
    def drawDeadHero(self, boardObj):
        print(f'drawDeadHero, id={boardObj.id} en {boardObj.row}, {boardObj.col}')
        cx, cy = self.rowcol2coords( boardObj.row, boardObj.col )
        svgShape = svg.circle(
            id = boardObj.id,
            cx = cx, 
            cy = cy,
            r  = self.cellSize / 2,
            style = {"fill": '#AF33FF'})
        self.svgRoot <= svgShape
        
    def drawFoe(self, boardObj):
        print(f'drawFoe, id={boardObj.id} en {boardObj.row}, {boardObj.col}')
        cx, cy = self.rowcol2coords( boardObj.row, boardObj.col )
        svgShape = svg.circle(
            id = boardObj.id,
            cx = cx, 
            cy = cy,
            r  = self.cellSize / 2,
            style = {"fill": '#C5C5C5'})
        self.svgRoot <= svgShape
        
    def drawFire(self, boardObj):
        print(f'drawFire, id={boardObj.id} en {boardObj.row}, {boardObj.col}')
        cx, cy = self.rowcol2coords( boardObj.row, boardObj.col )
        svgShape = svg.circle(
            id = boardObj.id,
            cx = cx, 
            cy = cy,
            r  = self.cellSize / 2,
            style = {"fill": '#515150'})
        self.svgRoot <= svgShape

    def drawSmallBomb(self, boardObj):
        print(f'drawSmallBomb, id={boardObj.id} en {boardObj.row}, {boardObj.col}')
        cx, cy = self.rowcol2coords( boardObj.row, boardObj.col )
        svgShape = svg.circle(
            id = boardObj.id,
            cx = cx, 
            cy = cy,
            r  = self.cellSize / 2,
            style = {"fill": '#FFC300'})
        self.svgRoot <= svgShape
        
    def drawBigBomb(self, boardObj):
        print(f'drawBigBomb, id={boardObj.id} en {boardObj.row}, {boardObj.col}')
        cx, cy = self.rowcol2coords( boardObj.row, boardObj.col )
        svgShape = svg.circle(
            id = boardObj.id,
            cx = cx, 
            cy = cy,
            r  = self.cellSize / 2,
            style = {"fill": '#FF5733'})
        self.svgRoot <= svgShape
        
    def drawSafeTeleport(self, boardObj):
        print(f'drawSafeTeleport, id={boardObj.id} en {boardObj.row}, {boardObj.col}')
        cx, cy = self.rowcol2coords( boardObj.row, boardObj.col )
        svgShape = svg.circle(
            id = boardObj.id,
            cx = cx, 
            cy = cy,
            r  = self.cellSize / 2,
            style = {"fill": '#03FC32'})
        self.svgRoot <= svgShape
        
    def drawGuidedTeleport(self, boardObj):
        print(f'drawGuidedTeleport, id={boardObj.id} en {boardObj.row}, {boardObj.col}')
        cx, cy = self.rowcol2coords( boardObj.row, boardObj.col )
        svgShape = svg.circle(
            id = boardObj.id,
            cx = cx, 
            cy = cy,
            r  = self.cellSize / 2,
            style = {"fill": '#027017'})
        self.svgRoot <= svgShape


    def translate(self, boardObj):
        print(f'translate, id={boardObj.id} en {boardObj.row}, {boardObj.col}')
        old_cx = browser.document[boardObj.id].cx.baseVal.value
        old_cy = browser.document[boardObj.id].cy.baseVal.value
        cx, cy = self.rowcol2coords( boardObj.row, boardObj.col )
        browser.document[boardObj.id].setAttributeNS(None, "transform", f"translate({cx - old_cx},{cy - old_cy})")


    def delete(self, boardObj):
        print(f'delete, id={boardObj.id} en {boardObj.row}, {boardObj.col} type={type(boardObj)}')
        browser.document[boardObj.id].remove()

    def pointerStart(self, evt):
        print(f'{evt.type} {evt.target.id}')
        if evt.type == 'mousedown':
            x, y = evt.x, evt.y
        elif evt.type == 'touchstart':
            evt.preventDefault()
            if len(evt.touches) == 1:
                x, y = evt.touches[0].pageX, evt.touches[0].pageY
            else:
                self.mouseDownRow, self.mouseDownCol = None, None  # cancel move
                return
        print(f'     x: {x}, y: {y}, cellSize: {self.cellSize}, coords: {self.coords2rowcol(x, y)}')
        self.mouseDownRow, self.mouseDownCol = self.coords2rowcol(x, y)
        self.mouseUpRow, self.mouseUpCol = self.mouseDownRow, self.mouseDownCol  # if there is no movement the ponterMove will not be fired...
        
    def pointerMove(self, evt):
        # print(f'{evt.type} {evt.target.id}')
        if evt.type == 'mousemove':
            x, y = evt.x, evt.y
        elif evt.type == 'touchmove':
            evt.preventDefault()
            if len(evt.touches) == 1:
                x, y = evt.touches[0].pageX, evt.touches[0].pageY
            else:
                self.mouseUpRow, self.mouseUpCol = None, None  # cancel move
                return
        # print(f'     x: {x}, y: {y}, cellSize: {self.cellSize}, coords: {self.coords2rowcol(x, y)}')
        self.mouseUpRow, self.mouseUpCol = self.coords2rowcol(x, y)

    def pointerEnd(self, evt):
        print(f'{evt.type} {evt.target.id}')
        print(f'    {self.mouseDownRow}, {self.mouseDownCol} -> {self.mouseUpRow}, {self.mouseUpCol}')
        print(f'last timestamp: {self.lastPointerMoveTimeStamp}, current: {evt.timeStamp}, dif: {evt.timeStamp - self.lastPointerMoveTimeStamp}')
        if evt.type == 'touchmove':
            evt.preventDefault()
        
        dc = self.mouseUpCol - self.mouseDownCol
        if abs( dc ) <= GUI.SMALL_MOVE:
            deltaC = 0
        elif dc > 0:
            deltaC = 1
        else:
            deltaC = -1

        dr = self.mouseUpRow - self.mouseDownRow
        if abs( dr ) <= GUI.SMALL_MOVE:
            deltaR = 0
        elif dr > 0:
            deltaR = 1
        else:
            deltaR = -1

        if self.board.guided:
            if deltaR == 0 and deltaC == 0:
                self.board.teleport(guided=True, coords=(self.mouseUpRow, self.mouseUpCol))
        else:
            self.board.repeat = self.board.repeat or (evt.timeStamp - self.lastPointerMoveTimeStamp < GUI.FAST_MOVE)
            self.board.repeat = self.board.repeat or (dc**2 + dr**2 > GUI.BIG_MOVE**2)
            self.board.move(deltaR,deltaC)
            self.lastPointerMoveTimeStamp = evt.timeStamp

    def keyPressed(self, evt):
        if evt.type == 'keydown':
            print('keydown', evt.key)
            if evt.key == 'Shift':
                self.board.setRepeat('on')
            elif evt.key in self.keydownArrows:
                self.keydownArrows[evt.key] = True
            return

        if evt.type == 'keyup':
            print('keyup', evt.key)
            if evt.key == 'Shift':
                self.board.setRepeat('off')
            elif evt.key in '123456789 ' or evt.key in ['Home', 'End', 'PageUp', 'PageDown', 'Clear']:
                deltaR, deltaC = 0, 0
                if evt.key in '741' or evt.key in ['Home', 'End']:
                    deltaC = -1
                elif evt.key in '963' or evt.key in ['PageUp', 'PageDown']:
                    deltaC = 1
                if evt.key in '789' or evt.key in ['Home', 'PageUp']:
                    deltaR = -1
                elif evt.key in '123' or evt.key in ['End', 'PageDown']:
                    deltaR = 1
                self.board.move(deltaR,deltaC)
            elif evt.key in self.keydownArrows:
                if not self.keydownArrows[evt.key]:
                    return # this is the keyup of an arrow that has been processed in combination with another
                deltaR, deltaC = 0, 0
                if self.keydownArrows['ArrowUp'   ]:
                    deltaR = deltaR - 1 
                if self.keydownArrows['ArrowDown' ]:
                    deltaR = deltaR + 1 
                if self.keydownArrows['ArrowLeft' ]:
                    deltaC = deltaC - 1 
                if self.keydownArrows['ArrowRight']:
                    deltaC = deltaC + 1 
                self.keydownArrows = {k: False for k in self.keydownArrows}
                print('move', deltaR, deltaC)
                self.board.move(deltaR,deltaC)
            elif evt.key in 'tT':
                self.board.teleport()
            elif evt.key in 'sS':
                self.board.teleport(safe=True)
            elif evt.key in 'gG':
                self.board.setGuided('toggle')
            elif evt.key in 'vV':
                self.board.bomb(big=False)
            elif evt.key in 'bB':
                self.board.bomb(big=True)
            elif evt.key in 'rR':
                self.board.setRepeat('toggle')
            elif evt.key in 'nN':
                self.board.newGame()
            return



    def refreshScores(self):
        browser.document['foeCount'].value = self.board.foeCount
        browser.document['score'].value = self.board.score
        browser.document['highScore'].value = self.board.highScore

    def refreshButtons(self, tool=None):
        tools = self.board.toolStock if tool is None else {tool}
        for t in tools:
            if self.board.toolStock[t] >= 0:
                browser.document[t].value = t + ' ' + str(self.board.toolStock[t] if board.toolStock[t] != 0 else '-')

    def refreshRepeat(self, value):
        if value:
            browser.document['repeat'].style = 'background-color:aqua'
        else:
            browser.document['repeat'].style = 'background-color:whitesmoke'

    def refreshGuided(self, value):
        if value:
            browser.document[BoardObject.TOOL_GUIDED_TELEPORT].style = 'background-color:aqua'
        else:
            browser.document[BoardObject.TOOL_GUIDED_TELEPORT].style = 'background-color:whitesmoke'

    def askNewGame(self):
        return browser.confirm('Play again?')


def test():
    # This is only for testing of the game objects and the interaction between them. It'll run only in a text based environment.

    board = Board( 22, 26, NoGui() )
    board.newGame()
    while True:
        k = input('key (n t s g v b 123456789 r):')
        if k == ' ':
            break

        if k in '123456789':
            deltaR, deltaC = 0, 0
            if k in '741':
                deltaC = -1
            elif k in '963':
                deltaC = 1
            if k in '789':
                deltaR = -1
            elif k in '123':
                deltaR = 1
            board.move(deltaR,deltaC)
        elif k in 'tT':
            board.teleport()
        elif k in 'sS':
            board.teleport(safe=True)
        elif k in 'gG':
            board.setGuided('on')
            board.teleport( guided=True, coords=( int(input('row: ')), int(input('col: ')) ) )
        elif k in 'vV':
            board.bomb(big=False)
        elif k in 'bB':
            board.bomb(big=True)
        elif k in 'rR':
            board.setRepeat('toggle')
        elif k in 'nN':
            board.newGame()
        board.gui.textDisplayBoard( board = board)


if __name__ == "__main__" and not BROWSER:
    test()


if BROWSER:
    board = Board(22, 26)
    gui = GUI(board)
    board.gui = gui
    board.newGame()


