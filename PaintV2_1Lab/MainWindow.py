# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QLabel


class Ui_MainWindow(object):
    def connectSignals(self):
        self.action.triggered.connect(self.openImage)

    def openImage(self):
        filePath, _ = QFileDialog.getOpenFileName(self.centralwidget, "Open Image", "",
                                                  "Images (*.png *.bmp *.jpg *.jpeg *.tiff)")
        if filePath:
            pixmap = QPixmap(filePath)
            self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.imageLabel = QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(10, 10, 780, 540))
        self.imageLabel.setObjectName("imageLabel")
        self.imageLabel.setScaledContents(True)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 37))
        self.menubar.setObjectName("menubar")
        self.menuLoad_Image = QtWidgets.QMenu(parent=self.menubar)
        self.menuLoad_Image.setObjectName("menuLoad_Image")
        self.menu = QtWidgets.QMenu(parent=self.menubar)
        self.menu.setObjectName("menu")
        self.menu_3 = QtWidgets.QMenu(parent=self.menu)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(parent=self.menu)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(parent=self.menu)
        self.menu_5.setObjectName("menu_5")
        self.menu_2 = QtWidgets.QMenu(parent=self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_6 = QtWidgets.QMenu(parent=self.menu_2)
        self.menu_6.setObjectName("menu_6")
        self.menu_7 = QtWidgets.QMenu(parent=self.menubar)
        self.menu_7.setObjectName("menu_7")
        MainWindow.setMenuBar(self.menubar)
        self.action = QtGui.QAction(parent=MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtGui.QAction(parent=MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtGui.QAction(parent=MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtGui.QAction(parent=MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtGui.QAction(parent=MainWindow)
        self.action_5.setObjectName("action_5")
        self.action_6 = QtGui.QAction(parent=MainWindow)
        self.action_6.setObjectName("action_6")
        self.action_7 = QtGui.QAction(parent=MainWindow)
        self.action_7.setObjectName("action_7")
        self.action_10 = QtGui.QAction(parent=MainWindow)
        self.action_10.setObjectName("action_10")
        self.action_11 = QtGui.QAction(parent=MainWindow)
        self.action_11.setObjectName("action_11")
        self.action_12 = QtGui.QAction(parent=MainWindow)
        self.action_12.setObjectName("action_12")
        self.action_13 = QtGui.QAction(parent=MainWindow)
        self.action_13.setObjectName("action_13")
        self.action_14 = QtGui.QAction(parent=MainWindow)
        self.action_14.setObjectName("action_14")
        self.action_15 = QtGui.QAction(parent=MainWindow)
        self.action_15.setObjectName("action_15")
        self.action_16 = QtGui.QAction(parent=MainWindow)
        self.action_16.setObjectName("action_16")
        self.action_20 = QtGui.QAction(parent=MainWindow)
        self.action_20.setObjectName("action_20")
        self.action_21 = QtGui.QAction(parent=MainWindow)
        self.action_21.setObjectName("action_21")
        self.action_23 = QtGui.QAction(parent=MainWindow)
        self.action_23.setObjectName("action_23")
        self.action_24 = QtGui.QAction(parent=MainWindow)
        self.action_24.setObjectName("action_24")
        self.action_26 = QtGui.QAction(parent=MainWindow)
        self.action_26.setObjectName("action_26")
        self.action_27 = QtGui.QAction(parent=MainWindow)
        self.action_27.setObjectName("action_27")
        self.action_29 = QtGui.QAction(parent=MainWindow)
        self.action_29.setObjectName("action_29")
        self.action_30 = QtGui.QAction(parent=MainWindow)
        self.action_30.setObjectName("action_30")
        self.action_31 = QtGui.QAction(parent=MainWindow)
        self.action_31.setObjectName("action_31")
        self.action_32 = QtGui.QAction(parent=MainWindow)
        self.action_32.setObjectName("action_32")
        self.action_33 = QtGui.QAction(parent=MainWindow)
        self.action_33.setObjectName("action_33")
        self.action_34 = QtGui.QAction(parent=MainWindow)
        self.action_34.setObjectName("action_34")
        self.action_35 = QtGui.QAction(parent=MainWindow)
        self.action_35.setObjectName("action_35")
        self.action_36 = QtGui.QAction(parent=MainWindow)
        self.action_36.setObjectName("action_36")
        self.action_37 = QtGui.QAction(parent=MainWindow)
        self.action_37.setObjectName("action_37")
        self.menuLoad_Image.addAction(self.action)
        self.menuLoad_Image.addAction(self.action_3)
        self.menuLoad_Image.addAction(self.action_15)
        self.menuLoad_Image.addAction(self.action_16)
        self.menu_3.addAction(self.action_20)
        self.menu_3.addAction(self.action_21)
        self.menu_4.addAction(self.action_23)
        self.menu_4.addAction(self.action_24)
        self.menu_5.addAction(self.action_26)
        self.menu_5.addAction(self.action_27)
        self.menu.addAction(self.action_4)
        self.menu.addAction(self.menu_3.menuAction())
        self.menu.addAction(self.menu_4.menuAction())
        self.menu.addAction(self.menu_5.menuAction())
        self.menu_6.addAction(self.action_29)
        self.menu_6.addAction(self.action_30)
        self.menu_6.addAction(self.action_31)
        self.menu_2.addAction(self.action_14)
        self.menu_2.addAction(self.menu_6.menuAction())
        self.menu_2.addAction(self.action_32)
        self.menu_2.addAction(self.action_33)
        self.menu_2.addAction(self.action_34)
        self.menu_7.addAction(self.action_35)
        self.menu_7.addAction(self.action_36)
        self.menu_7.addAction(self.action_37)
        self.menubar.addAction(self.menuLoad_Image.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_7.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.connectSignals()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuLoad_Image.setTitle(_translate("MainWindow", "Файл"))
        self.menu.setTitle(_translate("MainWindow", "Редактирование"))
        self.menu_3.setTitle(_translate("MainWindow", "Цветокоррекция"))
        self.menu_4.setTitle(_translate("MainWindow", "Трансформации"))
        self.menu_5.setTitle(_translate("MainWindow", "Фильтры"))
        self.menu_2.setTitle(_translate("MainWindow", "Анализ"))
        self.menu_6.setTitle(_translate("MainWindow", "Цветовые каналы"))
        self.menu_7.setTitle(_translate("MainWindow", "Инструменты"))
        self.action.setText(_translate("MainWindow", "Открыть"))
        self.action.setWhatsThis(_translate("MainWindow", "Загрузка изображения"))
        self.action_2.setText(_translate("MainWindow", "Экспортировать"))
        self.action_3.setText(_translate("MainWindow", "Сохранить"))
        self.action_4.setText(_translate("MainWindow", "Яркость/Контрастность"))
        self.action_5.setText(_translate("MainWindow", "Проанализировать \"однородные\" и \"неоднородные\" области"))
        self.action_6.setText(_translate("MainWindow", "Изменить яркость"))
        self.action_7.setText(_translate("MainWindow", "Изменить контрастность"))
        self.action_10.setText(_translate("MainWindow", "Получить негатив"))
        self.action_11.setText(_translate("MainWindow", "Обмен цветовых каналов"))
        self.action_12.setText(_translate("MainWindow", "Симметричное отображение"))
        self.action_13.setText(_translate("MainWindow", "Удаление шума"))
        self.action_14.setText(_translate("MainWindow", "Гистограмма яркости"))
        self.action_15.setText(_translate("MainWindow", "Сохранить как"))
        self.action_16.setText(_translate("MainWindow", "Выход"))
        self.action_20.setText(_translate("MainWindow", "Инверсия"))
        self.action_21.setText(_translate("MainWindow", "Обмен цветовых каналов"))
        self.action_23.setText(_translate("MainWindow", "Отражение"))
        self.action_24.setText(_translate("MainWindow", "Поворот"))
        self.action_26.setText(_translate("MainWindow", "Удаление шума"))
        self.action_27.setText(_translate("MainWindow", "Острота"))
        self.action_29.setText(_translate("MainWindow", "Красный"))
        self.action_30.setText(_translate("MainWindow", "Зеленый"))
        self.action_31.setText(_translate("MainWindow", "Синий"))
        self.action_32.setText(_translate("MainWindow", "Черно-белое изображение"))
        self.action_33.setText(_translate("MainWindow", "Анализ областей"))
        self.action_34.setText(_translate("MainWindow", "Карта контрастности"))
        self.action_35.setText(_translate("MainWindow", "Информация о пикселе"))
        self.action_36.setText(_translate("MainWindow", "Профиль яркости"))
        self.action_37.setText(_translate("MainWindow", "Настройки"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
