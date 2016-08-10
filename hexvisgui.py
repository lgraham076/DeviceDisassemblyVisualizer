#-------------------------------------------------------------------------------
# Name:        hexvisgui.py
# Purpose:     GUI used to display converted binary information
#
# Author:      Langston Graham			Macaulay Brown
#
# Created:     08/27/2013
#-------------------------------------------------------------------------------

import threading
import time
import binvis

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
from PIL import ImageTk, Image
from hexreader import *

SPLATTERWIDTH=512
SPLATTERHEIGHT=512

class gui(Frame):
    #Override Frame initialization
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent=parent
        self.hexlines=[]
        self.hexlineindex=0
        self.hexaddressoffset=400
        self.graphimages={}
        self.initialize()

    #Pass curve type to open
    def classwindow(self):
        self.createcurve("class")
    def hilbertwindow(self):
        self.createcurve("hilbert")
    def entropywindow(self):
        self.createcurve("entropy")
    def gradientwindow(self):
        self.createcurve("gradient")

    #Open curve type's window
    def createcurve(self,curvetype):
        try:
            args = []
            args.append(self.fileloc)
            graphloc=binvis.main(args,curvetype)
            self.graphimages[curvetype]=ImageTk.PhotoImage(Image.open(graphloc))

            win=Toplevel()
            curvecanvas=Canvas(win,height=512,width=128)
            curvecanvas.configure(background="black")
            curvecanvas.pack()

            curvecanvas.create_image(0,0,image=self.graphimages[curvetype])
        except AttributeError:
                print("No file selected!")

    #Opens requested file and updates display
    def openfile(self):
        self.fileloc=askopenfilename()
        self.hexlineindex=0
        self.hexvalues = readFile(self.fileloc)
        self.hexlines = formathexvalues(self.hexvalues)
        self.playslider.configure(from_=0,to=len(self.hexlines))
        self.playslider.set(0)

    #Called on slider used to determine location in hex address
    def playslider_moved(self,*args):
        sliderloc=int(self.playslider.get())
        slideroffset=sliderloc+self.hexaddressoffset
        self.updatehexbox(sliderloc,slideroffset)
        self.updateplotcanvas(sliderloc,slideroffset)
        hexaddress=gethexaddress(sliderloc)
        self.currhexaddress.configure(text=str(hexaddress)+"-"+gethexaddress(slideroffset))

    #Called on slider used to determine size of the hex window
    def windowslider_moved(self,*args):
        sliderloc=int(self.windowslider.get())
        self.hexaddressoffset=sliderloc
        self.curroffset.configure(text=str(sliderloc))

    #Update listbox of hex values
    def updatehexbox(self,begin,end):
        self.hexbox.delete(0,END)
        #Check values are in the correct order and not out of range
        if(begin > end):
            tmp=begin
            begin=end
            end=tmp
        if(begin < 0):
            begin=0
        if(end >= len(self.hexlines)):
            end=len(self.hexlines)-1
        #Insert the hex lines that match the given values into the listbox
        for i in range(begin,end):
            self.hexbox.insert(END,self.hexlines[i])

        return begin,end

    #Update canvas with new points within window
    def updateplotcanvas(self,begin,end):
        self.plotcanvas.delete(ALL)
        #Check values are in the correct order and not out of range
        if(begin > end):
            tmp=begin
            begin=end
            end=tmp
        if(begin < 0):
            begin=0
        if(end >= len(self.hexlines)):
            end=len(self.hexlines)-1
        #Parse the given hex lines
        hexes=[]
        for i in range(begin,end):
            line=self.hexlines[i]
            tmp=line.split(' | ')
            hexes+=tmp[1].split(' ')
        #Convert to 2d coordinates
        coords=hexcoordinates2d(hexes)
        for coord in coords:
            self.plotcanvas.create_line(coord[0],coord[1],coord[0]+1,coord[1]+1,width=1,fill="blue")

    #Hexvisgui initialization
    def initialize(self):
        #Create the menubar
        self.menubar=Menu(self)
        menu=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="File",menu=menu)
        menu.add_command(label="Open",command=self.openfile)
        #menu.add_command(label="Exit")
        menu=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Tools",menu=menu)
        menu.add_command(label="Class",command=self.classwindow)
        menu.add_command(label="Hilbert",command=self.hilbertwindow)
        menu.add_command(label="Entropy",command=self.entropywindow)
        menu.add_command(label="Gradient",command=self.gradientwindow)
        self.master.config(menu=self.menubar)

        #Configure grid layout
        self.columnconfigure(0,pad=5)
        self.columnconfigure(1,pad=5)
        self.columnconfigure(2,pad=5)
        self.rowconfigure(0,pad=5)
        self.rowconfigure(0,pad=5)

        #Add canvas to plot points from converted hex values
        self.plotcanvas=Canvas(self,width=256,height=256)
        self.plotcanvas.configure(background='black')
        self.plotcanvas.grid(row=0,column=0)

        #Add listbox to hold the current group of hexvalues
        listframe=Frame(self)
        hexscroll=Scrollbar(listframe,orient=VERTICAL)
        hexbox_font = Font(size=8)
        hexbox_font.config(family={"posix": "Monospace","nt": "Courier New"})
        self.hexbox=Listbox(listframe,width=75,height=20,font=hexbox_font,yscrollcommand=hexscroll.set,selectmode=EXTENDED)
        hexscroll.config(command=self.hexbox.yview)
        hexscroll.pack(side=RIGHT,fill=Y)
        self.hexbox.pack(side=LEFT)
        listframe.grid(row=0,column=1)

        #Add slider for location in hex lines and size of window of hex values
        commandframe=Frame(self)
        playframe=Frame(commandframe)
        windowframe=Frame(commandframe)
        self.playslider=Scale(playframe,command=self.playslider_moved)
        self.playslider.configure(from_=0,to=100)
        self.playslider.configure(orient=HORIZONTAL)
        self.playslider.pack(side=BOTTOM)
        hexaddress=gethexaddress(int(self.playslider.get()))
        self.currhexaddress=Label(playframe,width=20,text=hexaddress)
        self.currhexaddress.pack(side=TOP)
        self.curroffset=Label(windowframe,text=self.hexaddressoffset)
        self.curroffset.pack(side=TOP)
        self.windowslider=Scale(windowframe,command=self.windowslider_moved)
        self.windowslider.configure(from_=100,to=600,orient=HORIZONTAL)
        self.windowslider.pack(side=TOP)
        self.windowslider.set(self.hexaddressoffset)
        playframe.pack(side=LEFT)
        windowframe.pack(side=RIGHT)
        commandframe.grid(row=1,columnspan=2)

        self.pack()