from IHM import IHM_connexion
from tkinter import *

if __name__ == "__main__":

    root = Tk()
    root.resizable(False, False)
    IHM_connexion(root)
    root.mainloop()

#https://www.pythontutorial.net/tkinter/tkinter-window/