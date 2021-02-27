from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from main import Downloader


class Window:
    def __init__(self):
        self.root = Tk()
        self.root.title('Download images')
        self.root.geometry('300x250')
        self.root.resizable(width=False, height=False)
        self.entryPath = Entry(textvariable=StringVar(), font='Arial 14', width=20, bg='lightgray')
        self.entryUpc = Entry(textvariable=StringVar(), font='Arial 14', width=20, bg='lightgray')
        self.upc = ''
        self.SaveFunction()
        self.UpcFunction()

    def SaveFunction(self):
        self.entryPath.place(relx=.6, rely=.05, anchor="c")
        Button(self.root, text='Save to...', command=self.btnSaveClick).place(x=0, y=0)

    def UpcFunction(self):
        self.entryUpc.place(relx=.5, rely=.5, anchor="c")
        Button(self.root, text='Submit', command=self.btnUpc).place(relx=.5, rely=.85, anchor="c", height=30, width=130,
                                                                    bordermode=OUTSIDE)

    def btnSaveClick(self):
        self.entryPath = fd.askdirectory()
        Entry(textvariable=StringVar(value=f'{self.entryPath}'), font='Arial 14', width=20, bg='lightgray').place(relx=.6, rely=.05, anchor="c")

    def btnUpc(self):
        self.upc = self.entryUpc.get()
        mb.showinfo(message='Search is starting. Look in the folder')
        Downloader(self.entryPath, self.upc)


if __name__ == '__main__':
    window = Window()
    window.root.mainloop()
