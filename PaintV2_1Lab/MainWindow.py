import cv2
import numpy as np
from BrightnessContrastDialog import BrightnessContrastDialog
from ChannelExchangeDialog import ChannelExchangeDialog
from ImageEditor import ImageEditor
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QFileDialog, QLabel, QMainWindow


class UiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.imageLabel = QLabel(self)
        self.image = None
        self.imageEditor: ImageEditor
        self.brightnessContrastDialog = BrightnessContrastDialog(self)
        self.channelExchangeDialog = ChannelExchangeDialog(self)
        self.setupUi(self)
        self.connectSignals()

    def connectSignals(self):
        self.actionOpen.triggered.connect(self.openImage)
        self.actionAdjustBrightnessContrast.triggered.connect(lambda: self.brightnessContrastDialog.show())
        self.actionAdjustBrightnessContrast.triggered.connect(lambda: self.brightnessContrastDialog.show())
        self.actionInversion.triggered.connect(self.inversion)
        self.actionColorChannelsSwap.triggered.connect(lambda: self.channelExchangeDialog.show())
        self.channelExchangeDialog.channelChanged.connect(self.swap_channels)
        self.brightnessContrastDialog.brightnessChanged.connect(self.change_brightness_and_contrast)
        self.brightnessContrastDialog.channelChanged.connect(self.change_brightness_and_contrast)
        self.brightnessContrastDialog.contrastChanged.connect(self.change_brightness_and_contrast)
        self.brightnessContrastDialog.okButton.clicked.connect(self.onOkButtonClicked)
        self.brightnessContrastDialog.cancelButton.clicked.connect(self.onCancelButtonClicked)

    def onOkButtonClicked(self):
        if self.imageEditor:
            self.imageEditor.save()
            self.showImage(self.imageEditor.save_image)

    def onCancelButtonClicked(self):
        if self.imageEditor:
            self.imageEditor.cancel()
            self.showImage(self.imageEditor.save_image)

    def openImage(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.bmp *.tiff)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.imageEditor = ImageEditor(self.image)
            self.showImage(self.imageEditor.change_image)
            self.actionAdjustBrightnessContrast.setEnabled(True)
            self.actionInversion.setEnabled(True)
            self.actionColorChannelsSwap.setEnabled(True)

    def change_brightness_and_contrast(self):
        if self.imageEditor:
            brightness = self.brightnessContrastDialog.brightnessSlider.value()
            contrast = self.brightnessContrastDialog.contrastSlider.value()
            channel = self.brightnessContrastDialog.getActiveRadioButton()
            self.imageEditor.change_channel_intensity_and_cantrast(
                channel=channel,
                brightness_factor=brightness,
                contrast_factor=contrast,
            )
            self.showImage(self.imageEditor.getImage())

    def inversion(self):
        if self.imageEditor:
            self.imageEditor.invert_image()
            self.showImage(self.imageEditor.getImage())

    def swap_channels(self, source, destination):
        if self.imageEditor:
            print(source, destination)
            self.imageEditor.swap_channels(source, destination)
            self.showImage(self.imageEditor.getImage())

    def showImage(self, image: np.ndarray):
        height, width, channels = image.shape
        bytesPerLine = channels * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qImg)
        self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def setupUi(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(800, 600)

        # Основные компоненты интерфейса
        self.centralWidget = QtWidgets.QWidget(parent=main_window)
        self.centralWidget.setObjectName("centralWidget")
        main_window.setCentralWidget(self.centralWidget)

        self.imageLabel = QLabel(self.centralWidget)
        self.imageLabel.setGeometry(QtCore.QRect(10, 10, 780, 540))
        self.imageLabel.setObjectName("imageLabel")
        self.imageLabel.setScaledContents(True)

        self.statusbar = QtWidgets.QStatusBar(parent=main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.menubar = QtWidgets.QMenuBar(parent=main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 37))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)

        # Действия
        self.actionOpen = QtGui.QAction(parent=main_window)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(parent=main_window)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtGui.QAction(parent=main_window)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionExit = QtGui.QAction(parent=main_window)
        self.actionExit.setObjectName("actionExit")

        self.actionAdjustBrightnessContrast = QtGui.QAction(parent=main_window)
        self.actionAdjustBrightnessContrast.setObjectName("actionAdjustBrightnessContrast")
        self.actionBrightnessChange = QtGui.QAction(parent=main_window)
        self.actionBrightnessChange.setObjectName("actionBrightnessChange")
        self.actionContrastChange = QtGui.QAction(parent=main_window)
        self.actionContrastChange.setObjectName("actionContrastChange")
        self.actionNegative = QtGui.QAction(parent=main_window)
        self.actionNegative.setObjectName("actionNegative")
        self.actionMirrorDisplay = QtGui.QAction(parent=main_window)
        self.actionMirrorDisplay.setObjectName("actionMirrorDisplay")
        self.actionBrightnessHistogram = QtGui.QAction(parent=main_window)
        self.actionBrightnessHistogram.setObjectName("actionBrightnessHistogram")
        self.actionInversion = QtGui.QAction(parent=main_window)
        self.actionInversion.setObjectName("actionInversion")
        self.actionColorChannelsSwap = QtGui.QAction(parent=main_window)
        self.actionColorChannelsSwap.setObjectName("actionColorChannelsSwap")
        self.actionReflection = QtGui.QAction(parent=main_window)
        self.actionReflection.setObjectName("actionReflection")
        self.actionRotation = QtGui.QAction(parent=main_window)
        self.actionRotation.setObjectName("actionRotation")
        self.actionNoiseRemoval = QtGui.QAction(parent=main_window)
        self.actionNoiseRemoval.setObjectName("actionNoiseRemoval")
        self.actionSharpness = QtGui.QAction(parent=main_window)
        self.actionSharpness.setObjectName("actionSharpness")
        self.actionRedChannel = QtGui.QAction(parent=main_window)
        self.actionRedChannel.setObjectName("actionRedChannel")
        self.actionGreenChannel = QtGui.QAction(parent=main_window)
        self.actionGreenChannel.setObjectName("actionGreenChannel")
        self.actionBlueChannel = QtGui.QAction(parent=main_window)
        self.actionBlueChannel.setObjectName("actionBlueChannel")
        self.actionBlackWhite = QtGui.QAction(parent=main_window)
        self.actionBlackWhite.setObjectName("actionBlackWhite")
        self.actionRegionAnalysis = QtGui.QAction(parent=main_window)
        self.actionRegionAnalysis.setObjectName("actionRegionAnalysis")
        self.actionContrastMap = QtGui.QAction(parent=main_window)
        self.actionContrastMap.setObjectName("actionContrastMap")
        self.actionPixelInfo = QtGui.QAction(parent=main_window)
        self.actionPixelInfo.setObjectName("actionPixelInfo")
        self.actionBrightnessProfile = QtGui.QAction(parent=main_window)
        self.actionBrightnessProfile.setObjectName("actionBrightnessProfile")
        self.actionSettings = QtGui.QAction(parent=main_window)
        self.actionSettings.setObjectName("actionSettings")

        # TODO: Выключил все кнопки пока их не реализовали.
        # Реализовали - включили. Так проще будет понять.
        # self.actionOpen.setEnabled(False) Реализовано.
        self.actionSave.setEnabled(False)
        self.actionSaveAs.setEnabled(False)
        self.actionAdjustBrightnessContrast.setEnabled(False)
        self.actionBrightnessChange.setEnabled(False)
        self.actionContrastChange.setEnabled(False)
        self.actionNegative.setEnabled(False)
        self.actionMirrorDisplay.setEnabled(False)
        self.actionBrightnessHistogram.setEnabled(False)
        self.actionExit.setEnabled(False)
        self.actionInversion.setEnabled(False)
        self.actionColorChannelsSwap.setEnabled(False)
        self.actionReflection.setEnabled(False)
        self.actionRotation.setEnabled(False)
        self.actionNoiseRemoval.setEnabled(False)
        self.actionSharpness.setEnabled(False)
        self.actionRedChannel.setEnabled(False)
        self.actionGreenChannel.setEnabled(False)
        self.actionBlueChannel.setEnabled(False)
        self.actionBlackWhite.setEnabled(False)
        self.actionRegionAnalysis.setEnabled(False)
        self.actionContrastMap.setEnabled(False)
        self.actionPixelInfo.setEnabled(False)
        self.actionBrightnessProfile.setEnabled(False)
        self.actionSettings.setEnabled(False)

        # Меню
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(parent=self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuColorCorrection = QtWidgets.QMenu(parent=self.menuEdit)
        self.menuColorCorrection.setObjectName("menuColorCorrection")
        self.menuTransformations = QtWidgets.QMenu(parent=self.menuEdit)
        self.menuTransformations.setObjectName("menuTransformations")
        self.menuFilters = QtWidgets.QMenu(parent=self.menuEdit)
        self.menuFilters.setObjectName("menuFilters")
        self.menuAnalysis = QtWidgets.QMenu(parent=self.menubar)
        self.menuAnalysis.setObjectName("menuAnalysis")
        self.menuColorChannels = QtWidgets.QMenu(parent=self.menuAnalysis)
        self.menuColorChannels.setObjectName("menuColorChannels")
        self.menuTools = QtWidgets.QMenu(parent=self.menubar)
        self.menuTools.setObjectName("menuTools")

        # Добавление действий в меню
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addAction(self.actionExit)
        self.menuColorCorrection.addAction(self.actionInversion)
        self.menuColorCorrection.addAction(self.actionColorChannelsSwap)
        self.menuTransformations.addAction(self.actionReflection)
        self.menuTransformations.addAction(self.actionRotation)
        self.menuFilters.addAction(self.actionNoiseRemoval)
        self.menuFilters.addAction(self.actionSharpness)
        self.menuEdit.addAction(self.actionAdjustBrightnessContrast)
        self.menuEdit.addAction(self.menuColorCorrection.menuAction())
        self.menuEdit.addAction(self.menuTransformations.menuAction())
        self.menuEdit.addAction(self.menuFilters.menuAction())
        self.menuColorChannels.addAction(self.actionRedChannel)
        self.menuColorChannels.addAction(self.actionGreenChannel)
        self.menuColorChannels.addAction(self.actionBlueChannel)
        self.menuAnalysis.addAction(self.actionBrightnessHistogram)
        self.menuAnalysis.addAction(self.menuColorChannels.menuAction())
        self.menuAnalysis.addAction(self.actionBlackWhite)
        self.menuAnalysis.addAction(self.actionRegionAnalysis)
        self.menuAnalysis.addAction(self.actionContrastMap)
        self.menuTools.addAction(self.actionPixelInfo)
        self.menuTools.addAction(self.actionBrightnessProfile)
        self.menuTools.addAction(self.actionSettings)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        self.connectSignals()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        # Меню
        self.menuFile.setTitle(_translate("MainWindow", "Файл"))
        self.menuEdit.setTitle(_translate("MainWindow", "Редактирование"))
        self.menuColorCorrection.setTitle(_translate("MainWindow", "Цветокоррекция"))
        self.menuTransformations.setTitle(_translate("MainWindow", "Трансформации"))
        self.menuFilters.setTitle(_translate("MainWindow", "Фильтры"))
        self.menuAnalysis.setTitle(_translate("MainWindow", "Анализ"))
        self.menuColorChannels.setTitle(_translate("MainWindow", "Цветовые каналы"))
        self.menuTools.setTitle(_translate("MainWindow", "Инструменты"))

        # Действия
        self.actionOpen.setText(_translate("MainWindow", "Открыть"))
        self.actionSave.setText(_translate("MainWindow", "Сохранить"))
        self.actionSaveAs.setText(_translate("MainWindow", "Сохранить как"))
        self.actionExit.setText(_translate("MainWindow", "Выход"))

        self.actionAdjustBrightnessContrast.setText(_translate("MainWindow", "Яркость/Контрастность"))
        self.actionBrightnessChange.setText(_translate("MainWindow", "Изменить яркость"))
        self.actionContrastChange.setText(_translate("MainWindow", "Изменить контрастность"))
        self.actionNegative.setText(_translate("MainWindow", "Получить негатив"))
        self.actionMirrorDisplay.setText(_translate("MainWindow", "Симметричное отображение"))

        self.actionInversion.setText(_translate("MainWindow", "Инверсия"))
        self.actionColorChannelsSwap.setText(_translate("MainWindow", "Обмен цветовых каналов"))
        self.actionReflection.setText(_translate("MainWindow", "Отражение"))
        self.actionRotation.setText(_translate("MainWindow", "Поворот"))

        self.actionNoiseRemoval.setText(_translate("MainWindow", "Удаление шума"))
        self.actionSharpness.setText(_translate("MainWindow", "Острота"))

        self.actionRedChannel.setText(_translate("MainWindow", "Красный"))
        self.actionGreenChannel.setText(_translate("MainWindow", "Зеленый"))
        self.actionBlueChannel.setText(_translate("MainWindow", "Синий"))
        self.actionBlackWhite.setText(_translate("MainWindow", "Черно-белое изображение"))

        self.actionRegionAnalysis.setText(_translate("MainWindow", "Анализ областей"))
        self.actionContrastMap.setText(_translate("MainWindow", "Карта контрастности"))
        self.actionPixelInfo.setText(_translate("MainWindow", "Информация о пикселе"))
        self.actionBrightnessProfile.setText(_translate("MainWindow", "Профиль яркости"))
        self.actionBrightnessHistogram.setText(_translate("MainWindow", "Гистограмма яркости"))

        self.actionSettings.setText(_translate("MainWindow", "Настройки"))
