import node

l = []

l.append(node.Node())
l.append(node.Node())
l.append(node.Node())

l[0].setXY(5,10)
l[1].setXY(50,110)

for i in range(3) :
    print(l[i].x)