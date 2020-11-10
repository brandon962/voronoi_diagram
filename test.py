import tkinter as tk
import Node as nd
import voronoi as vo
import Line as ln
import time

# global variables
now_set = 0
node_set = []
line_set = []
# functions
def clearCanvas() :
    global node_set,line_set
    canvas.delete('all')
    node_set = []
    line_set = []

def show() :
    text = 'a'
    print(text)

def showNode():
    clearCanvas()
    global now_set
    global node_set
    node_set = nd.CgetNextSet(now_set)
    for i in (node_set) :
        i.node_id = canvas.create_oval(nd.circle(i.x,i.y),fill='red')
    now_set = now_set + 1 

def mouse_place(event):
    global node_set
    add_x, add_y = nd.inverseNode(event.x,event.y)
    node_set.append( nd.Node(add_x,add_y))
    node_set[-1].node_id = canvas.create_oval(nd.circle(add_x,add_y),fill='red')

def vor_recursive(start,end):
    global node_set,line_set
    
    if end - start > 1 :
        left = vor_recursive(start,int((start+end)/2))
        right = vor_recursive(int((start+end)/2)+1,end)
    else:
        if start == end :
            return [start,start]


        left = node_set[start]
        right = node_set[end]

        mx,my,vx,vy = vo.midline([left.x,left.y],[right.x,right.y])
        line_set.append(ln.Line(mx,my,vx,vy))
        line_set[-1].line_id = canvas.create_line(nd.node(line_set[-1].x+100*line_set[-1].b,line_set[-1].y-100*line_set[-1].a),nd.node(line_set[-1].x-100*line_set[-1].b,line_set[-1].y+100*line_set[-1].a),fill='black')
        line_set[-1].node_index.append(start)
        line_set[-1].node_index.append(end)
        node_set[start].line_index.append(len(line_set)-1)
        node_set[end].line_index.append(len(line_set)-1)
        return [start,end]

    # left_first = [left[0],node_set[left[0]].y]
    # for i in range(left[0],left[1]+1) :
    #     if node_set[i].y > left_first[1]:
    #         left_first = [i,node_set[i].y]

   

    temp_line = ln.Line(node_set[left[0]].x,node_set[left[0]].y,node_set[left[1]].x-node_set[left[0]].x,node_set[left[1]].y-node_set[left[0]].y)
    if ln.underLine(temp_line,node_set[right[0]]) == 0 :
        mx,my,vx,vy = vo.midline([node_set[left[1]].x,node_set[left[1]].y],[node_set[right[0]].x,node_set[right[0]].y])
        line_set.append(ln.Line(mx,my,vx,vy))
        line_set[-1].line_id = canvas.create_line(nd.node(line_set[-1].x+100*line_set[-1].b,line_set[-1].y-100*line_set[-1].a),nd.node(line_set[-1].x-100*line_set[-1].b,line_set[-1].y+100*line_set[-1].a),fill='black')
        line_set[-1].node_index.append(left[1])
        line_set[-1].node_index.append(right)

    else :

        temp_line = ln.Line(node_set[left[0]].x,node_set[left[0]].y,node_set[right[0]].x-node_set[left[0]].x,node_set[right[0]].y-node_set[left[0]].y)
        # canvas.create_line(nd.node(temp_line.x+100*temp_line.b,temp_line.y-100*temp_line.a),nd.node(temp_line.x-100*temp_line.b,temp_line.y+100*temp_line.a),fill='black')
        temp_flag = ln.underLine(temp_line,node_set[left[1]])
        # print(temp_flag)
        if temp_flag == 1:
            left_first = left[1]
        else  :
            left_first = left[0]


    
        mx,my,vx,vy = vo.midline([node_set[left_first].x,node_set[left_first].y],[node_set[right[0]].x,node_set[right[0]].y])
        line_set.append(ln.Line(mx,my,vx,vy))
        # line_set[-1].line_id = canvas.create_line(nd.node(line_set[-1].x+100*line_set[-1].b,line_set[-1].y-100*line_set[-1].a),nd.node(line_set[-1].x-100*line_set[-1].b,line_set[-1].y+100*line_set[-1].a),fill='black')
        line_set[-1].node_index.append(left_first)
        line_set[-1].node_index.append(right)

        # 取得左側線段的index
        line_temp_index = node_set[left_first].line_index[-1]
        # 將原左側線段從畫布上刪除
        # print(str(line_set[line_temp_index].line_id))
        canvas.delete(str(line_set[line_temp_index].line_id))
        
        # 兩線段的交點為cx,cy
        _,cx,cy = ln.crossLine(line_set[-1],line_set[line_temp_index])

        
        

        line_set[line_temp_index].x,line_set[line_temp_index].y = cx,cy

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


        temp_line = ln.Line(node_set[left[0]].x,node_set[left[0]].y,node_set[left[1]].x-node_set[left[0]].x,node_set[left[1]].y-node_set[left[0]].y)

        if ln.underLine(temp_line,node_set[right[0]]) == -1 :
            if line_set[line_temp_index].vy < 0 :
                line_set[line_temp_index].vx = -1 * line_set[line_temp_index].vx
                line_set[line_temp_index].vy = -1 * line_set[line_temp_index].vy


        if ln.underLine(temp_line,node_set[right[0]]) == 1 :
            if line_set[line_temp_index].vy > 0 :
                line_set[line_temp_index].vx = -1 * line_set[line_temp_index].vx
                line_set[line_temp_index].vy = -1 * line_set[line_temp_index].vy

        
        

        canvas.create_line(nd.node(cx,cy),nd.node(cx+1000*line_set[line_temp_index].vx,cy+1000*line_set[line_temp_index].vy),fill='red')

        if line_set[-1].vy < 0 :
            line_set[line_temp_index].vx = -1 * line_set[line_temp_index].vx
            line_set[line_temp_index].vy = -1 * line_set[line_temp_index].vy
        
        canvas.create_line(nd.node(cx,cy),nd.node(cx+100*line_set[-1].vx,cy+100*line_set[-1].vy),fill='blue')

        if left[0] == left_first :
            another = left[1]
        else :
            another = left[0]

        
        mx,my,vx,vy = vo.midline([node_set[another].x,node_set[another].y],[node_set[right[0]].x,node_set[right[0]].y])
        vx = -vx
        vy = -vy
        line_set.append(ln.Line(mx,my,vx,vy))
        line_set[-1].line_id = canvas.create_line(nd.node(cx,cy),nd.node(cx+100*line_set[-1].vx,cy+100*line_set[-1].vy),fill='green')
    

    










