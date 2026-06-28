import os
import pygame as pg
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class Track:
    def __init__(self, filepath):
        self.filepath = filepath
        self.name = os.path.basename(self.filepath)
        self.liked = False
    def like(self):
        Track.liked = not(Track.liked)
    def start_new(self):
        pg.mixer.music.load(self.filepath)
        print(f'Текущий трек: {self.name}')
        print(f'Введите 1 чтобы воспроизвести {self.name}')
    def add_to_queue(self):
        pg.mixer.music.queue(self.filepath)
        print(f'Трек {self.name} добавлен в очередь')
    def run1(self):
        pg.mixer.music.play()
        print('ВВедите 0 чтобы поставить на паузу')
    def pause1(self):
        pg.mixer.music.pause()
        print('Трек на паузе, введите 2 чтобы возобновить его')
    def continue1(self):
        pg.mixer.music.unpause()
cur_track = None
def change(newVal):
    pg.mixer.music.set_volume(float(newVal))
def open_trek():
    filepath = tk.filedialog.askopenfilename()
    global cur_track
    cur_track = Track(filepath)
    cur_track.start_new()
    lbl1 = tk.Label(root, text=f'Вы добавили трек: {os.path.basename(filepath)}')
    lbl1.pack()
    btn_play = ttk.Button(text='Играть сначала', command=cur_track.run1)
    btn_play.pack()
    btn_pause = ttk.Button(text='Пауза', command=cur_track.pause1)
    btn_pause.pack()
    btn_cont = ttk.Button(text='Продолжить', command=cur_track.continue1)
    btn_cont.pack()
    scale = ttk.Scale(length=100, from_=0.0, to=1.0, value=0.5, command=change)
    scale.pack()
class Playlist:
    def __init__(self, name):
        self.name = name
        self.tracks = []
    def add(self, track):
        self.tracks.append(track)
    def delete(self, track):
        self.tracks.remove(track)
pg.init()
pg.mixer.init()
root = tk.Tk()
root.title('MusicPlayer')
root.geometry("500x500")
btn = ttk.Button(text='Выберите трек', command=open_trek)
btn.pack()
root.mainloop()
# print('Введите load чтобы загрузить новый трек, а затем его название')
# print('Введите add чтобы добавить в очередь новый трек, а затем его название')
# MUSIC_END = pg.event.custom_type()
# pg.mixer.music.set_endevent(MUSIC_END)
# cur_track = Track('-1')
# next_track = Track('-1')
# while True:
#     command = input().strip().lower()
#     for event in pg.event.get():
#         if event.type == MUSIC_END:
#             cur_track = next_track
#             next_track = 0
#     if command == 'load':
#         name = input().strip()
#         sound = Track(name)
#         sound.start_new()
#         cur_track = sound
#     elif command == 'add':
#         name = input().strip()
#         sound = Track(name)
#         sound.add_to_queue()
#         nex_track = sound
#     elif command == '1':
#         if cur_track.name == '-1':
#             print('Сначала нужно загрузить трек')
#         else:
#             cur_track.run1()
#     elif command == '0':
#         cur_track.pause1()
#         print(f'{cur_track.name} на паузе')
#     elif command == '2':
#         cur_track.continue1()
#Riptide - Vance Joy.mp3
