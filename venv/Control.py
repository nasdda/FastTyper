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
    def __init__(self,initial_x,initial_y, width, height):
        self.kb = Controller()
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.width = width
        self.height = height
        self.time = 60
        self.queue = []

    def getCurrent(self):
        image = pyautogui.screenshot('image.png', region=(self.initial_x, self.initial_y, self.width, self.height))
        result =  pytesseract.image_to_string(PIL.Image.open('image.PNG').convert("RGB"),lang='eng')
        return " ".join(result.split("\n"))

    def start_main(self):
        time.sleep(3)
        start = time.time()
        while time.time() - start <= self.time:
            time.sleep(0.3)
            self.queue = self.getCurrent()
            for character in self.queue:
                self.kb.type(character)
                time.sleep(0.03)
            self.kb.type(' ')