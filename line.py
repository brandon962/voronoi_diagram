def crossLine(line_a,line_b):
    if line_a.a * line_b.b == line_a.b * line_b.a :
        return False,0,0
    
    return True,((line_a.b*line_b.c-line_a.c*line_b.b)/(line_a.a*line_b.b-line_a.b*line_b.a)),((line_a.a*line_b.c-line_a.c*line_b.a)/(line_a.b*line_b.a-line_a.a*line_b.b))
    
def underLine(line, node):
    if line.a * node.x + line.b * node.y + line.c  == 0 :
        return 0
    # print(line.a * node.x + line.b * node.y + line.c)
    if line.a * node.x + line.b * node.y + line.c  > 0 :
        return 1
    return -1

def sameSide(line,_x1,_y1,_x2,_y2) :
    temp1 = line.a*_x1 + line.b*_y1 + line.c
    temp2 = line.a*_x2 + line.b*_y2 + line.c

    if temp1*temp2 > 0 :
        return True
    return False

def eraseLine(l):
    l.draw = False
    return l.line_id


class Line() :
    def __init__(self,_x,_y,_vx,_vy):
        self.x = _x
        self.y = _y
        self.vx = _vx
        self.vy = _vy
        self.a = -1*_vy
        self.b = _vx
        self.c = -1*(self.a*_x+self.b*_y)

    def __lt__ (self,other):
        return (self.x,self.y,self.ex,self.ey) < (other.x,other.y,other.ex,other.ey)

    def test(self):
        print("?")
    
    def findY(self,_x):
        return -1*(self.a*_x+self.c)/self.b

    x = 0
    y = 0
    ex = 0
    ey = 0
    start = []
    end = []
    vx = 0
    vy = 0
    # ax + by + c = 0
    a = 0
    b = 0
    c = 0
    have_end = False
    node_index = []
    # 0 : right, 1 : left
    dir = 0
    line_id = 0
    draw = True

    




