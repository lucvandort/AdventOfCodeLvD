import sys
import numpy as np
import pandas as pd
import pyqtgraph as pg

from PyQt5 import uic
from PyQt5.QtCore import QPointF
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
        self.TimeSlider.valueChanged.disconnect(
            self.time_slider_changed
        )
        self.TimeSlider.setValue(self.TimeValue.value())
        self.TimeSlider.valueChanged.connect(
            self.time_slider_changed
        )
        self.update_star_locations()

    def time_slider_changed(self):
        self.TimeValue.valueChanged.disconnect(
            self.time_changed
        )
        self.TimeValue.setValue(self.TimeSlider.value())
        self.TimeValue.valueChanged.connect(
            self.time_changed
        )
        self.update_star_locations()

    def load_inputfile(self):
        self.inputfile = QFileDialog.getOpenFileName(
            self,
            'Select inputfile',
            )[0]
        self.statusbar.showMessage(self.inputfile)
        self.prepare_plot_from_inputfile()

    def prepare_plot_from_inputfile(self):
        pattern = \
            r"^position=<[ ]*([-0-9]*),[ ]*([-0-9]*)> " \
            r"velocity=<[ ]*([-0-9]*),[ ]*([-0-9]*)>$"
        self.inputdata = pd.read_csv(
            self.inputfile,
            sep=pattern,
            header=None,
            usecols=[1, 2, 3, 4, ],
            names=[
                'X',
                'Y',
                'dX',
                'dY',
            ],
            engine='python',
            dtype=int,
        )

        self.starSky.clear()
        self.starSky.invertY(True)

        for star in self.inputdata.itertuples():
            pos = QPointF(
                getattr(star, 'X'),
                getattr(star, 'Y')
            )
            angle = np.degrees(np.arctan(
                getattr(star, 'dY') /
                getattr(star, 'dX')
            ))

            line = self.starSky.addLine(
                pen=pg.mkPen(0.2, width=1)
            )
            line.setValue(pos)
            line.setAngle(angle)

        self.stars = self.starSky.plot(
            pen=None,
            symbol='o',
            symbolBrush='y',
        )
        self.update_star_locations()

    def update_star_locations(self):
        self.stars.clear()

        T = self.TimeValue.value()
        Xcoords = self.inputdata.loc[:, 'X'] + self.inputdata.loc[:, 'dX'] * T
        Ycoords = self.inputdata.loc[:, 'Y'] + self.inputdata.loc[:, 'dY'] * T

        self.stars.setData(x=Xcoords, y=Ycoords)


def main():
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    window = Day10App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
