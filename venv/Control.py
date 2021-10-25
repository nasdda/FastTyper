import pyautogui
from pytesseract import image_to_string
import pytesseract
from PIL import Image
import PIL.Image
from pynput.keyboard import Controller, Key
import time

#specify where pytesseract is installed
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
TESSDATA_PREFIX = 'C:/Program Files (x86)/Tesseract-OCR'

class Control:
    def __init__(self,initial_x,initial_y, width, height, stop_event):
        self.kb = Controller()
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.width = width
        self.height = height
        self.stop_event = stop_event
        self.pause_per_capture = 0.3
        self.pause_per_character = 0.02
        self.time = 60
        self.queue = []

    def getCurrent(self):
        image = pyautogui.screenshot('image.png', region=(self.initial_x, self.initial_y, self.width, self.height))
        result =  pytesseract.image_to_string(PIL.Image.open('image.PNG').convert("RGB"),lang='eng')
        result = [line.strip() for line in result.split()]
        return " ".join(result)

    def start_main(self):
        time.sleep(3)
        start = time.time()
        while (not self.stop_event.is_set()) and time.time() - start <= self.time:
            time.sleep(self.pause_per_capture)
            self.queue = self.getCurrent()
            for character in self.queue:
                if self.stop_event.is_set() or time.time() - start > self.time:
                    return
                self.kb.type(character)
                time.sleep(self.pause_per_character)
            self.kb.type(' ')