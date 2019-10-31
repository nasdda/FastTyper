import tkinter as tk
from capture_box import GUI
from Control import Control
from threading import Thread
from time import sleep



class Box:
    def __init__(self):
        self.dim = None
        self.t = None
        self.root = tk.Tk()
        self.root.title("FastTyper")
        self.root.resizable(False,False)
        self.canvas = tk.Canvas(self.root,height=250,width=400)
        self.canvas.pack()
        #Frames
        self.f1 = tk.Frame(self.root, height=30, width=80)
        self.f1.pack_propagate(0) # don't shrink
        self.f1.place(x=25,y=200)

        self.f2 = tk.Frame(self.root, height=30, width=80)
        self.f2.pack_propagate(0) # don't shrink
        self.f2.place(x=300,y=200)

        self.f3 = tk.Frame(self.root,height=30, width=140)
        self.f3.pack_propagate(0)
        self.f3.place(x=130,y=200)

        self.f4 = tk.Frame(self.root, height=30, width=80)
        self.f4.pack_propagate(0)  # don't shrink
        self.f4.place(x=300, y=160)

        #Buttons
        self.capture_button = tk.Button(self.f1,text="Capture",command=self.capture_button_clicked)
        self.capture_button.pack(fill=tk.BOTH,expand=1)

        self.start_button = tk.Button(self.f2,text="Start", command=self.start_button_clicked)
        self.start_button.pack(fill=tk.BOTH,expand=1)

        self.terminate_button = tk.Button(self.f4, text="Terminate", command=self.terminate_button_clicked)
        self.terminate_button.pack(fill=tk.BOTH,expand=1)

        #Entry/Labels
        vcmd = (self.f3.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.time_entry = tk.Entry(self.f3,font=("Calibri 12"),validate = 'key', validatecommand = vcmd)
        self.time_entry.pack(fill=tk.BOTH,expand=1)

        self.hint = tk.Label(self.root,text="Duration(seconds)")
        self.hint.place(x=130,y=170)

        self.center_label = tk.Label(self.root, text="Welcome")
        self.center_label.config(font=("Courier", 15))
        self.center_label.place(rely=0.35,relx=0.5,anchor=tk.CENTER)

        self.root.mainloop()

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        #Only allow up to 8 digits
        if len(value_if_allowed) > 8:
            return False

        #ensure only numbers are entered
        if (action == '1'):
            if text in '0123456789.-+':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

    #Button actions
    def capture_button_clicked(self):
        root = GUI()
        root.mainloop()

        # extracts initial_x, initial_y, width, height
        self.dim = [root.pos[0][0], root.pos[0][1], abs(root.pos[1][0] - root.pos[0][0]), abs(root.pos[1][1] - root.pos[0][1])]
        self.center_label.config(text="Ready To Type")

    def start_button_clicked(self):
        if self.dim is not None:
            if self.t is not None and self.t.isAlive():
                self.center_label.config(text="Process already started")
                return
            time = str(self.time_entry.get().strip())
            if not time:
                self.center_label.config(text="Invalid duration:\nPlease enter number of\nseconds")
            else:
                self.control = Control(self.dim[0], self.dim[1], self.dim[2], self.dim[3])
                self.control.time = int(time)
                self.t = Thread(target=self.control.start_main)
                self.t.start()
                self.center_label.config(text="Starting in 3 Seconds")
        else:
            self.center_label.config(text="No Target")

    def terminate_button_clicked(self):
        if self.t is not None:
            if self.t.isAlive():
                self.control.time = 0
                self.center_label.config(text="Terminates when stack is \nempty")

