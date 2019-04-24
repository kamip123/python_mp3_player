from tkinter.filedialog import askdirectory
import pygame
import tkinter as tk
import os
import time
import _thread
import shutil

song_list = []
directory = None
song_id = -1
listbox_with_music = None
song_name = None
playlist_empty = True


def update_song_name():
    global song_name
    song_name.set(song_list[song_id])


def music_play():
    pygame.mixer.music.unpause()


def music_pause():
    pygame.mixer.music.pause()


def music_stop():
    pygame.mixer.music.rewind()


def next_song():
    global song_id

    listbox_with_music.selection_clear(song_id)

    if len(song_list) >= song_id+2:
        song_id += 1
        pygame.mixer.music.load(song_list[song_id])
        pygame.mixer.music.play()
        update_song_name()

        listbox_with_music.select_set(song_id)
    else:
        song_id = 0
        pygame.mixer.music.load(song_list[song_id])
        update_song_name()
        listbox_with_music.select_set(song_id)


def previous_song():
    global song_id

    listbox_with_music.selection_clear(song_id)

    if song_id >= 1:
        song_id -= 1
    pygame.mixer.music.stop()
    pygame.mixer.music.load(song_list[song_id])
    pygame.mixer.music.play()
    update_song_name()

    listbox_with_music.select_set(song_id)


def volume_up():
    if pygame.mixer.music.get_volume() < 1.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)


def volume_down():
    if pygame.mixer.music.get_volume() > 0.0:
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)


def ask_for_directory():
    global directory
    global song_list
    global listbox_with_music
    global playlist_empty
    directory = askdirectory()
    os.chdir(directory)

    song_list = []

    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            song_list.append(file)

    if len(song_list) > 0:
        for song in song_list:
            listbox_with_music.insert('end', song)

        playlist_empty = False

        update_song_name()

        button_zip_files['state'] = 'normal'


def song_selection(self):
    global song_id

    song_id = listbox_with_music.curselection()[0]

    pygame.mixer.music.load(song_list[song_id])
    pygame.mixer.music.play()

    update_song_name()


def update_song_playing():
    global song_id
    global playlist_empty
    while True:
        if not playlist_empty:
            time.sleep(2)  # give time for new song to play and then check
            if not pygame.mixer.music.get_busy():
                print('test')
                next_song()


def ask_for_destination_directory():
    global directory_destination
    directory_destination = askdirectory()
    top.lift()


def zip_files():
    destination_string = directory_destination + '/' + entry_name.get()
    shutil.make_archive(destination_string, 'zip', directory)
    button_zip_files['state'] = 'normal'
    top.destroy()


def zip_music():
    button_zip_files['state'] = 'disabled'
    global top
    top = tk.Toplevel()
    top.minsize(250, 150)
    top.title("Save playlist")
    top.lift()
    button_choose_directory = tk.Button(top, text="Choose destination", command=ask_for_destination_directory, fg="red")
    button_choose_directory.pack()

    global entry_name
    entry_name = tk.Entry(top)
    entry_name.insert(tk.END, 'default')
    entry_name.pack()

    button_choose_directory = tk.Button(top, text="Save", command=zip_files, fg="red")
    button_choose_directory.pack()


def init_window():
    global listbox_with_music
    global song_name
    window = tk.Tk()
    window.minsize(250, 150)
    song_name = tk.StringVar()
    song_name.set('Nothing...')
    label_logo = tk.Label(window, text="MP3 Player", font=("Helvetica", 15))
    label_logo.grid(column=3, row=0)

    button_choose_directory = tk.Button(window, text="Choose files", command=ask_for_directory, fg="red")
    button_choose_directory.grid(column=0, row=0)

    button_previous = tk.Button(window, text="Previous", command=previous_song, fg="red")
    button_previous.grid(column=0, row=1)

    button_play = tk.Button(window, text="Play", command=music_play, fg="red")
    button_play.grid(column=1, row=1)

    button_pause = tk.Button(window, text="Pause", command=music_pause, fg="red")
    button_pause.grid(column=2, row=1)

    button_stop = tk.Button(window, text="Stop", command=music_stop, fg="red")
    button_stop.grid(column=3, row=1)

    button_next = tk.Button(window, text="Next", command=next_song, fg="red")
    button_next.grid(column=4, row=1)

    button_volume_up = tk.Button(window, text="+", command=volume_up, fg="red")
    button_volume_up.grid(column=1, row=2)

    button_volume_down = tk.Button(window, text="-", command=volume_down, fg="red")
    button_volume_down.grid(column=1, row=3)

    label_logo_playing = tk.Label(window, text="Currently playing: ", font=("Helvetica", 10))
    label_logo_playing.grid(column=2, row=2)

    label_song_name = tk.Label(window, textvariable=song_name, font=("Helvetica", 10))
    label_song_name.grid(column=3, row=2)

    label_songs = tk.Label(window, text="Songs: ", font=("Helvetica", 10))
    label_songs.grid(column=3, row=3)

    listbox_with_music = tk.Listbox(window, width='60', selectmode='single')
    listbox_with_music.grid(column=3, row=4)

    global button_zip_files
    button_zip_files = tk.Button(window, text="Save playlist", state='disabled', command=zip_music, fg="red")
    button_zip_files.grid(column=1, row=4)

    listbox_with_music.bind('<<ListboxSelect>>', song_selection)

    pygame.mixer.init()
    _thread.start_new_thread(update_song_playing, ())

    window.mainloop()


if __name__ == '__main__':
    init_window()
