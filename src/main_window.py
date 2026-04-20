import os
import json
import random
from PyQt5 import QtWidgets, uic, sip
from PyQt5.QtCore import Qt
from quizzcode import QuizApp
from history_window import CuaSoLichSu


class CuaSoChinh(QtWidgets.QMainWindow):
    def __init__(self, ten_nguoi_dung):
        super().__init__()
        # 1. Lưu thông tin User
        self.ten_nguoi_dung = ten_nguoi_dung
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 2. Load giao diện
        uic.loadUi(os.path.join(base_dir, "../ui/mainchinh.ui"), self)

        self.cua_so_quiz = None
        self.setWindowTitle(f"Học Tiếng Nhật - {self.ten_nguoi_dung}")
        self.showMaximized()

        # 3. Đọc dữ liệu Quizz từ JSON chung
        json_path = os.path.join(base_dir, "../data/data_quizz.json")
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                self.kho_du_lieu_quizz = json.load(f)
        except:
            self.kho_du_lieu_quizz = {}

        # 4. Kết nối các nút chức năng cố định
        if hasattr(self, 'btn_hira'):
            self.btn_hira.clicked.connect(lambda: self.pages.setCurrentIndex(0))

        if hasattr(self, 'btn_quizz'):
            self.btn_quizz.clicked.connect(self.mo_quizz_theo_trang)

        self.btn_truoc.clicked.connect(self.mo_bai_truoc)
        self.btn_tiep.clicked.connect(self.mo_bai_tiep)
        self.btn_dang_xuat.clicked.connect(self.dang_xuat)

        # Kết nối nút lịch sử
        if hasattr(self, 'btn_history'):
            self.btn_history.clicked.connect(self.mo_lich_su)

        # 5. Kết nối 10 nút bài học bên trái (Lật trang)
        for i in range(1, 11):
            nut_ten = f"btn_bai{i}"
            if hasattr(self, nut_ten):
                nut_bam = getattr(self, nut_ten)
                # Dùng lambda đúng cách để không bị kẹt ở bài cuối cùng
                nut_bam.clicked.connect(lambda checked, idx=i: self.pages.setCurrentIndex(idx))

        # 6. Vô hiệu hóa chỉnh sửa trực tiếp trên các bảng (bảng chữ cái, v.v.)
        self.vo_hieu_hoa_chinh_sua_bang()

        # 7. QUAN TRỌNG: Cập nhật màu sắc và khóa/mở bài ngay khi vào App
        self.cap_nhat_giao_dien_khoa()

    def get_progress_file(self):
        """Đường dẫn file tiến độ riêng của từng User"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, f"../data/progress/progress_{self.ten_nguoi_dung}.json")

    def get_unlocked_list(self):
        """Đọc danh sách bài đã mở từ file cá nhân"""
        file_path = self.get_progress_file()
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("unlocked_lessons", [1])
            return [1]  # Mặc định chỉ mở bài 1
        except:
            return [1]

    def vo_hieu_hoa_chinh_sua_bang(self):
        """Vô hiệu hóa chỉnh sửa trực tiếp trên tất cả các bảng"""
        # Tìm tất cả các QTableWidget trong giao diện
        for widget in self.findChildren(QtWidgets.QTableWidget):
            # Vô hiệu hóa các trigger chỉnh sửa
            widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            # Cũng có thể cấm chọn từng cell (nếu muốn)
            # widget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

    def cap_nhat_giao_dien_khoa(self):
        """Hàm 'phù thủy' đổi màu nút xám -> xanh ngay lập tức"""
        unlocked_list = self.get_unlocked_list()

        for i in range(1, 11):
            nut_ten = f"btn_bai{i}"
            if hasattr(self, nut_ten):
                nut_bam = getattr(self, nut_ten)

                if i in unlocked_list:
                    # NẾU ĐÃ MỞ: Cho phép bấm + Đổi sang màu xanh (xóa style xám)
                    nut_bam.setEnabled(True)
                    nut_bam.setText(f"Bài {i} 🔓")
                    nut_bam.setStyleSheet("")  # Xóa CSS cũ để lấy lại màu gốc trong QSS/Designer
                else:
                    # NẾU CHƯA MỞ: Khóa bấm + Nhuộm màu xám xịt
                    nut_bam.setEnabled(False)
                    nut_bam.setText(f"Bài {i} 🔒")
                    nut_bam.setStyleSheet("""
                        QPushButton {
                            background-color: #d1d1d1; 
                            color: #7f8c8d; 
                            border: 2px solid #bdc3c7;
                            border-radius: 20px;
                        }
                    """)

        if hasattr(self, 'btn_hira'):
            self.btn_hira.setEnabled(True)
            self.btn_hira.setStyleSheet("")

    def mo_quizz_theo_trang(self):
        """Mở Quiz và đặt chế độ 'Theo dõi' khi đóng cửa sổ"""
        if self.cua_so_quiz and not sip.isdeleted(self.cua_so_quiz):
            self.cua_so_quiz.close()

        index_hien_tai = self.pages.currentIndex()
        if index_hien_tai == 0: return  # Bảng chữ cái ko có quiz

        ten_key = f"bai_{index_hien_tai}"
        du_lieu = self.kho_du_lieu_quizz.get(ten_key, [])

        if du_lieu:
            du_lieu_tron = list(du_lieu)
            random.shuffle(du_lieu_tron)

            # Khởi tạo QuizApp
            self.cua_so_quiz = QuizApp(du_lieu_tron, index_hien_tai, self.ten_nguoi_dung)

            # --- LOGIC THẦN THÁNH CHỮA BỆNH 'PHẢI ĐĂNG XUẤT MỚI XANH' ---
            # 1. Ép cửa sổ Quiz tự hủy khi đóng để phát tín hiệu destroyed
            self.cua_so_quiz.setAttribute(Qt.WA_DeleteOnClose)
            # 2. Khi Quiz đóng, cửa sổ chính tự động 'vẽ' lại màu nút ngay lập tức
            self.cua_so_quiz.destroyed.connect(self.cap_nhat_giao_dien_khoa)

            self.cua_so_quiz.show()
        else:
            QtWidgets.QMessageBox.information(self, "Thông báo", f"Chưa có bài tập cho '{ten_key}'")

    def mo_bai_tiep(self):
        """Nút lật trang có kiểm tra 'giấy thông hành'"""
        target_idx = self.pages.currentIndex() + 1
        if target_idx >= self.pages.count(): return

        unlocked = self.get_unlocked_list()
        # Cho qua nếu là bài đã mở khóa hoặc trang bảng chữ cái (index 0)
        if target_idx == 0 or target_idx in unlocked:
            self.pages.setCurrentIndex(target_idx)
        else:
            QtWidgets.QMessageBox.warning(self, "Bị khóa", "Học xong bài hiện tại mới được sang bài tiếp!")

    def mo_bai_truoc(self):
        if self.pages.currentIndex() > 0:
            self.pages.setCurrentIndex(self.pages.currentIndex() - 1)

    def dang_xuat(self):
        """Đăng xuất an toàn về màn hình Login"""
        if self.cua_so_quiz and not sip.isdeleted(self.cua_so_quiz):
            self.cua_so_quiz.close()

        # Import tại chỗ để tránh lỗi import vòng quanh
        try:
            from login_window import CuaSoDangNhap
            self.man_hinh_dn = CuaSoDangNhap()
            self.man_hinh_dn.show()
            self.close()  # Đóng cửa sổ chính sau khi đã hiện màn hình login
        except Exception as e:
            print(f"Lỗi đăng xuất: {e}")
            self.close()

    def mo_lich_su(self):
        """Mở cửa sổ lịch sử làm bài"""
        self.cua_so_lich_su = CuaSoLichSu(self.ten_nguoi_dung, self)
        self.cua_so_lich_su.show()