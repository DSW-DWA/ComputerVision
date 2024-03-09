from PyQt6.QtWidgets import QApplication, QMainWindow
from MainWindow import UiMainWindow
import sys


def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
