class var:
    def __init__(self):
        self.jdstring = ''
        
def jdict():
    f = open(r"C:\Python26\go_analyzer\KJD_example1.sgf", 'r')
    #f = open(r"C:\Python26\go_analyzer\KJD_clean2.sgf", 'r')
    #jdstring = ''
    for line in f:
        jdstring = jdstring + line.strip()
    jt = tree.jtree()
    #imports the joseki dictionary
    #jt = tree.jtree()

def getchar():
    char = jdstring[0]
    jdstring = jdstring[1:]
    return char

def getmove():
    move = var.jdstring[0:5]
    jdstring = jdstring[5:]
    return move

def peekchar():
    return jdstring[0]

def recur_tom():
    ## removes leading (
    getchar()
    node = Node()
    while(peekchar() == '('):
        node.next.append(recur_tom())
    ## removes trailing )
    getchar()
    return node

def bad_recur():
    node = tree.Node()
    while peekchar() == ")" or peekchar() == "(" or peekchar() == ";":
        if peekchar() == ")": ### the end of a sequence!  return
            return None
        elif peekchar() == "(": ### I want to look at multiple ( then
            node.next.append(recur())

            data_string = data_string[1:]
            recur(data_string, temp.next[len(temp.next)])
        else: ### a move
            temp.data = Node(process_move(string[0:4]))
            data_string = data_string[4:]
            recur(data_string, temp.next)
    if line[i+1] == "W":
        player = 'W'              
    elif line[i+1] == "B":
        player = 'B'
    x = coord(line[i+3])
    y = coord(line[i+4])
    return [x, y, p]

        
def recur():
    paren = False
    node = tree.Node()
    if peekchar() == "(":
        getchar()
        paren = True
    if peekchar() == ";":
        move = getmove()
        if move[i+1] == "W":
            player = 'W'              
        elif line[i+1] == "B":
            player = 'B'
        x = coord(line[i+3])
        y = coord(line[i+4])
        return [x, y, p]        
    
    while peekchar() == "(":
        pass

def jdict_cleanformat():
    #imports the joseki dictionary
    jd = open(r"C:\Python26\go_analyzer\KJD_clean2.sgf")
    total = ""
    clean = ""
    comment = False
    for line in jd:
        word = line.strip()
        total = total + str(word)
    print len(total)
    
    for i in range(len(total)):
        if total[i] == '(' or total[i] == ')':
            print str(total[i])
        print str(total[i]),
    print "clean done"
    print len(clean)

    newjd = open(r"C:\Python26\go_analyzer\KJD_clean3.sgf", 'w')
    newjd.write(clean)
    return

#jdict_cleanformat()
