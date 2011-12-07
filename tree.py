#tree
class Node:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.p = player
        self.next = []

class jtree:
    def __init__(self):
        self.data = None

    def add(self, x, y, player):
        if self.data == None:
            self.data = Node(x, y, player)
        else:
            temp = self.data
            temp.next.append(Node(x, y, player))

    #def compare(self, sequence): #sequence is one corner's sequence

"""
def recur(data_string, temp): #data string is the file, temp is jtree
    while next_char == ")" or next_char == "(" or next_char == ";":
        if next_char == ")": ### the end of a sequence!  return
            return
        elif next_char == "(": ### I want to look at multiple ( then
            data_string = data_string[1:]
            temp.data = Node(process_move(string[0:4]))
            data_string = data_string[4:]
            recur(data_string, temp.next)
        else: ### a move
            temp.data = Node(process_move(string[0:4]))
            data_string = data_string[4:]
            recur(data_string, temp.next[0])
            return
"""

"""       
b = jtree()
print 'jtree'
b.add(3,4,'W')
print 'add5'
b.add(4,4,'B')
print 'add6'
print b.data.x
print b.data.y
print b.data.p
print b.data.next
"""

#print b.data.value
#print b.data.value
#print b.data.next

#lots of for loops in my .next stuff; don't make the list error again.


