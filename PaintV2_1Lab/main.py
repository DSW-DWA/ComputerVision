from PyQt6.QtWidgets import QApplication, QMainWindow
from MainWindow import Ui_MainWindow
import sys


def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
