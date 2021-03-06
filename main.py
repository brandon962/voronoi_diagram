# 許哲維 Che-wei, Hsu
# M093040082
import tkinter as tk
import node as nd
import voronoi as vo
import line as ln
import time
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from scipy.spatial import ConvexHull, convex_hull_plot_2d

# global variables
now_set = 0
node_set = []
line_set = []
outputfilename_offset = 0
step_offset = 0
read_step = 0
colorFlag = 0
first_step = True

# functions


def readFile():
    global node_set, now_set
    node_set = []
    now_set = 0
    filename = filedialog.askopenfilename()
    print(filename)
    nd.CreateNode(filename)


def readFile_old():
    global node_set, now_set
    clearCanvas()
    node_set = []
    line_set = []
    now_set = 0
    filename = filedialog.askopenfilename()
    print(filename)
    f = open(filename, 'r', encoding="utf-8")
    node_set, line_set = nd.CreateNode_old(filename)
    f.close()

    for i in range(len(node_set)):
        node_set[i].node_id = canvas.create_oval(
            nd.circle(node_set[i].x, node_set[i].y), fill='red')

    for i in range(len(line_set)):
        line_set[i].line_id = canvas.create_line(nd.node(line_set[i].x, line_set[i].y), nd.node(
            line_set[i].x+line_set[i].vx, line_set[i].y+line_set[i].vy), fill='black')


def checkrange(init):
    return int(init)


def writeFile():
    global outputfilename_offset
    temp_node_set = node_set.copy()
    temp_node_set.sort()

    for i in range(len(line_set)):
        if line_set[i].ex < line_set[i].x:
            tx, ty = line_set[i].x, line_set[i].y
            line_set[i].x = line_set[i].ex
            line_set[i].y = line_set[i].ey
            line_set[i].ex = tx
            line_set[i].ey = ty

    temp_line_set = line_set.copy()
    temp_line_set.sort()
    filename = 'output' + str(outputfilename_offset) + '.txt'
    outputfilename_offset += 1
    f = open(filename, 'w')

    for i in range(len(temp_node_set)):
        writeString = 'P ' + \
            str(int(temp_node_set[i].x)) + ' ' + \
            str(int(temp_node_set[i].y)) + '\n'
        f.write(writeString)

    for i in range(len(temp_line_set)):
        writeString = 'E ' + str(checkrange(temp_line_set[i].x)) + ' ' + str(checkrange(temp_line_set[i].y)) + ' ' + str(
            checkrange(temp_line_set[i].ex)) + ' ' + str(checkrange(temp_line_set[i].ey)) + '\n'
        f.write(writeString)

    f.close()

def readStep():
    global first_step,node_set, now_set,read_step
    if first_step:
        first_step = False
        test()
        clearCanvasStep()
        readStep()

    else:
        if read_step > step_offset -1:
            read_step = 0
            readStep()
            return

        clearCanvasStep()
        node_set = []
        line_set = []
        line_color = []
        now_set = 0
        filename = 'step/step' + str(read_step) + '.txt'
        read_step += 1
        # print(filename)
        f = open(filename, 'r', encoding="utf-8")
        node_set, line_set, node_color,line_color = nd.CreateNode_step(filename)
        f.close()


        for i in range(len(node_set)):
            if node_color[i] == 'b':
                color = 'blue'
            elif node_color[i] == 'r':
                color = 'red'
            elif node_color[i] == 'p':
                color = 'purple'
            elif node_color[i] == 'g':
                color = 'green'
            elif node_color[i] == 'o':
                color = 'dark green'
            else :
                color = 'black'
            node_set[i].node_id = canvas.create_oval(
                nd.circle(node_set[i].x, node_set[i].y), fill=color)

        for i in range(len(line_set)):
            if line_color[i] == 'b':
                color = 'blue'
            elif line_color[i] == 'r':
                color = 'red'
            elif line_color[i] == 'p':
                color = 'purple'
            elif line_color[i] == 'g':
                color = 'orange'
            elif line_color[i] == 'o':
                color = 'dark green'
            else :
                color = 'black'

            line_set[i].line_id = canvas.create_line(nd.node(line_set[i].x, line_set[i].y), nd.node(
                line_set[i].x+line_set[i].vx, line_set[i].y+line_set[i].vy), fill=color)

