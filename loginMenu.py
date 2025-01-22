import customtkinter as ctk
from PIL import Image
from settings import *
import json
from mainMenu import MainMenu

class LoginMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.pack(fill = "both", expand = True)

        src = Image.open("Images/appLogo.png")
        img = ctk.CTkImage(src, None, (500, 500))
        self.appLogo = ctk.CTkLabel(self, text = "", image = img)
        self.appLogo.place(relx = 0.2, rely = 0.4, anchor = "center")

        self.appName = ctk.CTkLabel(self, text = "Music Player", font = (APP_FONT_BOLD, 50))
        self.appName.place(relx = 0.2, rely = 0.75, anchor = "center")

        canvas = ctk.CTkCanvas(self, width = 5, height = 650, bg = DARK_GREY, bd = 0, highlightthickness = 0)
        canvas.place(relx = 0.4, rely = 0.5, anchor = "center")

        ctk.CTkLabel(self, text = "Enter details:", font = (APP_FONT_BOLD, 30)).place(relx = 0.42, rely = 0.08, anchor = "nw")

        self.entryBorderColour = "#4e5c59"
        fgColour = "#939b9c"
        entryOffset = 0.15

        self.userNameEntry = ctk.CTkEntry(self, width = 425, height = 50, corner_radius = 15, border_width = 3, border_color = self.entryBorderColour, fg_color = fgColour, text_color = self.entryBorderColour, placeholder_text_color = self.entryBorderColour, placeholder_text = "Username:")
        self.userNameEntry.place(relx = 0.63, rely = 0.2, anchor = "center")

        self.favArtistEntry = ctk.CTkEntry(self, width = 425, height = 50, corner_radius = 15, border_width = 3, border_color = self.entryBorderColour, fg_color = fgColour, text_color = self.entryBorderColour, placeholder_text_color = self.entryBorderColour, placeholder_text = "Favourite Artist:")
        self.favArtistEntry.place(relx = 0.63, rely = 0.2 + entryOffset, anchor = "center")

        self.favAlbumEntry = ctk.CTkEntry(self, width = 425, height = 50, corner_radius = 15, border_width = 3, border_color = self.entryBorderColour, fg_color = fgColour, text_color = self.entryBorderColour, placeholder_text_color = self.entryBorderColour, placeholder_text = "Favourite Album:")
        self.favAlbumEntry.place(relx = 0.63, rely = 0.2 + entryOffset * 2, anchor = "center")

        self.favSongEntry = ctk.CTkEntry(self, width = 425, height = 50, corner_radius = 15, border_width = 3, border_color = self.entryBorderColour, fg_color = fgColour, text_color = self.entryBorderColour, placeholder_text_color = self.entryBorderColour, placeholder_text = "Favourite Song:")
        self.favSongEntry.place(relx = 0.63, rely = 0.2 + entryOffset * 3, anchor = "center")

        self.favGenreEntry = ctk.CTkEntry(self, width = 425, height = 50, corner_radius = 15, border_width = 3, border_color = self.entryBorderColour, fg_color = fgColour, text_color = self.entryBorderColour, placeholder_text_color = self.entryBorderColour, placeholder_text = "Favourite Genre:")
        self.favGenreEntry.place(relx = 0.63, rely = 0.2 + entryOffset * 4, anchor = "center")

        self.loginButton = ctk.CTkButton(self, text = "Create Account", width = 100, height = 50, corner_radius = 10, fg_color = self.entryBorderColour, font = (APP_FONT_BOLD, 20), command = lambda: self.createAccount())
        self.loginButton.place(relx = 0.63, rely = 0.92, anchor = "center")

        self.entries = [self.userNameEntry, self.favArtistEntry, self.favAlbumEntry, self.favSongEntry, self.favGenreEntry]

    def createAccount(self):
        return_ = False
        for entry in self.entries:
            if entry.get() == "" or len(entry.get()) > 25:
                entry.configure(border_color = "#bd0e09")
                return_ = True
            
            else:
                entry.configure(border_color = self.entryBorderColour)

        if return_:
            return
        
        entry =  {
            "username": self.userNameEntry.get(),
            "favouriteArtist": self.favArtistEntry.get(),
            "favouriteAlbum": self.favAlbumEntry.get(),
            "favouriteSong": self.favSongEntry.get(),
            "favouriteGenre": self.favGenreEntry.get()
        }

        with open("data.json", "w") as file:
            json.dump(entry, file)

        playlistEntry1 = {
            "name": "All songs",
            "id": 0,
            "songs": []
        }

        playlistEntry2 = {
            "name": "Liked songs",
            "id": 1,
            "songs": []
        }

        try:
            with open('playlists.json', 'r') as file:
                data = json.load(file)
        except:
            data = []

        data.append(playlistEntry1)
        data.append(playlistEntry2)

        with open("playlists.json", "w") as file:
            json.dump(data, file)

        self.pack_forget()
        menu = MainMenu(self.parent)  