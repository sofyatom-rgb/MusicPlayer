import os
import pygame as pg
import time
class Track:
    def __init__(self, name):
        self.name = name
        self.liked = False
    def like(self):
        Track.liked = not(Track.liked)
    def start_new(self):
        pg.mixer.music.load(self.name)
        print(f'Текущий трек: {self.name}')
        print(f'Введите 1 чтобы воспроизвести {self.name}')
    def add_to_queue(self):
        pg.mixer.music.queue(self.name)
        print(f'Трек {self.name} добавлен в очередь')
    def run1(self):
        pg.mixer.music.play()
        print('ВВедите 0 чтобы поставить на паузу')
    def pause1(self):
        pg.mixer.music.pause()
        print('Трек на паузе, введите 2 чтобы возобновить его')
    def continue1(self):
        pg.mixer.music.unpause()


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
screen = pg.display.set_mode((400, 300))
pg.display.set_caption("Мой плеер")
print('Введите load чтобы загрузить новый трек, а затем его название')
print('Введите add чтобы добавить в очередь новый трек, а затем его название')
MUSIC_END = pg.event.custom_type()
pg.mixer.music.set_endevent(MUSIC_END)
cur_track = Track('-1')
next_track = Track('-1')
while True:
    command = input().strip().lower()
    for event in pg.event.get():
        if event.type == MUSIC_END:
            cur_track = next_track
            next_track = 0
    if command == 'load':
        name = input().strip()
        sound = Track(name)
        sound.start_new()
        cur_track = sound
    elif command == 'add':
        name = input().strip()
        sound = Track(name)
        sound.add_to_queue()
        nex_track = sound
    elif command == '1':
        if cur_track.name == '-1':
            print('Сначала нужно загрузить трек')
        else:
            cur_track.run1()
    elif command == '0':
        cur_track.pause1()
        print(f'{cur_track.name} на паузе')
    elif command == '2':
        cur_track.continue1()
#Riptide - Vance Joy.mp3