def writeStepTwoConvex(cl,cr,ls,le,rs,re):
    global step_offset,node_set,line_set
    temp_node_set = node_set.copy()
    temp_node_set.sort()

    

    l_temp_line_set = []
    r_temp_line_set = []

    for i in range(ls,le+1):
        for l in node_set[i].line_index:
            l_temp_line_set.append(line_set[l])
    for i in range(rs,re+1):
        for l in node_set[i].line_index:
            r_temp_line_set.append(line_set[l])

    filename = 'step/step' + str(step_offset) + '.txt'
    step_offset += 1
    f = open(filename, 'w')

    for i in range(len(temp_node_set)):
        writeString = 'P r ' + \
            str(int(temp_node_set[i].x)) + ' ' + \
            str(int(temp_node_set[i].y)) + '\n'
        f.write(writeString)

    for i in range(ls,le+1):
        writeString = 'P g ' + \
            str(int(temp_node_set[i].x)) + ' ' + \
            str(int(temp_node_set[i].y)) + '\n'
        f.write(writeString)

    for i in range(rs,re+1):
        writeString = 'P g ' + \
            str(int(temp_node_set[i].x)) + ' ' + \
            str(int(temp_node_set[i].y)) + '\n'
        f.write(writeString)

    for i in range(len(cl)-1):
        writeString = 'E ' + 'b' +' '+ str(node_set[cl[i][0]].x) + ' ' + str(node_set[cl[i][0]].y) + ' '+str(node_set[cl[i+1][0]].x) + ' ' + str(node_set[cl[i+1][0]].y)+ '\n'
        f.write(writeString)
    for i in range(len(cr)-1):
        writeString = 'E ' + 'b' +' '+ str(node_set[cr[i][0]].x) + ' ' + str(node_set[cr[i][0]].y) + ' '+str(node_set[cr[i+1][0]].x) + ' ' + str(node_set[cr[i+1][0]].y)+ '\n'
        f.write(writeString)

    for i in range(len(l_temp_line_set)):
        writeString = 'E r ' + str(checkrange(l_temp_line_set[i].x)) + ' ' + str(checkrange(l_temp_line_set[i].y)) + ' ' + str(
            checkrange(l_temp_line_set[i].ex)) + ' ' + str(checkrange(l_temp_line_set[i].ey)) + '\n'
        f.write(writeString)
    for i in range(len(r_temp_line_set)):
        writeString = 'E g ' + str(checkrange(r_temp_line_set[i].x)) + ' ' + str(checkrange(r_temp_line_set[i].y)) + ' ' + str(
            checkrange(r_temp_line_set[i].ex)) + ' ' + str(checkrange(r_temp_line_set[i].ey)) + '\n'
        f.write(writeString)

    

    f.close()

def writeStepOneConvex(con,ls,le,rs,re):
    global step_offset,node_set,line_set
    temp_node_set = node_set.copy()
    temp_node_set.sort()

    

    l_temp_line_set = []
    r_temp_line_set = []

    for i in range(ls,le+1):
        for l in node_set[i].line_index:
            l_temp_line_set.append(line_set[l])
    for i in range(rs,re+1):
        for l in node_set[i].line_index:
            r_temp_line_set.append(line_set[l])

    filename = 'step/step' + str(step_offset) + '.txt'
    step_offset += 1
    f = open(filename, 'w')

    for i in range(len(temp_node_set)):
        writeString = 'P r ' + \
            str(int(temp_node_set[i].x)) + ' ' + \
            str(int(temp_node_set[i].y)) + '\n'
        f.write(writeString)

    for i in range(ls,le+1):
        writeString = 'P g ' + \
            str(int(temp_node_set[i].x)) + ' ' + \
            str(int(temp_node_set[i].y)) + '\n'
        f.write(writeString)

    for i in range(rs,re+1):
        writeString = 'P g ' + \
            str(int(temp_node_set[i].x)) + ' ' + \
            str(int(temp_node_set[i].y)) + '\n'
        f.write(writeString)

    for i in range(len(con)-1):
        writeString = 'E ' + 'b' +' '+ str(node_set[con[i][0]].x) + ' ' + str(node_set[con[i][0]].y) + ' '+str(node_set[con[i+1][0]].x) + ' ' + str(node_set[con[i+1][0]].y)+ '\n'
        f.write(writeString)
    

    for i in range(len(l_temp_line_set)):
        writeString = 'E r ' + str(checkrange(l_temp_line_set[i].x)) + ' ' + str(checkrange(l_temp_line_set[i].y)) + ' ' + str(
            checkrange(l_temp_line_set[i].ex)) + ' ' + str(checkrange(l_temp_line_set[i].ey)) + '\n'
        f.write(writeString)
    for i in range(len(r_temp_line_set)):
        writeString = 'E g ' + str(checkrange(r_temp_line_set[i].x)) + ' ' + str(checkrange(r_temp_line_set[i].y)) + ' ' + str(
            checkrange(r_temp_line_set[i].ex)) + ' ' + str(checkrange(r_temp_line_set[i].ey)) + '\n'
        f.write(writeString)

    f.close()

def writeStepHy(ln,hn,s,e):
    global step_offset,node_set,line_set
    temp_node_set = node_set.copy()
    temp_node_set.sort()

    temp_line_set = []
    h_temp_line_set = line_set.copy()

    for i in range(s,e+1):
        for l in node_set[i].line_index:
            temp_line_set.append(line_set[l])
    
    filename = 'step/step' + str(step_offset) + '.txt'
    step_offset += 1
    f = open(filename, 'w')

    for i in range(len(temp_node_set)):
        writeString = 'P r ' + \
            str(int(temp_node_set[i].x)) + ' ' + \
            str(int(temp_node_set[i].y)) + '\n'
        f.write(writeString)

    for i in range(s,e+1):
        writeString = 'P g ' + \
            str(int(temp_node_set[i].x)) + ' ' + \
            str(int(temp_node_set[i].y)) + '\n'
        f.write(writeString)

    

    
    for i in range(len(temp_line_set)):
        writeString = 'E k ' + str(checkrange(temp_line_set[i].x)) + ' ' + str(checkrange(temp_line_set[i].y)) + ' ' + str(
            checkrange(temp_line_set[i].ex)) + ' ' + str(checkrange(temp_line_set[i].ey)) + '\n'
        f.write(writeString)

    for i in range(ln,hn+1):
        writeString = 'E p ' + str(checkrange(h_temp_line_set[i].x)) + ' ' + str(checkrange(h_temp_line_set[i].y)) + ' ' + str(
            checkrange(h_temp_line_set[i].ex)) + ' ' + str(checkrange(h_temp_line_set[i].ey)) + '\n'
        f.write(writeString)

    f.close()
    return

