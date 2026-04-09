import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

class CuaSoDangKy(QtWidgets.QMainWindow):
    def __init__(self, cua_so_dang_nhap_truoc_do):
        super().__init__()
        uic.loadUi('/Users/user/Desktop/project/dang ky tai khoan.ui', self)
        self.cua_so_dang_nhap = cua_so_dang_nhap_truoc_do
        self.lineEdit_pass_dk.setEchoMode(QtWidgets.QLineEdit.Password)

        # Gắn sự kiện
        self.pushButton_2.clicked.connect(self.kiem_tra_tuoi_va_chuyen)  
        self.pushButton.clicked.connect(self.dong_va_quay_ve_dang_nhap)  
        self.pushButton_3.clicked.connect(self.xu_ly_dang_ky)  
        self.btn_quay_lai_2.clicked.connect(self.quay_ve_trang_tuoi)
        self.label_2.linkActivated.connect(self.mo_file_dieu_khoan)

    def kiem_tra_tuoi_va_chuyen(self):
        tuoi = self.lineEdit_4.text().strip()
        if tuoi.isdigit() and 0 < int(tuoi) < 100:
            self.stackedWidget.setCurrentIndex(1)  
        else:
            QMessageBox.warning(self, "Lỗi", "Nhập tuổi thật đi bro!")

    def quay_ve_trang_tuoi(self):
        self.stackedWidget.setCurrentIndex(0)

    def xu_ly_dang_ky(self):
        if not self.checkBox.isChecked():
            QMessageBox.warning(self, "Lỗi", "Đồng ý Điều khoản dịch vụ mới được đăng ký nhé!")
            return

        user = self.lineEdit_user_dk.text().strip()
        email = getattr(self, 'lineEdit_email_dk', self.lineEdit_2).text().strip()
        password = self.lineEdit_pass_dk.text().strip()

        if not user or not password or not email:
            QMessageBox.warning(self, "Lỗi", "Đừng để trống thông tin nào nhé!")
            return

        file_path = '/Users/user/Desktop/database.txt'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 2:
                        if user == parts[0]:
                            QMessageBox.warning(self, "Trùng lặp", "Tài khoản này đã có người dùng!")
                            return
                        if len(parts) == 3 and email == parts[1] and email != "":
                            QMessageBox.warning(self, "Trùng lặp", "Email này đã được đăng ký!")
                            return

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"{user}|{email}|{password}\n")

        QMessageBox.information(self, "Thành công", "Đăng ký xong! Giờ đăng nhập đi bro.")
        self.dong_va_quay_ve_dang_nhap()

    def dong_va_quay_ve_dang_nhap(self):
        self.cua_so_dang_nhap.show()
        self.close()

    def mo_file_dieu_khoan(self, link_text):
        QDesktopServices.openUrl(QUrl.fromLocalFile('/Users/user/Desktop/12.txt'))