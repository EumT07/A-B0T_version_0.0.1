from tkinter import *
from tkinter import ttk


root = Tk()

#opciones
root.config(bg="black")
root.title("Hengar")
# root.resizable(0,0)
root.config(width=250,height=200)

#menu
menuBar = Menu(root)
root.config(menu=menuBar)
    
#Menu options
settings_menu = Menu(menuBar, tearoff=0)

#Settings - options
settings_menu.add_cascade(label="Settings",menu=settings_menu)
#Optionces

logo = PhotoImage(file="./img/javascript.png")
image = Label(root,image=logo,width=80,height=100)
image.pack(side="top",pady=40)



root.mainloop()