def writeStep():
    global step_offset,node_set,line_set
    temp_node_set = node_set.copy()
    temp_node_set.sort()

    temp_line_set = line_set.copy()

    
    filename = 'step/step' + str(step_offset) + '.txt'
    step_offset += 1
    f = open(filename, 'w')

    for i in range(len(temp_node_set)):
        writeString = 'P r ' + \
            str(int(temp_node_set[i].x)) + ' ' + \
            str(int(temp_node_set[i].y)) + '\n'
        f.write(writeString)

    
    for i in range(len(temp_line_set)):
        writeString = 'E k ' + str(checkrange(temp_line_set[i].x)) + ' ' + str(checkrange(temp_line_set[i].y)) + ' ' + str(
            checkrange(temp_line_set[i].ex)) + ' ' + str(checkrange(temp_line_set[i].ey)) + '\n'
        f.write(writeString)


    f.close()
    return

def clearCanvas():
    global node_set, line_set, step_offset, read_step, first_step
    canvas.delete('all')
    node_set = []
    line_set = []
    step_offset = 0
    read_step = 0
    first_step = True


def clearCanvasStep():
    global node_set, line_set, step_offset, read_step
    canvas.delete('all')
    
    


def show():
    text = 'a'
    print(text)


def showNode():
    clearCanvas()
    global now_set
    global node_set
    node_set = nd.CgetNextSet(now_set)
    for i in (node_set):
        i.node_id = canvas.create_oval(nd.circle(i.x, i.y), fill='red')
    now_set = now_set + 1


def mouse_place(event):
    global node_set
    add_x, add_y = nd.inverseNode(event.x, event.y)
    node_set.append(nd.Node(add_x, add_y))
    node_set[-1].node_id = canvas.create_oval(
        nd.circle(add_x, add_y), fill='red')


def cleanLine(atLeft, hyperLeft, hyperRight, temp, nowX, nowY):

    if atLeft == True:
        cleanWay = ln.underLine(line_set[-1], node_set[hyperLeft])
    else:
        cleanWay = ln.underLine(line_set[-1], node_set[hyperRight])

    lineSn = nd.Node(line_set[temp[0]].x, line_set[temp[0]].y)
    
    # lineEn = nd.Node(line_set[temp[0]].ex,line_set[temp[0]].ey)
    if cleanWay == ln.underLine(line_set[-1], lineSn):
        canvas.delete(str(line_set[temp[0]].line_id))
        line_set[temp[0]].ex = nowX
        line_set[temp[0]].ey = nowY
        line_set[temp[0]].line_id = canvas.create_line(nd.node(line_set[temp[0]].x, line_set[temp[0]].y), nd.node(
            line_set[temp[0]].ex, line_set[temp[0]].ey), fill='black')
    else:
        canvas.delete(str(line_set[temp[0]].line_id))
        line_set[temp[0]].x = line_set[temp[0]].ex
        line_set[temp[0]].y = line_set[temp[0]].ey
        line_set[temp[0]].ex = nowX
        line_set[temp[0]].ey = nowY
        line_set[temp[0]].line_id = canvas.create_line(nd.node(line_set[temp[0]].x, line_set[temp[0]].y), nd.node(
            line_set[temp[0]].ex, line_set[temp[0]].ey), fill='black')


