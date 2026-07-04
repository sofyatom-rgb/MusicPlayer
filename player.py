import os
import pygame as pg
import time
import customtkinter as ctk
from tkinter import filedialog
import json
paused = False
cur_playlist = None
cur_track = None
class Track:
    def __init__(self, filepath):
        self.filepath = filepath
        self.name = os.path.basename(self.filepath)
        self.liked = False
    def like(self):
        self.liked = not(self.liked)
    def start_new(self):
        pg.mixer.music.load(self.filepath)
        print(f'Текущий трек: {self.name}')
        print(f'Введите 1 чтобы воспроизвести {self.name}')
    def add_to_queue(self):
        pg.mixer.music.queue(self.filepath)
        print(f'Трек {self.name} добавлен в очередь')
    def run1(self):
        global paused
        paused = False
        pg.mixer.music.play()
    def pause1(self):
        global paused
        paused = True
        pg.mixer.music.pause()
    def continue1(self):
        global paused
        paused = False
        pg.mixer.music.unpause()
class Playlist:
    def __init__(self, name):
        self.name = name
        self.tracks = []
        self.cur_tr = None
    def _play_cur(self):
        pg.mixer.music.load(self.tracks[self.cur_tr].filepath)
        pg.mixer.music.play()
    def add(self, track):
        self.tracks.append(track)
        if self.cur_tr == None: self.cur_tr = 0
    def delete(self, track):
        self.tracks.remove(track)
    def start(self):
        if len(self.tracks) > 0:
            self.cur_tr = 0
            self._play_cur()
    def cont(self):
        if len(self.tracks) > 0:
            self._play_cur()
    def next(self):
        self.cur_tr += 1
        self.cur_tr %= len(self.tracks)
        self._play_cur()
    def prev(self):
        self.cur_tr -= 1
        if self.cur_tr < 0: self.cur_tr = len(self.tracks)-1
        self._play_cur()
def end_chek():
    global cur_playlist
    global paused
    if pg.mixer.music.get_busy() == False and paused == False and cur_playlist != None:
        cur_playlist.next()
    root.after(500, end_chek)
def change(newVal):
    global cur_track
    if cur_track:
        pg.mixer.music.set_volume(float(newVal))
def open_trek():
    filepath = ctk.filedialog.askopenfilename()
    global cur_track
    cur_track = Track(filepath)
    cur_track.start_new()
    btn_play.configure(state='normal')
    btn_pause.configure(state='normal')
    btn_cont.configure(state='normal')
    scale.configure(state='normal')
    Hello_lbl.configure(text=f'Текущий трек: {cur_track.name}')
def play():
    global cur_track
    if cur_track:
        cur_track.run1()
def pause():
    global cur_track
    if cur_track:
        cur_track.pause1()
def cont():
    global cur_track
    if cur_track:
        cur_track.continue1()
playlists = {}
def make_playlist(name):
    global playlists
    pl = Playlist(name)
    playlists[name] = pl
    global cur_playlist
    cur_playlist = pl
    with open('playlists.json', 'w', encoding='utf-8') as f:
        json.dump(playlists, f, default=track_ser, ensure_ascii=False)
    pick_menu.configure(values=[name for name in playlists.keys()])
def add_to_pl(pl, song):
    global playlists
    if song not in playlists[pl].tracks:
        playlists[pl].add(song)

def dell(pl, song):
    global playlists
    if song in playlists[pl].tracks:
        playlists[pl].delete(song)
def track_ser(pl):
    a = []
    for i in pl.tracks:
        a.append(i.filepath)
    return {'name': pl.name, 'tracks': a}
def loadd():
    global playlists
    with open('playlists.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for n, t in data.items():
        playlists[n] = Playlist(n)
        for i in t['tracks']:
            curt = Track(i)
            playlists[n].add(curt)
def pl_maker():
    dialog = ctk.CTkInputDialog(text='Введите название плейлиста', title='Новый плейлист')
    name = dialog.get_input().strip()
    if len(name) > 0:
        make_playlist(name)
def pl_picker(choice):
    global cur_playlist
    global playlists
    cur_playlist = playlists[choice]
    plstart_btn.configure(text=f'Играть {cur_playlist.name} сначала')
    plstart_btn.configure(state='normal')
def pl_start():
    global cur_playlist
    if cur_playlist != None:
        cur_playlist.start()
if os.path.isfile('playlists.json'):
    loadd()
pg.init()
pg.mixer.init()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title('MusicPlayer')
root.geometry("1000x500")
btn = ctk.CTkButton(root,text='Выберите трек', command=open_trek)
Hello_lbl = ctk.CTkLabel(root, text=f'Загрузите трек')
Hello_lbl.pack()
btn.pack()
frame_btn = ctk.CTkFrame(root, fg_color="transparent")
frame_btn.pack(pady=40)
btn_play = ctk.CTkButton(frame_btn,text='Играть сначала',state = 'disabled', command=play)
btn_play.pack(side="left", padx=10)
btn_pause = ctk.CTkButton(frame_btn,text='Пауза',state = 'disabled', command=pause)
btn_pause.pack(side="left", padx=10)
btn_cont = ctk.CTkButton(frame_btn,text='Продолжить',state = 'disabled', command=cont)
btn_cont.pack(side="left", padx=10)
lbl2 = ctk.CTkLabel(frame_btn,state = 'disabled', text='Гомкость:')
lbl2.pack(side="left", padx=10)
scale = ctk.CTkSlider(frame_btn,state = 'disabled', width=100, from_=0, to=1, command=change)
scale.pack(side="left", padx=10)
frame_pl = ctk.CTkFrame(root, fg_color="transparent")
frame_pl.pack(pady=40)
makepl_btn = ctk.CTkButton(frame_pl, text='Создать плейлист', command=pl_maker)
makepl_btn.pack(side="left", padx=10)
pick_menu = ctk.CTkOptionMenu(frame_pl, values=[name for name in playlists.keys()], command=pl_picker)
pick_menu.set('Выберите плейлист')
pick_menu.pack(side="left", padx=10)
plstart_btn = ctk.CTkButton(frame_pl, text=f'Играть плейлист сначала',state = 'disabled', command=pl_start)
plstart_btn.pack(side="left", padx=10)
end_chek()
root.mainloop()