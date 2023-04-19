import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSignal
from PyQt6 import QtCore
from gui import Ui_MainWindow
import numpy as np
import cv2 as cv
import pyautogui
pyautogui.FAILSAFE = False
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        
        self.thread = {}
        self.uic.pushButton.clicked.connect(self.acvite)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key.Key_F1.value:
            self.acvite()

    def acvite(self):
        status = self.uic.pushButton.text()
        if(status == "ACCEPT: OFF"):
            self.uic.pushButton.setStyleSheet('background-color: green;border-style:outset;border-width: 2px;\
                                        color: white;border-radius: 15px;font: bold 14px')
            self.uic.pushButton.setText("ACCEPT: ON")
            self.thread[1]  = ThreadClass(index=1)
            self.thread[1].start()      
        else:
            self.uic.pushButton.setStyleSheet('background-color: red;border-style:outset;border-width: 2px;\
                                        color: white;border-radius: 15px;font: bold 14px')
            self.uic.pushButton.setText("ACCEPT: OFF")
            self.thread[1].stop()
class ThreadClass(QtCore.QThread):
    signal = pyqtSignal(object)

    def __init__(self, index=0):
        super().__init__()
        self.index = index

    def run(self):
        while(True):
            try:
                image = pyautogui.screenshot()
                image = cv.cvtColor(np.array(image),cv.COLOR_RGB2GRAY)
            except IOError:
                time.sleep(1)
                pass
            blurred = cv.medianBlur(image, 5)
            circles = cv.HoughCircles(blurred, cv.HOUGH_GRADIENT, 1, 1000, param1=200, 
                            param2=100, minRadius=250, maxRadius=300)

            if circles is not None and len(circles == 1):
                circles = np.uint16(np.around(circles))
                x = circles[0,0][0]
                y = circles[0,0][1] + circles[0,0][2] - 20
                pyautogui.click(x, y)
                time.sleep(2)
            else:
                time.sleep(2)

    def stop(self):
        self.terminate()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())