def vor_main():
    global node_set,line_set
    node_set.sort()
    vor_recursive(0,len(node_set)-1)


def run():
    global node_set,line_set

    vor_main()

    #x,y,vx,vy = vo.midline([100,100],[100,50])
    #x,y,vx,vy = vo.midline(node_set[0],node_set[1])
   
    
    #line_id.append(canvas.create_line(cx+100*cvx,cy+100*cvy,cx-100*cvx,cy-100*cvy,fill='black'))
    #print(len(line_id))
    #line_id.append(canvas.create_line(nd.node(x-100*vx,y-100*vy),nd.node(x+100*vx,y+100*vy),fill='black'))
    
    #line_set.append(ln.Line(x,y,vx,vy))
    #line_id.append(canvas.create_line(nd.node(line_set[-1].x+100*line_set[-1].b,line_set[-1].y-100*line_set[-1].a),nd.node(line_set[-1].x-100*line_set[-1].b,line_set[-1].y+100*line_set[-1].a),fill='black'))
    #print(len(line_id))

def deleteline():
    print()





if __name__ == '__main__' :
    home_window = tk.Tk()

    home_window.title('voronoi diagram')
    home_window.geometry('750x700')
    home_window.configure(background='green')

    bottom_frame = tk.Frame(home_window)
    bottom_frame.pack(side=tk.TOP)

    entry_coordinate = tk.Entry(home_window, relief = 'sunken')
    entry_coordinate.place(x = 650, y = 50, width = 80, height = 600)

    canvas = tk.Canvas(home_window, bg = 'white',height = 600,width = 600, relief = 'sunken')
    canvas.bind('<Button-1>', mouse_place)
    canvas.place(x = 20, y = 50, width = 600, height = 600)

    burtton_read = tk.Button(bottom_frame, text='read file', fg='black')
    burtton_read.pack(side=tk.LEFT)
    burtton_next = tk.Button(bottom_frame, text='next set', fg='black', command=showNode)
    burtton_next.pack(side=tk.LEFT)
    burtton_write = tk.Button(bottom_frame, text='write file', fg='black')
    burtton_write.pack(side=tk.LEFT)
    button_play = tk.Button(bottom_frame, text='play', fg='black', command=run)
    button_play.pack(side=tk.LEFT)
    button_step = tk.Button(bottom_frame, text='step by step', fg='black', command=deleteline)
    button_step.pack(side=tk.LEFT)
    button_clear = tk.Button(bottom_frame, text='clear', fg='black', command=clearCanvas)
    button_clear.pack(side=tk.LEFT)
    
    nd.CreadNode('node1.txt')


    home_window.mainloop()

    
    
    