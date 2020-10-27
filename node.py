total_node_set = []

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

    #print(total_node_set)

def getNextSet(num_set):
    return total_node_set[num_set]

class Node() :
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
    cx = 0
    cy = 0
    line_index = []
    close = False



