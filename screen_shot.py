# -*- coding:utf-8 -*-
from mttkinter import mtTkinter as tk
import os
from PIL import ImageGrab
from time import sleep
#from tk import StringVar, IntVar

class ScreenCapture:

    def __init__(self):
        pass
    def start(self):
        self.root = tk.Tk()
        self.root.geometry('0x0+0+0')
        self.root.resizable(False, False)
        self.X = tk.IntVar(value=0)
        self.Y = tk.IntVar(value=0)

        self.selectPosition=None
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        self.top = tk.Toplevel(self.root, width=screenWidth, height=screenHeight)
        self.top.overrideredirect(True)
        self.canvas = tk.Canvas(self.top,bg='white', width=screenWidth, height=screenHeight)
        self.p_w_picpath = tk.PhotoImage(file=self.filename)
        self.canvas.create_image(screenWidth//2, screenHeight//2, image=self.p_w_picpath)

        def onOtherButtonDown(event):
            return
        self.canvas.bind('<Button-2>', onOtherButtonDown)
        self.canvas.bind('<Button-3>', onOtherButtonDown)
        self.canvas.bind('<Button-4>', onOtherButtonDown)
        self.canvas.bind('<Button-5>', onOtherButtonDown)

        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            #开始截图
            self.sel = True
        self.canvas.bind('<Button-1>', onLeftButtonDown)

        def onLeftButtonMove(event):
            if not self.sel:
                return
            global lastDraw
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='red',width=2)
        self.canvas.bind('<B1-Motion>', onLeftButtonMove)

        def onLeftButtonUp(event):
            self.sel = False
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            #sleep(0.1)
            myleft, myright = sorted([self.X.get(), event.x])
            mytop, mybottom = sorted([self.Y.get(), event.y])
            self.selectPosition=(myleft,myright,mytop,mybottom)
            pic = ImageGrab.grab((myleft+1, mytop+1, myright, mybottom))
            self.destroy()
            if self.callback:
                self.callback(pic)

        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

    def destroy(self):
        self.top.destroy()
        self.root.destroy()

    def are_capture(self,callback):
        self.callback = callback
        self.filename = 'temp.png'
        im = ImageGrab.grab()
        im.save(self.filename)
        im.close()
        self.start()
        self.root.state('icon')
        os.remove(self.filename)
        self.root.mainloop()


# def are_capture(callback):AAaa
#     filename = 'temp.png'
#     im = ImageGrab.grab()
#     im.save(filename)
#     im.close()
#     capture = MyCapture(filename)
#     capture.callback = callback
#     capture.root.state('icon')
#     sleep(0.2)
#     os.remove(filename)
#     capture.root.mainloop()
