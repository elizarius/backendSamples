from Tkinter import *

class Application(Frame):
    def printEntry(self):
        inputstring = self.entryfield.get()
        print inputstring
        
    def createWidgets(self):
        self.entryfield = Entry(self)
              
        self.entryfield.pack({"side": "top"})

        self.quitbutton = Button(self, text="Quit", fg="red", bg="white")
        self.quitbutton["command"] =  self.quit

        self.quitbutton.pack({"side": "right"})

        self.printbutton = Button(self, text="Print out", fg="white", bg="black")
        self.printbutton["command"] = self.printEntry

        self.printbutton.pack({"side": "left"})

             

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
