import http
import math
from constant import CSSClass, HTMLElmnt, Metrics, Tools, Anim, PlayMode, ToolHTMLElement
from util import int2az, az2int

try:
    import browser
    from browser import document, svg, alert, timer, window, html
    # I'm running in a web browser => use Brython to manage the GUI (https://brython.info/)
    BROWSER = True
except:
    # Brython isn't available
    BROWSER = False


class GUI:
    # class to manage all the Graphical User Interfase based on Brython and the browser objects

    SMALL_MOVE = 1
    BIG_MOVE = 15
    FAST_MOVE = 250  # milliseconds between clicks in a double click

    def __init__(self, board):

        self.board = board

        self.field = browser.document[HTMLElmnt.BATTLE_FIELD]

        self.animWhen = 0
        
        self.width =  self.field.offsetWidth
        self.height =  self.field.offsetHeight
        print(f'w:{self.width}, h:{self.height}')
        self.cellWidth = self.width / self.board.maxC
        self.cellHeight = self.height / self.board.maxR
        print('cell width, height:', self.cellWidth, self.cellHeight)
        self.relativeTop  = 0
        self.relativeLeft = 0
        self.absoluteTop  = self.field.abs_top  + self.relativeTop
        self.absoluteLeft = self.field.abs_left + self.relativeLeft

        print('rel top left', self.relativeTop, self.relativeLeft)
        print('abs top left', self.absoluteTop, self.absoluteLeft)
        
        self.mouseDownX = None
        self.mouseDownY = None 
        self.mouseUpX = None
        self.mouseUpY = None
        self.lastPointerMoveTimeStamp = 0
        self.lastKeyEventTimeStamp = 0

        self.keydownArrows = {'ArrowUp':False, 'ArrowDown':False, 'ArrowLeft':False, 'ArrowRight':False}
        self.playing = False

        self.audio = True

        self.buttonFunc = []

        self.bindsTitleScreen(bind=True)


    def bindsTitleScreen(self, bind):
        if bind:
            window.bind("mouseup", self.removeTitleAndStart)
            window.bind('touchend', self.removeTitleAndStart)
            window.bind('keyup', self.removeTitleAndStart)
        else:
            window.removeEventListener("mouseup", self.removeTitleAndStart)
            window.removeEventListener('touchend', self.removeTitleAndStart)
            window.removeEventListener('keyup', self.removeTitleAndStart)

    def removeTitleAndStart(self, evt):
        if browser.document[HTMLElmnt.TITLE_SCREEN_DIALOG].classList.contains(CSSClass.TITLE_SCREEN_ACTIVE):
            browser.document[HTMLElmnt.TITLE_SCREEN_DIALOG].classList.remove(CSSClass.TITLE_SCREEN_ACTIVE)
            self.bindsTitleScreen(bind=False)
            if self.board.mode != PlayMode.PUZZLE:
                print('removeTitleAndStart, calling bindsGamePlay ON')
                self.bindsGamePlay(bind=True)
                self.playing = True
                self.field.focus()


    def bindsGamePlay(self, bind):
        if bind:
            print('bindsGamePlay ON')
            self.field.bind("mousedown", self.pointerStart)
            self.field.bind("mousemove", self.pointerMove)
            self.field.bind("mouseup", self.pointerEnd)
            self.field.bind('touchstart', self.pointerStart)
            self.field.bind('touchmove', self.pointerMove)
            self.field.bind('touchend', self.pointerEnd)
            self.field.bind('keydown', self.keyPressed)
            self.field.bind('keyup', self.keyPressed)
            browser.document[HTMLElmnt.INSTRUCTIONS_TOGGLE].bind( 'click', lambda e: self.gameClickButton(HTMLElmnt.INSTRUCTIONS_TOGGLE) )
            browser.document[HTMLElmnt.AUDIO].bind('click', lambda e: self.gameClickButton(HTMLElmnt.AUDIO) )
            browser.document[HTMLElmnt.AUDIO_OFF].bind('click', lambda e: self.gameClickButton(HTMLElmnt.AUDIO_OFF) )
            browser.document[HTMLElmnt.TELEPORT_BUTTON].bind( 'click', lambda e: self.gameClickButton(HTMLElmnt.TELEPORT_BUTTON) )
            browser.document[HTMLElmnt.SAFE_TELEPORT_BUTTON].bind( 'click', lambda e: self.gameClickButton(HTMLElmnt.SAFE_TELEPORT_BUTTON) )
            browser.document[HTMLElmnt.GUIDED_TELEPORT_BUTTON].bind( 'click', lambda e: self.gameClickButton(HTMLElmnt.GUIDED_TELEPORT_BUTTON) )
            browser.document[HTMLElmnt.SMALL_BOMB_BUTTON].bind( 'click', lambda e: self.gameClickButton(HTMLElmnt.SMALL_BOMB_BUTTON) )
            browser.document[HTMLElmnt.BIG_BOMB_BUTTON].bind( 'click', lambda e: self.gameClickButton(HTMLElmnt.BIG_BOMB_BUTTON) )
            browser.document[HTMLElmnt.NEW_GAME_BUTTON].bind( 'click', lambda e: self.gameClickButton(HTMLElmnt.NEW_GAME_BUTTON) )
        else:
            self.field.unbind("mousedown")
            self.field.unbind("mousemove")
            self.field.unbind("mouseup")
            self.field.unbind('touchstart')
            self.field.unbind('touchmove')
            self.field.unbind('touchend')
            self.field.unbind('keydown')
            self.field.unbind('keyup')
            browser.document[HTMLElmnt.INSTRUCTIONS_TOGGLE].unbind( 'click')
            browser.document[HTMLElmnt.AUDIO].unbind('click')
            browser.document[HTMLElmnt.AUDIO_OFF].unbind('click')
            browser.document[HTMLElmnt.TELEPORT_BUTTON].unbind( 'click')
            browser.document[HTMLElmnt.SAFE_TELEPORT_BUTTON].unbind( 'click')
            browser.document[HTMLElmnt.GUIDED_TELEPORT_BUTTON].unbind( 'click')
            browser.document[HTMLElmnt.SMALL_BOMB_BUTTON].unbind( 'click')
            browser.document[HTMLElmnt.BIG_BOMB_BUTTON].unbind( 'click')
            browser.document[HTMLElmnt.NEW_GAME_BUTTON].unbind( 'click')

    def gameClickButton(self, elemId):
        if elemId == HTMLElmnt.INSTRUCTIONS_TOGGLE:
            self.showInstructions(True)
        elif elemId == HTMLElmnt.AUDIO:
            self.toggleAudio(False)
        elif elemId == HTMLElmnt.AUDIO_OFF:
            self.toggleAudio(True)
        elif elemId == HTMLElmnt.TELEPORT_BUTTON:
            self.board.teleport()
        elif elemId == HTMLElmnt.SAFE_TELEPORT_BUTTON:
            self.board.teleport(safe=True)
        elif elemId == HTMLElmnt.GUIDED_TELEPORT_BUTTON:
            self.board.setGuided('toggle')
        elif elemId == HTMLElmnt.SMALL_BOMB_BUTTON:
            self.board.bomb(big=False)
        elif elemId == HTMLElmnt.BIG_BOMB_BUTTON:
            self.board.bomb(big=True)
        elif elemId == HTMLElmnt.NEW_GAME_BUTTON:
            self.board.newGame()
        self.field.focus()    

    def showInstructions(self, show=True):
        if show:
            self.playing = False
            self.field.blur()
            print('showInstructions, calling bindsGamePlay OFF')
            self.bindsGamePlay(bind=False)
            browser.document[HTMLElmnt.INSTRUCTIONS].classList.remove(CSSClass.HIDE)
            browser.document[HTMLElmnt.INSTRUCTIONS_CLOSE].bind( 'click', lambda evt: self.showInstructions(False) )
        else:
            browser.document[HTMLElmnt.INSTRUCTIONS].classList.add(CSSClass.HIDE)
            browser.document[HTMLElmnt.INSTRUCTIONS_CLOSE].unbind('click')
            self.bindsGamePlay(bind=True)
            self.playing = True
            self.field.focus()

    def toggleAudio(self, audio):
        self.audio = audio
        if audio:
            browser.document[HTMLElmnt.AUDIO].classList.remove(CSSClass.HIDE)
            browser.document[HTMLElmnt.AUDIO_OFF].classList.add(CSSClass.HIDE)
        else:
            browser.document[HTMLElmnt.AUDIO].classList.add(CSSClass.HIDE)
            browser.document[HTMLElmnt.AUDIO_OFF].classList.remove(CSSClass.HIDE)
        self.field.focus()

    def _showCard(self, title, content, buttons):
        print('_showCard', title)
        browser.document[HTMLElmnt.CARD_TITLE].innerText = title
        browser.document[HTMLElmnt.CARD_TEXT].innerHTML = content
        for i in range(3):
            browser.document[HTMLElmnt.CARD_BTN[i]].innerText = ''
            browser.document[HTMLElmnt.CARD_BTN[i]].unbind('click')
            browser.document[HTMLElmnt.CARD_BTN[i]].classList.add(CSSClass.HIDE)
        self.buttonFunc = []
        for i, b in enumerate(buttons):
            browser.document[HTMLElmnt.CARD_BTN[i]].innerText = b[0]
            browser.document[HTMLElmnt.CARD_BTN[i]].classList.remove(CSSClass.HIDE)
            browser.document[HTMLElmnt.CARD_BTN[i]].bind('click', b[1])
            self.buttonFunc.append(b[1])
        browser.document[HTMLElmnt.CARD].classList.remove(CSSClass.HIDE)

    def showCard(self, title, content, buttons, immediate=True):
        print('showCard, calling bindsGamePlay OFF')
        self.bindsGamePlay(False)
        self.playing = False
        self.field.blur()
        w = 0 if immediate else self.animWhen + Anim.STEP_TIME
        timer.set_timeout(self._showCard, w, title, content, buttons)

    def hideCard(self, *args, **kwargs):
        print('hideCard')
        browser.document[HTMLElmnt.CARD].classList.add(CSSClass.HIDE)
        browser.document[HTMLElmnt.CARD_TITLE].innerText = ''
        browser.document[HTMLElmnt.CARD_TEXT].innerHTML = ''
        for i in range(len(self.buttonFunc)):
            browser.document[HTMLElmnt.CARD_BTN[i]].innerText = ''
            browser.document[HTMLElmnt.CARD_BTN[i]].unbind('click')
            browser.document[HTMLElmnt.CARD_BTN[i]].classList.add(CSSClass.HIDE)
        self.buttonFunc = []
        print('hideCard, calling bindsGamePlay ON')
        self.bindsGamePlay(True)
        self.playing = True
        self.field.focus()

    def _puzzleResponse(self, title, content, buttons):
        print('_puzzleResponse', title)
        browser.document[HTMLElmnt.RESPONSE_TITLE].innerText = title
        browser.document[HTMLElmnt.RESPONSE_TEXT].innerHTML = content
        self.buttonFunc = []
        for i, b in enumerate(buttons):
            browser.document[HTMLElmnt.RESPONSE_BTN[i]].classList.remove(CSSClass.HIDE)
            browser.document[HTMLElmnt.RESPONSE_BTN[i]].bind('click', b)
            self.buttonFunc.append(b)
        browser.document[HTMLElmnt.PUZZLE_RESPONSE].classList.remove(CSSClass.HIDE)

    def puzzleResponse(self, title, content, buttons, immediate=True):
        print('puzzleResponse, calling bindsGamePlay OFF')
        self.bindsGamePlay(False)
        self.playing = False
        self.field.blur()
        w = 0 if immediate else self.animWhen + Anim.STEP_TIME
        timer.set_timeout(self._puzzleResponse, w, title, content, buttons)
    
    def hidePuzzleResponse(self, *args, **kwargs):
        print('hidePuzzleResponse')
        browser.document[HTMLElmnt.PUZZLE_RESPONSE].classList.add(CSSClass.HIDE)
        for i in range(len(self.buttonFunc)):
            browser.document[HTMLElmnt.RESPONSE_BTN[i]].unbind('click')
            browser.document[HTMLElmnt.RESPONSE_BTN[i]].classList.add(CSSClass.HIDE)
        self.buttonFunc = []
        print('hidePuzzleResponse, calling bindsGamePlay ON')
        self.bindsGamePlay(True)
        self.playing = True
        self.field.focus()
        self.board.puzzle.respSoluc = ''

    def copyPuzzleToClipboard(self):
        self.board.puzzle.respondent = browser.document[HTMLElmnt.RESPONSE_RESPONDENT].value
        self.board.puzzle.response = browser.document[HTMLElmnt.RESPONSE_RESPONSE].value
        area = browser.document[HTMLElmnt.RESPONSE_CLIPBOARD_COPY]
        href = browser.document.location.href
        href = href.split('://')
        protocol = href[0]
        domain = href[1].split('/')[0]
        area.value = protocol + '://' + domain + '/?puzzle=' + str(self.board.puzzle)
        area.classList.remove(CSSClass.HIDE)
        area.focus()
        area.select()
        area.setSelectionRange(0, 99999)
        browser.document.execCommand("copy")
        area.classList.add(CSSClass.HIDE)
        print('Copiado al clipboard:', area.value)

    def startFreeMode(self, *args, **kwargs):
        browser.document.location.href = '.'

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
        if not self.audio:
            return
        timer.set_timeout(browser.document[HTMLElmnt.SND_FIRE].play, self.animWhen + Anim.STEP_TIME)

    def sndGetTool(self):
        if not self.audio:
            return
        timer.set_timeout(browser.document[HTMLElmnt.SND_GET_TOOL].play, self.animWhen)

    def sndLevelUp(self):
        if not self.audio:
            return
        timer.set_timeout(browser.document[HTMLElmnt.SND_LEVEL_UP].play, self.animWhen)

    def sndLost(self):
        if not self.audio:
            return
        timer.set_timeout(browser.document[HTMLElmnt.SND_LOST].play, self.animWhen + Anim.STEP_TIME)

    def resetAnim(self):
        self.animWhen = 0

    def nextStepTime(self):
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
            Class = CSSClass.BOARD_OBJECT, 
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

    def cleanBoard(self):
        timer.set_timeout(self._cleanBoard, self.animWhen + Anim.STEP_TIME)

    def _cleanBoard(self):
        boardObjects = browser.document.select('.'+CSSClass.BOARD_OBJECT)
        print('cleanBoard:', len(boardObjects), 'objects')
        for ob in boardObjects:
            ob.remove()

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
            repeat = evt.shiftKey or \
                     (evt.timeStamp - self.lastPointerMoveTimeStamp < GUI.FAST_MOVE) or \
                     ((length/self.cellWidth) > GUI.BIG_MOVE)
            user = (evt.timeStamp - self.lastPointerMoveTimeStamp < GUI.FAST_MOVE)  # if repeating with double click don't count this as two steps
            self.board.move(deltaR, deltaC, repeat, user)
            self.lastPointerMoveTimeStamp = evt.timeStamp


    def keyPressed(self, evt):
        print(evt.type, evt.key, f"playing: {self.playing}")
        print(f"lastKeyEventTimeStamp: {self.lastKeyEventTimeStamp}, timeStamp: {evt.timeStamp}, diff: {evt.timeStamp-self.lastKeyEventTimeStamp}")
        if evt.timeStamp-self.lastKeyEventTimeStamp < GUI.FAST_MOVE:
            return
        if evt.type == 'keyup':
            self.lastKeyEventTimeStamp = evt.timeStamp

        # Por acá nunca va a pasar!! Llevar todo esto a un event handler especifico XXXXXXX
        if not self.playing:
            if evt.type == 'keyup':
                if evt.key in [' ', 'Enter'] and 0 < len(self.buttonFunc) <= 2:  # if there are 1 or 2 buttons, "click" the 1st one
                    self.buttonFunc[0](evt)
                elif evt.key == 'Escape' and len(self.buttonFunc) > 0:  # if there is at least one button, click the last one
                    self.buttonFunc[-1](evt)
            return

        if evt.type == 'keydown':
            if evt.key in self.keydownArrows:
                self.keydownArrows[evt.key] = True
            return

        if evt.type == 'keyup':
            if evt.key in '123456789 ' or evt.key in ['Home', 'End', 'PageUp', 'PageDown', 'Clear', 'Enter']:
                deltaR, deltaC = 0, 0
                if evt.key in '741' or evt.key in ['Home', 'End']:
                    deltaC = -1
                elif evt.key in '963' or evt.key in ['PageUp', 'PageDown']:
                    deltaC = 1
                if evt.key in '789' or evt.key in ['Home', 'PageUp']:
                    deltaR = -1
                elif evt.key in '123' or evt.key in ['End', 'PageDown']:
                    deltaR = 1
                self.board.move(deltaR, deltaC, evt.shiftKey)
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
                self.board.move(deltaR, deltaC, evt.shiftKey)
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
            elif evt.key in 'nN':
                self.board.newGame()
            return


    def refreshScores(self):
        if self.board.puzzle:
            browser.document[HTMLElmnt.DIV_LEVEL].classList.add(CSSClass.HIDE)
            browser.document[HTMLElmnt.DIV_FOE_COUNT].classList.remove(CSSClass.HIDE)
            browser.document[HTMLElmnt.DIV_SCORE].classList.add(CSSClass.HIDE)
            browser.document[HTMLElmnt.DIV_STEPS].classList.remove(CSSClass.HIDE)
            browser.document[HTMLElmnt.DIV_HIGH_SCORE].classList.add(CSSClass.HIDE)
        else:
            browser.document[HTMLElmnt.DIV_LEVEL].classList.remove(CSSClass.HIDE)
            browser.document[HTMLElmnt.DIV_FOE_COUNT].classList.add(CSSClass.HIDE)
            browser.document[HTMLElmnt.DIV_SCORE].classList.remove(CSSClass.HIDE)
            browser.document[HTMLElmnt.DIV_STEPS].classList.add(CSSClass.HIDE)
            browser.document[HTMLElmnt.DIV_HIGH_SCORE].classList.remove(CSSClass.HIDE)

        browser.document[HTMLElmnt.TEXT_TITLE].textContent = self.board.puzzle.title if self.board.puzzle else 'Chase'
        browser.document[HTMLElmnt.TEXT_LEVEL].textContent = self.board.level
        browser.document[HTMLElmnt.TEXT_FOE_COUNT].textContent = self.board.foeCount
        browser.document[HTMLElmnt.TEXT_SCORE].textContent = self.board.score
        browser.document[HTMLElmnt.TEXT_STEPS].textContent = self.board.steps
        browser.document[HTMLElmnt.TEXT_HIGH_SCORE].textContent = self.board.highScore

    def refreshButtons(self, tool=None):
        tools = self.board.toolStock if tool is None else {tool}
        for t in tools:
            print('refresh buttons', t, self.board.toolStock[t])
            if self.board.toolStock[t] < 0:
                browser.document[ToolHTMLElement[t]].classList.add(CSSClass.HIDE)
            elif self.board.toolStock[t] == Metrics.TOOL_INFINITE:
                browser.document[ToolHTMLElement[t]].classList.remove(CSSClass.HIDE)
                browser.document[HTMLElmnt.INFINITE_ID_PREFIX + ToolHTMLElement[t]].classList.remove(CSSClass.HIDE)
                browser.document[HTMLElmnt.CIRCLES_PARENT_ID_PREFIX + ToolHTMLElement[t]].classList.add(CSSClass.HIDE)
            else:
                browser.document[ToolHTMLElement[t]].classList.remove(CSSClass.HIDE)
                browser.document[HTMLElmnt.INFINITE_ID_PREFIX + ToolHTMLElement[t]].classList.add(CSSClass.HIDE)
                browser.document[HTMLElmnt.CIRCLES_PARENT_ID_PREFIX + ToolHTMLElement[t]].classList.remove(CSSClass.HIDE)
                for c in range(Metrics.MAX_TOOL_STOCK):
                    idCircle = ToolHTMLElement[t] + HTMLElmnt.CIRCLES_ID_SUFFIX + str(c+1)
                    if self.board.toolStock[t] > c:
                        browser.document[idCircle].classList.add(CSSClass.COUNT_INDICATOR)
                    else:
                        browser.document[idCircle].classList.remove(CSSClass.COUNT_INDICATOR)
            browser.document[ToolHTMLElement[t]].blur()  # take the focus off the button (avoid <Enter> or <Space> to erroneously trigger the button)

    def refreshGuided(self, value):
        if value:
            browser.document[HTMLElmnt.GUIDED_TELEPORT_CURSOR_SCOPE].classList.add(CSSClass.GUIDED_TELEPORT_CURSOR)
            browser.document[HTMLElmnt.GUIDED_TELEPORT_BUTTON].classList.add(CSSClass.SELECTED_BUTTON)
        else:
            browser.document[HTMLElmnt.GUIDED_TELEPORT_CURSOR_SCOPE].classList.remove(CSSClass.GUIDED_TELEPORT_CURSOR)
            browser.document[HTMLElmnt.GUIDED_TELEPORT_BUTTON].classList.remove(CSSClass.SELECTED_BUTTON)

    def refreshSafeness(self):
        browser.document[HTMLElmnt.TEXT_SAFENESS].textContent = "{:.4f}".format(self.board.safeness)



