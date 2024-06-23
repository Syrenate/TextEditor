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

def createRope(node, par, text, l, r):
    rope = Rope()
    rope.parent = par

    size = r-l+1

    if size <= leaf_size:
        rope.str = text[l:r+1]
        rope.weight = size
        rope.is_leaf = True
    else:
        even_c = 1 - (size % 2)
        split = math.floor(size / 2)
         
        rope.left = createRope(node, rope, text, l, l+split-even_c)
        rope.right = createRope(node, rope, text, r-(split)+1,r)
        rope.weight = split
    return rope


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

class Cursor:
    def __init__(self, p): 
        self.pos = p
        self.mask = [' ']*p + ['|']
    def set(self, p): 
        if p >= 0 and p < len(display_label.get()): self.pos = p
    def get(self): return self.pos

cursor = Cursor(len(input)-1)
cursor_label = StringVar(root, 'AAAAAAA')
cursor_active = False

class EditorWindow:
    def __init__(self):
        root.title("Text Editor")

        frame = ttk.Frame(root)
        frame.grid(column=0, row=0, sticky=N+E+S+W)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        display = ttk.Label(frame, textvariable=display_label)
        #cursor_mask = ttk.Label(frame, textvariable=cursor_label)
        #for x in [display, cursor_mask]: x.grid(column=0, row=1, columnspan=2)
        display.grid(column=0, row=1, columnspan=2)

        clear_button = ttk.Button(frame, text="Clear", command=self.clear_text)
        clear_button.grid(column=0, row=0)
        quit_button = ttk.Button(frame, text="Quit", command=root.destroy)
        quit_button.grid(column=1, row=0, sticky=N)


        for child in frame.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky=N+W)
        self.set_text(StringVar.get(display_label))

    def clear_text(self):
        display_label.set([])

    def set_text(self, text):
        display_label.set(text)

    def update_text(self, text):
        lab = display_label.get()
        pos = cursor.get()
        display_label.set(lab[:pos+1] + text + lab[pos+1:])
        cursor.set(pos + 1)

    def backspace(self):
        pos = cursor.get()
        if pos >= 0:
            lab = display_label.get()
            display_label.set(lab[:pos] + lab[pos+1:])
            cursor.set(pos - 1)

    def move_cursor(self, id):
        match id:
            case 37: cursor.set(cursor.get() - 1)
            case 38: pass #cursor.set(cursor.get - 1)
            case 39: cursor.set(cursor.get() + 1)
            case 40: pass #cursor.set(cursor.get - 1)

    def update_cursor_pos(self):
        pos = cursor.get()
        lab = display_label.get()
        new_lab = lab[:pos] + underline_str(lab[pos] + " ")[:2] + lab[pos+2:]
        display_label.set(new_lab)
        #display_label.set(lab[:pos] + underline_str([lab[pos]]) + lab[pos:])


def underline_str(s):
    var = "\u0332".join(s)
    return var

var = underline_str("hello")
print(var, var[1])

window = EditorWindow()


# Event Handling
def event_handler(event, id):
    if id == "<Key>": key_handler(event)
    if id == "<Motion>": mouse_move_handler(event)

def key_handler(event):
    #print(event.char, event.keysym, event.keycode)
    if event.keycode == 8:
        window.backspace()
    elif event.keycode in [37,38,39,40]:
        window.move_cursor(event.keycode)
    else:
        window.update_text(event.char)
    window.update_cursor_pos()

def mouse_move_handler(event):
    print(event.x, event.y)

def click_handler(event, id):
    if id == "<Button-1>": pass
        

root.bind("<Key>", lambda e : event_handler(e, "<Key>"))
root.bind("<Motion>", lambda e : event_handler(e, "<Motion>"))
root.bind("<Button-1>", lambda e : click_handler(e, "<Button-1>"))


root.mainloop()