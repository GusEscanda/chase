class HTMLElmnt:
    BATTLE_FIELD                  = 'field'
    SMALL_BOMB_BUTTON             = 'v'
    BIG_BOMB_BUTTON               = 'b'
    TELEPORT_BUTTON               = 't'
    SAFE_TELEPORT_BUTTON          = 's'
    GUIDED_TELEPORT_BUTTON        = 'g'
    CIRCLES_ID_SUFFIX             = 'Circle'
    CIRCLES_PARENT_ID_PREFIX      = 'count-indicator-'
    INFINITE_ID_PREFIX            = 'count-infinite-'
    NEW_GAME_BUTTON               = 'new'
    GUIDED_TELEPORT_CURSOR_SCOPE  = 'separationWrapper'
    TITLE_SCREEN_DIALOG           = 'gameTitleScreen'
    TEXT_LEVEL                    = 'level'
    DIV_LEVEL                     = 'div-level'
    TEXT_FOE_COUNT                = 'foeCount'
    DIV_FOE_COUNT                 = 'div-foeCount'
    TEXT_SCORE                    = 'score'
    DIV_SCORE                     = 'div-score'
    TEXT_HIGH_SCORE               = 'highScore'
    DIV_HIGH_SCORE                = 'div-highScore'
    TEXT_SAFENESS                 = 'safeness'
    DIV_SAFENESS                  = 'div-safeness'
    TEXT_STEPS                    = 'steps'
    DIV_STEPS                     = 'div-steps'
    SND_FIRE                      = 'sndFire'
    SND_GET_TOOL                  = 'sndGetTool'
    SND_LEVEL_UP                  = 'sndLevelUp'
    SND_LOST                      = 'sndLost'
    INSTRUCTIONS_TOGGLE           = 'instructions-toggle'
    INSTRUCTIONS                  = 'instructions'
    INSTRUCTIONS_CLOSE            = 'instructions-close'



class CSSClass:
    COUNT_INDICATOR               = 'count-indicator__circle--active'
    GUIDED_TELEPORT_CURSOR        = 'separation-wrapper--guided-teleport-cursor'
    SELECTED_BUTTON               = 'button-selected'
    HIDE                          = 'hide'
    TITLE_SCREEN_ACTIVE           = 'game-title--active'
    INSTRUCTIONS_ACTIVE           = 'instructions--active'


class Tools:
    # Types of tools that the Hero can find in the Board.
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

class Metrics:
    # metrics that will determine how difficult the game will be to play
    BOARD_DIM = (26,22)
    INIT_FOE_COUNT = 0
    INCREMENT_FOE_COUNT_BY_LEVEL = 10
    DROP_TOOL_MU = 0
    DROP_TOOL_SIGMA = 1
    MAX_TOOL_STOCK = 5
    TOOL_INFINITE = 100
    TOOL_DISABLE = -1
    INIC_TOOL_STOCK = {
        Tools.TELEPORT: TOOL_INFINITE,
        Tools.SAFE_TELEPORT: 3,
        Tools.GUIDED_TELEPORT: 3,
        Tools.SMALL_BOMB: 3,
        Tools.BIG_BOMB: 3,            
    }
    DIE_BEYOND_EDGES = False

class Anim:
    # times involved in animation (in ms)
    STEP_TIME = 50
