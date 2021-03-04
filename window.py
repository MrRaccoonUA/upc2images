from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from main import Downloader


class Window:
    def __init__(self):
        self.root = Tk()
        self.root.title('Download images')
        self.root.geometry('300x400')
        self.root.resizable(width=False, height=False)
        self.entryPath = Entry(textvariable=StringVar(), font='Arial 14', width=20, bg='lightgray')
        self.entryCoolDown = Entry(textvariable=StringVar(), font='Arial 14', width=5, bg='lightgray')
        self.labelCoolDown = Label(self.root, text='Enter user key', font='Arial 12')
        self.entryUpc = Entry(textvariable=StringVar(), font='Arial 14', width=20, bg='lightgray')
        self.entryKey = Entry(textvariable=StringVar(), font='Arial 14', width=20, bg='lightgray')
        self.entryWidth = Entry(textvariable=StringVar(value=600), font='Arial 14', width=5, bg='lightgray')
        self.entryHeight = Entry(textvariable=StringVar(value=600), font='Arial 14', width=5, bg='lightgray')
        self.choice = StringVar(value=0)
        self.upc = ''
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'user_key': 'only_for_dev_or_pro',
            'key_type': '3scale'
        }
        self.UpcFunction()
        self.SaveFunction()
        self.radiobutton()

    def SaveFunction(self):
        Button(self.root, text='Save to...', command=self.btnSaveClick).place(x=0, y=0)

    def radiobutton(self):
        Radiobutton(self.root, variable=self.choice, text='Dev/Pro', font='Arial 14', value=1,
                    command=self.dev_pro).place(relx=.6, rely=.12)
        Radiobutton(self.root, variable=self.choice, text='Trial', font='Arial 14', value=0, command=self.clear).place(
            relx=.15, rely=.12)

    def UpcFunction(self):
        self.entryWidth.place(relx=.25, rely=.48, anchor="c")
        Label(self.root, text='Width', font='Arial 12').place(relx=.17, rely=.38)
        self.entryHeight.place(relx=.79, rely=.48, anchor="c")
        Label(self.root, text='Height', font='Arial 12').place(relx=.704, rely=.38)
        Label(self.root, text='Enter UPC', font='Arial 12').place(relx=.38, rely=.55)
        self.entryUpc.place(relx=.52, rely=.65, anchor="c")
        Button(self.root, text='Submit', command=self.btnSubmit).place(relx=.5, rely=.9, anchor="c", height=30,
                                                                       width=130)

    def clear(self):
        self.entryKey.delete(0, 'end')
        self.labelCoolDown.pack(padx=500)
        self.entryKey.pack(padx=500)

    def dev_pro(self):
        self.labelCoolDown.place(relx=.34, rely=.23)
        self.entryKey.place(relx=.15, rely=.3)

    def btnSaveClick(self):
        self.entryPath = fd.askdirectory()
        Entry(textvariable=StringVar(value=self.entryPath), font='Arial 14', width=20, bg='lightgray').place(
            relx=.6, rely=.036, anchor="c")

    def btnSubmit(self):
        if self.entryKey.get():
            self.headers['user_key'] = self.entryKey.get()
        if self.entryUpc.get() and self.entryWidth.get() and self.entryHeight.get():
            mb.showinfo(message='Search is starting. Look in the folder')
            Downloader(self.entryPath, self.entryUpc.get(), self.entryWidth.get(), self.entryHeight.get(), self.root, self.headers)
        else:
            mb.showerror(message='Select path or enter UPC')


if __name__ == '__main__':
    window = Window()
    window.root.mainloop()
