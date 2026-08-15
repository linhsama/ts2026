# 🎓 Tra Cứu Điểm Thi THPT & Tính Điểm Học Bạ 2026 (TS2026)

Ứng dụng web hiện đại, siêu tốc và trực quan phục vụ công tác tư vấn tuyển sinh đại học: **Tra cứu điểm thi tốt nghiệp THPT theo Số Báo Danh (SBD)**, **tự động tính điểm tất cả các tổ hợp môn xét tuyển**, và **bảng tính điểm xét tuyển học bạ 3 năm THPT**.

---

## ✨ Tính Năng Nổi Bật

### 1. 🔍 Tra Cứu Điểm Thi THPT Theo SBD Siêu Tốc
* **Tốc độ dưới 0.2 giây**: Tích hợp backend Python đa luồng (`server.py`) kiểm tra song song các năm, khắc phục 100% lỗi chặn CORS.
* **Bộ nhớ đệm thông minh (`scoreCache`)**: Tra lại các SBD đã xem tức thì không cần tải lại dữ liệu.
* **Bảng điểm ngang 12 môn**: Hiển thị đầy đủ 12 môn thi (Ngữ văn, Toán, Vật lí, Hóa học, Sinh học, Lịch sử, Địa lí, GD KTPL, Tin học, CNCN, CNNN, Ngoại ngữ).

### 2. 🏆 Tự Động Tính & Tổng Hợp Tổ Hợp Môn
* **Dải Tag Liền Mạch 1 Dòng (Horizontal Tag Ribbon)**:
  * 👑 **Tag Tổ hợp cao nhất (Top 1)**: Nổi bật với huy hiệu xanh đại học, điểm số vàng hổ phách.
  * 🧮 **Tag Toán, Văn + 1 môn max**: Thể hiện điểm số nền tảng Toán + Văn.
  * 🏷️ **Dải tất cả tổ hợp**: Quét tự động 33 tổ hợp xét tuyển 2026 (A00–D84, X01–X78).
* **Hover Tooltip Chi Tiết**: Rê chuột vào bất kỳ tag tổ hợp nào để xem công thức và điểm số chi tiết từng môn cấu thành.

### 3. 📝 Bảng Tính Điểm Học Bạ 3 Năm (3x3 Realtime)
* **Gõ số thông minh**: Gõ 2 số tự động chuyển thành số thập phân (VD: `85` ➔ `8.5`) và tự động nhảy sang ô tiếp theo.
* **Điều hướng phím tắt**: Hỗ trợ đầy đủ phím mũi tên (↑ ↓ ← →), <kbd>Enter</kbd>, <kbd>Space</kbd>, <kbd>Backspace</kbd>.
* **Chân bảng chuẩn mực (Success Theme)**: Đồng bộ độ cao `h-9` với thân bảng, 4 ô điểm trung bình và tổng điểm xét tuyển học bạ nổi bật với tông màu xanh lá **Emerald Success**.

### 4. 🔄 Nút "Nhập lại" & Phím tắt Esc
* Xóa trắng 100% dữ liệu (SBD, 12 môn, tổ hợp, bảng học bạ) và **tự động focus ngay về ô Số Báo Danh** để tiếp tục thí sinh mới.

### 5. 🕒 Quản Lý Lịch Sử Tra Cứu (LocalStorage)
* Tự động lưu trữ tối đa 50 lượt tra cứu / tính điểm gần nhất.
* Nạp lại dữ liệu hoặc xóa lịch sử chỉ với 1 cú click.

---

## 🚀 Hướng Dẫn Sử Dụng Trong Mạng LAN Nội Bộ

### Bước 1: Khởi động máy chủ (Trên máy Host của bạn)
Bạn có 2 lựa chọn:

* **Cách 1 (Khuyên dùng - Tự động chạy ngầm mỗi khi bật máy tính)**:
  * Nhấp đúp vào file **`install_autostart.bat`** (chạy 1 lần duy nhất).
  * Server sẽ tự động thêm vào Windows Startup và chạy ngầm trên cổng `8080`.
* **Cách 2 (Chạy trực tiếp có xem log)**:
  * Nhấp đúp vào file **`run.bat`**.

---

### Bước 2: Sử dụng trên các máy tính / điện thoại khác cùng mạng Wi-Fi / LAN
* Bạn chỉ cần gửi **1 file duy nhất** là **[`launcher.html`](./launcher.html)** sang máy khác (qua Zalo, USB, chia sẻ mạng nội bộ...).
* Người nhận chỉ cần **nhấp đúp mở file `launcher.html`**:
  * Trình duyệt sẽ **tự động dò tìm máy chủ nội bộ và mở trang web ngay lập tức** mà **hoàn toàn không cần phải nhập địa chỉ IP**!

---

## 📁 Cấu Trúc Thư Mục Dự Án

```text
ts2026/
├── index.html               # Giao diện chính của ứng dụng (phóng to 125%, responsive)
├── launcher.html            # File gửi cho máy khác để mở web tự động trong mạng LAN
├── server.py                # Backend Python đa luồng xử lý API và đồng bộ IP mạng LAN
├── run.bat                  # File khởi động server trực tiếp xem console log
├── install_autostart.bat    # Cài đặt server tự động khởi động ngầm cùng Windows
├── run_background.vbs       # Khởi động server chạy ngầm không hiện cửa sổ đen
├── stop_server.bat          # Dừng server đang chạy ngầm trên cổng 8080
├── uninstall_autostart.bat  # Gỡ bỏ tính năng tự khởi động cùng Windows
├── .gitignore               # Cấu hình bỏ qua các file tạm của Python
└── README.md                # Tài liệu hướng dẫn sử dụng chi tiết
```

---

## 🌐 Triển Khai Trực Tuyến
* Ứng dụng cũng đã được triển khai tự động qua GitHub Pages:
  👉 **`https://linhsama.github.io/ts2026/`**

---

© 2026 Tuyển Sinh Đại Học - Thiết kế tinh gọn, hiệu năng cao, tối ưu cho máy tính và thiết bị di động.
