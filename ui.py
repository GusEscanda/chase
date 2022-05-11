import time
import os
import math
from constant import SoundEffects, Tools, Anim

try:
    import browser
    from browser import document, svg, alert, timer, window, html
    # I'm running in a web browser => use Brython to manage the GUI (https://brython.info/)
    BROWSER = True
except:
    # Brython isn't available so use standard python text based interfase
    import os
    BROWSER = False



class UI:

    nullFunction = lambda *args, **kwargs: None

    # override all or any of these functions depending on the type of interfase, text (standard os console) or graphic (via Brython)
    resetAnim = nullFunction
    nextStep = nullFunction
    draw = nullFunction
    translate = nullFunction
    delete = nullFunction
    
    refreshScores = nullFunction
    refreshButtons = nullFunction
    refreshRepeat = nullFunction
    refreshGuided = nullFunction

    sndFire = nullFunction
    sndGetTool = nullFunction
    sndLevelUp = nullFunction
    sndLost = nullFunction

    askNewGame = nullFunction

    textDisplayBoard = nullFunction


class NoGui(UI):
    # when testing the game in text mode (no graphics available) use this class instead to manage the user interfase

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
        
        self.board = board
        
        # self.svgRoot = browser.document["svg_root"] # deprecar si es posible...
        self.field = browser.document["field"]

        self.animWhen = 0
        
        self.width =  self.field.offsetWidth
        self.height =  self.field.offsetHeight
        print(f'w:{self.width}, h:{self.height}')
        self.cellWidth = self.width / self.board.maxC
        self.cellHeight = self.height / self.board.maxR
        print('HOLA!! ', self.width, self.board.maxC, self.board.maxR)
        print('cell width, height:', self.cellWidth, self.cellHeight)
        self.relativeTop  = 0
        self.relativeLeft = 0
        self.absoluteTop  = self.field.abs_top  + self.relativeTop
        self.absoluteLeft = self.field.abs_left + self.relativeLeft

        print('rel top left', self.relativeTop, self.relativeLeft)
        print('abs top left', self.absoluteTop, self.absoluteLeft)
        
        browser.document <= html.AUDIO(id='sndFire', src=SoundEffects.FIRE)
        browser.document <= html.AUDIO(id='sndGetTool', src=SoundEffects.GET_TOOL)
        browser.document <= html.AUDIO(id='sndLevelUp', src=SoundEffects.LEVEL_UP)
        browser.document <= html.AUDIO(id='sndLost', src=SoundEffects.LOST)

        self.mouseDownX = None
        self.mouseDownY = None 
        self.mouseUpX = None
        self.mouseUpY = None
        self.lastPointerMoveTimeStamp = 0

        self.field.bind("mousedown", self.pointerStart)
        self.field.bind("mousemove", self.pointerMove)
        self.field.bind("mouseup", self.pointerEnd)

        self.field.bind('touchstart', self.pointerStart)
        self.field.bind('touchmove', self.pointerMove)
        self.field.bind('touchend', self.pointerEnd)

        window.bind('keydown', self.keyPressed)
        window.bind('keyup', self.keyPressed)
        self.keydownArrows = {'ArrowUp':False, 'ArrowDown':False, 'ArrowLeft':False, 'ArrowRight':False}

        browser.document[Tools.TELEPORT].bind( 'click', lambda evt: self.board.teleport() )
        browser.document['repeat'].bind( 'click', lambda evt: self.board.setRepeat('toggle') )

        browser.document[Tools.SAFE_TELEPORT].bind( 'click', lambda evt: self.board.teleport(safe=True) )
        browser.document[Tools.GUIDED_TELEPORT].bind( 'click', lambda evt: self.board.setGuided('toggle') )
        browser.document[Tools.SMALL_BOMB].bind( 'click', lambda evt: self.board.bomb(big=False) )
        browser.document[Tools.BIG_BOMB].bind( 'click', lambda evt: self.board.bomb(big=True) )

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
        return ( int(left + col * self.cellWidth), int(top + row * self.cellHeight) )

    def coords2rowcol(self, x, y, relative=False):
        top  = self.relativeTop  if relative else self.absoluteTop
        left = self.relativeLeft if relative else self.absoluteLeft
        row = round((y - top - self.cellHeight/2) / self.cellHeight)
        col = round((x - left - self.cellWidth/2) / self.cellWidth)
        row = min( max(0,row), self.board.maxR - 1)
        col = min( max(0,col), self.board.maxC - 1)
        return ( row, col )

    def sndFire(self):
        timer.set_timeout(browser.document['sndFire'].play, self.animWhen + Anim.STEP_TIME)

    def sndGetTool(self):
        timer.set_timeout(browser.document['sndGetTool'].play, self.animWhen)

    def sndLevelUp(self):
        timer.set_timeout(browser.document['sndLevelUp'].play, self.animWhen)

    def sndLost(self):
        timer.set_timeout(browser.document['sndLost'].play, self.animWhen + Anim.STEP_TIME)

    def resetAnim(self):
        self.animWhen = 0

    def nextStep(self):
        self.animWhen += Anim.STEP_TIME

    def _draw(self, img):
        print(f'_draw {img}')
        self.field <= img

    def _translate(self, id, x, y):
        print(f'_translate, id={id} en x:{x}, y:{y}')
        o = browser.document[id]
        o.style['top'] = y
        o.style['left'] = x

    def _delete(self, id):
        print(f'_delete, id={id}')
        browser.document[id].remove()


    def draw(self, boardObj):
        print(f'draw {boardObj.char}, id={boardObj.id} en {boardObj.row}, {boardObj.col}')
        x, y = self.rowcol2coords( boardObj.row, boardObj.col )
        print(f'    x:{x}, y:{y}')
        img = html.IMG(
            id = boardObj.id,
            src = boardObj.shape, 
            alt = boardObj.char,
            Class = 'board-object', 
            style = {
                'height': int(self.cellHeight),
                'width': int(self.cellWidth),
                'top': y, 
                'left': x,
            }
        )        
        timer.set_timeout(self._draw, self.animWhen + Anim.STEP_TIME, img)

    def translate(self, boardObj):
        print(f'translate, id={boardObj.id} en {boardObj.row}, {boardObj.col}')
        x, y = self.rowcol2coords( boardObj.row, boardObj.col )
        timer.set_timeout(self._translate, self.animWhen, boardObj.id, x, y)

    def delete(self, boardObj):
        print(f'delete, id={boardObj.id} en {boardObj.row}, {boardObj.col} type={type(boardObj)}')
        timer.set_timeout(self._delete, self.animWhen + Anim.STEP_TIME, boardObj.id)

    def pointerStart(self, evt):
        print(f'{evt.type} {evt.target.id}')
        if evt.type == 'mousedown':
            x, y = evt.x, evt.y
        elif evt.type == 'touchstart':
            evt.preventDefault()
            if len(evt.touches) == 1:
                x, y = evt.touches[0].pageX, evt.touches[0].pageY
            else:
                self.mouseDownX, self.mouseDownY = None, None  # cancel move
                return
        print(f'     x: {x}, y: {y}, coords: {self.coords2rowcol(x, y)}')
        self.mouseDownX, self.mouseDownY = x, y
        self.mouseUpX, self.mouseUpY = x, y  # if there is no movement the ponterMove will not be fired...
        
    def pointerMove(self, evt):
        # print(f'{evt.type} {evt.target.id}')
        if evt.type == 'mousemove':
            x, y = evt.x, evt.y
        elif evt.type == 'touchmove':
            evt.preventDefault()
            if len(evt.touches) == 1:
                x, y = evt.touches[0].pageX, evt.touches[0].pageY
            else:
                self.mouseUpX, self.mouseUpY = None, None  # cancel move
                return
        # print(f'     x: {x}, y: {y}, coords: {self.coords2rowcol(x, y)}')
        self.mouseUpX, self.mouseUpY = x, y

    def pointerEnd(self, evt):
        print(f'{evt.type} {evt.target.id}')
        print(f'    {self.mouseDownX}, {self.mouseDownY} -> {self.mouseUpX}, {self.mouseUpY}')
        print(f'last timestamp: {self.lastPointerMoveTimeStamp}, current: {evt.timeStamp}, dif: {evt.timeStamp - self.lastPointerMoveTimeStamp}')
        if evt.type == 'touchmove':
            evt.preventDefault()

        deltaX = self.mouseUpX - self.mouseDownX
        deltaY = self.mouseUpY - self.mouseDownY
        length = math.sqrt( deltaX**2 + deltaY**2 )
        print(f'deltaX: {deltaX}, deltaY: {deltaY}, length: {length}')
        if (length/self.cellWidth) < GUI.SMALL_MOVE:
            deltaC, deltaR = 0, 0
        else:
            angle = math.asin(deltaY/length) if deltaX > 0 else math.pi - math.asin(deltaY/length)
            angle = angle + 2*math.pi if angle < 0 else angle
            cuadrant = ( round((angle / math.pi) * 4) / 4 ) * math.pi
            print(f'Angle: {angle/math.pi}*pi, cuadrant: {cuadrant/math.pi}*pi')
            print(f'sin(cuadrant): {math.sin(cuadrant)}, cos(cuadrant): {math.cos(cuadrant)}')
            sign = lambda x: 0 if x == 0 else ( 1 if x > 0 else -1 )
            deltaR = sign(round(math.sin(cuadrant),3))
            deltaC = sign(round(math.cos(cuadrant),3))

        if self.board.guided:
            if deltaR == 0 and deltaC == 0:
                self.board.teleport(guided=True, coords=self.coords2rowcol(self.mouseUpX, self.mouseUpY))
        else:
            self.board.repeat = self.board.repeat or (evt.timeStamp - self.lastPointerMoveTimeStamp < GUI.FAST_MOVE)
            self.board.repeat = self.board.repeat or ((length/self.cellWidth) > GUI.BIG_MOVE)
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
        browser.document['level'].textContent = self.board.level
        browser.document['foeCount'].textContent = self.board.foeCount
        browser.document['score'].textContent = self.board.score
        browser.document['highScore'].textContent = self.board.highScore

    def refreshButtons(self, tool=None):
        tools = self.board.toolStock if tool is None else {tool}
        for t in tools:
            if self.board.toolStock[t] >= 0:
                browser.document[t].value = t + ' ' + str(self.board.toolStock[t] if self.board.toolStock[t] != 0 else '-')

    def refreshRepeat(self, value):
        if value:
            browser.document['repeat'].style['background-color'] = 'aqua'
        else:
            browser.document['repeat'].style['background-color'] = 'whitesmoke'

    def refreshGuided(self, value):
        if value:
            browser.document[Tools.GUIDED_TELEPORT].style['background-color'] = 'aqua'
        else:
            browser.document[Tools.GUIDED_TELEPORT].style['background-color'] = 'whitesmoke'

    def askNewGame(self):
        return browser.confirm('Play again?')

