#!/usr/bin/python3

from tkinter import *
root = Tk()

top = Frame(root)
bot = Frame(root)
top.pack()
bot.pack()

puzzle_db = {} # empty puzzle database (a dictionary)
puzzle_db["size"] = 4
puzzle_db["top"] = top
puzzle_db["bot"] = bot
puzzle_db["walk"] = 40
puzzle_db["debug"] = True

def create_puzzle():
    i = 1
    for r in range(puzzle_db["size"]):
        # try a new approach, use tuple as key
        for c in range(puzzle_db["size"]):
            b = Button(puzzle_db["top"], text=str(i), width=5, bg="tan",
                   command=lambda _r=r, _c=c : make_move(_r, _c))
            puzzle_db[(r,c)] = b
            b.grid(row=r, column=c)
            i += 1
    b["text"] = " "

create_puzzle()

def make_move(r, c): # you can use cget config instead of ["text"]
    s = puzzle_db["size"]
    sym = puzzle_db[(r,c)]["text"]
    if sym == " ":
        return # click on space will do nothing
    l = [(r, c-1), (r, c+1), (r-1, c), (r+1, c)]
    for nbr_r, nbr_c in l:
        if nbr_r<0 or nbr_r==s or nbr_c<0 or nbr_c==s:
            continue
        nbr_sym = puzzle_db[(nbr_r, nbr_c)]
        if puzzle_db[(nbr_r, nbr_c)].cget("text") == " ":
            puzzle_db[(nbr_r, nbr_c)].config(text=sym)
            puzzle_db[(r,c)].config(text=" ")
            return

u = puzzle_db["user choice"] = IntVar()
Spinbox(bot, from_=2, to=6, width=2,
        textvariable=u).pack(side="left")
Button(bot, text="Reset", command=lambda _parent=root :
       redraw(_parent)).pack(side="left")
Button(bot, text="Scramble", command=lambda :
       random_move()).pack(side="left")

def redraw(parent):
    if puzzle_db["user choice"].get() == puzzle_db["size"]:
        i = 1
        for r in range(puzzle_db["size"]):
            for c in range(puzzle_db["size"]):
                puzzle_db[(r,c)]["text"] = str(i)
                i += 1
        last = puzzle_db["size"]-1
        puzzle_db[(last,last)]["text"] = " "
        return
    puzzle_db["top"].destroy()
    top = Frame(parent)
    top.pack(before=puzzle_db["bot"])
    puzzle_db["top"] = top
    for r in range(puzzle_db["size"]):
        for c in range(puzzle_db["size"]):
            del puzzle_db[(r,c)]
    puzzle_db["size"] = puzzle_db["user choice"].get()
    create_puzzle()

from random import *
def random_move():
    s = puzzle_db["size"]
    steps = puzzle_db["walk"]
    for r in range(s):
        for c in range(s):
            if puzzle_db[(r,c)]["text"] == " ":
                spc_r, spc_c = r, c
    if puzzle_db["debug"]:
        print("I will make", steps, "random moves of the space tile located at",
        spc_r, spc_c)
    for i in range(steps):
        r, c = spc_r, spc_c
        direction = random() # random() return something between [0.0, 1.0)
        if direction < 0.25: # move left
            c -= 1
        elif 0.25 <= direction < 0.5: # move right
            c += 1
        elif 0.5 <= direction < 0.75: # move up
            r -= 1
        else: # move down
            r += 1
        if r < 0 or r == s or c < 0 or c == s:
            continue
        puzzle_db[(spc_r,spc_c)]["text"] = puzzle_db[(r,c)]["text"]
        puzzle_db[(r,c)]["text"] = " "
        spc_r, spc_c = r, c
        if puzzle_db["debug"]: # the following will be covered in future class
            root.update() # update gui immediately
            root.after(300) # wait 300 miliseconds

root.mainloop()
