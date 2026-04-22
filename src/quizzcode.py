import os
import json
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
import datetime


class QuizApp(QtWidgets.QMainWindow):
    def __init__(self, quiz_data, lesson_index, ten_nguoi_dung, main_window=None):
        super().__init__()

        self.main_window = main_window
        self.ten_nguoi_dung = ten_nguoi_dung

        base_dir = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(base_dir, "../ui/quiz/quizzcheckui.ui"), self)

        self.quiz_data = quiz_data
        self.lesson_index = lesson_index
        self.current_index = 0
        self.score = 0
        self.showMaximized()

        # 1. Gom nhóm nút đáp án
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

        # 4. Nút quay lại
        if hasattr(self, "Quay_lai"):
            self.Quay_lai.clicked.connect(self.quay_lai)

        self.load_question()

    def load_question(self):
        """Reset giao diện khi sang câu mới"""
        data = self.quiz_data[self.current_index]
        self.label_cauhoi.setText(data["question"])

        # Progress bar
        phan_tram = int(((self.current_index + 1) / len(self.quiz_data)) * 100)
        self.progressBar.setValue(phan_tram)

        # Reset nút đáp án
        for btn in self.buttons:
            btn.setEnabled(True)
            btn.setStyleSheet("")
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)

        # Load options
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
                btn.setStyleSheet("""
                    background-color: #58CC02; 
                    color: white; 
                    border-radius: 15px; 
                    font-weight: bold; 
                    border-bottom: 4px solid #58CC02;
                """)
            elif i == idx:
                btn.setStyleSheet("""
                    background-color: #FF4B4B; 
                    color: white; 
                    border-radius: 15px; 
                    font-weight: bold; 
                    border-bottom: 4px solid #BB1932;
                """)

            btn.setEnabled(False)

    def next_question(self):
        """Chuyển câu hoặc kết thúc bài"""
        tong_so_cau_thuc_te = len(self.quiz_data)

        if self.current_index < tong_so_cau_thuc_te - 1:
            self.current_index += 1
            self.load_question()
        else:
            diem_can_thiet = 5
            passed = self.score >= diem_can_thiet

            # LUÔN lưu lịch sử dù đạt hay không
            self.luu_lich_su(passed)

            if passed:
                self.mo_khoa_bai_tiep_theo()
                QtWidgets.QMessageBox.information(
                    self,
                    "Tuyệt vời!",
                    f"Bạn đạt {self.score}/{tong_so_cau_thuc_te} điểm!\nBài tiếp theo đã được mở khóa."
                )
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Chưa đủ điểm",
                    f"Bạn đạt {self.score}/{tong_so_cau_thuc_te}.\nHãy cố gắng đạt ít nhất {diem_can_thiet} câu để mở bài tiếp theo!"
                )

            if self.main_window:
                self.main_window.show()

            self.close()

    def prev_question(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_question()

    def quay_lai(self):
        if self.main_window:
            self.main_window.show()
        self.close()

    def mo_khoa_bai_tiep_theo(self):
        """Chỉ mở khóa bài tiếp theo, KHÔNG lưu lịch sử ở đây"""
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

        if "unlocked_lessons" not in data:
            data["unlocked_lessons"] = [1]

        next_lesson = self.lesson_index + 1
        if next_lesson not in data["unlocked_lessons"]:
            data["unlocked_lessons"].append(next_lesson)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def luu_lich_su(self, passed):
        """Lưu lịch sử làm bài (luôn lưu kể cả không đạt)"""
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

        if "history" not in data:
            data["history"] = []

        history_entry = {
            "lesson": self.lesson_index,
            "score": self.score,
            "total": len(self.quiz_data),
            "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "passed": passed
        }

        data["history"].append(history_entry)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)