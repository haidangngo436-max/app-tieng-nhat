import sys
import os
from PyQt5 import QtWidgets

from login_window import CuaSoDangNhap

if __name__ == "__main__":

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    app = QtWidgets.QApplication(sys.argv)

    main_window = CuaSoDangNhap()
    main_window.show()

    sys.exit(app.exec())

    