import time

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

from src import view
from src.filter import get_all_values

import os


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Program")
        self.setGeometry(100, 100, 550, 350)
        self.setFixedSize(550, 350)

        self.setStyleSheet("background-color:white;")

        self.titleLabel = QLabel("Data Analysis Software", self)
        self.titleLabel.setFont(QFont('Arial bold', 15))
        self.titleLabel.move(50, 30)
        self.titleLabel.resize(300, 30)

        self.waferLabel = QLabel("Wafer : ", self)
        self.waferLabel.setFont(QFont('Arial', 10))
        self.waferLabel.move(50, 100)
        self.waferLabel.resize(150, 20)

        self.coordinateLabel = QLabel("Coordinates : ", self)
        self.coordinateLabel.setFont(QFont('Arial', 10))
        self.coordinateLabel.move(50, 150)
        self.coordinateLabel.resize(150, 20)

        self.deviceLabel = QLabel("Device ID : ", self)
        self.deviceLabel.setFont(QFont('Arial', 10))
        self.deviceLabel.move(50, 200)
        self.deviceLabel.resize(150, 20)

        self.waferEdit = QLineEdit('', self)
        self.waferEdit.setStyleSheet("border-radius:5px;border: 1px solid black;text-align: center")
        self.waferEdit.move(170, 100)
        self.waferEdit.resize(100, 20)

        self.coordinateEdit = QLineEdit('', self)
        self.coordinateEdit.setStyleSheet("border-radius:5px;border: 1px solid black;text-align: center")
        self.coordinateEdit.move(170, 150)
        self.coordinateEdit.resize(100, 20)

        self.deviceEdit = QLineEdit('', self)
        self.deviceEdit.setStyleSheet("border-radius:5px;border: 1px solid black;text-align: center")
        self.deviceEdit.move(170, 200)
        self.deviceEdit.resize(100, 20)

        self.showEdit = QCheckBox("Show Output", self)
        self.showEdit.move(350, 90)
        self.showEdit.resize(200, 20)

        self.saveEdit = QCheckBox("Save Output", self)
        self.saveEdit.move(350, 140)
        self.saveEdit.resize(200, 20)

        string = "background-color: grey;border: none;color: white;text-align: " \
                 "center;text-decoration: none;display: inline-block;font-size: 10px;margin: 4px 2px;cursor: pointer; "

        self.processBtn = QPushButton("OK", self)
        self.processBtn.setStyleSheet(string)
        self.processBtn.resize(130, 30)
        self.processBtn.move(380, 290)
        self.processBtn.clicked.connect(self.btn_click)

        self.folderBtn = QPushButton("Results folder", self)
        self.folderBtn.setStyleSheet(string)
        self.folderBtn.resize(130, 30)
        self.folderBtn.move(220, 290)
        self.folderBtn.clicked.connect(self.open_folder)

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btn_click(self):
        wafer = self.waferEdit.text()
        coordinates = self.coordinateEdit.text()
        device = self.deviceEdit.text()

        values = get_all_values()
        try:
            if wafer != '' and not all(elem in values[0] for elem in list(map(str, wafer.split()))):
                QMessageBox.information(self, 'Message', str('Wafer ID doesnt exist!'))
            elif coordinates != 'all' and not all(elem in values[1] for elem in list(map(str, coordinates.split()))):
                QMessageBox.information(self, 'Message', str('Coordinates doesnt exist!'))
            elif device != '' and not any(device in s for s in values[2]):
                QMessageBox.information(self, 'Message', str('Device ID doesnt exist!'))
            else:
                start = time.time()
                view.initMainView(wafer, coordinates, device, self.saveEdit.isChecked(), self.showEdit.isChecked())
                print("time :", time.time() - start)
        except ValueError as e:
            QMessageBox.information(self, 'Error', str(e))

    def open_folder(self):
        path = "res"
        path = os.path.realpath(path)
        os.startfile(path)
