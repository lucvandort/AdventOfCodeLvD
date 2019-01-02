import sys
import numpy as np
import pyqtgraph as pg

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    print(args)


sys.excepthook = trap_exc_during_debug


class Day10App(QMainWindow):

    def __init__(self):
        super(Day10App, self).__init__()
        uic.loadUi('Day10.ui', self)
        self.show()

        self.filename = None

        self.TimeSlider.valueChanged.connect(
            self.time_slider_changed
        )
        self.TimeSliderMin.valueChanged.connect(
            self.timeslider_min_changed
        )
        self.TimeSliderMax.valueChanged.connect(
            self.timeslider_max_changed
        )
        self.TimeValue.valueChanged.connect(
            self.time_changed
        )
        self.actionLoad_inputfile.triggered.connect(
            self.load_inputfile
        )

    def timeslider_min_changed(self):
        self.TimeSlider.setMinimum(self.TimeSliderMin.value())

    def timeslider_max_changed(self):
        self.TimeSlider.setMaximum(self.TimeSliderMax.value())

    def time_changed(self):
        self.TimeSlider.setValue(self.TimeValue.value())

    def time_slider_changed(self):
        self.TimeValue.setValue(self.TimeSlider.value())

    def load_inputfile(self):
        self.filename = QFileDialog.getOpenFileName(self, 'Select inputfile')[0]
        self.statusbar.showMessage(self.filename)
        self.prepare_plot_from_inputfile()

    def prepare_plot_from_inputfile(self):
        pass

    def update_plot(self):
        pass

    

def main():
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    window = Day10App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
