import os
import sys
from datetime import datetime
from timeit import default_timer
from tkinter import Toplevel, messagebox
from tkinter.ttk import Progressbar

import numpy
import sounddevice as sd
from moviepy.audio import AudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import ImageClip
from PIL import Image, ImageTk


class Recorder:
    def __init__(self) -> None:
        self.img = Image.new("RGB", (80, 80), (0, 0, 0))
        self.img = numpy.array(self.img)
        self.frequency = 44100
        self.seconds = 600
        self.is_recording = False

    def start_rec(self):
        self.file_name = (
            str(datetime.now()).split(".")[0].replace(" ", "_").replace(":", "-")
        )
        self.recording = sd.rec(
            int(self.seconds * self.frequency), samplerate=self.frequency, channels=2
        )
        self.start = default_timer()
        self.is_recording = True
        print("started recording...")

    def stop_rec(self, progress_bar):
        print("stopped recording...")
        sd.stop()
        self.is_recording = False
        self.end = default_timer()
        self.final = int(self.end - self.start) + 1
        self.audio = AudioClip.AudioArrayClip(self.recording, self.frequency)
        self.audio.duration = self.final
        self.clip = ImageClip(self.img, duration=self.final)
        self.clip.fps = 1
        self.final_clip = self.clip.set_audio(self.audio)
        self.final_clip.write_videofile(f"{self.file_name}.mp4")
        progress_bar.destroy()
        messagebox.showinfo(
            "Process Finnished!", f"{self.file_name} created sucefully!"
        )

    def create_from_audio(self, path, progress_bar):
        self.audio = AudioFileClip(path)
        self.clip = ImageClip(self.img, duration=self.audio.duration)
        self.clip.fps = 1
        self.final_clip = self.clip.set_audio(self.audio)
        name, ext = path.split("\\")[-1].split(".")
        if ext == "mp4":
            self.final_clip.write_videofile(f"{name} audio.mp4")
        else:
            self.final_clip.write_videofile(f"{name}.mp4")
        progress_bar.destroy()
        messagebox.showinfo("Process Finnished!", f"{name} created sucefully!")


class BarWindow(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind("<Button-1>", self.click)
        self.bind("<B1-Motion>", self.drag)

    def drag(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry("+{x}+{y}".format(x=x, y=y))

    def click(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def pg_bar(self):
        self.bar = Progressbar(
            self, orient="horizontal", length=200, mode="indeterminate"
        )
        self.bar.pack(padx=5, pady=5)
        self.bar.start(5)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def display_img(img, size=(100, 100)):
    displayed_img = Image.open(img)
    displayed_img = displayed_img.resize(size, Image.ANTIALIAS)
    displayed_img = ImageTk.PhotoImage(displayed_img)
    return displayed_img


ICON = resource_path("images/icon.ico")
