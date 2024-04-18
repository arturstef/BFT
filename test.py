from tkinter import *

root = Tk()

obraz = PhotoImage(file="img/node.png").subsample(x=25, y=25)

etykieta = Label(root, image=obraz)
etykieta.place(x= 150, y= 150)
etykieta.pack()

root.mainloop()