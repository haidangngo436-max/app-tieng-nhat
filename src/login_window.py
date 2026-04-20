import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap

# NHÚNG 2 MÀN HÌNH KIA VÀO ĐÂY
from register_window import CuaSoDangKy
from main_window import CuaSoChinh
from quizzcode import QuizApp

class CuaSoDangNhap(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(base_dir, "../ui/manhinhdangnhap.ui"), self)
        
        # Tải hình ảnh từ đường dẫn tưyệt đối
        self.tai_hinh_anh()
        self.showMaximized()
        
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_chuyen_trang.clicked.connect(self.mo_cua_so_dang_ky)
        self.btn_dang_nhap.clicked.connect(self.xu_ly_dang_nhap)

    def tai_hinh_anh(self):
        """Tại hình ảnh đăng nhập từ đường dẫn tưyệt đố"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_dir, "../assets/picture/concu.jpg")
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                for widget in self.findChildren(QtWidgets.QLabel):
                    # Kiểm tra xem label này có pixmap không
                    if widget.pixmap() and not widget.pixmap().isNull():
                        if pixmap and not pixmap.isNull():
                            widget.setPixmap(pixmap)
                            widget.setScaledContents(True)
                        break
        except Exception as e:
            print(f"Lỗi tải hình ảnh: {e}")


    def xu_ly_dang_nhap(self):
        chuoi_nhap_vao = self.lineEdit_user.text().strip()
        pass_nhap = self.lineEdit_pass.text().strip()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "../data/database.txt")

        if not os.path.exists(file_path):
            hop_thoai = QMessageBox.question(self, "Chưa có dữ liệu",
                                             "Chưa có tài khoản nào! Bro có muốn đăng ký ngay không?",
                                             QMessageBox.Yes | QMessageBox.No)
            if hop_thoai == QMessageBox.Yes: self.mo_cua_so_dang_ky()
            return

        found = False
        ten_that = ""
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    u = parts[0]
                    p = parts[-1] # Pass luôn ở cuối cùng
                    e = parts[1] if len(parts) == 3 else ""
                    if (chuoi_nhap_vao == u or chuoi_nhap_vao == e) and pass_nhap == p:
                        found, ten_that = True, u
                        break

        if found:
            self.mo_man_hinh_chinh(ten_that)
        else:
            hop_thoai = QMessageBox.question(self, "Lỗi đăng nhập",
                                             "Sai tài khoản, email hoặc mật khẩu!\nBro có muốn Đăng ký không?",
                                             QMessageBox.Yes | QMessageBox.No)
            if hop_thoai == QMessageBox.Yes: self.mo_cua_so_dang_ky()

    def mo_man_hinh_chinh(self, ten_nguoi_dung):
        # Mở màn hình CuaSoChinh (đã import từ main_window.py)
        self.man_hinh_chinh = CuaSoChinh(ten_nguoi_dung)
        self.man_hinh_chinh.show()
        self.close()

    def mo_cua_so_dang_ky(self):
        # Mở màn hình CuaSoDangKy (đã import từ register_window.py)
        self.cua_so_2 = CuaSoDangKy(self)
        self.cua_so_2.show()
        self.hide()