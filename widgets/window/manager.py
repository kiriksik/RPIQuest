import tkinter as tk
from .window import Window


class WindowManager:
    def __init__(self, root):
        self.root = root
        self.windows = []

    def create_window(self, title="Window", content=None, size=(60, 60, 260, 200), flags=0):
        win = Window(parent=self.root, title=title, content=content, size=size, flags=flags)
        self.windows.append(win)
        return win

