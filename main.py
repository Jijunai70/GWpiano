import os
import re
import time
import json
from abc import abstractmethod
from queue import Queue


def adb_connect():
    os.system("adb connect localhost:16384")


def click_multiple_spots(coordinates):
    if len(coordinates) == 0:
        return
    command = " & ".join([f"adb -s localhost:16384 shell input tap {x} {y}" for x, y in coordinates])
    # print(command)
    os.system(command)


class MyQueue(Queue):
    def peek(self):
        if not self.empty():
            return self.queue[0]
        else:
            return None


class MusicPlayerBase:
    def __init__(self):
        self.keyMap = [
            (640, 100),
            (771, 100),
            (902, 100),
            (1033, 100),
            (1164, 100),
            (640, 222),
            (771, 222),
            (902, 222),
            (1033, 222),
            (1164, 222),
            (640, 344),
            (771, 344),
            (902, 344),
            (1033, 344),
            (1164, 344),
        ]

    @abstractmethod
    def loadMusic(self, file_path):
        pass

    @abstractmethod
    def play(self):
        pass


class MyMusicPlayer(MusicPlayerBase):
    def __init__(self):
        super().__init__()
        self.beat_interval = 0.15
        self.music = []

    def loadMusic(self, file_path):
        self.music = []
        try:
            with open(file_path, 'r') as file:
                size = 0
                music_size = 0
                for line in file:
                    line_without_spaces = line.replace(' ', '').strip()
                    if len(line_without_spaces) == 0:
                        continue
                    if line_without_spaces.find('/') != -1:
                        continue

                    beat = []
                    i = 0
                    for c in line_without_spaces:
                        if c == '1':
                            beat.append(self.keyMap[i])
                        i += 1
                    self.music.append(beat)
                    size += 1
                    len_bit = len(beat)
                    if len(beat) > 0:
                        music_size = size
        except Exception as e:
            print(f"{e}")
        self.music = self.music[:music_size]

    def play(self):
        for beat in self.music:
            click_multiple_spots(beat)
            time.sleep(self.beat_interval)


class MusicPlayer(MusicPlayerBase):
    def __init__(self):
        super().__init__()
        self.music = MyQueue()
        self.bpm = None
        self.author = None
        self.name = None
        self.time = None

    def loadMusic(self, file_path):
        while not self.music.empty():
            self.music.get()

        try:
            with open(file_path, 'r', encoding='utf-16') as file:
                data = json.load(file)

                for item in data:
                    self.name = item['name']
                    self.author = item['author']
                    self.bpm = item['bpm']
                    songNotes = item['songNotes']

                for note in songNotes:
                    match = re.search(r'\d+$', note['key'])
                    note['key'] = int(match.group())
                    note['time'] = int(note['time'])
                    # note['time'] = int(note['time']) * 0.8
                    self.time = note['time'] / 1000

                    self.music.put(note)
                    # print(note)

        except Exception as e:
            print(f"{e}")

    def printMsg(self):
        print(f"Name: {self.name}")
        print(f"Author: {self.author}")
        print(f"BPM: {self.bpm}")
        print(f"Time: {self.time}秒")

    def play(self):
        begin_time = time.time() * 1000
        while not self.music.empty():
            now = time.time() * 1000 - begin_time
            if self.music.peek()['time'] > now:
                wait_time = (self.music.peek()['time'] - now) / 1000
                time.sleep(wait_time)

            coordinates = []
            while not self.music.empty():
                now = time.time() * 1000 - begin_time
                if self.music.peek()['time'] > now:
                    break
                key_map_index = self.music.get()['key']
                coordinates.append(self.keyMap[key_map_index])
            click_multiple_spots(coordinates)


def getSongs(folder_path="./songs/"):
    songs = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            songs.append(file_name)
    return songs


if __name__ == "__main__":
    # music_player = MyMusicPlayer()
    # music_player.loadMusic("./有形的翅膀.txt")

    music_player = MusicPlayer()

    folder_path = "./songs/"
    songs = getSongs()
    for song in songs:
        print(song)

    # music_player.loadMusic("./songs/打上花火.txt")
    # music_player.loadMusic("./songs/蒲公英的约定.txt")
    # music_player.loadMusic("./songs/小星星.txt")
    # music_player.loadMusic("./songs/Canon in C.txt")
    # music_player.loadMusic("./songs/赤伶.txt")
    # music_player.loadMusic("./songs/起风了.txt")
    # music_player.loadMusic("./songs/康康舞曲.txt")
    music_player.loadMusic("./songs/千本樱.txt")
    music_player.printMsg()
    music_player.play()
