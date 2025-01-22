import customtkinter as ctk
from ctypes import windll
from settings import *
import json
from loginMenu import LoginMenu
from mainMenu import MainMenu

class MusicPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()

        # setup
        windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')
        self.iconbitmap("Images/appLogo.ico")
        self.title("Music Player")
        ctk.set_appearance_mode("dark")
        self.geometry(str(APP_SIZE[0]) + "x" + str(APP_SIZE[1]))
        self.resizable(False, False)

        self.chooseScreen()

        self.mainloop()

    def chooseScreen(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except:
            data = []

        if data == []:
            login = LoginMenu(self)
        else:
            mainMenu = MainMenu(self)

if __name__ == "__main__":
    MusicPlayer()