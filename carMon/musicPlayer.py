# Makes sure your sound card is enabled before executing the script
# For Ubuntu running in VMware:
#   In task-bar:
#       VM --> Settings --> Add --> Sound Card

# -*- coding: utf-8 -*-
import os
import pickle


class musicLib:

    def __init__(self):
        self.playlist = []

    def getInfo(self, fileName):
        with open(fileName, 'rb') as infoStream:
            targetInfo = pickle.load(infoStream)
        return targetInfo

    def writeInfo(self, targetInfo, fileName):
        with open(fileName, 'wb') as infoStream:
            pickle.dump(targetInfo, infoStream)

    def creatPlaylist(self):
        # https://www.blog.pythonlibrary.org/2013/10/29/python-101-how-to-find-the-path-of-a-running-script/
        # Finds the path of the running scrip
        script_path = os.path.dirname(os.path.abspath(__file__))
        musicLib_path = script_path + '/static'
        # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
        self.playlist = os.listdir(musicLib_path)
        self.playlist.sort()
        if len(self.playlist) == 0:
            self.playlist.append("Empty list...")
        self.writeInfo(self.playlist, 'playlistStream')

    def shiftList(self, index):
        newPlayList = self.playlist[index:len(self.playlist)]
        newPlayList += self.playlist[0:index]
        self.writeInfo(newPlayList, 'playlistStream')
        self.playlist = newPlayList

    def writeFreqDict(self, song):
        try:
            freqDict = self.getInfo('freqDictStream')
        except FileNotFoundError:
            freqDict = {}.fromkeys(self.playlist, 0)
        try:
            freqDict[song] += 1
        except KeyError:
            freqDict[song] = 1
        self.writeInfo(freqDict, 'freqDictStream')

    def freqList(self):
        try:
            freqDict = self.getInfo('freqDictStream')
        except FileNotFoundError:
            freqDict = {}.fromkeys(self.playlist, 0)
            self.writeInfo(freqDict, 'freqDictStream')
        tempList = [[value, key] for key, value in freqDict.items()]
        tempList.sort(reverse=True)
        freqList = [tempList[i][1] for i in range(0, len(tempList))]
        # Finds the intersection of freqList & playlist
        newFreqList = [i for i in freqList if i in self.playlist]
        self.writeInfo(newFreqList, 'playlistStream')
        self.playlist = newFreqList