def vorononi_merge(left, right, left_convex, right_convex):
    global colorFlag, line_set, node_set
    # for i in left_convex:
    #     canvas.delete(str(i[1]))
    # for i in right_convex:
    #     canvas.delete(str(i[1]))
    if left[0]+2 == right[0]:
        if (node_set[left[0]].x-node_set[left[1]].x)*(node_set[left[0]].y-node_set[right[0]].y) == (node_set[left[0]].x-node_set[right[0]].x)*(node_set[left[0]].y-node_set[left[1]].y):
            vor_recursive(left[0],right[0])
            return
    
    clr = build_convex_1(left[0], right[1]+1)
    
    writeStepOneConvex(clr,left[0],left[1],right[0],right[1])
        
    if True:
        deleteConvex(clr)

        state = find_convex(left_convex, clr[0][0])

        cutline = []
        threeFlag = False

        for i in range(len(clr)):
            # print(find_convex(left_convex,clr[i][0]))
            if find_convex(left_convex, clr[i][0]) != state:
                cutline.append(i-1)
                state = find_convex(left_convex, clr[i][0])

        
        canvas.delete(str(clr[cutline[0]][1]))
        canvas.delete(str(clr[cutline[1]][1]))
        # except:
        #     cutline = []
        #     cutline.append(0)
        #     cutline.append(1)
        #     clr.append([right[1],-1])
        #     print(clr)
        #     print(left_convex)
        #     print(right_convex)
        #     canvas.delete(str(clr[0][1]))
        #     canvas.delete(str(clr[1][1]))
        #     threeFlag = True

        if True:
            midx = 0.5*(node_set[left[-1]].x + node_set[right[0]].x)
            templ1 = ln.Line(node_set[clr[cutline[0]][0]].x, node_set[clr[cutline[0]][0]].y, node_set[clr[cutline[0]+1]
                                                                                                      [0]].x - node_set[clr[cutline[0]][0]].x, node_set[clr[cutline[0]+1][0]].y - node_set[clr[cutline[0]][0]].y)
            templ2 = ln.Line(node_set[clr[cutline[1]][0]].x, node_set[clr[cutline[1]][0]].y, node_set[clr[cutline[1]+1]
                                                                                                      [0]].x - node_set[clr[cutline[1]][0]].x, node_set[clr[cutline[1]+1][0]].y - node_set[clr[cutline[1]][0]].y)
            if templ1.b == 0:
                templ1.b = 0.00000000000001
            if templ2.b == 0:
                templ2.b = 0.00000000000001

            templ1y = -1*(templ1.a*midx+templ1.c)/templ1.b
            templ2y = -1*(templ2.a*midx+templ2.c)/templ2.b

            if templ1y > templ2y:
                if find_convex(left_convex, clr[cutline[0]][0]) == True:
                    hyperLeft = clr[cutline[0]][0]
                    hyperRight = clr[cutline[0]+1][0]
                else:
                    hyperLeft = clr[cutline[0]+1][0]
                    hyperRight = clr[cutline[0]][0]
            else:
                if find_convex(left_convex, clr[cutline[1]][0]) == True:
                    hyperLeft = clr[cutline[1]][0]
                    hyperRight = clr[cutline[1]+1][0]
                else:
                    hyperLeft = clr[cutline[1]+1][0]
                    hyperRight = clr[cutline[1]][0]

            if threeFlag == True:
                hyperLeft = left[1]
                hyperRight = right[0]

            notDone = True
            maxY = 100000
            maxX = -4105056004
            lineList = []
            

            nowY = 0
            nowX = 0
            for l in node_set[hyperLeft].line_index:
                lineList.append([l, True])
            for l in node_set[hyperRight].line_index:
                lineList.append([l, False])

            # canvas.create_oval(nd.circle(node_set[hyperLeft].x, node_set[hyperLeft].y), fill='green')
            # canvas.create_oval(nd.circle(node_set[hyperRight].x, node_set[hyperRight].y), fill='yellow')
            mx, my, vx, vy = vo.midline([node_set[hyperLeft].x, node_set[hyperLeft].y], [
                                        node_set[hyperRight].x, node_set[hyperRight].y])
           
            line_set.append(ln.Line(mx, my, vx, vy))
            line_set[-1].node_index = []
            line_set[-1].node_index.append(hyperLeft)
            line_set[-1].node_index.append(hyperRight)
            node_set[hyperLeft].line_index.append(len(line_set)-1)
            node_set[hyperRight].line_index.append(len(line_set)-1)

            for l in lineList:
                _, htx, hty = ln.crossLine(line_set[l[0]], line_set[-1])
                if hty > nowY and hty < maxY and htx != maxX:
                    nowY = hty
                    nowX = htx
                    atLeft = l[1]
                    temp = l

            # canvas.create_line(nd.node(line_set[temp[0]].x,line_set[temp[0]].y),nd.node(line_set[temp[0]].ex,line_set[temp[0]].ey),fill='purple')
            try :
                if atLeft == True:
                    atLeft = True
            except :
                # print(hyperLeft)
                # print(hyperRight)
                # print(node_set[hyperLeft].line_index)
                # print(node_set[hyperRight].line_index)
                atLeft = True
                temp = []
                temp.append(node_set[hyperLeft].line_index[0])
                # print(temp[0])
                # print('p')
                # print(line_set[temp[0]].node_index[0])
                # print('i')

            
            if atLeft == True:
                if hyperLeft == line_set[temp[0]].node_index[0]:
                    nexthyper = line_set[temp[0]].node_index[1]
                else:
                    nexthyper = line_set[temp[0]].node_index[0]
            else:
                if hyperRight == line_set[temp[0]].node_index[0]:
                    nexthyper = line_set[temp[0]].node_index[1]
                else:
                    nexthyper = line_set[temp[0]].node_index[0]

            line_set[-1].ex = nowX
            line_set[-1].ey = nowY

            if line_set[-1].vy < 0:
                line_set[-1].vx = -1 * line_set[-1].vx
                line_set[-1].vy = -1 * line_set[-1].vy

            line_set[-1].x = line_set[-1].ex + 1000*line_set[-1].vx
            line_set[-1].y = line_set[-1].ey + 1000*line_set[-1].vy

            line_set[-1].line_id = canvas.create_line(nd.node(
                line_set[-1].x, line_set[-1].y), nd.node(line_set[-1].ex, line_set[-1].ey), fill='black')

            # 消線
            cleanLine(atLeft, hyperLeft, hyperRight, temp, nowX, nowY)

            bX = nowX
            bY = nowY
            maxY = nowY
            maxX = nowX

            if atLeft == True:
                hyperLeft = nexthyper
            else:
                hyperRight = nexthyper

            while notDone == True:
                lineList = []

                nowY = 0
                nowX = 0
                for l in node_set[hyperLeft].line_index:
                    lineList.append([l, True])
                for l in node_set[hyperRight].line_index:
                    lineList.append([l, False])

                # canvas.create_oval(nd.circle(node_set[hyperLeft].x, node_set[hyperLeft].y), fill='green')
                # canvas.create_oval(nd.circle(node_set[hyperRight].x, node_set[hyperRight].y), fill='yellow')
                mx, my, vx, vy = vo.midline([node_set[hyperLeft].x, node_set[hyperLeft].y], [
                                            node_set[hyperRight].x, node_set[hyperRight].y])
                
                line_set.append(ln.Line(mx, my, vx, vy))
                line_set[-1].node_index = []
                line_set[-1].node_index.append(hyperLeft)
                line_set[-1].node_index.append(hyperRight)
                node_set[hyperLeft].line_index.append(len(line_set)-1)
                node_set[hyperRight].line_index.append(len(line_set)-1)

                nowY = -1

                for l in lineList:
                    _, htx, hty = ln.crossLine(line_set[l[0]], line_set[-1])
                    if hty > nowY and hty < maxY and htx != maxX:
                        nowY = hty
                        nowX = htx
                        atLeft = l[1]
                        temp = l

                if nowY == -1:
                    break
                try:
                    if atLeft == True:
                        if hyperLeft == line_set[temp[0]].node_index[0]:
                            nexthyper = line_set[temp[0]].node_index[1]
                        else:
                            nexthyper = line_set[temp[0]].node_index[0]
                    else:
                        if hyperRight == line_set[temp[0]].node_index[0]:
                            nexthyper = line_set[temp[0]].node_index[1]
                        else:
                            nexthyper = line_set[temp[0]].node_index[0]
                except:
                    # print(len(line_set))
                    # print(temp)
                    # print(line_set[temp[0]].node_index)
                    print()
                line_set[-1].ex = nowX
                line_set[-1].ey = nowY

                line_set[-1].x = bX
                line_set[-1].y = bY

                line_set[-1].line_id = canvas.create_line(nd.node(
                    line_set[-1].x, line_set[-1].y), nd.node(line_set[-1].ex, line_set[-1].ey), fill='black')

                bX = nowX
                bY = nowY
                maxY = nowY
                maxX = nowX

                # 消線
                cleanLine(atLeft, hyperLeft, hyperRight, temp, nowX, nowY)

                if atLeft == True:
                    hyperLeft = nexthyper
                else:
                    hyperRight = nexthyper

            # mx, my, vx, vy = vo.midline([node_set[hyperLeft].x, node_set[hyperLeft].y], [node_set[hyperRight].x, node_set[hyperRight].y])
            if line_set[-1].vy > 0:
                line_set[-1].vy = line_set[-1].vy * -1
                line_set[-1].vx = line_set[-1].vx * -1
            if line_set[-1].vy == 0:
                if atLeft == True:
                    if line_set[-1].vx < 0:
                        line_set[-1].vy = line_set[-1].vy * -1
                        line_set[-1].vx = line_set[-1].vx * -1
                else:
                    if line_set[-1].vx > 0:
                        line_set[-1].vy = line_set[-1].vy * -1
                        line_set[-1].vx = line_set[-1].vx * -1
            line_set[-1].x = bX
            line_set[-1].y = bY
            line_set[-1].ex = line_set[-1].x + 100*line_set[-1].vx
            line_set[-1].ey = line_set[-1].y + 100*line_set[-1].vy
            # print(line_set[-1].y)
            # print(line_set[-1].vy)
            # print(line_set[-1].y + 100*vy)
            # print(line_set[-1].ey)
            line_set[-1].line_id = 0
            line_set[-1].line_id = canvas.create_line(nd.node(line_set[-1].x, line_set[-1].y), nd.node(
                line_set[-1].ex, line_set[-1].ey), fill='black')

            line_set[-1].node_index = []
            line_set[-1].node_index.append(hyperLeft)
            line_set[-1].node_index.append(hyperRight)
            node_set[hyperLeft].line_index.append(len(line_set)-1)
            node_set[hyperRight].line_index.append(len(line_set)-1)
            line_set[-1].testflag = 1
            detectLine()

        detectLine()
        return clr


