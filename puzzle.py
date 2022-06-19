import urllib.parse
import hashlib
from util import bytes2az, az2int, int2az
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
        'fhhehhjkedelcsbhhycvfaabctcgcxhc/Gustavo/Easy/Try%20this%20one%20first...//////aaa/XgnngpmponrmuHln',
        'flgyfghigggfgyfodpiyjsfdbhebangj/Gustavo/Wait/Just%20sit%20down%20and%20wait%20for%20them//////aaa/XabbbccdcedfdgeheifjfkglgmhnhoinjmjlkkkjlilhlhmgmfngohohpipjpkqlqmrnrosntmtlukujvivhwgwfxexdycybzazHvn',
        'ggcnhugrcljvihhkbqamaefzjhamacii/Gustavo/Lothlorien///////aaa/XcpdxfsfjgeiiimioiqishwmvpqooolnernsksrsauavdvevgHln',
        'hxdogsjrhlgkesezdfijjqgidhaejncz/Gustavo/Tronador///////aaa/XcfecdkcoctfhfnfsfwhehqjqktkwmunrnoproxsvuwkdlhnboerducsipksmHin',
        'ipfyhvgwexirctdpiiccdaambpjchzbf/Gustavo/Gravity///////aaa/VmllmBnpXijggeicgcablfmiogsfvfzczcvizcrfalekgiapeohlapklzoasgslozrqraucuasuuouzrzntjuHln',
        'fkgqhnfxjdfobqhhbhipfsiafxhefsit/Gustavo/Snow/Find%20at%20leat%202%20solutions%20in%207%20steps%21%21//////aab/XafanbobzcycwdudtetexemdkdddbeagifrjwkvmxnvntotvouourtrjpkpjljkljmhnbmmnnqprnqsrsrtrysytxukujqdtbucudHlz',
        'dqcfacghjpjjdqbxiafuijgzjrhshyii/Gustavo/Solve%20this%20one/if%20you%20can...//////aab/BmrnrnsXhngpgqgsirjskqlqlsjuhvkwjymwmyouoqopeudsctbsbvdvbxdyfwendmambiagbeddcbdhfgejflhjjgkejchdfbkkmklimglbncparboeqdtcvaudufsfqgoirjthukrnqppmpxrtsrtouqustusxuyvvHcq',
        'dkccdbhxccdienaibjcqfsjbhhjrhidx/Gustavo/Mendieta///////aab/XfmfnfogngohohphqjskrlsouovownwmzmpoppopqolpkpmpgoenendnalclekfmflglhkimiljlljmjkjghhiigjfhjceefeebdbcdceadbhbidjamcncoapardsctcubsbwcxeyewdvqtruvytyrxspsrrrvrvpurvtuntnsmrjrhsftfufsetivgvhvjukveudtaqcHtw',
        'gsasfabwjcbdbshmddifhbgofadhcibz/Gustavo/Two%20ways/to%20do%20the%20same%20score.%20Find%20them%21%21//////aab/XgqeqeseteufuftdrcrcsdxeybwbvbuauataxhuivkwkxlwnznvowpwpyqvbfdfdgbhchcdddeefegefhekangnhlhkhiihjhjijmlllmlolpmpkqksjsosopnnojoklingnhpgmflefagbicjakalbmbobpbqbrbrcrgrhsitftevdvgqjrkpmvjvkqnqpvqvrsyrzuzuxtwHln',
        'cxcsgrdvgzaahcijemhxbdfnhrighwgq/Gustavo/El%20Renegau///////aab/XkxkumxlxmzhzhqhrhshtgqmqmononqoqorooonnnnmmlminsnunxoyqzpwqvrtsuusuuvhugtgtfsjsktkqjtnrppmqmqgrgsdrdqdqbtbnelekdkgjgihijhjhkjmhnglflelekejeidkckbkfidmendoamajbrcweugvewgxeydzbdbgdfhfjcibgbfaeceddacabaHln',
        'ilcucierauhicaeiabhsiufcgzczjjfn/Gustavo/Taxi%21%21///////aab/XlmkmklkninimlqnroqmtltkulxotrtttpwqvpxnzrztytzuzuwuvupuntntprpqovmvlabbdaeafcfdfdgdifjfkflelclbkbnaobocsbwcwdvcyeygyiygwfqgqdaebfdhdiakalblclekejehghhjikjlimjljkgmgndodpdqatascsdtdvaretfthtitjukriqjpiHln',
        'hujqjufchwisjkjnhbjpeidjbcaeaqap/Gustavo/Walk/just%20walk%20and%20see//////aaa/XabacadaeafagahaiajakalamanaoapavbvcvdvevfvgvhvivjvkvlvmvnvovpvqvrvsvtvvtvsvrvqvpvovnvmvlvkvjvivhvgvfvevdvcvbpaoanamalakajaiahagafaeadacabaazHbb',
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
            self.repondent,
            self.response,
            self.respSoluc,
            self.tools,
            self.bObjs,
        ) = puzzle

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
        
        puzzle = [
            self.author,
            self.title,
            self.message,
            self.authSoluc,
            self.editPass,
            self.repondent,
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
        print(f"'{str(Puzzle(p))}',")
