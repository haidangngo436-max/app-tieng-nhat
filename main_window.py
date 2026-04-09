import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CuaSoChinh(QtWidgets.QMainWindow):
    def __init__(self, ten_nguoi_dung):
        super().__init__()
        uic.loadUi('/Users/user/Desktop/project/mainchinh.ui', self)
        self.setWindowTitle(f"App Học Tiếng Nhật - こんにちは {ten_nguoi_dung}!")

        # Load QSS
        qss_file_path = '/Users/user/Desktop/style.qss'
        if os.path.exists(qss_file_path):
            with open(qss_file_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())

        # Gắn sự kiện lật trang bài học
        self.btn_bai1.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.btn_bai2.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        self.btn_bai3.clicked.connect(lambda: self.pages.setCurrentIndex(3))
        self.btn_bai4.clicked.connect(lambda: self.pages.setCurrentIndex(4))
        self.btn_bai5.clicked.connect(lambda: self.pages.setCurrentIndex(5))
        self.btn_bai6.clicked.connect(lambda: self.pages.setCurrentIndex(6))
        self.btn_bai7.clicked.connect(lambda: self.pages.setCurrentIndex(7))
        self.btn_bai8.clicked.connect(lambda: self.pages.setCurrentIndex(8))
        self.btn_bai9.clicked.connect(lambda: self.pages.setCurrentIndex(9))
        self.btn_bai10.clicked.connect(lambda: self.pages.setCurrentIndex(10))

        # Gắn nút điều hướng dưới cùng
        self.btn_quiz.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.btn_truoc.clicked.connect(self.mo_bai_truoc)
        self.btn_tiep.clicked.connect(self.mo_bai_tiep)
        self.btn_dang_xuat.clicked.connect(self.dang_xuat)

        self.load_bang_katakana_co_ban()

    def mo_bai_truoc(self):
        if self.pages.currentIndex() > 0:
            self.pages.setCurrentIndex(self.pages.currentIndex() - 1)

    def mo_bai_tiep(self):
        if self.pages.currentIndex() < self.pages.count() - 1:
            self.pages.setCurrentIndex(self.pages.currentIndex() + 1)

    def dang_xuat(self):
        self.close()
        # MẸO NHỎ: Đặt lệnh import ở đây để tránh lỗi "Circular Import" (Import chéo)
        from login_window import CuaSoDangNhap
        self.man_hinh_dang_nhap = CuaSoDangNhap()
        self.man_hinh_dang_nhap.show()

    def load_bang_katakana_co_ban(self):
        bang = self.tableWidget_4
        bang.setRowCount(0)
        bang.setShowGrid(False)
        bang.setAlternatingRowColors(True)

        font_chu = QFont()
        font_chu.setPointSize(16)

        file_path = '/Users/user/Desktop/data_katakana.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                for row_index, line in enumerate(f):
                    row_data = line.strip().split('|')
                    bang.insertRow(row_index)
                    for col_index, cell_data in enumerate(row_data):
                        item = QTableWidgetItem(cell_data)
                        item.setFont(font_chu)
                        item.setTextAlignment(Qt.AlignCenter)
                        bang.setItem(row_index, col_index, item)
        bang.resizeColumnsToContents()
        bang.resizeRowsToContents()