def detectLine():
    global node_set, line_set
    changes = 0
    special = [-41050560082, -41050560082]
    for l in line_set:
        numLine1 = 0
        numLine2 = 0
        n1 = [l.x, l.y]
        n2 = [l.ex, l.ey]
        for _l in line_set:
            if _l != l:
                _n1 = [_l.x, _l.y]
                if _n1 == special:
                    continue
                _n2 = [_l.ex, _l.ey]
                if n1 == _n1:
                    numLine1 += 1
                if n1 == _n2:
                    numLine1 += 1
                if n2 == _n1:
                    numLine2 += 1
                if n2 == _n2:
                    numLine2 += 1

        if numLine1 + numLine2 < 2:
            changes += 1
            canvas.delete(str(l.line_id))
            for ln in l.node_index:
                for nl in node_set[ln].line_index:
                    if l == line_set[nl]:
                        nl = 0
            l.node_index = []
            l.x = -41050560082
            l.y = -41050560082
            l.ex = -41050560082
            l.ey = -41050560082

    return


def find_convex(listN, node):
    flag = False
    for i in range(len(listN)):
        if node == listN[i][0]:
            flag = True
            break
    return flag


def build_convex(start, end):
    convex_list = []
    if end-start == 2:
        tempID = canvas.create_line(nd.node(node_set[start].x, node_set[start].y), nd.node(
            node_set[end-1].x, node_set[end-1].y), fill='green')
        convex_list.append([start, tempID])
        convex_list.append([end-1, tempID])
        convex_list.append([start, tempID])

    if end-start > 2:

        temp_node = []

        for i in range(start, end):
            temp_node.append([node_set[i].x, node_set[i].y])
        try :
            hull = ConvexHull(temp_node)

            hull_list = []
            for i in hull.vertices:
                hull_list.append(i+start)
            hull_list.append(hull.vertices[0]+start)

            for i in range(len(hull_list)-1):
                tempID = canvas.create_line(nd.node(node_set[hull_list[i]].x, node_set[hull_list[i]].y), nd.node(
                    node_set[hull_list[i+1]].x, node_set[hull_list[i+1]].y), fill='green')
                convex_list.append([hull_list[i], tempID])

            tempID = canvas.create_line(nd.node(node_set[hull_list[0]].x, node_set[hull_list[0]].y), nd.node(
                node_set[hull_list[0+1]].x, node_set[hull_list[0+1]].y), fill='green')
            convex_list.append([hull_list[0], tempID])
        except:
            tempID = canvas.create_line(nd.node(node_set[start].x, node_set[start].y), nd.node(node_set[start+1].x, node_set[start+1].y), fill='red')
            convex_list.append([start,tempID])
            tempID = canvas.create_line(nd.node(node_set[start+1].x, node_set[start+1].y), nd.node(node_set[end-1].x, node_set[end-1].y), fill='red')
            convex_list.append([start+1,tempID])
            tempID = canvas.create_line(nd.node(node_set[end-1].x, node_set[end-1].y), nd.node(node_set[start].x, node_set[start].y), fill='red')
            convex_list.append([end-1,tempID])
            tempID = canvas.create_line(nd.node(node_set[start].x, node_set[start].y), nd.node(node_set[start+1].x, node_set[start+1].y), fill='red')
            convex_list.append([start,tempID])

    return convex_list


