
import random
import ui
from ui import UI, NoGui, GUI

from constant import Tools

class BoardObject:
    # Mother class for all the board objects, implements the standard behavior and atributes of them.
    
    # Priority to remain in a cell of the grid when two BoardObject run into each other.
    PRIO_LOWER     = 0
    PRIO_HERO      = 10
    PRIO_FOE       = 50
    PRIO_FIRE      = 80
    PRIO_DEAD_HERO = 90

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
        self.tool = Tools.SMALL_BOMB
        self.char = 'v'
        self.draw = self.gui.drawSmallBomb

class BigBomb( BoardObject ):
    def __init__(self, board, row, col):
        BoardObject.__init__(self, board, row, col)
        self.priority = BoardObject.PRIO_LOWER
        self.tool = Tools.BIG_BOMB
        self.char = 'b'
        self.draw = self.gui.drawBigBomb

class SafeTeleport( BoardObject ):
    def __init__(self, board, row, col):
        BoardObject.__init__(self, board, row, col)
        self.priority = BoardObject.PRIO_LOWER
        self.tool = Tools.SAFE_TELEPORT
        self.char = 's'
        self.draw = self.gui.drawSafeTeleport

class GuidedTeleport( BoardObject ):
    def __init__(self, board, row, col):
        BoardObject.__init__(self, board, row, col)
        self.priority = BoardObject.PRIO_LOWER
        self.tool = Tools.GUIDED_TELEPORT
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
            Tools.TELEPORT: -1,
            Tools.SAFE_TELEPORT: 1,
            Tools.GUIDED_TELEPORT: 1,
            Tools.SMALL_BOMB: 1,
            Tools.BIG_BOMB: 1,            
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
        self.guided = value and ( self.tool(Tools.GUIDED_TELEPORT) != 0 )
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
        if safe and self.tool(Tools.SAFE_TELEPORT) == 0:
            return
        if guided and self.tool(Tools.GUIDED_TELEPORT) == 0:
            return
        if not safe and not guided and self.tool(Tools.TELEPORT) == 0:
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
            self.tool(Tools.SAFE_TELEPORT, -1)
        if guided:
            self.tool(Tools.GUIDED_TELEPORT, -1)
        if not safe and not guided:
            self.tool(Tools.TELEPORT, -1)

        self.hero.row = row
        self.hero.col = col
        self.hero.translate( boardObj = self.hero )
        self.setRepeat('off')
        self.move(0,0)
        self.gui.textDisplayBoard(board = self)

    def bomb(self, big=False):
        if self.checkNewGame():
            return
        bombType = Tools.BIG_BOMB if big else Tools.SMALL_BOMB
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


if __name__ == "__main__" and not ui.BROWSER:
    test()


if ui.BROWSER:
    board = Board(26, 22)
    gui = GUI(board)
    board.gui = gui
    board.newGame()


