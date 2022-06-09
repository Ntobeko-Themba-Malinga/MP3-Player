import os
import tkinter
from tkinter import filedialog
from pygame import mixer

mixer.init()
load_new_songs = True
song_paused = False
folder = ''
songs = []
current_playing_song = 0


def song_directory():
    global folder, load_new_songs, songs
    songs = []
    song_list.delete(0, tkinter.END)
    folder = filedialog.askdirectory(title="Open Folder")
    directories = os.listdir(folder)
    print(directories)

    i = 1
    for directory in directories:
        if directory[:-4:-1][::-1] == 'mp3':
            songs.append(folder+'/'+directory)
            song_list.insert(i, directory)
            i += 1
    play()


def load_song():
    global current_playing_song

    mixer.music.load(songs[current_playing_song])
    mixer.music.play()


def play():
    global load_new_songs, current_playing_song, song_paused

    if load_new_songs:
        song_list.select_set(current_playing_song)
        load_song()
        load_new_songs = False
    else:
        song_paused = False
        play_pause_button.config(image=pause_image, command=pause)
        mixer.music.unpause()


def pause():
    global song_paused

    song_paused = True

    if mixer.music.get_busy():
        play_pause_button.config(image=play_image, command=play)
        mixer.music.pause()


def next_song():
    global current_playing_song
    if current_playing_song < len(songs):
        song_list.select_clear(current_playing_song)
        current_playing_song += 1
        song_list.select_set(current_playing_song)
    load_song()


def previous_song():
    global current_playing_song
    if current_playing_song > 0:
        song_list.select_clear(current_playing_song)
        current_playing_song -= 1
        song_list.select_set(current_playing_song)
    load_song()


def volume():
    mixer.music.set_volume(float(int(volume_scale.get())/100))


def select_song(event):
    global folder, current_playing_song
    current_playing_song = song_list.curselection()[0]
    song = song_list.get(song_list.curselection())
    play_pause_button.config(image=pause_image, command=pause)
    mixer.music.load(folder+'/'+song)
    mixer.music.play()


def play_entire_song_list():
    global current_playing_song
    if mixer.music.get_busy() == False and current_playing_song < len(songs)-1 and song_paused == False:
        song_list.select_clear(current_playing_song)
        current_playing_song += 1
        song_list.select_set(current_playing_song)
        load_song()
    window.after(1000, play_entire_song_list)


window = tkinter.Tk()
window.title("MP3 Player")
icon_image = tkinter.PhotoImage(file="images\\icon.png")
window.iconphoto(True, icon_image)

menu = tkinter.Menu(master=window)
window.config(menu=menu)

open_file_menu = tkinter.Menu(master=menu, tearoff=False)
menu.add_cascade(menu=open_file_menu, label="Load")
open_file_menu.add_command(label="Open", command=song_directory)

frame_1 = tkinter.Frame(master=window)
frame_1.pack()

scrollbar = tkinter.Scrollbar(master=frame_1)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

song_list = tkinter.Listbox(
    master=frame_1,
    width=52,
    bg='black',
    fg='red',
    yscrollcommand=scrollbar.set
)
song_list.pack()
scrollbar.config(command=song_list.yview)

song_list.bind("<Double-Button-1>", select_song)

frame_2 = tkinter.Frame(master=window)
frame_2.pack(pady=10)

# previous button
# https://www.flaticon.com/premium-icon/next-track_3240697?term=continue&page=1&position=39&page=1&position=39&related_id=3240697&origin=tag
previous_image = tkinter.PhotoImage(file="images\\previous-track.png")
previous_button = tkinter.Button(
    master=frame_2,
    image=previous_image,
    command=previous_song
)
previous_button.grid(row=0, column=0)

# play, pause button
# <a href="https://www.flaticon.com/free-icons/play-button" title="play button icons">Play button icons created by Freepik - Flaticon</a>
play_image = tkinter.PhotoImage(file="images\\play.png")
# <a href="https://www.flaticon.com/free-icons/pause-button" title="pause button icons">Pause button icons created by Pixel perfect - Flaticon</a>
pause_image = tkinter.PhotoImage(file="images\\pause-button.png")
play_pause_button = tkinter.Button(
    master=frame_2,
    image=pause_image,
    command=pause
)
play_pause_button.grid(row=0, column=1)

# next
# https://www.flaticon.com/premium-icon/next-track_3240697?term=continue&page=1&position=39&page=1&position=39&related_id=3240697&origin=tag
next_image = tkinter.PhotoImage(file="images\\next-track.png")
next_button = tkinter.Button(
    master=frame_2,
    image=next_image,
    command=next_song
)
next_button.grid(row=0, column=2)

# volume scale
# <a href="https://www.flaticon.com/free-icons/play-button" title="play button icons">Play button icons created by Freepik - Flaticon</a>
volume_image = tkinter.PhotoImage(file="images\\volume.png")
volume_label = tkinter.Label(
    master=window,
    image=volume_image,
    pady=10
)
volume_label.pack(side='left')
volume_scale = tkinter.Scale(
    master=window,
    from_=0,
    to=100,
    orient=tkinter.HORIZONTAL,
    command=lambda data: volume(),
    length=300,
    tickinterval=10
)
volume_scale.set(100)
volume_scale.pack(side='right')

play_entire_song_list()

window.mainloop()
