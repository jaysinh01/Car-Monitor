# Makes sure your sound card is enabled before executing the script
# For Ubuntu running in VMware:
#   In task-bar:
#       VM --> Settings --> Add --> Sound Card
# -*- coding: utf-8 -*-
import os
import pickle


class musicLib:
    '''
    Creates & modifies the playlist for a given music library
    '''

    def __init__(self):
        # The playlist would be stored in self.playlist
        self.playlist = []

    def getInfo(self, fileName):
        # Reads the pickled info from a given file 'fileName'
        with open(fileName, 'rb') as infoStream:
            targetInfo = pickle.load(infoStream)
        return targetInfo

    def writeInfo(self, targetInfo, fileName):
        # Pickles the info 'targetInfo' into a given file 'fileName'
        with open(fileName, 'wb') as infoStream:
            pickle.dump(targetInfo, infoStream)

    def creatPlaylist(self):
        # Code varied from:
        # https://www.blog.pythonlibrary.org/2013/10/29/python-101-how-to-find-the-path-of-a-running-script/
        # Gets the absolute path of the running scrip
        script_path = os.path.dirname(os.path.abspath(__file__))
        # Songs are stored in 'static' folder under the script directory
        musicLib_path = script_path + '/static'
        # Lists all the files in the musicLib_path directory
        self.playlist = os.listdir(musicLib_path)
        self.playlist.sort()
        # If the list is empty
        if len(self.playlist) == 0:
            self.playlist.append("Empty list...")
        # Pickles the list into file 'playlistStream'
        self.writeInfo(self.playlist, 'playlistStream')

    def shiftList(self, index):
        # Shifts songs left by 'index' in the playlist
        newPlayList = self.playlist[index:len(self.playlist)]
        newPlayList += self.playlist[0:index]
        # Pickles the new list into the file 'playlistStream'
        self.writeInfo(newPlayList, 'playlistStream')
        self.playlist = newPlayList

    def writeFreqDict(self, song):
        # Records the number of times a song has been played
        # into dictionary 'freqDict'
        try:
            # Gets freqDict from file 'freqDictStream'
            freqDict = self.getInfo('freqDictStream')
        # If freqDict DNE, initializes it
        except FileNotFoundError:
            freqDict = {}.fromkeys(self.playlist, 0)
        try:
            # self.writeFreqDict(song) would be called
            # after 'song' is played
            freqDict[song] += 1
        except KeyError:
            # If 'song' hasn't been record
            freqDict[song] = 1
        # Pickles the list into file 'playlistStream'
        self.writeInfo(freqDict, 'freqDictStream')

    def freqList(self):
        # Sorts songs by their frequency
        try:
            # Gets freqDict from file 'freqDictStream'
            freqDict = self.getInfo('freqDictStream')
        except FileNotFoundError:
            # If freqDict DNE, initializes it
            freqDict = {}.fromkeys(self.playlist, 0)
            self.writeInfo(freqDict, 'freqDictStream')
        # Sorts items in freqDict by their value
        tempList = [[value, key] for key, value in freqDict.items()]
        tempList.sort(reverse=True)
        # Gets items' key
        freqList = [tempList[i][1] for i in range(0, len(tempList))]
        # Finds the intersection of freqList & playlist
        # Some songs may be removed from the folder currently
        # but their record would be saved
        newFreqList = [i for i in freqList if i in self.playlist]
        # # Pickles the list into file 'playlistStream'
        self.writeInfo(newFreqList, 'playlistStream')
        self.playlist = newFreqList
