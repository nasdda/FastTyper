import tkinter as tk
from PIL import ImageTk,ImageGrab
import pyautogui

class GUI(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.pos = []
        self.withdraw()
        self.attributes('-fullscreen', True)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both",expand=True)

        image = pyautogui.screenshot()
        self.image = ImageTk.PhotoImage(image)
        self.photo = self.canvas.create_image(0,0,image=self.image,anchor="nw")

        self.x, self.y = 0, 0
        self.rect, self.start_x, self.start_y = None, None, None
        self.deiconify()

        self.canvas.tag_bind(self.photo,"<ButtonPress-1>", self.on_button_press)
        self.canvas.tag_bind(self.photo,"<B1-Motion>", self.on_move_press)
        self.canvas.tag_bind(self.photo,"<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.pos.append((event.x,event.y))
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        x,y = pyautogui.position()
        self.pos.append((x,y))
        self.pos = sorted(self.pos,key=lambda x:x[0])
        self.destroy()
        self.quit()