def build_convex_1(start, end):
    convex_list = []
    if end-start == 2:
        tempID = canvas.create_line(nd.node(node_set[start].x, node_set[start].y), nd.node(
            node_set[end-1].x, node_set[end-1].y), fill='red')
        convex_list.append([start, tempID])
        convex_list.append([end-1, tempID])

    if end-start > 2:

        temp_node = []

        for i in range(start, end):
            temp_node.append([node_set[i].x, node_set[i].y])
        try :
            hull = ConvexHull(temp_node)

            hull_list = []
            for i in hull.vertices:
                hull_list.append(i+start)
            hull_list.append(hull.vertices[0]+start)

            for i in range(len(hull_list)-1):
                tempID = canvas.create_line(nd.node(node_set[hull_list[i]].x, node_set[hull_list[i]].y), nd.node(
                    node_set[hull_list[i+1]].x, node_set[hull_list[i+1]].y), fill='red')
                convex_list.append([hull_list[i], tempID])

            tempID = canvas.create_line(nd.node(node_set[hull_list[0]].x, node_set[hull_list[0]].y), nd.node(
                node_set[hull_list[0+1]].x, node_set[hull_list[0+1]].y), fill='green')
            convex_list.append([hull_list[0], tempID])
        except:
            tempID = canvas.create_line(nd.node(node_set[start].x, node_set[start].y), nd.node(node_set[start+1].x, node_set[start+1].y), fill='red')
            convex_list.append([start,tempID])
            tempID = canvas.create_line(nd.node(node_set[start+1].x, node_set[start+1].y), nd.node(node_set[end-1].x, node_set[end-1].y), fill='red')
            convex_list.append([start+1,tempID])
            tempID = canvas.create_line(nd.node(node_set[end-1].x, node_set[end-1].y), nd.node(node_set[start].x, node_set[start].y), fill='red')
            convex_list.append([end-1,tempID])
            tempID = canvas.create_line(nd.node(node_set[start].x, node_set[start].y), nd.node(node_set[start+1].x, node_set[start+1].y), fill='red')
            convex_list.append([start,tempID])
    return convex_list


def vorononi_two_point(start, end):

    global node_set, line_set

    left = node_set[start]
    right = node_set[end]

    mx, my, vx, vy = vo.midline([left.x, left.y], [right.x, right.y])
    line_set.append(ln.Line(mx, my, vx, vy))
    line_set[-1].line_id = canvas.create_line(nd.node(line_set[-1].x+1000*line_set[-1].b, line_set[-1].y-1000*line_set[-1].a), nd.node(
        line_set[-1].x-1000*line_set[-1].b, line_set[-1].y+1000*line_set[-1].a), fill='black')

    line_set[-1].node_index.append(start)
    line_set[-1].node_index.append(end)
    tx, ty = line_set[-1].x, line_set[-1].y
    line_set[-1].x = tx+1000*line_set[-1].b
    line_set[-1].y = ty-1000*line_set[-1].a
    line_set[-1].ex = tx-1000*line_set[-1].b
    line_set[-1].ey = ty+1000*line_set[-1].a

    node_set[start].line_index = []
    node_set[start].line_index.append(len(line_set)-1)

    node_set[end].line_index = []
    node_set[end].line_index.append(len(line_set)-1)

    return start, end


def vorononi_recursive(start, end):
    global node_set, line_set

    if end == start:
        return[start, end]

    if end - start == 1:
        vorononi_two_point(start, end)
        return [start, end]
    else:
        left = vorononi_recursive(start, int((start+end)/2))
        right = vorononi_recursive(int((start+end)/2)+1, end)
        left_convex = build_convex(left[0], left[1]+1)
        right_convex = build_convex(right[0], right[1]+1)
        writeStepTwoConvex(left_convex,right_convex,left[0],left[1],right[0],right[1])
        deleteConvex(left_convex)
        deleteConvex(right_convex)
        line_num = len(line_set)
        vorononi_merge(left, right, left_convex, right_convex)
        hyper_num = len(line_set)-1
        # detectLine()
        writeStepHy(line_num,hyper_num,start,end)
    return [start, end]


