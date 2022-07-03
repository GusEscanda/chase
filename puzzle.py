import urllib.parse
import hashlib
from util import bytes2az, az2int, int2az, decode, encode
from constant import Tools, Metrics, PUZZLE_BOARD_ELEMENTS

class Puzzle:

    PRESETS = [
        'eeRSC445EEeezz85RRy/Gustavo/Easy/Try this one first...//////aaa/HlnXgnngpmponrmu',
        'eeRSC445EEeezz85RRy/Gustavo/Wait/Just sit down and wait for them//////aaa/HvnXabbbccdcedfdgeheifjfkglgmhnhoinjmjlkkkjlilhlhmgmfngohohpipjpkqlqmrnrosntmtlukujvivhwgwfxexdycybzaz',
        'eeRSC445EEeezz85RRy/Gustavo/Lothlorien///////aaa/HlnXcpdxfsfjgeiiimioiqishwmvpqooolnernsksrsauavdvevg',
        'eeRSC445EEeezz85RRy/Gustavo/Tronador///////aaa/HinXcfecdkcoctfhfnfsfwhehqjqktkwmunrnoproxsvuwkdlhnboerducsipksm',
        'eeRSC445EEeezz85RRy/Gustavo/Gravity///////aaa/HlnVmllmBnpXijggeicgcablfmiogsfvfzczcvizcrfalekgiapeohlapklzoasgslozrqraucuasuuouzrzntju',
        'eeRSC445EEeezz85RRy/Gustavo/Snow/Find at leat 2 solutions in 7 steps!!//////aab/HlzXafanbobzcycwdudtetexemdkdddbeagifrjwkvmxnvntotvouourtrjpkpjljkljmhnbmmnnqprnqsrsrtrysytxukujqdtbucud',
        'eeRSC445EEeezz85RRy/Gustavo/Solve this one/if you can...//////aab/HcqBmrnrnsXhngpgqgsirjskqlqlsjuhvkwjymwmyouoqopeudsctbsbvdvbxdyfwendmambiagbeddcbdhfgejflhjjgkejchdfbkkmklimglbncparboeqdtcvaudufsfqgoirjthukrnqppmpxrtsrtouqustusxuyvv',
        'eeRSC445EEeezz85RRy/Gustavo/Mendieta///////aab/HtwXfmfnfogngohohphqjskrlsouovownwmzmpoppopqolpkpmpgoenendnalclekfmflglhkimiljlljmjkjghhiigjfhjceefeebdbcdceadbhbidjamcncoapardsctcubsbwcxeyewdvqtruvytyrxspsrrrvrvpurvtuntnsmrjrhsftfufsetivgvhvjukveudtaqc',
        'eeRSC445EEeezz85RRy/Gustavo/Two ways/to do the same score. Find them!!//////aab/HlnXgqeqeseteufuftdrcrcsdxeybwbvbuauataxhuivkwkxlwnznvowpwpyqvbfdfdgbhchcdddeefegefhekangnhlhkhiihjhjijmlllmlolpmpkqksjsosopnnojoklingnhpgmflefagbicjakalbmbobpbqbrbrcrgrhsitftevdvgqjrkpmvjvkqnqpvqvrsyrzuzuxtw',
        'eeRSC445EEeezz85RRy/Gustavo/El Renegau///////aab/HlnXkxkumxlxmzhzhqhrhshtgqmqmononqoqorooonnnnmmlminsnunxoyqzpwqvrtsuusuuvhugtgtfsjsktkqjtnrppmqmqgrgsdrdqdqbtbnelekdkgjgihijhjhkjmhnglflelekejeidkckbkfidmendoamajbrcweugvewgxeydzbdbgdfhfjcibgbfaeceddacaba',
        'eeRSC445EEeezz85RRy/Gustavo/Taxi!!///////aab/HlnXlmkmklkninimlqnroqmtltkulxotrtttpwqvpxnzrztytzuzuwuvupuntntprpqovmvlabbdaeafcfdfdgdifjfkflelclbkbnaobocsbwcwdvcyeygyiygwfqgqdaebfdhdiakalblclekejehghhjikjlimjljkgmgndodpdqatascsdtdvaretfthtitjukriqjpi',
        'eeRSC445EEeezz85RRy/Gustavo/Walk/just walk and see//////aaa/HbbXabacadaeafagahaiajakalamanaoapavbvcvdvevfvgvhvivjvkvlvmvnvovpvqvrvsvtvvtvsvrvqvpvovnvmvlvkvjvivhvgvfvevdvcvbpaoanamalakajaiahagafaeadacabaaz',
    ]

    PRESETS = [
        'http://127.0.0.1:5500/?puzzle=achfbuhxdlapdhccbucqfehzerethudj/Mmd2INt/rIdK/PXw%20QtzV%20tBa%209j8V8.../123456123456123456/////aaa/XgnngpmponrmuHln',
        'http://127.0.0.1:5500/?puzzle=dojocsapaxhgjajgjsaugreyhzbccyhu/Mmd%20pdHILhI/WIj2/Nmd2%20dzQ%20h2fx%20Sxc%209Ij2%20ytX%202Was/123/////aaa/XabbbccdcedfdgeheifjfkglgmhnhoinjmjlkkkjlilhlhmgmfngohohpipjpkqlqmrnrosntmtlukujvivhwgwfxexdycybzazHvn',
        'http://127.0.0.1:5500/?puzzle=aejrfyfjgucsicclfoehfvgdgmbkaghy/MIQRc9zNQ/528QAn87ax//123456789.1123456789.1123456789.1/////aaa/XcpdxfsfjgeiiimioiqishwmvpqooolnernsksrsauavdvevgHln',
        'http://127.0.0.1:5500/?puzzle=dheehlehjhanecategjdamhzfcftbdcx/6Q8t%20Ju7QzBe/PXnxIGtX//123456789.123456789.123456789./////aaa/XcfecdkcoctfhfnfsfwhehqjqktkwmunrnoproxsvuwkdlhnboerducsipksmHin',
        'http://127.0.0.1:5500/?puzzle=dudliteagrjdcvafjnjogefcgpjkdbet/MNn8Fa%204Ss2f/MXSE78K//123456789.123456789.123456789./////aaa/VmllmBnpXijggeicgcablfmiogsfvfzczcvizcrfalekgiapeohlapklzoasgslozrqraucuasuuouzrzntjuHln',
        'http://127.0.0.1:5500/?puzzle=jdfqgtiegybdddgwejbugmdodeafieiy/N2L%20tLt1/FBn9/47Lh%20S2%20QuI8%203%20S2QDQjtBd%207L%20U%20SQaJV%21%21/123456712345671234567/////aab/XafanbobzcycwdudtetexemdkdddbeagifrjwkvmxnvntotvouourtrjpkpjljkljmhnbmmnnqprnqsrsrtrysytxukujqdtbucudHlz',
        'http://127.0.0.1:5500/?puzzle=ceccanjbcgdsbgdjelfvjshdaobycmfw/Mmd%20pdHILhI/F2QEN%202WjS%20nxN/z9%20K2W%20oSx.../123451234512345/////aab/BmrnrnsXhngpgqgsirjskqlqlsjuhvkwjymwmyouoqopeudsctbsbvdvbxdyfwendmambiagbeddcbdhfgejflhjjgkejchdfbkkmklimglbncparboeqdtcvaudufsfqgoirjthukrnqppmpxrtsrtouqustusxuyvvHcq',
        'http://127.0.0.1:5500/?puzzle=gnajgkeadqgcfjhfgoejdvfwenesfbdd/Y2BuX8t%20UtB8RBS8XnSI/ONLh7a2I//123123123/////aab/XfmfnfogngohohphqjskrlsouovownwmzmpoppopqolpkpmpgoenendnalclekfmflglhkimiljlljmjkjghhiigjfhjceefeebdbcdceadbhbidjamcncoapardsctcubsbwcxeyewdvqtruvytyrxspsrrrvrvpurvtuntnsmrjrhsftfufsetivgvhvjukveudtaqcHtw',
        'http://127.0.0.1:5500/?puzzle=jpiqbagvaxehjddndkaabqcwcuarfkbi/rua%20pdHILhI/P1n%201SKV/22%20h2%202Wa%20VSsN%20Son8N.%20djxc%202Was%21%21/123456789.1123456789.1123456789.1/////aab/XgqeqeseteufuftdrcrcsdxeybwbvbuauataxhuivkwkxlwnznvowpwpyqvbfdfdgbhchcdddeefegefhekangnhlhkhiihjhjijmlllmlolpmpkqksjsosopnnojoklingnhpgmflefagbicjakalbmbobpbqbrbrcrgrhsitftevdvgqjrkpmvjvkqnqpvqvrsyrzuzuxtwHln',
        'http://127.0.0.1:5500/?puzzle=etisjvffdeatjkfndxgqjpdpdeateagn/TNe82%2042L2ILRX9tVS/rA%20YNLuFSD//123456123456123456/////aab/XkxkumxlxmzhzhqhrhshtgqmqmononqoqorooonnnnmmlminsnunxoyqzpwqvrtsuusuuvhugtgtfsjsktkqjtnrppmqmqgrgsdrdqdqbtbnelekdkgjgihijhjhkjmhnglflelekejeidkckbkfidmendoamajbrcweugvewgxeydzbdbgdfhfjcibgbfaeceddacabaHln',
        'http://127.0.0.1:5500/?puzzle=hxjmhheedggcdgcndschflathujoimgr/T7Et%20gSoSxcS/PIOz%21%21//123456712345671234567/////aab/XlmkmklkninimlqnroqmtltkulxotrtttpwqvpxnzrztytzuzuwuvupuntntprpqovmvlabbdaeafcfdfdgdifjfkflelclbkbnaobocsbwcwdvcyeygyiygwfqgqdaebfdhdiakalblclekejehghhjikjlimjljkgmgndodpdqatascsdtdvaretfthtitjukriqjpiHln',
        'http://127.0.0.1:5500/?puzzle=htegjsgsimfhcudchwfycsekgodkczfz/Mmd2INt/WIQ0/lmd2%20fRAh%20ILh%20duN/123/////aaa/XabacadaeafagahaiajakalamanaoapavbvcvdvevfvgvhvivjvkvlvmvnvovpvqvrvsvtvvtvsvrvqvpvovnvmvlvkvjvivhvgvfvevdvcvbpaoanamalakajaiahagafaeadacabaazHbb',
    ]

    def __init__(self, puzzleString):
        puzzle = puzzleString.split('/')
        godPass = 'eeRSC445EEeezz85RRy'
        self.invalid = False
        if len(puzzle) != 11:
            self.invalid = True
            return
        self.integrity = puzzle[0]
        puzzle = puzzle[1:]
        if self.integrity != godPass:
            if self.integrity != bytes2az(hashlib.md5('/'.join(puzzle).encode()).digest()):
                self.invalid = True
                return

        puzzle = [urllib.parse.unquote(elem) for elem in puzzle]
        (
            self.author,
            self.title,
            self.message,
            self.authSoluc,
            self.editPass,
            self.respondent,
            self.response,
            self.respSoluc,
            self.tools,
            self.bObjs,
        ) = puzzle

        self.author = decode(self.author)
        self.title = decode(self.title)
        self.message = decode(self.message)
        self.editPass = decode(self.editPass)
        self.respondent = decode(self.respondent)
        self.response = decode(self.response)

        self.toolStock = { tool: -1 for tool in Metrics.INIC_TOOL_STOCK }
        self.toolStock[Tools.SMALL_BOMB] = az2int(self.tools[0])
        self.toolStock[Tools.BIG_BOMB] = az2int(self.tools[1])
        self.toolStock[Tools.GUIDED_TELEPORT] = az2int(self.tools[2])

        self.bObjList = { bElem: [] for bElem in PUZZLE_BOARD_ELEMENTS }
        i = 0
        while i < len(self.bObjs):
            if self.bObjs[i] in PUZZLE_BOARD_ELEMENTS:
                bElem = self.bObjs[i]
                i += 1
            self.bObjList[bElem].append((az2int(self.bObjs[i]), az2int(self.bObjs[i+1])))
            i += 2

    def __str__(self):
        if self.invalid:
            return ''
        self.tools = int2az(self.toolStock[Tools.SMALL_BOMB]) + \
                     int2az(self.toolStock[Tools.BIG_BOMB]) + \
                     int2az(self.toolStock[Tools.GUIDED_TELEPORT])
        self.bObjs = ''
        for elem in self.bObjList:
            if len(self.bObjList[elem]) > 0:
                self.bObjs += elem
            for row, col in self.bObjList[elem]:
                self.bObjs += int2az(row) + int2az(col)
        self.author = encode(self.author)
        self.title = encode(self.title)
        self.message = encode(self.message)
        self.editPass = encode(self.editPass)
        self.respondent = encode(self.respondent)
        self.response = encode(self.response)
        puzzle = [
            self.author,
            self.title,
            self.message,
            self.authSoluc,
            self.editPass,
            self.respondent,
            self.response,
            self.respSoluc,
            self.tools,
            self.bObjs,
        ]
        integrity = bytes2az(hashlib.md5('/'.join(puzzle).encode()).digest())
        puzzle = [urllib.parse.quote(elem, safe='') for elem in puzzle]
        puzzle = '/'.join(puzzle)
        return integrity + '/' + puzzle


def printPresets():
    for p in Puzzle.PRESETS:
        p = p.split('=')[1]
        print(f"'{str(Puzzle(p))}',")

