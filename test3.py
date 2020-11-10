import Line
import Node

l = [Node.Node(1,2),Node.Node(2,4),Node.Node(2,2)]
l.sort()

for i in range(len(l)):
    print(l[i].x)
    print(l[i].y)
    print()