def deleteConvex(convex):
    for c in convex:
        canvas.delete(str(c[1]))

    return


def test():
    node_set.sort()
    vorononi_recursive(0, len(node_set)-1)
    writeStep()
    return


def convex():

    build_convex(0, len(node_set))

    return


def vor_recursive(start, end):
    global node_set, line_set

    if end - start > 1:
        left = vor_recursive(start, int((start+end)/2))
        right = vor_recursive(int((start+end)/2)+1, end)
    else:
        if start == end:
            return [start, start]

        left = node_set[start]
        right = node_set[end]

        mx, my, vx, vy = vo.midline([left.x, left.y], [right.x, right.y])
        line_set.append(ln.Line(mx, my, vx, vy))
        line_set[-1].line_id = canvas.create_line(nd.node(line_set[-1].x+100*line_set[-1].b, line_set[-1].y-100*line_set[-1].a), nd.node(
            line_set[-1].x-100*line_set[-1].b, line_set[-1].y+100*line_set[-1].a), fill='black')
        line_set[-1].node_index.append(start)
        line_set[-1].node_index.append(end)
        tx, ty = line_set[-1].x, line_set[-1].y
        line_set[-1].x = tx+100*line_set[-1].b
        line_set[-1].y = ty-100*line_set[-1].a
        line_set[-1].ex = tx-100*line_set[-1].b
        line_set[-1].ey = ty+100*line_set[-1].a
        node_set[start].line_index.append(len(line_set)-1)
        node_set[end].line_index.append(len(line_set)-1)
        return [start, end]

    # left_first = [left[0],node_set[left[0]].y]
    # for i in range(left[0],left[1]+1) :
    #     if node_set[i].y > left_first[1]:
    #         left_first = [i,node_set[i].y]

    temp_line = ln.Line(node_set[left[0]].x, node_set[left[0]].y, node_set[left[1]
                                                                           ].x-node_set[left[0]].x, node_set[left[1]].y-node_set[left[0]].y)
    if ln.underLine(temp_line, node_set[right[0]]) == 0:
        mx, my, vx, vy = vo.midline([node_set[left[1]].x, node_set[left[1]].y], [
                                    node_set[right[0]].x, node_set[right[0]].y])
        line_set.append(ln.Line(mx, my, vx, vy))
        line_set[-1].line_id = canvas.create_line(nd.node(line_set[-1].x+100*line_set[-1].b, line_set[-1].y-100*line_set[-1].a), nd.node(
            line_set[-1].x-100*line_set[-1].b, line_set[-1].y+100*line_set[-1].a), fill='black')

        line_set[-1].node_index.append(left[1])
        line_set[-1].node_index.append(right[0])
        tx, ty = line_set[-1].x, line_set[-1].y
        line_set[-1].x = tx+100*line_set[-1].b
        line_set[-1].y = ty-100*line_set[-1].a
        line_set[-1].ex = tx-100*line_set[-1].b
        line_set[-1].ey = ty+100*line_set[-1].a

    else:

        temp_line = ln.Line(node_set[left[0]].x, node_set[left[0]].y, node_set[right[0]
                                                                               ].x-node_set[left[0]].x, node_set[right[0]].y-node_set[left[0]].y)
        # canvas.create_line(nd.node(temp_line.x+100*temp_line.b,temp_line.y-100*temp_line.a),nd.node(temp_line.x-100*temp_line.b,temp_line.y+100*temp_line.a),fill='black')
        temp_flag = ln.underLine(temp_line, node_set[left[1]])
        # print(temp_flag)
        if temp_flag == 1:
            left_first = left[1]
        else:
            left_first = left[0]

        mx, my, vx, vy = vo.midline([node_set[left_first].x, node_set[left_first].y], [
                                    node_set[right[0]].x, node_set[right[0]].y])
        line_set.append(ln.Line(mx, my, vx, vy))
        # line_set[-1].line_id = canvas.create_line(nd.node(line_set[-1].x+100*line_set[-1].b,line_set[-1].y-100*line_set[-1].a),nd.node(line_set[-1].x-100*line_set[-1].b,line_set[-1].y+100*line_set[-1].a),fill='black')
        line_set[-1].node_index.append(left_first)
        line_set[-1].node_index.append(right[0])

        # 取得左側線段的index
        line_temp_index = node_set[left_first].line_index[-1]
        # 將原左側線段從畫布上刪除
        # print(str(line_set[line_temp_index].line_id))
        canvas.delete(str(line_set[line_temp_index].line_id))

        # 兩線段的交點為cx,cy
        _, cx, cy = ln.crossLine(line_set[-1], line_set[line_temp_index])

        line_set[line_temp_index].x, line_set[line_temp_index].y = cx, cy

        # tempy = line_set[line_temp_index].findY(node_set[left_high[0]].x)
        # print(tempy)
        # # 將該線段重畫
        # #canvas.delete(line_set[line_temp_index].line_id)
        # print(ln.sameSide(line_set[line_temp_index],node_set[left_high[0]].x,node_set[left_high[0]].y,node_set[left_high[0]].x + line_set[line_temp_index].vx,node_set[left_high[0]].y + line_set[line_temp_index].vy))
        # #print(ln.sameSide(line_set[line_temp_index],node_set[left_high[0]].x,node_set[left_high[0]].y,node_set[left_high[0]].x + line_set[line_temp_index].vx,node_set[left_high[0]].y + line_set[line_temp_index].vy))

        # canvas.create_line(nd.node(cx,cy),nd.node(node_set[left_high[0]].x,node_set[left_high[0]].y),fill='green')
        # canvas.create_line(nd.node(cx,cy),nd.node(cx+line_set[line_temp_index].vx,cy),fill='blue')

        # if line_set[line_temp_index].vx > 0 :
        #     line_set[line_temp_index].vx = -1 * line_set[line_temp_index].vx
        #     line_set[line_temp_index].vy = -1 * line_set[line_temp_index].vy

        temp_line = ln.Line(node_set[left[0]].x, node_set[left[0]].y, node_set[left[1]
                                                                               ].x-node_set[left[0]].x, node_set[left[1]].y-node_set[left[0]].y)

        if ln.underLine(temp_line, node_set[right[0]]) == -1:
            if line_set[line_temp_index].vy < 0:
                line_set[line_temp_index].vx = - \
                    1 * line_set[line_temp_index].vx
                line_set[line_temp_index].vy = - \
                    1 * line_set[line_temp_index].vy

        if ln.underLine(temp_line, node_set[right[0]]) == 1:
            if line_set[line_temp_index].vy > 0:
                line_set[line_temp_index].vx = - \
                    1 * line_set[line_temp_index].vx
                line_set[line_temp_index].vy = - \
                    1 * line_set[line_temp_index].vy

        line_set[line_temp_index].line_id = canvas.create_line(nd.node(cx, cy), nd.node(
            cx+1000*line_set[line_temp_index].vx, cy+1000*line_set[line_temp_index].vy), fill='black')
        line_set[line_temp_index].x = cx
        line_set[line_temp_index].y = cy
        line_set[line_temp_index].ex = cx+1000*line_set[line_temp_index].vx
        line_set[line_temp_index].ey = cy+1000*line_set[line_temp_index].vy

        # if line_set[-1].vy < 0 :
        #     line_set[line_temp_index].vx = -1 * line_set[line_temp_index].vx
        #     line_set[line_temp_index].vy = -1 * line_set[line_temp_index].vy

        line_set[-1].line_id = canvas.create_line(nd.node(cx, cy), nd.node(
            cx+100*line_set[-1].vx, cy+100*line_set[-1].vy), fill='black')
        line_set[-1].x = cx
        line_set[-1].y = cy
        line_set[-1].ex = cx+100*line_set[-1].vx
        line_set[-1].ey = cy+100*line_set[-1].vy

        if left[0] == left_first:
            another = left[1]
        else:
            another = left[0]

        mx, my, vx, vy = vo.midline([node_set[another].x, node_set[another].y], [
                                    node_set[right[0]].x, node_set[right[0]].y])
        vx = -vx
        vy = -vy
        line_set.append(ln.Line(mx, my, vx, vy))
        line_set[-1].line_id = canvas.create_line(nd.node(cx, cy), nd.node(
            cx+100*line_set[-1].vx, cy+100*line_set[-1].vy), fill='black')
        line_set[-1].x = cx
        line_set[-1].y = cy
        line_set[-1].ex = cx+100*line_set[-1].vx
        line_set[-1].ey = cx+100*line_set[-1].vy
        line_set[-1].node_index.append(another)
        line_set[-1].node_index.append(right[0])


