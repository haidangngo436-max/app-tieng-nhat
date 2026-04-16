import os
import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt


class CuaSoLichSu(QtWidgets.QDialog):
    """Cửa sổ hiển thị lịch sử làm bài của người dùng"""
    
    def __init__(self, ten_nguoi_dung, parent=None):
        super().__init__(parent)
        self.ten_nguoi_dung = ten_nguoi_dung
        self.setWindowTitle(f"Lịch sử làm bài - {ten_nguoi_dung}")
        self.setGeometry(100, 100, 700, 500)
        
        # Tạo layout chính
        layout = QtWidgets.QVBoxLayout()
        
        # Tiêu đề
        title = QtWidgets.QLabel(f"Lịch sử làm bài của {ten_nguoi_dung}")
        font = title.font()
        font.setPointSize(12)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)
        
        # Tạo bảng hiển thị lịch sử
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Bài học", "Điểm", "Ngày làm", "Trạng thái", "Chi tiết"])
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 180)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 150)
        
        layout.addWidget(self.table)
        
        # Nút đóng
        btn_dong = QtWidgets.QPushButton("Đóng")
        btn_dong.clicked.connect(self.close)
        layout.addWidget(btn_dong)
        
        self.setLayout(layout)
        
        # Tải dữ liệu lịch sử
        self.tai_lich_su()
    
    def tai_lich_su(self):
        """Tải lịch sử từ file progress"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, f"../data/progress/progress_{self.ten_nguoi_dung}.json")
        
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                self.table.setRowCount(1)
                item = QtWidgets.QTableWidgetItem("Chưa có lịch sử làm bài")
                self.table.setItem(0, 0, item)
                return
            
            history = data.get("history", [])
            
            if not history:
                self.table.setRowCount(1)
                item = QtWidgets.QTableWidgetItem("Chưa có lịch sử làm bài")
                self.table.setItem(0, 0, item)
                return
            
            # Sắp xếp lịch sử theo ngày mới nhất trước
            history_sorted = sorted(history, key=lambda x: x.get("date", ""), reverse=True)
            
            self.table.setRowCount(len(history_sorted))
            
            for row, entry in enumerate(history_sorted):
                lesson = entry.get("lesson", "?")
                score = entry.get("score", 0)
                total = entry.get("total", 0)
                date = entry.get("date", "?")
                passed = entry.get("passed", False)
                status = "✓ Đạt" if passed else "✗ Chưa đạt"
                
                # Bài học
                item_lesson = QtWidgets.QTableWidgetItem(f"Bài {lesson}")
                item_lesson.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 0, item_lesson)
                
                # Điểm
                item_score = QtWidgets.QTableWidgetItem(f"{score}/{total}")
                item_score.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 1, item_score)
                
                # Ngày
                item_date = QtWidgets.QTableWidgetItem(date)
                item_date.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 2, item_date)
                
                # Trạng thái
                item_status = QtWidgets.QTableWidgetItem(status)
                item_status.setTextAlignment(Qt.AlignCenter)
                if passed:
                    item_status.setBackground(QtCore.Qt.green)
                    item_status.setForeground(QtCore.Qt.white)
                else:
                    item_status.setBackground(QtCore.Qt.red)
                    item_status.setForeground(QtCore.Qt.white)
                self.table.setItem(row, 3, item_status)
                
                # Chi tiết
                percentage = int((score / total * 100)) if total > 0 else 0
                item_detail = QtWidgets.QTableWidgetItem(f"{percentage}%")
                item_detail.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 4, item_detail)
        
        except Exception as e:
            print(f"Lỗi tải lịch sử: {e}")
            self.table.setRowCount(1)
            item = QtWidgets.QTableWidgetItem(f"Lỗi: {str(e)}")
            self.table.setItem(0, 0, item)
