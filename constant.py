class HTMLElmnt:
    BATTLE_FIELD                  = 'field'
    SMALL_BOMB_BUTTON             = 'v'
    BIG_BOMB_BUTTON               = 'b'
    TELEPORT_BUTTON               = 't'
    SAFE_TELEPORT_BUTTON          = 's'
    GUIDED_TELEPORT_BUTTON        = 'g'
    NEW_GAME_BUTTON               = 'new'
    GUIDED_TELEPORT_CURSOR_SCOPE  = 'separationWrapper'
    TITLE_SCREEN_DIALOG           = 'gameTitleScreen'
    TEXT_LEVEL                    = 'level'
    TEXT_FOE_COUNT                = 'foeCount'
    TEXT_SCORE                    = 'score'
    TEXT_HIGH_SCORE               = 'highScore'


class CSSClass:
    COUNT_INDICATOR               = 'count-indicator__circle--active'
    GUIDED_TELEPORT_CURSOR        = 'separation-wrapper--guided-teleport-cursor'
    SELECTED_BUTTON               = 'button-selected'
    TITLE_SCREEN_ACTIVE           = 'game-title--active'


class Tools:
    # Types of tools that the Hero can find in the Board. 
    # These will be the id(s) of the corresponding buttons in the DOM and the keys in the dictionary 
    # that keeps account of the stock of each tool
    SMALL_BOMB      = 'SmalBomb'
    BIG_BOMB        = 'BigBomb'
    TELEPORT        = 'Teleport'
    SAFE_TELEPORT   = 'SafeTeleport'
    GUIDED_TELEPORT = 'GuidedTeleport'

ToolHTMLElement = {
    Tools.SMALL_BOMB:      HTMLElmnt.SMALL_BOMB_BUTTON,
    Tools.BIG_BOMB:        HTMLElmnt.BIG_BOMB_BUTTON,
    Tools.TELEPORT:        HTMLElmnt.TELEPORT_BUTTON,
    Tools.SAFE_TELEPORT:   HTMLElmnt.SAFE_TELEPORT_BUTTON,
    Tools.GUIDED_TELEPORT: HTMLElmnt.GUIDED_TELEPORT_BUTTON,
}

class Prio:
    # Priority to remain in a cell of the grid when two BoardObject run into each other.
    LOWER     = 0
    HERO      = 10
    FOE       = 50
    FIRE      = 80
    DEAD_HERO = 90

class TextChar:
    HERO            = '\u00B7'
    DEAD_HERO       = 'X'
    FOE             = '\u03A9'
    FIRE            = '\u039E'
    SMALL_BOMB      = 'v'
    BIG_BOMB        = 'b'
    SAFE_TELEPORT   = 's'
    GUIDED_TELEPORT = '\u0398'

class GraphShape:
    HERO            = 'assets/img/user-green.svg'
    DEAD_HERO       = 'assets/img/user-red.svg'
    FOE             = 'assets/img/omega.svg'
    FIRE            = 'assets/img/fire.svg'
    SMALL_BOMB      = 'assets/img/small-bomb.svg'
    BIG_BOMB        = 'assets/img/big-bomb.svg'
    SAFE_TELEPORT   = 'assets/img/safe-teleport.svg'
    GUIDED_TELEPORT = 'assets/img/guided-teleport.svg'

class SoundEffects:
    FIRE        = 'assets/audio/sndFire.wav'
    GET_TOOL    = 'assets/audio/sndTool.mp3'
    LEVEL_UP    = 'assets/audio/sndLevel.mp3'
    LOST        = 'assets/audio/sndLost.mp3'

class Metrics:
    # metrics that will determine how difficult the game will be to play
    BOARD_DIM = (26,22)
    INIT_FOE_COUNT = 0
    INCREMENT_FOE_COUNT_BY_LEVEL = 10
    DROP_TOOL_MU = 0
    DROP_TOOL_SIGMA = 1
    INIC_TOOL_STOCK = {
        Tools.TELEPORT: -1,
        Tools.SAFE_TELEPORT: 3,
        Tools.GUIDED_TELEPORT: 3,
        Tools.SMALL_BOMB: 3,
        Tools.BIG_BOMB: 3,            
    }
    DIE_BEYOND_EDGES = False
    MAX_TOOL_STOCK = 5

class Anim:
    # times involved in animation (in ms)
    STEP_TIME = 50
