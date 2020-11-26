import math
import Line as ln
total_node_set = []
Ctotal_node_set = []
def distance(a,b):
    len = math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)
    return len

def node(x,y):
    return x,600-y

def inverseNode(x,y):
    return x,600-y

def show2 ():
    print("123")

def circle(x,y):
    minx , miny = node(x-3,y-3)
    maxx, maxy = node(x+3,y+3)
    
    return minx, miny, maxx, maxy

def readNode(path):
    temp_set = []
    start = 1
    with open(path,encoding='utf-8') as f:
        for _,line in enumerate(f) :
            line = line.replace('\n','')
            if len(line) != 0 :
                if line.find('#') :
                    if line.find(' ') == -1 :
                        if start == 0:
                            total_node_set.append(temp_set)
                        start = 0
                        temp_set = []
                    else :
                        temp = line.replace('\n','')
                        a,b = temp.split(' ')
                        temp_set.append([float(a),float(b)])
def CreateNode_old(path):
    n_set = []
    l_set = []
    with open(path,encoding='utf-8') as f:
        for _,line in enumerate(f):
            if line.find('P') == 0:
                # print(line)
                line = line.replace('\n','')
                _,x,y=line.split(' ')
                n_set.append(Node(int(x),int(y)))
                # n_set.append(Node(1,2))
            if line.find('E') == 0:
                line = line.replace('\n','')
                _,x,y,x2,y2=line.split(' ')
                print([x,y,x2,y2])
                l_set.append(ln.Line(int(x),int(y),int(x2)-int(x),int(y2)-int(y)))
    return n_set, l_set

def CreateNode(path):
    temp_set = []
    start = 1
    with open(path,encoding='utf-8') as f:
        for _,line in enumerate(f) :
            line = line.replace('\n','')
            if len(line) != 0 :
                if line.find('#') :
                    if line.find(' ') == -1 :
                        if start == 0:
                            Ctotal_node_set.append(temp_set)
                        start = 0
                        temp_set = []
                    else :
                        temp = line.replace('\n','')
                        a,b = temp.split(' ')
                        temp_set.append(Node(float(a),float(b)))

    #print(total_node_set)

def getNextSet(num_set):
    return total_node_set[num_set]

def CgetNextSet(num_set) :
    return Ctotal_node_set[num_set]

class Node() :
    def __init__(self,_x,_y):
        self.x = _x
        self.y = _y
        self.cx,self.cy = node(self.x,self.y)
        self.line_index = []

    def __lt__ (self,other):
        return (self.x,self.y) < (other.x,other.y)

    def test(self):
        print("!")

    def setXY(self,_x,_y):
        self.x = _x
        self.y = _y
        self.cx,self.cy = node(self.x,self.y)

    def setCXY(self,_cx,_cy):
        self.cx = _cx
        self.cy = _cy
        self.x,self.y = inverseNode(self.cx,self.cy)
    x = 0
    y = 0
    # canvas xy
    cx = 0
    cy = 0
    line_index = []
    close = False
    node_id = 0