def vor_main():
    global node_set, line_set
    node_set.sort()
    vor_recursive(0, len(node_set)-1)


def run():
    global node_set, line_set

    vor_main()


def deleteline():
    print()


if __name__ == '__main__':
    home_window = tk.Tk()

    home_window.title('voronoi diagram')
    home_window.geometry('640x670')
    home_window.configure(background='green')

    bottom_frame = tk.Frame(home_window)
    bottom_frame.pack(side=tk.TOP)

    # entry_coordinate = tk.Entry(home_window, relief='sunken')
    # entry_coordinate.place(x=650, y=50, width=80, height=600)

    canvas = tk.Canvas(home_window, bg='white', height=600,
                       width=600, relief='sunken')
    canvas.bind('<Button-1>', mouse_place)
    canvas.place(x=20, y=50, width=600, height=600)

    burtton_read = tk.Button(
        bottom_frame, text='read file', fg='black', command=readFile)
    burtton_read.pack(side=tk.LEFT)
    burtton_read = tk.Button(
        bottom_frame, text='read file(old)', fg='black', command=readFile_old)
    burtton_read.pack(side=tk.LEFT)
    burtton_next = tk.Button(
        bottom_frame, text='next set', fg='black', command=showNode)
    burtton_next.pack(side=tk.LEFT)
    burtton_write = tk.Button(
        bottom_frame, text='write file', fg='black', command=writeFile)
    burtton_write.pack(side=tk.LEFT)
    button_play = tk.Button(bottom_frame, text='play', fg='black', command=test)
    button_play.pack(side=tk.LEFT)
    button_step = tk.Button(
        bottom_frame, text='step by step', fg='black', command=readStep)
    button_step.pack(side=tk.LEFT)
    button_clear = tk.Button(bottom_frame, text='clear',
                             fg='black', command=clearCanvas)
    button_clear.pack(side=tk.LEFT)
    # button_clear = tk.Button(bottom_frame, text='convex',
    #                          fg='black', command=convex)
    # button_clear.pack(side=tk.LEFT)
    # button_clear = tk.Button(bottom_frame, text='test',
    #                          fg='black', command=test)
    button_clear.pack(side=tk.LEFT)

    home_window.mainloop()

