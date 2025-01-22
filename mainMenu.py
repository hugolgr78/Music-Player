import customtkinter as ctk
from PIL import Image
from settings import *
import json, os, shutil, copy, pygame, threading, random
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
from mutagen.mp3 import MP3

class MainMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill = "both", expand = True)

        self.userData = UserData(self)
        self.playlistData = PlaylistData(self, parent)
        self.musicData = MusicData(self)

class UserData(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, width = 300, height = 590, fg_color = GREY_BACKGROUND, border_color = DARK_GREY, corner_radius = 5, border_width = 3)
        self.place(x = 5, y = 5, anchor = "nw")

        self.userFrameData()

        ctk.CTkLabel(self, text = "Playlists", font = (APP_FONT_BOLD, 18)).place(x = 150, y = 130, anchor = "center")
        self.newPlaylistButton = ctk.CTkButton(self, text = "+", font = (APP_FONT, 12), height = 10, width = 20, fg_color = GREY, hover_color = GREY, corner_radius = 5, command = self.newPlaylist)
        self.newPlaylistButton.place(x = 280, y = 130, anchor = "center")
        self.playlistUserData()

        self.importButton = ctk.CTkButton(self, text = "Import Music", font = (APP_FONT_BOLD, 18), width = 280, height = 50, fg_color = APP_BACKGROUND, hover_color = PURPLE_HOVER, corner_radius = 35, command = self.importSongs)
        self.importButton.place(x = 150, y = 550, anchor = "center")

    def userFrameData(self):
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except:
            data = []

        self.userData = ctk.CTkFrame(self, width = 280, height = 95, fg_color = APP_BACKGROUND, corner_radius = 5)
        self.userData.place(x = 150, y = 55, anchor = "center")

        src = Image.open("Images/defaultPfp.png")
        img = ctk.CTkImage(src, None, (60, 60))
        self.userPfp = ctk.CTkLabel(self.userData, text = "", image = img)
        self.userPfp.place(x = 45, y = 50, anchor = "center")

        self.userName = ctk.CTkLabel(self.userData, text = data["username"], font = (APP_FONT_BOLD, 18))
        self.userName.place(x = 90, y = 25, anchor = "nw")

        self.currSongLabel = ctk.CTkLabel(self.userData, text = "Currently Playing:", font = (APP_FONT, 12))
        self.currSongLabel.place(x = 90, y = 48, anchor = "nw")

        for widget in self.userData.winfo_children():
            widget.bind("<Enter> <Button-1>", lambda event: print("User settings"))
        
        self.userData.bind("<Enter> <Button-1>", lambda event: print("User settings"))

    def playlistUserData(self):
        try:
            with open("playlists.json", "r") as file:
                playlists = json.load(file)
        except:
            playlists = []

        self.playlistNames = ctk.CTkScrollableFrame(self, width = 260, height = 360, fg_color = DARK_GREY, corner_radius = 5)
        self.playlistNames.place(x = 150, y = 330, anchor = "center")

        for playlist in playlists:
            if playlist["id"] == 0 or playlist["id"] == 1:
                self.addPlaylist(playlist["name"], playlist["id"], edit = False, imported = True)
            else:
                self.addPlaylist(playlist["name"], playlist["id"], imported = True)

    def importSongs(self):

        def getSongs():
            songs = filedialog.askopenfilenames(initialdir = "Music", title = "Select songs", filetypes = (("mp3 files", "*.mp3"), ("all files", "*.*")))
            
            if songs:
                for song in songs:
                    songFrame = ctk.CTkFrame(songsAddedFrame, width = 500, height = 40, fg_color = GREY_BACKGROUND)

                    songName = song.split("/")[-1]
                    text = checkName(songName)

                    songEntry = {
                        "filePath": song,
                        "name": songName,
                        "playlists": ["All songs"]
                    }
                    songsAdded.append(songEntry)

                    ctk.CTkLabel(songFrame, text = "Name:", font = (APP_FONT, 15)).place(x = 10, y = 0, anchor = "nw")
                    ctk.CTkLabel(songFrame, text = text, font = (APP_FONT, 15)).place(x = 60, y = 0, anchor = "nw")

                    src = Image.open("Images/add.png")
                    img = ctk.CTkImage(src, None, (15, 15))
                    ctk.CTkButton(songFrame, text = "", image = img, width = 10, height = 20, fg_color = DARK_GREY, corner_radius = 10, hover_color = DARK_GREY, command = lambda song = song: addToPlaylist(song)).place(x = 415, y = 0, anchor = "nw")

                    src = Image.open("Images/delete.png")
                    img = ctk.CTkImage(src, None, (15, 15))
                    ctk.CTkButton(songFrame, text = "", image = img, width = 10, height = 20, fg_color = DARK_GREY, corner_radius = 10, hover_color = DARK_GREY, command = lambda frame = songFrame, song = song: deleteSong(frame, song)).place(x = 460, y = 0, anchor = "nw")

                    songFrame.pack()

            if len(songsAdded) > 0:
                doneButton.configure(state = "normal")

        def checkName(str):
            if len(str) > 45:
                return str[:45] + "..."
        
            else:
                return str

        def deleteSong(frame, song):

            for songEntry in songsAdded:
                if songEntry["filePath"] == song:
                    songsAdded.remove(songEntry)

            frame.destroy()

            if len(songsAdded) == 0:
                doneButton.configure(state = "disabled")

        def addToPlaylist(song):

            doneButton.configure(state = "disabled")
            undoButton.configure(state = "disabled")

            playlistFrame = ctk.CTkFrame(importFrame, width = 550, height = 310, fg_color = DARK_GREY)
            playlistFrame.place(relx = 0.5, rely = 0.5, anchor = "center")

            backButton = ctk.CTkButton(playlistFrame, text = "Done", font = (APP_FONT, 15), width = 50, height = 20, fg_color = APP_BACKGROUND, corner_radius = 30, hover_color = PURPLE_HOVER, command = lambda: finishAdd(playlistFrame))
            backButton.place(relx = 0.1, rely = 0.1, anchor = "center")

            ctk.CTkLabel(playlistFrame, text = "Select playlists", font = (APP_FONT_BOLD, 25)).place(relx = 0.5, rely = 0.15, anchor = "center")

            scrollFrame = ctk.CTkScrollableFrame(playlistFrame, width = 500, height = 150, fg_color = GREY_BACKGROUND)
            scrollFrame.place(relx = 0.5, rely = 0.6, anchor = "center")

            try:
                with open("playlists.json", "r") as file:
                    data = json.load(file)
            except:
                data = []

            for playlist in data:
                if playlist["id"] != 0 and playlist["id"] != 1:
                    frame = ctk.CTkFrame(scrollFrame, width = 500, height = 40, fg_color = GREY_BACKGROUND)
                    frame.pack()

                    ctk.CTkLabel(frame, text = playlist["name"], font = (APP_FONT, 15)).place(x = 10, y = 0, anchor = "nw")

                    for songEntry in songsAdded:
                        if songEntry["filePath"] == song:
                            isChecked = ctk.BooleanVar(value=playlist["name"] in songEntry["playlists"])
                            checkbox = ctk.CTkCheckBox(frame, text = "", width = 20, height = 20, fg_color = GREY_BACKGROUND, corner_radius = 5, border_color = DARK_GREY, border_width = 2, variable = isChecked, command = lambda name = playlist["name"]: checkPlaylist(name, song))
                            checkbox.place(x = 460, y = 0, anchor = "nw")

        def finishAdd(frame):
            frame.destroy()
            doneButton.configure(state = "normal")
            undoButton.configure(state = "normal")

        def checkPlaylist(name, song):
            for songEntry in songsAdded:
                if songEntry["filePath"] == song:
                    if name in songEntry["playlists"]:
                        songEntry["playlists"].remove(name)
                    else:
                        songEntry["playlists"].append(name)

        def getRunTime(filePath):
            audio = MP3(filePath)
            length = audio.info.length

            minutes = int(length // 60)
            seconds = int(length % 60)

            if seconds < 10:
                seconds = "0" + str(seconds)

            return str(minutes) + ":" + str(seconds)

        def addSongs():
            try:
                with open("playlists.json", "r") as file:
                    data = json.load(file)
            except:
                data = []

            for songEntry in songsAdded:
                name = os.path.splitext(songEntry["name"])[0]
                destinationPath = os.path.join("SavedSongs/", name + "_0.mp3")

                id_ = 0
                while os.path.exists(destinationPath):
                    id_ += 1
                    destinationPath = os.path.join("SavedSongs/", name + "_" + str(id_) + ".mp3")

                shutil.copy(songEntry["filePath"], destinationPath)

                newSong = {
                    "name": name,
                    "runTime": getRunTime(songEntry["filePath"]),
                    "favourited": False,
                    "folderID": id_
                }

                for playlist in data:
                    if playlist["name"] in songEntry["playlists"]:
                        playlist["songs"].append(newSong)

            with open("playlists.json", "w") as file:
                json.dump(data, file)

            importFrame.destroy()

        importFrame = ctk.CTkFrame(self.parent, width = 1000, height = 600, fg_color = GREY_BACKGROUND)
        importFrame.place(x = 0, y = 0, anchor = "nw")

        importButton = ctk.CTkButton(importFrame, text = "Import songs", font = (APP_FONT_BOLD, 25), width = 300, height = 60, fg_color = APP_BACKGROUND, corner_radius = 30, hover_color = PURPLE_HOVER, command = getSongs)
        importButton.place(relx = 0.5, rely = 0.3, anchor = "center")

        songsAdded = []

        songsAddedFrame = ctk.CTkScrollableFrame(importFrame, width = 500, height = 200, fg_color = GREY_BACKGROUND, border_color = DARK_GREY, corner_radius = 5, border_width = 3)
        songsAddedFrame.place(relx = 0.495, rely = 0.57, anchor = "center")

        doneButton = ctk.CTkButton(importFrame, text = "Done", font = (APP_FONT, 22), width = 200, height = 40, state = "disabled", fg_color = APP_BACKGROUND, corner_radius = 30, hover_color = PURPLE_HOVER, command = addSongs)
        doneButton.place(relx = 0.893, rely = 0.95, anchor = "center")

        undoButton = ctk.CTkButton(importFrame, text = "Undo", font = (APP_FONT, 22), width = 200, height = 40, fg_color = APP_BACKGROUND, corner_radius = 30, hover_color = PURPLE_HOVER, command = importFrame.destroy)
        undoButton.place(relx = 0.68, rely = 0.95, anchor = "center")

    def addPlaylist(self, name, id_, frame = None, edit = True, imported = False):

        if frame is not None:
            frame.destroy()

        frame = ctk.CTkFrame(self.playlistNames, width = 260, height = 40, fg_color = DARK_GREY)
        frame.grid_columnconfigure((0, 2), weight = 1)
        frame.grid_columnconfigure(1, weight = 2)
        frame.grid_propagate(False)

        if not imported:
            try:
                with open("playlists.json", "r") as file:
                    data = json.load(file)
            except:
                data = []
        
            highestID = 0
            for playlist in data:
                if playlist["id"] > highestID:
                    highestID = playlist["id"]
            
            id_ = highestID + 1

        ctk.CTkLabel(frame, text = "-", font = (APP_FONT_BOLD, 14)).grid(row = 0, column = 0)    
        nameButton = ctk.CTkButton(frame, text = name, anchor = "w", font = (APP_FONT_BOLD, 14), width = 200, height = 30, fg_color = GREY, hover_color = GREY, command = lambda plid = id_: self.parent.playlistData.openPlaylist(plid))
        nameButton.grid(row = 0, column = 1, sticky = "w", padx = 5)

        frame.id = id_

        if edit:
            src = Image.open("Images/pencil.png")
            img = ctk.CTkImage(src, None, (15, 15))
            options = ctk.CTkButton(frame, text = "", image = img, width = 10, height = 10, fg_color = DARK_GREY, hover_color = DARK_GREY, command = lambda plid = id_, frame = frame, name = name: self.editPlaylist(id_, frame, name))
            options.grid(row = 0, column = 2)
        else:
            filler = ctk.CTkLabel(frame, text = "farts", width = 10, height = 10, text_color = DARK_GREY)
            filler.grid(row = 0, column = 2)

        frame.pack()

        if not imported:
            newEntry = {
                "name": name,
                "id": id_,
                "songs": []
            }

            data.append(newEntry)

            with open("playlists.json", "w") as file:
                json.dump(data, file)

    def editPlaylist(self, id_, frame, name):

        def finish(name, id_, frame):
            if name == "" or len(name) > 25:
                return
            
            for i, widget in enumerate(frame.winfo_children()):
                if i == 1:
                    widget.destroy()
                    nameButton = ctk.CTkButton(frame, text = "", width = 200, height = 30, fg_color = GREY, hover_color = GREY, command = lambda plid = id_: self.openPlaylist(plid))
                    nameButton.grid(row = 0, column = 1, sticky = "w", padx = 5)

                    label = ctk.CTkLabel(nameButton, text = name, font = (APP_FONT_BOLD, 14), height = 10, anchor = "w")
                    label.place(relx = 0.02, rely = 0.5, anchor = "w")
                
                if i == 2:
                    widget.destroy()
                    src = Image.open("Images/pencil.png")
                    img = ctk.CTkImage(src, None, (15, 15))
                    options = ctk.CTkButton(frame, text = "", image = img, width = 10, height = 10, fg_color = DARK_GREY, hover_color = DARK_GREY, command = lambda plid = id_, frame = frame, name = name: self.editPlaylist(id_, frame, name))
                    options.grid(row = 0, column = 2)
            
            try:
                with open("playlists.json", "r") as file:
                    data = json.load(file)
            except:
                data = []

            data[id_]["name"] = name

            with open("playlists.json", "w") as file:
                json.dump(data, file)

        for i, widget in enumerate(frame.winfo_children()):
            if i == 1:
                widget.destroy()
                nameEntry = ctk.CTkEntry(frame, width = 200, height = 30, corner_radius = 10, border_width = 3, border_color = GREY, fg_color = "#939b9c", text_color = GREY, placeholder_text_color = GREY)
                nameEntry.insert(0, name)
                nameEntry.grid(row = 0, column = 1, sticky = "w", padx = 5)
            
            if i == 2:
                widget.destroy()
                src = Image.open("Images/tick.png")
                img = ctk.CTkImage(src, None, (16, 16))
                tickButton = ctk.CTkButton(frame, text = "", image = img, width = 10, height = 10, fg_color = DARK_GREY, hover_color = DARK_GREY, command = lambda: finish(nameEntry.get(), id_, frame))
                tickButton.grid(row = 0, column = 2)

    def newPlaylist(self):

        def checkName(name, id_, frame):
            if name == "" or len(name) > 25:
                return

            self.newPlaylistButton.configure(state = "normal")
            self.addPlaylist(name, id_, frame)

        self.newPlaylistButton.configure(state = "disabled")
        frame = ctk.CTkFrame(self.playlistNames, width = 260, height = 40, fg_color = DARK_GREY)
        frame.grid_columnconfigure((0, 2), weight = 1)
        frame.grid_columnconfigure(1, weight = 2)
        frame.grid_propagate(False)

        ctk.CTkLabel(frame, text = "-", font = (APP_FONT_BOLD, 14)).grid(row = 0, column = 0)    
        nameEntry = ctk.CTkEntry(frame, width = 200, height = 30, corner_radius = 10, border_width = 3, border_color = GREY, fg_color = "#939b9c", text_color = GREY, placeholder_text_color = GREY)
        nameEntry.grid(row = 0, column = 1, sticky = "w", padx = 5)

        src = Image.open("Images/tick.png")
        img = ctk.CTkImage(src, None, (16, 16))
        tickButton = ctk.CTkButton(frame, text = "", image = img, width = 10, height = 10, fg_color = DARK_GREY, hover_color = DARK_GREY, command = lambda: checkName(nameEntry.get(), 0, frame))
        tickButton.grid(row = 0, column = 2)

        frame.pack()

class PlaylistData(ctk.CTkFrame):
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.afterID = None

        super().__init__(parent, width = 685, height = 470, fg_color = GREY_BACKGROUND, border_color = DARK_GREY, corner_radius = 5, border_width = 3)
        self.place(x = 310, y = 5, anchor = "nw")

        ctk.CTkLabel(self, text = "Open a playlist to\n start listening", font = (APP_FONT_BOLD, 35)).place(relx = 0.5, rely = 0.5, anchor = "center")

    def openPlaylist(self, plid):

        def chooseLogo():
            file = filedialog.askopenfilename(initialdir = "Images", title = "Select an image", filetypes = (("png files", "*.png"), ("all files", "*.*"))) # get the file using a file dialog

            if file:
                src = Image.open(file)
                logoImage = ctk.CTkImage(src, None, (110, 110))

                playlistImage.configure(image = logoImage)

                src.save("SavedImages/" + str(plid) + ".png")

        def onEnter(event, frame):

            def checkLabel():
                if len(frame.name) > 45 and self.afterID is None:
                    i = 0
                    n = 45
                    self.changeLabel(frame.name, frame.songName, i, n)

            frame.configure(fg_color = DARK_GREY)
            frame.playButton.place(x = 20, y = 2, anchor = "nw")
            frame.heartButton.place(x = 600, y = 2, anchor = "nw")
            frame.heartButton.configure(fg_color = DARK_GREY, hover_color = DARK_GREY)
            frame.mouseInside = True

            self.after(10, checkLabel)

            if hasattr(frame, "deleteButton"):
                frame.addButton.place(x = frame.addX, y = 2, anchor = "nw")
                frame.deleteButton.place(x = frame.deleteX, y = 2, anchor = "nw")
            else:
                frame.addButton.place(x = frame.addX, y = 2, anchor = "nw")

        def onLeave(event, frame):
            frame.mouseInside = False
            frame.after(10, checkMousePosition, frame)

        def onChildEnter(event, frame):
            frame.mouseInside = True
            onEnter(event, frame)

        def onChildLeave(event, frame):
            frame.mouseInside = False
            frame.after(10, checkMousePosition, frame)

        def checkMousePosition(frame):
            if not frame.mouseInside:
                widget = frame.winfo_containing(frame.winfo_pointerx(), frame.winfo_pointery())
                if widget is None or not widget.winfo_ismapped() or widget.master != frame:
                    frame.configure(fg_color = GREY_BACKGROUND)
                    frame.playButton.place_forget()
                    frame.addButton.place_forget()

                    if len(frame.name) > 45 and self.afterID is not None:
                        self.stopChangeLabel()
                        frame.songName.configure(text = frame.name[:45] + "...")

                    if hasattr(frame, "deleteButton"):
                        frame.deleteButton.place_forget()
                    
                    if not frame.liked:
                        frame.heartButton.place_forget()
                    else:
                        frame.heartButton.configure(fg_color = GREY_BACKGROUND, hover_color = GREY_BACKGROUND)

        for widget in self.winfo_children():
            widget.destroy()

        try:
            with open("playlists.json", "r") as file:
                data = json.load(file)
        except:
            data = []

        for i, playlist in enumerate(data):
            if playlist["id"] == plid:
                index = i

        playlistInfoFrame = ctk.CTkFrame(self, width = 675, height = 145, fg_color = GREY_BACKGROUND)
        playlistInfoFrame.place(x = 5, y = 5, anchor = "nw")
        canvas = ctk.CTkCanvas(self, width = 700, height = 5, bg = DARK_GREY, bd = 0, highlightthickness = 0)
        canvas.place(x = 75, y = 180, anchor = "nw")

        try:
            src = Image.open("SavedImages/" + str(plid) + ".png")
        except:
            src = Image.open("Images/defaultPlaylist.png")

        img = ctk.CTkImage(src, None, (110, 110))
        playlistImage = ctk.CTkLabel(playlistInfoFrame, text = "", image = img)
        playlistImage.place(x = 30, y = 15, anchor = "nw")

        playlistName = ctk.CTkLabel(playlistInfoFrame, text = data[index]["name"], font = (APP_FONT_BOLD, 35))
        playlistName.place(x = 170, y = 15, anchor = "nw")

        if len(data[index]["songs"]) == 1:
            numSongs = ctk.CTkLabel(playlistInfoFrame, text = str(len(data[index]["songs"])) + " song", font = (APP_FONT, 15))
        else:
            numSongs = ctk.CTkLabel(playlistInfoFrame, text = str(len(data[index]["songs"])) + " songs", font = (APP_FONT, 15))

        numSongs.place(x = 170, y = 55, anchor = "nw")

        uploadButton = ctk.CTkButton(playlistInfoFrame, text = "Change image", text_color = "black", font = (APP_FONT, 15), width = 150, height = 30, fg_color = GREY, corner_radius = 10, hover_color = GREY, command = chooseLogo)
        uploadButton.place(x = 500, y = 15, anchor = "nw")

        deleteButton = ctk.CTkButton(playlistInfoFrame, text = "Delete playlist", text_color = "black", font = (APP_FONT, 15), width = 150, height = 30, fg_color = GREY, corner_radius = 10, hover_color = GREY, command = lambda: self.deletePlaylist(plid))
        deleteButton.place(x = 500, y = 55, anchor = "nw")

        if plid == 0 or plid == 1:
            deleteButton.configure(state = "disabled")
        
        songsFrame = ctk.CTkScrollableFrame(self, width = 655, height = 295, fg_color = GREY_BACKGROUND)
        songsFrame.place(x = 5, y = 155, anchor = "nw")

        frame = ctk.CTkFrame(songsFrame, width = 655, height = 30, fg_color = GREY_BACKGROUND)
        frame.pack()

        ctk.CTkLabel(frame, text = "#", font = (APP_FONT_BOLD, 15)).place(x = 5, y = 5, anchor = "nw")
        ctk.CTkLabel(frame, text = "Name", font = (APP_FONT_BOLD, 15)).place(x = 60, y = 5, anchor = "nw")
        ctk.CTkLabel(frame, text = "Runtime", font = (APP_FONT_BOLD, 15)).place(x = 418, y = 20, anchor = "center")

        self.sortButton = ctk.CTkButton(frame, text = "Sort", text_color = "black", font = (APP_FONT, 15), width = 100, height = 20, fg_color = APP_BACKGROUND, corner_radius = 10, hover_color = APP_BACKGROUND, command = lambda: print("Sort"))
        self.sortButton.place(x = 650, y = 5, anchor = "ne")
        
        for i, song in enumerate(data[index]["songs"]):
            frame = ctk.CTkFrame(songsFrame, width = 655, height = 30, fg_color = GREY_BACKGROUND)
            frame.pack()

            frame.name = song["name"]

            if len(frame.name) > 45:
                nameText = frame.name[:45] + "..."
            else:
                nameText = frame.name

            frame.liked = song["favourited"]

            ctk.CTkLabel(frame, text = str(i + 1), font = (APP_FONT, 15)).place(x = 5, y = 0, anchor = "nw")

            frame.songName = ctk.CTkLabel(frame, text = nameText, font = (APP_FONT, 15))
            frame.songName.place(x = 60, y = 0, anchor = "nw")
            ctk.CTkLabel(frame, text = song["runTime"], font = (APP_FONT, 15)).place(x = 418, y = 15, anchor = "center")

            src = Image.open("Images/play.png")
            img = ctk.CTkImage(src, None, (15, 15))
            frame.playButton = ctk.CTkButton(frame, text = "", image = img, width = 10, height = 20, fg_color = DARK_GREY, corner_radius = 10, hover_color = DARK_GREY, command = lambda i = i: self.playSong(plid, i))

            if plid == 1:
                src = Image.open("Images/add.png")
                img = ctk.CTkImage(src, None, (15, 15))
                frame.addButton = ctk.CTkButton(frame, text = "", image = img, width = 10, height = 20, fg_color = DARK_GREY, corner_radius = 10, hover_color = DARK_GREY, command = lambda i = i: self.addToPlaylist(i, plid))
                frame.addX = 550
            else:
                src = Image.open("Images/add.png")
                img = ctk.CTkImage(src, None, (15, 15))
                frame.addButton = ctk.CTkButton(frame, text = "", image = img, width = 10, height = 20, fg_color = DARK_GREY, corner_radius = 10, hover_color = DARK_GREY, command = lambda i = i: self.addToPlaylist(i, plid))
                frame.addX = 500
                
                src = Image.open("Images/delete.png")
                img = ctk.CTkImage(src, None, (15, 15))
                frame.deleteButton = ctk.CTkButton(frame, text = "", image = img, width = 10, height = 20, fg_color = DARK_GREY, corner_radius = 10, hover_color = DARK_GREY, command = lambda i = i: self.deleteFromPlaylist(i, plid))
                frame.deleteX = 550

            if frame.liked:
                src = Image.open("Images/liked.png")
                img = ctk.CTkImage(src, None, (15, 15))
                frame.heartButton = ctk.CTkButton(frame, text = "", image = img, width = 10, height = 20, fg_color = GREY_BACKGROUND, corner_radius = 10, hover_color = GREY_BACKGROUND)
                frame.heartButton.configure(command = lambda i = i, heart = frame.heartButton, frame = frame: self.unlikeSong(i, plid, heart, frame))
                frame.heartButton.place(x = 600, y = 2, anchor = "nw")
            else:
                src = Image.open("Images/emptyHeart.png")
                img = ctk.CTkImage(src, None, (15, 15))
                frame.heartButton = ctk.CTkButton(frame, text = "", image = img, width = 10, height = 20, fg_color = DARK_GREY, corner_radius = 10, hover_color = DARK_GREY)
                frame.heartButton.configure(command = lambda i = i, heart = frame.heartButton, frame = frame: self.likeSong(i, plid, heart, frame))
            
            for widget in frame.winfo_children():
                widget.bind("<Enter>", lambda event, i = i, frame = frame: onChildEnter(event, frame))
                widget.bind("<Leave>", lambda event, i = i, frame = frame: onChildLeave(event, frame))

            frame.bind("<Enter>", lambda event, frame = frame: onEnter(event, frame))
            frame.bind("<Leave>", lambda event, frame = frame: onLeave(event, frame))

    def changeLabel(self, string, label, i, n):

        def updateLabel(string, label, i, n):
            if i + n <= len(string):
                label.configure(text = string[i:i+n])
            else:
                label.configure(text = string[i:] + "  " +  string[:(i+n) % len(string)])

            self.update_idletasks()

            i += 1

            if i == len(string):
                i = 0
            
            return i

        i = updateLabel(string, label, i, n)
        self.afterID = self.after(150, lambda: self.changeLabel(string, label, i, n))

    def stopChangeLabel(self):
        if self.afterID is not None:
            self.after_cancel(self.afterID)
            self.afterID = None

    def addToPlaylist(self, songIndex, plid):

        def checkPlaylist(name):
            if name in playlistsChecked:
                playlistsChecked.remove(name)
            else:
                playlistsChecked.append(name)

        def finishAdd(frame):
            frame.destroy()

            try:
                with open("playlists.json", "r") as file:
                    data = json.load(file)
            except:
                data = []

            for playlist in data:
                if playlist["id"] == plid:
                    songEntry = playlist["songs"][songIndex]

            for playlist in playlistsChecked:
                for pl in data:
                    if pl["name"] == playlist:
                        pl["songs"].append(songEntry)

            with open("playlists.json", "w") as file:
                json.dump(data, file)

            self.parent.pack(fill = "both", expand = True)
        
        playlistsChecked = []

        self.parent.pack_forget()
        playlistFrame = ctk.CTkFrame(self.root, width = 550, height = 310, fg_color = DARK_GREY)
        playlistFrame.place(relx = 0.5, rely = 0.5, anchor = "center")

        backButton = ctk.CTkButton(playlistFrame, text = "Done", font = (APP_FONT, 15), width = 50, height = 20, fg_color = APP_BACKGROUND, corner_radius = 30, hover_color = PURPLE_HOVER, command = lambda: finishAdd(playlistFrame))
        backButton.place(relx = 0.1, rely = 0.1, anchor = "center")

        ctk.CTkLabel(playlistFrame, text = "Select playlists", font = (APP_FONT_BOLD, 25)).place(relx = 0.5, rely = 0.15, anchor = "center")

        scrollFrame = ctk.CTkScrollableFrame(playlistFrame, width = 500, height = 150, fg_color = GREY_BACKGROUND)
        scrollFrame.place(relx = 0.5, rely = 0.6, anchor = "center")

        try:
            with open("playlists.json", "r") as file:
                data = json.load(file)
        except:
            data = []

        playlists = False
        for playlist in data:
            if playlist["id"] != 0 and playlist["id"] != 1 and playlist["id"] != plid:
                frame = ctk.CTkFrame(scrollFrame, width = 500, height = 40, fg_color = GREY_BACKGROUND)
                frame.pack()

                ctk.CTkLabel(frame, text = playlist["name"], font = (APP_FONT, 15)).place(x = 10, y = 0, anchor = "nw")

                checkbox = ctk.CTkCheckBox(frame, text = "", width = 20, height = 20, fg_color = GREY_BACKGROUND, corner_radius = 5, border_color = DARK_GREY, border_width = 2, command = lambda name = playlist["name"]: checkPlaylist(name))
                checkbox.place(x = 460, y = 0, anchor = "nw")

                playlists = True
        
        if not playlists:
            ctk.CTkLabel(scrollFrame, text = "No playlists available", font = (APP_FONT_BOLD, 25)).pack(pady = 75)

    def deleteFromPlaylist(self, songIndex, plid):

        try:
            with open("playlists.json", "r") as file:
                data = json.load(file)
        except:
            data = []

        if plid == 0:
            warning = CTkMessagebox(title = "Delete song", message = "Deleting the song from All songs will delete the song from the app.\n\nAre you sure you want to proceed?", icon = "question", option_1 = "Cancel", option_2 = "Yes", button_color = APP_BACKGROUND, fg_color = DARK_GREY, cancel_button_color = DARK_GREY, justify = "center")
            response = warning.get()

            if response == "Cancel":
                return
            
            for playlist in data:
                if playlist["id"] == 0:
                    songEntry = playlist["songs"][songIndex]

                # Create a new list excluding the songEntry
                playlist["songs"] = [song for song in playlist["songs"] if song != songEntry]

            with open("playlists.json", "w") as file:
                json.dump(data, file)

            os.remove("SavedSongs/" + songEntry["name"] + "_" + str(songEntry["folderID"]) + ".mp3")

        else:
            for playlist in data:
                if playlist["id"] == plid:
                    del playlist["songs"][songIndex]

            with open("playlists.json", "w") as file:
                json.dump(data, file)

        self.openPlaylist(plid)

    def likeSong(self, songIndex, plid, heartButton, frame):
        src = Image.open("Images/liked.png")
        img = ctk.CTkImage(src, None, (15, 15))
        heartButton.configure(image = img, command = lambda: self.unlikeSong(songIndex, plid, heartButton, frame))
        frame.liked = True

        try:
            with open("playlists.json", "r") as file:
                data = json.load(file)
        except:
            data = []

        for playlist in data:
            if playlist["id"] == plid:
                songEntry = playlist["songs"][songIndex]

                songEntryCopy = copy.deepcopy(songEntry)

                songEntry["favourited"] = True
            

        for playlist in data:
            for song in playlist["songs"]:
                if song == songEntryCopy:
                    song["favourited"] = True

            if playlist["id"] == 1:
                playlist["songs"].append(songEntry)

        with open("playlists.json", "w") as file:
            json.dump(data, file)

    def unlikeSong(self, songIndex, plid, heartButton, frame):
        src = Image.open("Images/emptyHeart.png")
        img = ctk.CTkImage(src, None, (15, 15))
        heartButton.configure(image = img, command = lambda: self.likeSong(songIndex, plid, heartButton, frame))
        frame.liked = False
        
        try:
            with open("playlists.json", "r") as file:
                data = json.load(file)
        except:
            data = []

        for playlist in data:
            if playlist["id"] == plid:
                songEntry = playlist["songs"][songIndex]

                songEntryCopy = copy.deepcopy(songEntry)

                if plid != 1:
                    songEntry["favourited"] = False
            
        for playlist in data:
            if playlist["id"] == 1:
                playlist["songs"] = [song for song in playlist["songs"] if song != songEntryCopy]

            for song in playlist["songs"]:
                if song == songEntryCopy:
                    song["favourited"] = False

        with open("playlists.json", "w") as file:
            json.dump(data, file)

        if plid == 1:
            self.openPlaylist(plid)

    def playSong(self, plid, songId):
        try:
            with open("playlists.json", "r") as file:
                data = json.load(file)
        except:
            data = []

        for playlist in data:
            if playlist["id"] == plid:
                song = playlist["songs"][songId]

                if songId == len(playlist["songs"]) - 1:
                    self.parent.musicData.lastSong = True
                else:
                    self.parent.musicData.lastSong = False

                songPath = "SavedSongs/" + song["name"] + "_" + str(song["folderID"]) + ".mp3"
                self.parent.musicData.playSong(songPath, song["name"], song["runTime"], plid, song["folderID"])

    def deletePlaylist(self, plid):

        question = CTkMessagebox(title = "Delete playlist", message = "Are you sure you want to delete this playlist?", icon = "question", option_1 = "Cancel", option_2 = "Yes", button_color = APP_BACKGROUND, fg_color = DARK_GREY, cancel_button_color = DARK_GREY, justify = "center")
        response = question.get()

        if response == "Cancel": # if no, exit
            return


        with open("playlists.json", "r") as file:
            data = json.load(file)

        for playlist in data:
            if playlist["id"] == plid:
                data.remove(playlist)

        with open("playlists.json", "w") as file:
            json.dump(data, file)

        # Attempt to find a profile icon in the SavedImages folder, and delete it if it exists
        try:
            os.remove("SavedImages/" + str(plid) + ".png")
        except:
            pass

        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text = "Open a playlist to\n start listening", font = (APP_FONT_BOLD, 35)).place(relx = 0.5, rely = 0.5, anchor = "center")

        for frame in self.parent.userData.playlistNames.winfo_children():
            if frame.id == plid:
                frame.destroy()

