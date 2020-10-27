import tkinter as tk
import node as nd
import voronoi as vo
import time

# global variables
now_set = 0
node_set = []
node_id = []
line_id = []

# functions
def clearCanvas() :
    canvas.delete('all')

def show() :
    text = 'a'
    print(text)

def showNode():
    clearCanvas()
    global now_set
    global node_set
    global node_id
    node_set = nd.getNextSet(now_set)
    for i in (node_set) :
        node_id.append(canvas.create_oval(nd.circle(i[0],i[1]),fill='red'))
    now_set = now_set + 1 

def mouse_place(event):
    global node_set,node_id
    add_x, add_y = nd.inverseNode(event.x,event.y)
    node_set.append([add_x,add_y])
    node_id.append(canvas.create_oval(nd.circle(add_x,add_y),fill='red'))

def run():
    global node_set,node_id,line_id

    # x,y,vx,vy = vo.midline([50,100],[100,50])
    x,y,vx,vy = vo.midline(node_set[0],node_set[1])
   
    
    #line_id.append(canvas.create_line(cx+100*cvx,cy+100*cvy,cx-100*cvx,cy-100*cvy,fill='black'))
    print(len(line_id))
    line_id.append(canvas.create_line(nd.node(x-100*vx,y-100*vy),nd.node(x+100*vx,y+100*vy),fill='black'))
    print(len(line_id))

def deleteline():
    canvas.delete(line_id[-1])
    line_id.remove(line_id[-1])
    print(len(line_id))





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
    
    nd.readNode('node1.txt')


    home_window.mainloop()

    
    
    