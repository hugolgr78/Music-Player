 def playSong(self, songPath, songName, runTime, plid, folderID, manual=False):

        def checkMusicPlaying():
            while not self.stopThread:
                if pygame.mixer.music.get_busy():
                    updateProgress()
                else:
                    self.stopThread = True
                pygame.time.Clock().tick(10)

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
        self.playButton = ctk.CTkButton(self, text="", image=img, width=20, height=20, fg_color=GREY_BACKGROUND, corner_radius=25, hover_color=GREY_BACKGROUND, command=lambda: print("pause"))
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