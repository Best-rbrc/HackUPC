import sys
from PyQt5.QtWidgets import QApplication
from gui import TravelApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TravelApp()
    window.show()
    sys.exit(app.exec_())
