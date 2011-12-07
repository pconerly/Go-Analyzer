#go_analyzer, 11-9-2010, Peter Conerly
import os

def import_game(sgf):
    corners = [[],[],[],[],[],[],[],[]]
    #print len(corners)
    first_corner = [None,None,None,None]
    tempx = 0
    tempy = 0
    tempp = ''
    tempq = 0
    templist = []
    for line in sgf:
        word = line.strip()
        for i in range(len(line)-5):
            if line[i] == ';' and line[i+2] == '[':
                if line[i+1] == "W":
                    tempp = 'W'              
                elif line[i+1] == "B":
                    tempp = 'B'
                tempx = coord(line[i+3])
                tempy = coord(line[i+4])
                tempq = quadrant(tempx, tempy)
                tempmove = []
                tempmove[2] = tempp
                tempmove[0],tempmove[1] = normalize_coord(tempx, tempy, tempq)
                if tempq != None:
                    if len(corners[tempq]) == 0:
                        first_corner[tempq] = tempp
                    elif corners[tempq][len(corners[tempq])-1][2] == tempp: #not first and previous
                        corners[tempq].append([-1,-1,switch_player(tempp)])
                    corners[tempq].append(tempmove)
    #need to clean each corner
    for k in range(4):
        if len(corners[k]) != 0:
            if corners[k][0][2] == first_corner[k]:
                pass
            else:
                for m in range(len(corners[k])):
                    corners[k][m][2] = switch_player(corners[k][m][2])

    k = 0
    for k in range(4):
        if len(corners[k]) != 0:
            for m in range(len(corners[k])):
                tempmove = [corners[k][m][0], corners[k][m][1], corners[k][m][2]]
                corners[k+4].append(tempmove)
    
    return corners

def switch_player(c):
    if c == "W":
        return "B"
    elif c == "B":
        return "W"
    else:
        print "no player"
        return None

def coord(x):
    x = ord(x) - ord('a')
    #y = ord(y) - ord('a')
    return x

def quadrant(x, y):
    if x < 10 and y < 10:
        return 0
    if x < 10 and y > 10:
        return 1
    if x > 10 and y < 10:
        return 2
    if x > 10 and y > 10:
        return 3
    return None

def normalize_coord(x, y, q):
    if q == 0: #no correction needed
        pass
    if q == 1: #adjust y
        y = 18 - y
    if q == 2: #adjust x
        x = 18 - x
    if q == 3: #adjust x & y
        x = 18 - x
        y = 18 - y
    return (x, y)

def jdict_count():
    #imports the joseki dictionary and counts the number of moves
    jd = open(r"C:\Python26\go_analyzer\Kogo's Joseki Dictionary.sgf")
    count = 0
    for line in jd:
        word = line.strip()
        for i in range(len(line)-5):
            if line[i] == ';':
                count = count + 1
    print count
    return count

def jdict_clean():
    #cleans up the Joseki dictionary
    jd = open(r"C:\Python26\go_analyzer\Kogo's Joseki Dictionary_manual.sgf")
    #jd = open(r"C:\Python26\go_analyzer\KJD_clean_source.sgf")
    #jd = open(r"C:\Python26\go_analyzer\test01.txt")
    #this file is about 1,150,308 characters long
    total = ""
    clean = ""
    comment = False
    for line in jd:
        word = line.strip()
        total = total + str(word)
    print len(total)
    for i in range(len(total)):
        if total[i:i+2] == 'C[':
            comment = True
        elif comment == True and total[i] == ']':
            comment = False
        elif comment == False:
            clean = clean + str(total[i])  
    print "clean done"
    print len(clean)
    clean2 = ""
    for i in range(len(clean)):
        if clean[i:i+2] == 'LB':
            comment = True
        elif comment == True and ( clean[i] == '(' or clean[i] == ')'):
            comment = False
        if comment == False:
            clean2 = clean2 + str(clean[i])
    print "clean done X2"
    print len(clean2)
    clean3 = ""
    bad = ['PL','MA','AW','AB','TR','CR','AE', 'SQ']
    for i in range(len(clean2)):
        if clean2[i:i+2] in bad:
            comment = True
        elif clean2[i:i+3] == ';PL' or clean2[i:i+3] == ';AW':
            comment = True
        elif comment == True and clean2[i] == ']' and clean2[i+1] != '[':
            comment = False
        elif comment == False:
            clean3 = clean3 + str(clean2[i])
    print "clean done X3"
    print len(clean3)
    clean4 = ""
    badsemicolon = [';;', ';(', ';)']
    for i in range(len(clean3)):
        if clean3[i:i+2] in badsemicolon:
            pass
        else:
            clean4 = clean4 + str(clean3[i])
    print "clean done X4"
    print len(clean4)    
    
    jd.close()
    newjd = open(r"C:\Python26\go_analyzer\KJD_clean5.sgf", 'w')
    newjd.write(clean4)
    newjd.close()
    return

