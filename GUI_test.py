# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:46:15 2019

@author: Mars
"""
import os, sys, base64, io
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtWidgets import (QApplication, 
                            QMainWindow, 
                            QVBoxLayout, 
                            QFileDialog)
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import cv2
import numpy as np
import requests
import json
import config

from encodedUi import Ui_MainWindow

from pylonCameraView import singleCapture, liveView

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.readImgButton.clicked.connect(self.readImage)
        self.analyzeImgButton.clicked.connect(self.analyzeImage)
        self.saveImgButton.clicked.connect(self.saveImage)
        self.liveStreamButton.clicked.connect(self.liveStream)
        self.plotting_widget.setLayout(QVBoxLayout())
            
        self.plotting_matplotlib_canvas = FigureCanvas(figure=Figure())
        self.plotting_widget.layout().addWidget(
                NavigationToolbar(self.plotting_matplotlib_canvas, self))
            
        self.plotting_widget.layout().addWidget(
                self.plotting_matplotlib_canvas)
        self.plot_ax = self.plotting_matplotlib_canvas.figure.subplots()
        self.plot_ax.axis('off')
    
    def liveStream(self):
        liveView(16, 1e4, 4, "Mono12p")

    def readImage(self):
        self.image = singleCapture(12, 1e4, 4, "Mono12p")
        self.plot_ax.clear()
        self.plot_ax.imshow(self.image, cmap='gray')
        self.plot_ax.axis('off')
        self.plot_ax.figure.canvas.draw()
        self.bottomDialogBox.setText(QtWidgets.QApplication.translate("", "image captued", None, -1))
    
    def analyzeImage(self):
        with open(self.filePath, "rb") as image_file:
            b64_imageBytes = base64.b64encode(image_file.read())
        b64_imgString = str(b64_imageBytes, encoding='utf-8')
        URL = "http://127.0.0.1:5000/imageUpload"
        #URL = "http://vcm-9184.vm.duke.edu:5000/imageUpload"
        payload = {"client" : "GUI-test",
                   "image" : b64_imgString,
                   "user": self.user,
                   "img_grp": self.img_grp,
                   "batch": self.batch,
                   "filename": self.filePath.split('/')[-1]}
        response = requests.post(URL, json=payload)
  #     image_rgb = decodeImage(response.json()['ver_Img'], color = True)
        self.plot_ax.clear()
        self.plot_ax.imshow(image_rgb, interpolation='nearest')
        self.plot_ax.axis('off')
        self.plot_ax.figure.canvas.draw()
        self.serverResponse.setText(QtWidgets.QApplication.translate("", "results: " + str(response.json()['intensities']) + "\n" + 
                                                                                           " background: " + str(response.json()['background']), None, -1))
    def saveImage(self):
        fileName = self.lineEdit.text()
        fileName = fileName + ".tiff"
        cv2.imwrite(fileName, self.image)
        self.bottomDialogBox.setText(QtWidgets.QApplication.translate("", fileName + " has been saved", None, -1))
    
        
def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    app.setWindowIcon(QtGui.QIcon(config.ICON))
    app.setApplicationName(config.TITLE)
    frame = MainWindow()
    frame.setWindowTitle(config.TITLE)
    frame.show()
    app.exec_()
    app.quit()

if __name__ == '__main__':
    main()
