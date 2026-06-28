import os
import pygame as pg
import time
import customtkinter as ctk
from tkinter import filedialog

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
    filepath = ctk.filedialog.askopenfilename()
    global cur_track
    cur_track = Track(filepath)
    cur_track.start_new()
    lbl1 = ctk.CTkLabel(root, text=f'Вы добавили трек: {os.path.basename(filepath)}')
    lbl1.pack()
    frame_row = ctk.CTkFrame(root, fg_color="transparent")
    frame_row.pack(pady=40)
    btn_play = ctk.CTkButton(frame_row,text='Играть сначала', command=cur_track.run1)
    btn_play.pack(side="left", padx=10)
    btn_pause = ctk.CTkButton(frame_row,text='Пауза', command=cur_track.pause1)
    btn_pause.pack(side="left", padx=10)
    btn_cont = ctk.CTkButton(frame_row,text='Продолжить', command=cur_track.continue1)
    btn_cont.pack(side="left", padx=10)
    lbl2 = ctk.CTkLabel(frame_row, text='Гомкость:')
    lbl2.pack(side="left", padx=10)
    scale = ctk.CTkSlider(frame_row, width=100, from_=0, to=1, command=change)
    scale.pack(side="left", padx=10)
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
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title('MusicPlayer')
root.geometry("500x500")
btn = ctk.CTkButton(root,text='Выберите трек', command=open_trek)
btn.pack()
root.mainloop()