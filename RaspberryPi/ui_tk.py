#!/usr/bin/env python #If you have several versions of Python installed, /usr/bin/env will ensure the interpreter used is the first one on your environment's $PATH
"""
G-code streaming script for grbl and automatized camera
"""

# libraries import
import config as con
import functions as fun
import serial
from tkinter import *
from tkinter.ttk import *
from picamera import PiCamera
import RPi.GPIO as GPIO


# Main program:

with serial.Serial(con.ser_set["board_path"], con.ser_set["baudrate"]) as s:
    fun.homing(s, GPIO, con)
    
    window = Tk()
    window.title("Blabla")
    window.geometry("400x600+500+200")

    lbl = Label(window, text="Camera : ")
    #lbl.grid(column=0, row=0, sticky=W, padx=20)
    lbl.place(x=10, y=10)

    camera = PiCamera()
    camera.rotation = 270
    def start_preview():
        camera.start_preview(fullscreen=False, window=(1000, 200, 640, 480), hflip=True)
    def stop_preview():
       camera.stop_preview()
    
    var1 = IntVar()
    var1.set(0)
    rad1=Radiobutton(window, text="Start preview", variable=var1, value=1, command=start_preview)
    rad2=Radiobutton(window, text="Stop preview", variable=var1, value=2, command=stop_preview)
#     rad1.grid(column=0, row=1, sticky=W, padx=20)
#     rad2.grid(column=1, row=1, sticky=W)
    rad1.place(x=10, y=30)
    rad2.place(x=200, y=30)
    
    lbl2 = Label(window, text="Steps : ")
    #lbl2.grid(column=0, row=2, sticky=W, padx=20)
    lbl2.place(x=10, y=100)
    
    var2 = DoubleVar()
    var2.set(0)
    rad3=Radiobutton(window, text="0.1 mm", variable=var2, value=0.1)
    rad4=Radiobutton(window, text="1 mm", variable=var2, value=1)
    rad5=Radiobutton(window, text="10 mm", variable=var2, value=10)
#     rad3.grid(column=0, row=3, sticky=W, padx=20)
#     rad4.grid(column=1, row=3, sticky=W)
#     rad5.grid(column=2, row=3, sticky=W)
    rad3.place(x=10, y=130)
    rad4.place(x=110, y=130)
    rad5.place(x=210, y=130)
    
# 
#     lbl2 = Label(window, text="\nMotor steps, currently not set.")
#     lbl2.grid(column=0, row=2, sticky=W, padx=20)
# 
#     def comboget():
#         comboval = combo.get()
#         newtext = "\nMotor steps, set to " + comboval + " setps."
#         lbl2.configure(text=newtext)
#         print(comboval)
#         return comboval
#     
#     combo = Combobox(window)
#     combo['values']=(1,10)
#     combo.current(1)
#     combo.grid(column=0, row=3, sticky=W, padx=20)
#     print("combo['values'] : ")
#     print(combo['values'])
#     print("combo.current(1) :")
#     print(combo.current(1))
#     print("combo :")
#     print(combo)
# 
#     btn = Button(window, text="Click Me", command=comboget)
#     btn.grid(column=1, row=3, sticky=W, padx=20)


    lbl3 = Label(window, text="\nMove the camera:")
    #lbl3.grid(column=0, row=4, sticky=W, padx=20)
    lbl3.place(x=10, y=200)
    
    xpos = DoubleVar()
    xpos.set(0)
    ypos = DoubleVar()
    ypos.set(0)
    def left():
        xmove=-var2.get()
        ymove=0
        fun.simple_line(s, GPIO, xmove, ymove)
        xpos.set(round(xpos.get(),1) + round(xmove,1))
        ypos.set(round(ypos.get(),1) + round(ymove,1))
        postext = "\nCurrent position: x=" + str(round(xpos.get(),1)) + ", y=" + str(round(ypos.get(),1))
        lbl4.configure(text = postext)
    def right():
        xmove=round(var2.get(),1)
        ymove=0
        fun.simple_line(s, GPIO, xmove, ymove)
        xpos.set(round(xpos.get(),1) + round(xmove,1))
        ypos.set(round(ypos.get(),1) + round(ymove,1))
        postext = "\nCurrent position: x=" + str(round(xpos.get(),1)) + ", y=" + str(round(ypos.get(),1))
        lbl4.configure(text = postext)
    def up():
        xmove=0
        ymove=var2.get()
        fun.simple_line(s, GPIO, xmove, ymove)
        xpos.set(round(xpos.get(),1) + round(xmove,1))
        ypos.set(round(ypos.get(),1) + round(ymove,1))
        postext = "\nCurrent position: x=" + str(round(xpos.get(),1)) + ", y=" + str(round(ypos.get(),1))
        lbl4.configure(text = postext)
    def down():
        xmove=0
        ymove=-var2.get()
        fun.simple_line(s, GPIO, xmove, ymove)
        xpos.set(round(xpos.get(),1) + round(xmove,1))
        ypos.set(round(ypos.get(),1) + round(ymove,1))
        postext = "\nCurrent position: x=" + str(round(xpos.get(),1)) + ", y=" + str(round(ypos.get(),1))
        lbl4.configure(text = postext)
    
    btn = Button(window, text="Left", command=left)
    #btn.grid(column=0, row=5)
    btn.place(x=10, y=250)
    btn2 = Button(window, text="Right", command=right)
    #btn2.grid(column=0, row=6)
    btn2.place(x=100, y=250)
    btn3 = Button(window, text="Up", command=up)
    #btn3.grid(column=0, row=7)
    btn3.place(x=10, y=300)
    btn4 = Button(window, text="Down", command=down)
    #btn4.grid(column=0, row=8)
    btn4.place(x=100, y=300)
    
    lbl4 = Label(window, text="\nCurrent position: ")
    #lbl4.grid(column=0, row=9, sticky=W, padx=20)
    lbl4.place(x=10, y=450)
    
    window.mainloop()



# with serial.Serial(con.ser_set["board_path"], con.ser_set["baudrate"]) as s:
#     fun.homing(s, con)
#     xmove=30
#     ymove=50
#     fun.simple_line(s, xmove, ymove)

# well_coord = fun.well_scanning_zigzag(con, zigzag=False)
# box_coord = fun.box_scanning_zigzag(con, zigzag=False)
# fun.camera_control(
#     well_coord, box_coord, con
# )