class Node:
    def __init__(self):
        self.x = None
        self.y = None
        self.p = None
        self.next = []

class jtree:
    def __init__(self):
        self.jdstring = ''
        self.data = None
        #self.file = 
        
    def jdict(self):
        #imports and prepares jdstring
        #f = open(r"C:\Python26\go_analyzer\KJD_example2.sgf", 'r')
        f = open(r"C:\Python26\go_analyzer\KJD_clean5.sgf", 'r')
        for line in f:
            self.jdstring = self.jdstring + line.strip()
        print "jdstring length is: " + str(len(self.jdstring))
        print

    def getchar(self):
        char = self.jdstring[0]
        self.jdstring = self.jdstring[1:]
        return char

    def getmove(self):
        move = self.jdstring[0:6]
        self.jdstring = self.jdstring[6:]
        return move

    def peekchar(self):
        return self.jdstring[0]
            
    def make_tree(self, step=0):
        paren = False
        node = Node()
        #every ( has a ; following it.
        if self.peekchar() == "(":
            self.getchar()
            paren = True
        if self.peekchar() == ";":
            move = self.getmove()
            if move[1] == "W":
                node.p = 'W'              
            elif move[1] == "B":
                node.p = 'B'
            tempx = coord(move[3])
            tempy = coord(move[4])
            tempq = quadrant(tempx, tempy)
            node.x, node.y = normalize_coord(tempx, tempy, tempq)
        else: #except the first time
            node.x = None
            node.y = None
            node.p = None
        #every move may have ( following it, or a ;
        #if it is a ; then there will only be one entry
        if self.peekchar() == ";":
            node.next.append(self.make_tree(step+1))
        #if it is a ( then there may be multiple ones
        while self.peekchar() == "(":
            node.next.append(self.make_tree(step+1))
        if paren == True:
            tmp = self.getchar()
            if tmp != ')':
                print str(tmp) + " " + str(step)
                print self.getmove() + self.getmove() + self.getmove()
                if node.x != None and node.y != None and node.p != None:
                    print "%d, %d, %s" %(node.x, node.y, node.p)
                else:
                    print "nope"
                print
        return node

def print_tree(j, count = 0):
    if j.x != None and j.y != None and j.p != None:
        print "    "*(count-1) + "%d, %d, %s" %(j.x, j.y, j.p)
    count = count + 1
    for i in range(len(j.next)):
        print_tree(j.next[i], count)
    
def compare(corner, j, step, limit): #returns true or false
    if step == limit:
        return True
    elif len(j.next) == 0:
        return True
    if len(corner) == 0:
        return False
    for i in range(len(j.next)):
        #print j.next[i].x
        #print corner[step][0]
        if corner[0][0] == j.next[i].x and corner[0][1] == j.next[i].y and corner[0][2] == j.next[i].p:
            #print 'ping'
            return compare(corner[1:], j.next[i], step + 1, limit)
    return False
    
def j_analysis(path, j, limit):
    #get the directory of all the games
    #iterate through them with import_game(file)
    #add them through the main list
    game_archive = []
    files = os.listdir(path)
    
    for i in range(len(files)):
        fin = open(path + "/" + files[i])
        if i % 1000 == 0:
            #print i
            pass
        game_archive.append(import_game(fin)) 
        fin.close()
    
    jsum = 0
    for i in range(len(game_archive)):
        if i % 1000 == 0 and i != 0:
            print i
        for q in range(8):
            if len(game_archive[i][q]) != 0:
                if compare(game_archive[i][q], j.data, 0, limit) == True:
                    jsum += 1
    print path
    print str(jsum) + " joseki in " + str(len(game_archive)) + " games"
    print 1.0*jsum/len(game_archive)
    print

def test():
    #jdstring = ''
    #print jdstring + "_this is jdstring"
    j = jtree()
    j.jdict()
    j.data = j.make_tree()
    print_tree(j.data)
#jdict_clean()

    
def master():
    j = jtree()
    j.jdict()
    j.data = j.make_tree()

    game_dirs = []
    game_dirs.append(r'C:\Python26\go_analyzer\go_games\42784games')
    game_dirs.append(r'C:\Python26\go_analyzer\go_games\kgs-19-2010-10-new')
    game_dirs.append(r'C:\Python26\go_analyzer\go_games\847GoSeigen')
    
    for f in game_dirs:
        for i in range(5,10):
            j_analysis(f, j, i)

test()
#master()

