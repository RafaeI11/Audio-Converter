from tkinter import Tk, Button, filedialog, messagebox, font
from threading import Thread

from utils import Recorder, BarWindow, display_img, ICON

# Animation for when rec_button is pressed
def press_rec(self):
    if recorder.is_recording:
        rec_btn.configure(image=stop_pressed)
    else:
        rec_btn.configure(image=mic_pressed)


# starts/stops recording and creates video file
def release_rec(self):
    if recorder.is_recording:
        rec_btn.configure(image=mic)
        progress_bar = BarWindow()
        Thread(target=recorder.stop_rec, args=(progress_bar,)).start()
        progress_bar.pg_bar()

    else:
        recorder.start_rec()
        rec_btn.configure(image=stop)


# Open selected file and converts into video
def create_from_audio():
    root.filename = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(
            ("MP3", "*.mp3"),
            ("All", "*.*"),
        ),
    )
    if root.filename != "":
        progress_bar = BarWindow()
        try:
            Thread(
                target=recorder.create_from_audio, args=(root.filename, progress_bar)
            ).start()
            progress_bar.pg_bar()
        except Exception as error:
            messagebox.showerror("Error", error)


root = Tk()
root.configure(width=800, height=550, bg="black")
root.minsize(width=200, height=200)
root.title("Audio Converter")
root.iconbitmap(ICON)
recorder = Recorder()

# rec_btn images
mic = display_img("images/mic.png")
mic_pressed = display_img("images/mic_pressed.png")
stop = display_img("images/stop.png")
stop_pressed = display_img("images/stop_pressed.png")

rec_btn = Button(
    image=mic, borderwidth=0, relief="sunken", bg="black", activebackground="black"
)
rec_btn.bind("<ButtonPress>", press_rec)
rec_btn.bind("<ButtonRelease>", release_rec)

convert_btn = Button(
    text="♫ → 📷",
    command=create_from_audio,
    relief="flat",
    fg="white",
    bg="black",
    activebackground="gray",
)
convert_btn["font"] = font.Font(size=15)

if __name__ == "__main__":
    rec_btn.place(relx=0.5, rely=0.5, anchor="center")
    convert_btn.place(relx=1.0, y=0, anchor="ne")
    root.mainloop()
