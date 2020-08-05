from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType
import os
import urllib.request
import pafy
from os import path
import youtube_dl
import humanize

ui, _ = loadUiType('main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handel_Buttons()

    def InitUI(self):
        # contains all ui changes in loading
        self.tabWidget.tabBar().setVisible(False)
        # self.Move_Box1()

    def Handel_Buttons(self):
        # handel all buttons in the app
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handel_Browse)

        self.pushButton_7.clicked.connect(self.Get_Video_Data)
        self.pushButton_6.clicked.connect(self.Download_Video)
        self.pushButton_5.clicked.connect(self.Save_Browse)

        self.pushButton_15.clicked.connect(self.Get_Audio_Data)
        self.pushButton_16.clicked.connect(self.Download_Audio)
        self.pushButton_17.clicked.connect(self.Save_Audio)

        self.pushButton_26.clicked.connect(self.Get_Playlist_Data)
        self.pushButton_8.clicked.connect(self.Playlist_Download)
        self.pushButton_9.clicked.connect(self.Save_Playlist)

        self.pushButton_3.clicked.connect(self.Open_Home)
        self.pushButton_11.clicked.connect(self.Open_Download)
        self.pushButton_10.clicked.connect(self.Open_Youtube)
        self.pushButton_4.clicked.connect(self.Open_Settings)

        self.pushButton_12.clicked.connect(self.Apply_Original)
        self.pushButton_13.clicked.connect(self.Apply_DarkOrange)
        self.pushButton_14.clicked.connect(self.Apply_MaterialDark)

    def Handel_Progress(self, blocknum, blocksize, totalsize):
        # calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = (readed_data * 100) / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def Handel_Browse(self):
        # enable browsing to our system, & pick save location
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        print(save_location)
        self.lineEdit_2.setText(str(save_location[0]))

    def Download(self):
        # Download file
        print('Started Downloading')
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL")
        elif save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid save Location")
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.Handel_Progress)
            except Exception:
                QMessageBox.warning(self, "Download Error", "Provide a valid URL or save Location")
                return

            self.progressBar.setValue(100)
            QMessageBox.information(self, "Download Completed", "Download Completed Successfully")
            self.lineEdit.text('')
            self.lineEdit_2.text('')
            self.progressBar.setValue(0)

    ############# Download Single Youtube Video #################

    def Save_Browse(self):
        # save location in the line edit
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_7.setText(str(save_location[0]))

    def Get_Video_Data(self):
        video_url = self.lineEdit_3.text()

        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL")
        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)

            video_streams = video.streams
            for stream in video_streams:
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {}  ({})".format(stream.mediatype, stream.extension, stream.quality, size)
                self.comboBox.addItem(data)

    def Download_Video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_7.text()

        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL")
        elif save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid save Location")
        else:
            video = pafy.new(video_url)
            video_stream = video.streams
            video_quality = self.comboBox.currentIndex()
            video_stream[video_quality].download(filepath=save_location, callback=self.Video_progress)
            QMessageBox.information(self, "Download Completed", "Download Completed Successfully")
            self.progressBar_3.setValue(0)

    def Video_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            #download_percentage = read_data * 100 / total
            self.progressBar_3.setValue(ratio*100)
            remaining_time = round(time/60, 2)

            self.label_5.setText(str('{} min remaining').format(remaining_time))

    ############# Download Audio Only From Videos  #################

    def Save_Audio(self):
        # save location in the line edit
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_10.setText(str(save_location[0]))

    def Get_Audio_Data(self):
        video_url = self.lineEdit_4.text()

        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL")
        else:
            video = pafy.new(video_url)

            audio_streams = video.audiostreams
            for stream in audio_streams:
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {}  ({})".format(stream.mediatype, stream.extension, stream.quality, size)
                self.comboBox_3.addItem(data)

    def Download_Audio(self):
        video_url = self.lineEdit_4.text()
        save_location = self.lineEdit_10.text()

        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL")
        elif save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid save Location")
        else:
            video = pafy.new(video_url)
            audio_stream = video.audiostreams
            audio_quality = self.comboBox_3.currentIndex()
            audio_stream[audio_quality].download(filepath=save_location, callback=self.Audio_progress)
            QMessageBox.information(self, "Download Completed", "Download Completed Successfully")
            self.progressBar_5.setValue(0)

    def Audio_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            # download_percentage = read_data * 100 / total
            self.progressBar_5.setValue(ratio * 100)
            remaining_time = round(time / 60, 2)

            self.label_17.setText(str('{} min remaining').format(remaining_time))

    ##################### Youtube Playlist Download ############################

    def Get_Playlist_Data(self):
        Playlist_url = self.lineEdit_8.text()

        if Playlist_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL")
        else:
            playlist = pafy.get_playlist(Playlist_url)
            playlist_videos = playlist['items']
            video = playlist_videos[0]
            first_video = video['pafy']

            video_streams = first_video.streams
            for stream in video_streams:
                data = "{}  [{}]".format(stream.extension, stream.quality)
                self.comboBox_2.addItem(data)

    def Playlist_Download(self):
        playlist_url = self.lineEdit_8.text()
        save_location = self.lineEdit_9.text()

        if playlist_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid PlayList URL")
        elif save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid save Location")
        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))

        print(playlist['title'])
        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.comboBox_2.currentIndex()

        for video in playlist_videos:
            self.lcdNumber.display(current_video_in_download)
            current_video = video['pafy']
            current_video_stream = current_video.streams
            print(current_video_stream)
            download = current_video_stream[quality].download(callback=self.Playlist_Progress)
            QApplication.processEvents()
            current_video_in_download +=1
        QMessageBox.information(self, "Download Completed", "Download Completed Successfully")
        self.progressBar_4.setValue(0)
        self.lcdNumber.display(0)
        self.lcdNumber_2.display(0)

    def Playlist_Progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            #download_percentage = read_data * 100 / total
            self.progressBar_4.setValue(ratio * 100)
            remaining_time = round(time / 60, 2)

            self.label_6.setText(str('{} min remaining').format(remaining_time))
            QApplication.processEvents()

    def Save_Playlist(self):
        # save location in the line edit
        save_location = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_9.setText(str(save_location))


######################### UI Changes ###########################################
    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Youtube(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(3)

######################### App Themes ##########################

    def Apply_Original(self):
        style = open("Theme/Original.css", 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_DarkOrange(self):
        self.Apply_Original()
        style = open("Theme/Dark_Orange.css", 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Apply_MaterialDark(self):
        self.Apply_Original()
        style = open("Theme/Materialdark.css", 'r')
        style = style.read()
        self.setStyleSheet(style)


    ################ App Animation ######################

    '''
    def Move_Box1(self):
        box_animation = QPropertyAnimation(self.groupBox, b"geometry")
        box_animation.setDuration(1000)
        box_animation.setStartValue(QRect(0,0,0,0))
        box_animation.setEndValue(QRect(70,80,201,111))
        box_animation.start()
        self.box_animation = box_animation
    '''


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "2"  # to make app size constant in different screen sizes
    main()
