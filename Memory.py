#  Memory card Game

import simplegui
import random

list_of_numbers = []

# helper function to initialize globals
def init():
    global list_of_numbers
    global no_of_moves
    
    #global exposed
    global step
    global is_exposed
    no_of_moves = 0
    step = 50
    list1 = range(1,9)
    list2 = range(1,9)
    list_of_numbers = list1 +list2   
    label.set_text("Moves = 0")
    random.shuffle(list_of_numbers)
    
    is_exposed = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global is_exposed
    global point
    global prev_point
    global no_of_moves
    
    #begining
    if sum(is_exposed) == 0:
        is_exposed[pos [0] // step] = 1
        point = pos
    #one card exposed    
    elif(sum(is_exposed)%2 != 0) and (is_exposed[pos[0]//step] != 1):
        is_exposed[pos [0] // step] = 1
        prev_point = point
        point = pos
        no_of_moves +=1
        label.set_text("Moves = "+str(no_of_moves))
    #two cards exposed
    elif (sum(is_exposed)%2 == 0) and (is_exposed[pos[0]//step] != 1):
        #two cards match
        if list_of_numbers[point[0]//step] == list_of_numbers[prev_point[0]//step]:
            is_exposed[pos[0] // step] = 1
        #two cards do not match
        else:
            is_exposed[point[0]//step] = 0
            is_exposed[prev_point[0]//step] = 0
            is_exposed[pos[0] // step] = 1
        point = pos
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
   
    global l_on_can
    l_on_can = [0,50, 0, 100]
    loc_on_canvas = [18, 60]
    
  
    for num,exposed in zip(list_of_numbers,is_exposed):
        
        if exposed == False:
            canvas.draw_polygon([(l_on_can[0], l_on_can[2]), (l_on_can[0], l_on_can[3]), (l_on_can[1], l_on_can[3]), (l_on_can[1], l_on_can[2])], 2, "white","Green")
        else:
            canvas.draw_text(str(num),loc_on_canvas, 30, "Red")
       
        loc_on_canvas[0] += step
        l_on_can[0] += step
        l_on_can[1] += step

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()

