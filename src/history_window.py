import os
import json
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


class CuaSoLichSu(QtWidgets.QMainWindow):
    def __init__(self, ten_nguoi_dung, parent=None):
        super().__init__(parent)
        self.ten_nguoi_dung = ten_nguoi_dung

        # 1. Load giao diện từ file .ui mới
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_dir, "../ui/History.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle(f"Lịch sử học tập - {ten_nguoi_dung}")
        self.showMaximized()

        # 2. Kết nối nút bấm dựa trên Object Name trong ảnh bạn gửi
        # Nút "Quay lại" trong ảnh của bạn tên là 'pushButton'
        if hasattr(self, 'pushButton'):
            self.pushButton.clicked.connect(self.close)

        # Nút "Đăng xuất" tên là 'Logout_Button'
        if hasattr(self, 'Logout_Button'):
            self.Logout_Button.clicked.connect(self.close)  # Hoặc xử lý đăng xuất riêng

        # 3. Ánh xạ bảng từ UI
        # Trong ảnh của bạn, QTableWidget có tên là 'tbl_LichSuNopBai'
        self.table = self.findChild(QtWidgets.QTableWidget, "tbl_LichSuNopBai")

        if self.table:
            self.setup_table_style()
            self.tai_lich_su()
        else:
            print("Lỗi: Không tìm thấy bảng 'tbl_LichSuNopBai' trong file UI!")

    def setup_table_style(self):
        """Định dạng bảng để khớp với các cột: Bài tập, Thời gian, Kết quả, Đánh giá"""
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Bài tập", "Thời gian", "Kết quả", "Đánh giá"])

        # Giãn đều các cột
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Ẩn cột số thứ tự bên trái
        self.table.verticalHeader().setVisible(False)

        # Style cho bảng (giữ màu sắc Cyan nhẹ nhàng)
        self.table.setStyleSheet("""
            QTableWidget { gridline-color: #e0f7fa; font-size: 13px; }
            QHeaderView::section {
                background-color: #00bcd4;
                color: white;
                padding: 5px;
                font-weight: bold;
                border: 1px solid #00acc1;
            }
        """)

    def tai_lich_su(self):
        """Đọc dữ liệu từ file progress_{user}.json"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, f"../data/progress/progress_{self.ten_nguoi_dung}.json")

        if not os.path.exists(file_path):
            self.table.setRowCount(1)
            self.table.setColumnCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("Chưa có lịch sử làm bài."))
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                history = data.get("history", [])

            # Sắp xếp lịch sử: mới nhất lên đầu
            history.sort(key=lambda x: x.get("date", ""), reverse=True)

            self.table.setRowCount(len(history))
            for row, entry in enumerate(history):
                # Tạo các ô dữ liệu
                item_lesson = QTableWidgetItem(f"Bài {entry.get('lesson', '?')}")
                item_time = QTableWidgetItem(entry.get('date', ''))

                score = entry.get('score', 0)
                total = entry.get('total', 0)
                item_result = QTableWidgetItem(f"{score}/{total}")

                passed = entry.get('passed', False)
                status_text = "Đạt ✓" if passed else "Chưa đạt ✗"
                item_status = QTableWidgetItem(status_text)

                # Căn giữa và tô màu
                for item in [item_lesson, item_time, item_result, item_status]:
                    item.setTextAlignment(Qt.AlignCenter)

                if passed:
                    item_status.setForeground(QtCore.Qt.darkGreen)
                else:
                    item_status.setForeground(QtCore.Qt.red)

                self.table.setItem(row, 0, item_lesson)
                self.table.setItem(row, 1, item_time)
                self.table.setItem(row, 2, item_result)
                self.table.setItem(row, 3, item_status)

        except Exception as e:
            print(f"Lỗi load dữ liệu: {e}")