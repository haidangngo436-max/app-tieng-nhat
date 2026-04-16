# Ứng Dụng Học Tiếng Nhật

Một ứng dụng học tiếng Nhật được xây dựng với PyQt5.

## Cấu Trúc Thư Mục

```
app-tieng-nhat/
├── src/                      # Mã nguồn Python
│   ├── main.py              # Điểm vào chính
│   ├── main_window.py       # Cửa sổ chính (học bài)
│   ├── login_window.py      # Cửa sổ đăng nhập
│   ├── register_window.py   # Cửa sổ đăng ký
│   ├── quizzcode.py         # Logic quiz/bài tập
│   └── history_window.py    # Cửa sổ lịch sử làm bài
│
├── ui/                       # File giao diện UI (PyQt Designer)
│   ├── mainchinh.ui         # UI cửa sổ chính
│   ├── manhinhdangnhap.ui   # UI đăng nhập
│   ├── dang ky tai khoan.ui # UI đăng ký
│   ├── quizzcheckui.ui      # UI quiz
│   └── quiz/                # UI các bài quiz
│       ├── quiz_b1.ui
│       ├── quiz_b2.ui
│       ├── ...
│       └── quiz_b10.ui
│
├── styles/                   # Style sheets (CSS)
│   └── style_main.qss       # Stylesheet chính
│
├── data/                     # Dữ liệu ứng dụng
│   ├── data_quizz.json      # Dữ liệu bài tập/quiz
│   ├── database.txt         # Dữ liệu tài khoản người dùng
│   └── progress/            # Tiến độ học tập của người dùng
│       ├── progress_user1.json
│       ├── progress_user2.json
│       └── ...
│
├── assets/                   # Tài nguyên (hình ảnh, v.v.)
│   └── picture/             # Thư mục hình ảnh
│
├── docs/                     # Tài liệu
│   ├── 12.txt
│   └── Bản sao 12.txt
│
└── README.md                # File này
```

## Tính Năng

- ✅ Đăng nhập/Đăng ký tài khoản
- ✅ Học các bài tiếng Nhật (Hiragana, Katakana, v.v.)
- ✅ Làm bài tập/quiz
- ✅ Theo dõi tiến độ học tập
- ✅ Xem lịch sử làm bài

## Lưu Ý

- Tiến độ học của mỗi người dùng được lưu riêng biệt trong `data/progress/progress_[username].json`
- Dữ liệu tài khoản được lưu trong `data/database.txt`
- Các bài quiz được định nghĩa trong `data/data_quizz.json`
