from tkinter import *
from tkinter import ttk

# Set up a master frame for the whole window, as well as one frame for the game board and one for the configuration section
root = Tk()
general_frame = ttk.Frame(root,width=1000,height=1000)
general_frame.grid(column=0,row=0,columnspan=20,rowspan=20)
general_frame.columnconfigure(1,weight=1)
general_frame.rowconfigure(1,weight=1)
board_frame = ttk.Frame(general_frame, borderwidth = 5,width=800,height=1000)
board_frame.grid(column=0,row=0,columnspan=20,rowspan=20)
board_frame.columnconfigure(1,weight=1)
board_frame.rowconfigure(1,weight=1)
config_frame = ttk.Frame(general_frame,borderwidth=5)
config_frame.grid(column=0,row=0,columnspan=20,rowspan=20)
config_frame.columnconfigure(1,weight=1)
config_frame.rowconfigure(1,weight=1)

# Titles
board_title = ttk.Label(board_frame,text='Puzzle Board')
board_title.grid(column=0,row=0,columnspan=13,rowspan=1)


# Set up a Canvas for the 7x7 board (will try to adjust for variable board size later if I figure out how)
board_canvas = Canvas(board_frame)
# Create a list of locations for the circles representing houses/utilities/nodes
for x in range(10,370,60):
    for y in range(10,370,60):
        board_canvas.create_oval(x,y,x+30,y+30)
        board_canvas.create_line(x+15,y+30,x+15,y+60)
        board_canvas.create_line(x+30,y+15,x+60,y+15)

board_canvas.grid(column=1,row=0,columnspan=13,rowspan=13)

root.mainloop()