from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from time import sleep
import sys, os

class MyCustomWidget(QWidget):

    def __init__(self, parent=None):
        super(MyCustomWidget, self).__init__(parent)
        layout = QVBoxLayout(self)

        # Create a progress bar and a button and add them to the main layout
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0,1)
        layout.addWidget(self.progressBar)
        button = QPushButton("Start", self)
        layout.addWidget(button)

        button.clicked.connect(self.onStart)

        self.myLongTask = TaskThread()
        self.myLongTask.taskFinished.connect(self.onFinished)

    def onStart(self):
        self.progressBar.setRange(0,0)
        self.myLongTask.start()

    def onFinished(self):
        # Stop the pulsation
        self.progressBar.setRange(0,1)
        self.progressBar.setValue(1)


class TaskThread(QThread):
    taskFinished = pyqtSignal()
    def run(self):
        os.system('sudo apt-get install leafpad')
        self.taskFinished.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyCustomWidget()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())