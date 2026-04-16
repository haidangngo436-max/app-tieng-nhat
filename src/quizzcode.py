import os
import json
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
import datetime

class QuizApp(QtWidgets.QMainWindow):
    def __init__(self, quiz_data, lesson_index, ten_nguoi_dung):
        super().__init__()
        self.ten_nguoi_dung = ten_nguoi_dung  # Lưu tên người dùng
        base_dir = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(base_dir, "../ui/quiz/quizzcheckui.ui"), self)

        self.quiz_data = quiz_data
        self.current_index = 0
        self.lesson_index = lesson_index
        self.score = 0

        # 1. Gom nhóm nút và thiết lập ban đầu
        self.buttons = []
        for name in ['pushButton', 'pushButton_2', 'pushButton_3', 'pushButton_4']:
            if hasattr(self, name):
                btn = getattr(self, name)
                btn.setCheckable(True)
                btn.setAutoExclusive(True)
                self.buttons.append(btn)

        # 2. Kết nối nút điều hướng
        if hasattr(self, 'btn_tiep'):
            self.btn_tiep.clicked.connect(self.next_question)
        elif hasattr(self, 'btn_sau'):
            self.btn_sau.clicked.connect(self.next_question)

        if hasattr(self, 'btn_truoc'):
            self.btn_truoc.clicked.connect(self.prev_question)

        # 3. Kết nối chọn đáp án
        for i, btn in enumerate(self.buttons):
            btn.clicked.connect(lambda checked, idx=i: self.check_answer(idx))

        self.load_question()

    def load_question(self):
        """Reset giao diện khi sang câu mới"""
        data = self.quiz_data[self.current_index]
        self.label_cauhoi.setText(data["question"])

        # Cập nhật ProgressBar
        phan_tram = int(((self.current_index + 1) / len(self.quiz_data)) * 100)
        self.progressBar.setValue(phan_tram)

        for btn in self.buttons:
            btn.setEnabled(True)
            btn.setStyleSheet("")
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)

        for i, btn in enumerate(self.buttons):
            if i < len(data["options"]):
                btn.setText(data["options"][i])
                btn.show()
            else:
                btn.hide()
        self.frame_giaithich.hide()

    def check_answer(self, idx):
        """Xử lý chấm điểm và đổi màu"""
        data = self.quiz_data[self.current_index]
        correct_idx = data.get("correct_idx", -1)

        if idx == correct_idx:
            self.score += 1

        self.label_noidung_gt.setText(data["explanation"])
        self.frame_giaithich.show()

        for i, btn in enumerate(self.buttons):
            if i == correct_idx:
                btn.setStyleSheet("background-color: #58cc02; color: white; border-radius: 10px; font-weight: bold;")
            elif i == idx:
                btn.setStyleSheet("background-color: #ff4b4b; color: white; border-radius: 10px; font-weight: bold;")
            btn.setEnabled(False)

    def next_question(self):
        """Chuyển câu hoặc kết thúc bài"""
        tong_so_cau_thuc_te = len(self.quiz_data)

        if self.current_index < tong_so_cau_thuc_te - 1:
            self.current_index += 1
            self.load_question()
        else:
            # Điều kiện mở khóa (Ví dụ: đúng từ 1 câu trở lên - ông có thể sửa số 1 này)
            diem_can_thiet = 1

            if self.score >= diem_can_thiet:
                self.mo_khoa_bai_tiep_theo()
                QtWidgets.QMessageBox.information(self, "Tuyệt vời!",
                                                  f"Bạn đạt {self.score}/{tong_so_cau_thuc_te} điểm!\nBài tiếp theo đã được mở khóa.")
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Chưa đủ điểm",
                                              f"Bạn đạt {self.score}/{tong_so_cau_thuc_te}.\nHãy cố gắng đạt ít nhất {diem_can_thiet} câu để mở bài tiếp theo!")
                self.close()

    def prev_question(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_question()

    def mo_khoa_bai_tiep_theo(self):
        """Ghi bài mới vào tiến độ RIÊNG của từng User và lưu lịch sử"""
        # SỬA LỖI Ở ĐÂY: Dùng file_path có chứa tên người dùng
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, f"../data/progress/progress_{self.ten_nguoi_dung}.json")

        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {"unlocked_lessons": [1], "history": []}
        except:
            data = {"unlocked_lessons": [1], "history": []}

        # Đảm bảo history key luôn tồn tại
        if "history" not in data:
            data["history"] = []

        next_lesson = self.lesson_index + 1
        if next_lesson not in data["unlocked_lessons"]:
            data["unlocked_lessons"].append(next_lesson)
        
        # Lưu lịch sử bài làm
        history_entry = {
            "lesson": self.lesson_index,
            "score": self.score,
            "total": len(self.quiz_data),
            "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "passed": self.score >= 1  # Điều kiện đạt
        }
        data["history"].append(history_entry)
        
        # Ghi vào đúng file_path của user đó
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)