class MusicData(ctk.CTkFrame):  
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent, width = 685, height = 115, fg_color = GREY_BACKGROUND, border_color = DARK_GREY, corner_radius = 5, border_width = 3)
        self.place(x = 310, y = 480, anchor = "nw")

        self.noSongLabel = ctk.CTkLabel(self, text = "No song currently playing", font = (APP_FONT_BOLD, 25))
        self.noSongLabel.place(relx = 0.5, rely = 0.5, anchor = "center")

        self.currentSong = None
        self.shuffle = False
        self.songsPlayed = []
        self.shuffleSongs = []
        self.currentSongIndex = 0
        self.stopThread = False
        self.lastSong = False
        self.paused = False
        self.afterID = None

        pygame.mixer.init()

    def playSong(self, songPath, songName, runTime, plid, folderID, manual=False):

        def checkMusicPlaying():
            while not self.stopThread:
                if pygame.mixer.music.get_busy():
                    updateProgress()
                else:
                    self.stopThread = True
                pygame.time.Clock().tick(10)

            if not self.paused:
                if len(self.songsPlayed) - 1 == self.currentSongIndex:
                    self.getNextSongManual(plid, songName, folderID)
                else:
                    self.getNextSongList(plid, songName)

        def updateProgress():
            currentTime = pygame.mixer.music.get_pos() / 1000  # Get current time in seconds
            minutes, seconds = map(int, runTime.split(':'))

            totalTime = minutes * 60 + seconds
            progress = (currentTime / totalTime) * 100

            # Update the progress bar
            songProgress.set(progress)

            # Update the time label
            currentMinutes = int(currentTime // 60)
            currentSeconds = int(currentTime % 60)
            timeLabel.configure(text=f"{currentMinutes}:{currentSeconds:02d} / {runTime}")

        self.currentSong = songName
        self.paused = False

        for widget in self.winfo_children():
            widget.place_forget()

        if not manual:
            self.songsPlayed = self.songsPlayed[:self.currentSongIndex + 1]
            self.songsPlayed.append([songName, plid, folderID, runTime])
            self.currentSongIndex = len(self.songsPlayed) - 1

        self.nameLabel = ctk.CTkLabel(self, text = "", font = (APP_FONT_BOLD, 25))
        self.nameLabel.place(relx = 0.5, rely = 0.2, anchor = "center")

        self.stopChangeLabel(songName)

        songProgress = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, height=10, width=250, fg_color=DARK_GREY, progress_color=APP_BACKGROUND, button_color=APP_BACKGROUND, corner_radius=15, border_color=APP_BACKGROUND, border_width=2, button_length=0, state="disabled")
        songProgress.place(relx=0.5, rely=0.5, anchor="center")
        songProgress.set(0)

        timeLabel = ctk.CTkLabel(self, text="0:00 / " + runTime, font=(APP_FONT, 15))
        timeLabel.place(relx=0.5, rely=0.77, anchor="center")

        src = Image.open("Images/pause.png")
        img = ctk.CTkImage(src, None, (50, 50))
        self.playButton = ctk.CTkButton(self, text="", image=img, width=20, height=20, fg_color=GREY_BACKGROUND, corner_radius=25, hover_color=GREY_BACKGROUND, command=lambda: self.pauseToggle())
        self.playButton.place(relx=0.075, rely=0.5, anchor="center")

        src = Image.open("Images/nextSong.png")
        img = ctk.CTkImage(src, None, (15, 15))
        self.nextButton = ctk.CTkButton(self, text="", image=img, width=20, height=20, fg_color=GREY_BACKGROUND, corner_radius=25, hover_color=GREY_BACKGROUND, command=lambda: self.getNextSong(plid, songName, folderID))
        self.nextButton.place(relx=0.72, rely=0.5, anchor="center")

        src = Image.open("Images/previousSong.png")
        img = ctk.CTkImage(src, None, (15, 15))
        previousButton = ctk.CTkButton(self, text="", image=img, width=20, height=20, fg_color=GREY_BACKGROUND, corner_radius=25, hover_color=GREY_BACKGROUND, command=lambda: self.getPreviousSongList())
        previousButton.place(relx=0.28, rely=0.5, anchor="center")

        if self.currentSongIndex == 0:
            previousButton.configure(state="disabled")

        if self.lastSong:
            self.nextButton.configure(state="disabled")

        if self.shuffle:
            src = Image.open("Images/shuffleOn.png")
        else:
            src = Image.open("Images/shuffleOff.png")

        img = ctk.CTkImage(src, None, (20, 20))
        self.shuffleButton = ctk.CTkButton(self, text="", image=img, width=20, height=20, fg_color=GREY_BACKGROUND, corner_radius=25, hover_color=GREY_BACKGROUND, command=lambda: self.shuffleToggle(songName, plid, folderID))
        self.shuffleButton.place(relx=0.77, rely=0.5, anchor="center")

        # Start the music playback
        pygame.mixer.music.load(songPath)
        pygame.mixer.music.play()

        # Start the thread to check music playing
        self.stopThread = False
        thread = threading.Thread(target=checkMusicPlaying, daemon=True)
        thread.start()

    def setNameLabel(self, songName):
        self.nameLabel.configure(text = songName[:40])

        if len(songName) > 40 and self.afterID is None:
            i = 0
            n = 40
            self.changeLabel(songName, i, n, True)

    def changeLabel(self, string, i, n, first = True):

        time = 1000 if first else 300

        def updateLabel(string, i, n):
            if i + n <= len(string):
                self.nameLabel.configure(text = string[i:i+n])
            else:
                self.nameLabel.configure(text = string[i:] + "  " +  string[:(i+n) % len(string)])

            self.update_idletasks()

            i += 1

            if i == len(string):
                i = 0
            
            return i

        i = updateLabel(string, i, n)
        self.afterID = self.after(time, lambda: self.changeLabel(string, i, n, False))

    def stopChangeLabel(self, songName):
        if self.afterID is not None:
            self.after_cancel(self.afterID)
            self.afterID = None

        self.nameLabel.configure(text = "")
        self.setNameLabel(songName)

    def pauseToggle(self):
        if self.paused:
            pygame.mixer.music.unpause()
            src = Image.open("Images/pause.png")
        else:
            pygame.mixer.music.pause()
            src = Image.open("Images/play.png")
        
        img = ctk.CTkImage(src, None, (50, 50))
        self.playButton.configure(image = img)
        self.paused = not self.paused

    def shuffleToggle(self, songName, plid, folderID):
        if self.shuffle:
            src = Image.open("Images/shuffleOff.png")

            try:
                with open("playlists.json", "r") as file:
                    data = json.load(file)
            except:
                data = []

            for playlist in data:
                if playlist["id"] == plid:
                    if playlist["songs"][-1]["name"] == songName and playlist["songs"][-1]["folderID"] == folderID:
                        self.lastSong = True
                        self.nextButton.configure(state = "disabled")
                        break

                    self.lastSong = False
                    self.nextButton.configure(state = "normal")

        else:
            src = Image.open("Images/shuffleOn.png")
            self.setShuffle(plid)
            self.lastSong = False
            self.nextButton.configure(state = "normal")

        img = ctk.CTkImage(src, None, (20, 20))
        self.shuffleButton.configure(image = img, command = lambda: self.shuffleToggle(songName, plid, folderID))

        self.shuffle = not self.shuffle

    def setShuffle(self, plid):

        self.shuffleSongs = []
        try:
            with open("playlists.json", "r") as file:
                data = json.load(file)
        except:
            data = []

        for playlist in data:
            if playlist["id"] == plid:
                for song in playlist["songs"]:
                    if self.songsPlayed and not (song["name"] == self.songsPlayed[-1][0] and song["folderID"] == self.songsPlayed[-1][2]):
                        self.shuffleSongs.append(song)

    def getNextSong(self, plid, songName, folderID):
        if len(self.songsPlayed) - 1 == self.currentSongIndex:
            self.getNextSongManual(plid, songName, folderID)
        else:
            self.getNextSongList(plid, songName)

    def getNextSongManual(self, plid, songName, folderID):
        try:
            with open("playlists.json", "r") as file:
                data = json.load(file)
        except:
            data = []

        for playlist in data:
            if playlist["id"] == plid:
                if not self.shuffle:
                    for i, song in enumerate(playlist["songs"]):
                        if song["name"] == songName and song["folderID"] == folderID:
                            if i + 1 < len(playlist["songs"]):
                                if i + 1 == len(playlist["songs"]) - 1:
                                    self.lastSong = True
                                else:
                                    self.lastSong = False
                                nextSongEntry = playlist["songs"][i + 1]
                            else:
                                for widget in self.winfo_children():
                                    widget.place_forget()
                                
                                self.endPlay()
                                return
                else:
                    if len(self.shuffleSongs) == 0:  
                        self.setShuffle(plid)

                    nextSongEntry = random.choice(self.shuffleSongs)
                    self.shuffleSongs.remove(nextSongEntry)

        songPath = "SavedSongs/" + nextSongEntry["name"] + "_" + str(nextSongEntry["folderID"]) + ".mp3"
        self.playSong(songPath, nextSongEntry["name"], nextSongEntry["runTime"], plid, nextSongEntry["folderID"])

    def getNextSongList(self, plid, songName):
        self.currentSongIndex += 1
        songName = self.songsPlayed[self.currentSongIndex][0]
        plid = self.songsPlayed[self.currentSongIndex][1]
        folderID = self.songsPlayed[self.currentSongIndex][2]
        runTime = self.songsPlayed[self.currentSongIndex][3]

        songPath = "SavedSongs/" + songName + "_" + str(folderID) + ".mp3"
        self.playSong(songPath, songName, runTime, plid, folderID, manual = True)

        try:
            with open("playlists.json", "r") as file:
                data = json.load(file)
        except:
            data = []

        for playlist in data:
                if playlist["id"] == plid:
                    if playlist["songs"][-1]["name"] == songName and playlist["songs"][-1]["folderID"] == folderID:
                        self.lastSong = True
                        self.nextButton.configure(state = "disabled")
                        break

                    self.lastSong = False
                    self.nextButton.configure(state = "normal")

    def getPreviousSongList(self):
        self.currentSongIndex -= 1
        songName = self.songsPlayed[self.currentSongIndex][0]
        plid = self.songsPlayed[self.currentSongIndex][1]
        folderID = self.songsPlayed[self.currentSongIndex][2]
        runTime = self.songsPlayed[self.currentSongIndex][3]

        self.lastSong = False

        songPath = "SavedSongs/" + songName + "_" + str(folderID) + ".mp3"
        self.playSong(songPath, songName, runTime, plid, folderID, manual = True)

    def joinThread(self):
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join()

    def endPlay(self):

        self.stopThread = True
        pygame.mixer.music.stop()

        self.after(1000, self.joinThread)
        
        self.noSongLabel.place(relx = 0.5, rely = 0.5, anchor = "center")

        self.currentSong = None
        self.shuffle = False
        self.songsPlayed = []
        self.currentSongIndex = 0

