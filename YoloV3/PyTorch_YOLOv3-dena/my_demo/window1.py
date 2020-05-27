import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyLabel( QLabel ) :
    def __init__(self, *args , **kwargs ) :
        super().__init__( *args )
        self.setMinimumSize( 300 , 300 )
        self.setAcceptDrops( True )
        self.drop_callback = kwargs.get( "drop_callback" , None )
        self.qpixmap = kwargs.get( "qpixmap" , None )

        if { "width" , "height" } & kwargs.keys() :
            self.resize(
                kwargs["width"] , kwargs["height"]
            )

        # if self.qpixmap :
        #     self.setPixmap( self.qpixmap.scaled( self.width() , self.height() )  )

    @property
    def qpixmap(self) :
        return self._qpixmap

    @qpixmap.setter
    def qpixmap(self , img ) :
        self._qpixmap = img
        self.setPixmap(self._qpixmap.scaled(self.width(), self.height()))

    def dragEnterEvent(self, e):
        m = e.mimeData()
        if m.hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        m = e.mimeData()
        if m.hasUrls():
            self.url = m.urls()[0].toLocalFile()
            self.qpixmap = QPixmap( self.url )
            self.setPixmap(
                self.qpixmap.scaled(
                    self.width() , self.height() ,Qt.KeepAspectRatio
                )
            )

            if self.drop_callback :
                self.drop_callback( self.url )

    def resizeEvent(self, *args, **kwargs):

        if self.qpixmap :
            self.setPixmap(
                self.qpixmap.scaled(
                    self.width() , self.height()  , Qt.KeepAspectRatio  )
            )

from demo import main as demo_main

class Worker(QRunnable ) :

    class Signals(QObject) :
        start = pyqtSignal()
        data = pyqtSignal( object )

    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.setAutoDelete( False )
        self.image_path = None
        self.signals = Worker.Signals()

    @pyqtSlot()
    def run(self) :
        self.signals.start.emit()
        img = None
        if self.image_path :
            img = demo_main(
                self.image_path,
                # weights_path= "../weights/yolov3.weights",
                background=True
            )
        self.signals.data.emit( img )

class QMovieLabel(QLabel):
    def __init__(self, fileName, parent=None):
        super(QMovieLabel, self).__init__(parent)
        m = QMovie(fileName)
        self.setMovie(m)
        m.start()

    def setMovie(self, movie):
        super(QMovieLabel, self).setMovie(movie)
        s=movie.currentImage().size()
        self._movieWidth = s.width()
        self._movieHeight = s.height()

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.init_threading()
        self.initUI2()

    def init_threading(self) :
        self.threadpool = QThreadPool()
        self.worker = Worker()

        self.worker.signals.start.connect( self.show_loading )
        self.worker.signals.data.connect( self.display_data )


    def display_data(self , img_path ) :
        if img_path:
            self.mylabel.qpixmap = QPixmap( img_path )

        self.hide_loading()

    def show_loading(self):
        # self.loading_gif.adjustSize()
        # self.loading_gif.show()
        pass

    def hide_loading(self):
        # self.loading_gif.hide()
        pass

    def initUI2(self) :
        self.setWindowTitle('Simple drag & drop')
        self.setGeometry(300, 300, 300, 300)

        def make_prediction( image_path ) :
            # img = demo_main(
            #     image_path , weights_path= "../weights/yolov3.weights" ,
            #     background = True
            # )
            #
            # if img :
            #     self.mylabel.qpixmap = img
            self.worker.image_path = image_path
            self.threadpool.start( self.worker )

            pass


        self.mylabel = MyLabel(
            self,
            qpixmap= QPixmap( "./image_asset/drop_here_600x600.jpg" ) ,
            drop_callback= make_prediction ,
            width= self.width(),
            height= self.height()
        )

        # self.loading_gif = QMovieLabel( "image_asset/loading.gif" , self )


    def resizeEvent(self, *args, **kwargs):
        if self.mylabel:
            self.mylabel.resize(self.width(), self.height() )



if __name__ == '__main__':
    try :
        app = QApplication(sys.argv)
        ex = Example()
        ex.show()
        app.exec_()
    except :
        os.system("pause")