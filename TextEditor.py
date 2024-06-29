input_file = open("TextEditorInput.txt", "r")
input = input_file.read()

# Rope Data Structure
import math

leaf_size = 6
class Rope:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.str = []
        self.weight = 0
        self.is_leaf = False

    def append_substring(self, s):
        output = self.str + s
        print(output)    


    def display_rope(self):
        output = ""
        if self.is_leaf:
            output += str(self.weight) + " - " + str(self.str) + "\n"
        else:
            if self.left != None: output += self.left.display_rope()
            if self.right != None: output += self.right.display_rope()
        return output
    
    def return_text(self):
        if self.is_leaf:
            return self.str
        
        output = []
        if self.left != None: output += self.left.return_text()
        if self.right != None: output += self.right.return_text()
        return output
    
def CreateRope(root, par, s):
    rope = Rope()
    rope.parent = par

    if len(s) > leaf_size:
        split = math.floor(len(s) / 2)

        rope.left = CreateRope(root, rope, s[:split])
        rope.right = CreateRope(root, rope, s[split:])
        rope.weight = split
    else:
        rope.str = s
        rope.weight = len(s)
        rope.is_leaf = True
    return rope
    

root_rope = Rope()
root_node = CreateRope(root_rope, input, input)
root_node.str = input


# Tkinter Interface 
from tkinter import *
from tkinter import ttk

root = Tk()
display_label = StringVar(root, input)
display_label_clean = StringVar(root, input)


def remove_underline(s):
    output = ""
    for x in s:
        if x != '\u0332': output += x
    return output


class Cursor:
    def __init__(self, p): 
        self.pos = p
    def set(self, p): 
        if p < 0:                          self.pos = 0
        elif p <= len(display_label_clean.get()): self.pos = p
        else:                              self.pos = len(display_label_clean.get())
    def get(self): return self.pos
cursor = Cursor(len(input)-1)

class Mouse:
    def __init__(self): self.pos = (0,0)
    def set(self, p):   self.pos = p
    def get(self):      return self.pos
mouse = Mouse()


class EditorWindow:
    def __init__(self):
        root.title("Text Editor")

        frame = ttk.Frame(root)
        frame.grid(column=0, row=0, sticky=N+E+S+W)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        display = ttk.Label(frame, textvariable=display_label)
        display.grid(column=0, row=1, columnspan=2)

        clear_button = ttk.Button(frame, text="Clear", command=clear_text)
        clear_button.grid(column=0, row=0)
        quit_button = ttk.Button(frame, text="Quit", command=root.destroy)
        quit_button.grid(column=1, row=0, sticky=N)


        for child in frame.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky=N+W)

        set_text(StringVar.get(display_label))
        update_text()

window = EditorWindow()


# Display label functions
def clear_text(): display_label_clean.set("")
def set_text(text): display_label_clean.set(text)

def insert_text(text):
    lab = display_label_clean.get()
    if len(lab) == 0:
        display_label_clean.set(text)
        cursor.set(len(text))
    else:
        pos = cursor.get()
        display_label_clean.set(lab[:pos] + text + lab[pos:])
        cursor.set(pos + len(text))

def backspace():
    pos = cursor.get()
    lab = display_label_clean.get()
    display_label_clean.set(lab[:pos-1] + lab[pos:])
    cursor.set(pos - 1)

def move_cursor(id):
    match id:
        case 37: cursor.set(cursor.get() - 1)
        case 38: pass 
        case 39: cursor.set(cursor.get() + 1)
        case 40: pass 

def update_text():
    pos = cursor.get()
    lab = display_label_clean.get()
    if len(lab) == 0:
        display_label.set("\u0332")
    else:
        display_label.set(lab[:pos] + "\u0332".join((lab + " ")[pos] + " ")[:2] + lab[pos+1:])
    print(cursor.get(), lab)


# Event Handling
def event_handler(event, id):
    if id == "<Key>": key_handler(event)
    if id == "<Motion>": mouse_move_handler(event)

def key_handler(event):
    #print(event.char, event.keysym, event.keycode)
    if event.keycode == 8:
        backspace()
    elif event.keycode in [37,38,39,40]:
        move_cursor(event.keycode)
    else:
        insert_text(event.char)
    update_text()

def mouse_move_handler(event):
    mouse.set((event.x, event.y))

def click_handler(event, id):
    if id == "<Button-1>": pass
             

root.bind("<Key>", lambda e : event_handler(e, "<Key>"))
root.bind("<Motion>", lambda e : event_handler(e, "<Motion>"))
root.bind("<Button-1>", lambda e : click_handler(e, "<Button-1>"))


root.mainloop()