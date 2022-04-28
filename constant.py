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


