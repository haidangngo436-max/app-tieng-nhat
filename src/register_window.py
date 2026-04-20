import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QDesktopServices, QPixmap
from PyQt5.QtCore import QUrl


class CuaSoDangKy(QtWidgets.QMainWindow):
    def __init__(self, cua_so_dang_nhap_truoc_do):
        super().__init__()
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Load giao diện
        uic.loadUi(os.path.join(base_dir, "../ui/dang ky tai khoan.ui"), self)

        # Đảm bảo khi mở lên luôn ở trang nhập tuổi (Index 0)
        if hasattr(self, 'stackedWidget'):
            self.stackedWidget.setCurrentIndex(0)
        self.showMaximized()
        self.tai_hinh_anh()
        self.cua_so_dang_nhap = cua_so_dang_nhap_truoc_do
        self.lineEdit_pass_dk.setEchoMode(QtWidgets.QLineEdit.Password)

        # --- Gắn sự kiện ---
        # 1. Trang tuổi -> Trang đăng ký
        self.pushButton_2.clicked.connect(self.kiem_tra_tuoi_va_chuyen)

        # 2. Trang đăng ký -> Quay lại trang tuổi
        if hasattr(self, 'btn_quay_lai_2'):
            self.btn_quay_lai_2.clicked.connect(self.quay_ve_trang_tuoi)

        # 3. Xử lý đăng ký và thoát
        self.pushButton_3.clicked.connect(self.xu_ly_dang_ky)
        self.pushButton.clicked.connect(self.dong_va_quay_ve_dang_nhap)
        self.label_2.linkActivated.connect(self.mo_file_dieu_khoan)

    def tai_hinh_anh(self):
        """Tải hình ảnh từ đường dẫn tuyệt đối"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_dir, "../assets/picture/concu.jpg")
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                for widget in self.findChildren(QtWidgets.QLabel):
                    # Chỉ set pixmap cho những label bạn đã quy định sẵn placeholder trong Designer
                    if widget.objectName() == "label_hinh_anh":
                        widget.setPixmap(pixmap)
                        widget.setScaledContents(True)
        except Exception as e:
            print(f"Lỗi tải hình ảnh: {e}")

    def kiem_tra_tuoi_va_chuyen(self):
        """Logic kiểm tra tuổi để chuyển trang"""
        tuoi_text = self.lineEdit_4.text().strip()
        if tuoi_text.isdigit():
            tuoi = int(tuoi_text)
            if 6 <= tuoi <= 100:  # Ví dụ từ 6 tuổi trở lên mới được học
                self.stackedWidget.setCurrentIndex(1)  # Chuyển sang trang điền thông tin (Index 1)
            else:
                QMessageBox.warning(self, "Lỗi", "Tuổi của bạn không phù hợp để đăng ký!")
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số tuổi hợp lệ!")

    def quay_ve_trang_tuoi(self):
        """Quay lại Index 0"""
        self.stackedWidget.setCurrentIndex(0)

    def xu_ly_dang_ky(self):
        """Logic ghi file database.txt giống bản gốc của bạn"""
        if not self.checkBox.isChecked():
            QMessageBox.warning(self, "Lỗi", "Bạn phải đồng ý với Điều khoản dịch vụ!")
            return

        user = self.lineEdit_user_dk.text().strip()
        email = getattr(self, 'lineEdit_email_dk', self.lineEdit_2).text().strip()
        password = self.lineEdit_pass_dk.text().strip()

        if not user or not password or not email:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Kiểm tra trùng lặp và ghi file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "../data/database.txt")

        # Đảm bảo thư mục data tồn tại
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if len(parts) >= 1 and user == parts[0]:
                            QMessageBox.warning(self, "Lỗi", "Tài khoản đã tồn tại!")
                            return

            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f"{user}|{email}|{password}\n")

            QMessageBox.information(self, "Thành công", "Đăng ký tài khoản thành công!")
            self.dong_va_quay_ve_dang_nhap()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu dữ liệu: {e}")

    def dong_va_quay_ve_dang_nhap(self):
        self.cua_so_dang_nhap.show()
        self.close()

    def mo_file_dieu_khoan(self, link_text):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "../docs/12.txt")
        if os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))