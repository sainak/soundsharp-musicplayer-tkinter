import os
from tkinter import Button, Listbox, PhotoImage, Tk
from tkinter.filedialog import askdirectory
from pathlib import Path

from pygame import mixer


class Player(Tk):
    def __init__(self) -> None:
        mixer.pre_init(44100, -16, 2, 1024)
        mixer.init()
        self.playlist = []
        self.playing = False
        self.now_playing = -1
        self.directory = ""

        # box
        super().__init__()
        self.title("soundsharp")
        self.state("iconic")

        # symbols to be displayed on button
        assets = Path(__file__).resolve().parent / "assets"
        self.play_image = PhotoImage(file=assets / "play.png").subsample(3)
        self.pause_image = PhotoImage(file=assets / "pause.png").subsample(3)
        self.next_image = PhotoImage(file=assets / "next.png").subsample(3)
        self.prev_image = PhotoImage(file=assets / "priv.png").subsample(3)
        self.list_image = PhotoImage(file=assets / "list.png").subsample(3)
        self.exit_image = PhotoImage(file=assets / "exit.png").subsample(3)

        # gui structure
        self.playback_button = self.__create_button(
            "play", self.play_image, self.toggle_playback
        )
        self.prev_button = self.__create_button("prev", self.prev_image, self.prev)
        self.next_button = self.__create_button("next", self.next_image, self.next)
        self.list_button = self.__create_button(
            "list", self.list_image, self.select_dir
        )
        self.exit_button = self.__create_button("exit", self.exit_image, self.destroy)
        self.listbox = Listbox(self, relief="sunken", width=32, height=20)

        self.playback_button.grid(column=0, row=0)
        self.prev_button.grid(column=1, row=0, padx=2, pady=2)
        self.next_button.grid(column=2, row=0, padx=2, pady=2)
        self.list_button.grid(column=3, row=0, padx=2, pady=2)
        self.exit_button.grid(column=4, row=0, padx=2, pady=2)
        self.listbox.grid(row=1, columnspan=8)

    def __create_button(self, text, image, command):
        return Button(
            self,
            text=text,
            image=image,
            command=command,
            height=40,
            width=40,
            padx=2,
            pady=2,
        )

    def __select_track_from_list(self, index):
        length = len(self.playlist)
        self.listbox.selection_clear(0, length)
        self.listbox.selection_set(index)

    def select_dir(self):
        directory = askdirectory()
        if isinstance(directory, tuple):
            # no selection
            return
        path = Path(directory).resolve()
        self.pause()
        self.now_playing = -1
        self.listbox.delete(0, len(self.playlist))
        self.playlist = []
        i = 0
        for file in path.iterdir():
            if file.is_file() and file.suffix == ".mp3":
                self.playlist.append(file)
                self.listbox.insert(i, file.stem)
                i += 1

    def set_track(self):
        mixer.music.unload()
        self.__select_track_from_list(self.now_playing)
        mixer.music.load(self.playlist[self.now_playing])
        mixer.music.play()

    def pause(self):
        mixer.music.pause()
        self.playback_button.config(image=self.play_image)
        self.playing = False

    def play(self):
        try:
            current_selection = self.listbox.curselection()[0]
        except IndexError:
            if not self.playlist:
                return
            current_selection = 0
            self.__select_track_from_list(current_selection)
        if self.now_playing == current_selection:
            mixer.music.unpause()
        else:
            self.now_playing = current_selection
            self.set_track()
        self.playback_button.config(image=self.pause_image)
        self.playing = True

    def toggle_playback(self):
        if self.playing:
            self.pause()
        else:
            self.play()

    def prev(self):
        if self.now_playing > 0:
            self.now_playing -= 1
        self.set_track()

    def next(self):
        if self.now_playing < len(self.playlist) - 1:
            self.now_playing += 1
        self.set_track()

    def stop():
        mixer.music.stop()


def main():
    player = Player()
    player.mainloop()


if __name__ == "__main__":
    main()
