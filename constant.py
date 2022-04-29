class Tools:
    # Types of tools that the Hero can find in the Board. 
    # These will be the id(s) of the corresponding buttons in the DOM and the keys in the dictionary 
    # that keeps account of the stock of each tool
    SMALL_BOMB      = 'v'
    BIG_BOMB        = 'b'
    TELEPORT        = 't'
    SAFE_TELEPORT   = 's'
    GUIDED_TELEPORT = '\u0398'
    
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
    HERO            = 'imgHero.png'
    DEAD_HERO       = 'imgDeadHero.png'
    FOE             = 'imgFoe.png'
    FIRE            = 'imgFire.png'
    SMALL_BOMB      = 'imgSmallBomb.png'
    BIG_BOMB        = 'imgBigBomb.png'
    SAFE_TELEPORT   = 'imgSafeTeleport.png'
    GUIDED_TELEPORT = 'imgGuidedTeleport.png'

class Metrics:
    # metrics that will determine how difficult the game will be to play
    BOARD_DIM = (26,22)
    INIT_FOE_COUNT = 0
    INCREMENT_FOE_COUNT_BY_LEVEL = 5
    DROP_TOOL_MU = 0
    DROP_TOOL_SIGMA = 1
    INIC_TOOL_STOCK = {
        Tools.TELEPORT: -1,
        Tools.SAFE_TELEPORT: 1,
        Tools.GUIDED_TELEPORT: 1,
        Tools.SMALL_BOMB: 1,
        Tools.BIG_BOMB: 1,            
    }
    DIE_BEYOND_EDGES = False


