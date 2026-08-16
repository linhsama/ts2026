# 🎓 Tra Cứu Điểm Thi THPT & Tính Điểm Học Bạ 2026 (TS2026)

Ứng dụng web hiện đại, siêu tốc và trực quan phục vụ công tác tư vấn tuyển sinh đại học: **Tra cứu điểm thi tốt nghiệp THPT theo Số Báo Danh (SBD)**, **tự động tính điểm tất cả các tổ hợp môn xét tuyển**, và **bảng tính điểm xét tuyển học bạ 3 năm THPT**.

---

## ✨ Tính Năng Nổi Bật

### 1. 🔍 Tra Cứu Điểm Thi THPT Theo SBD Siêu Tốc
* **Tốc độ dưới 0.2 giây**: Tích hợp backend Python đa luồng (`server.py`) kiểm tra song song các năm, khắc phục 100% lỗi chặn CORS.
* **Bộ nhớ đệm thông minh (`scoreCache`)**: Tra lại các SBD đã xem tức thì không cần tải lại dữ liệu.
* **Bảng điểm ngang 12 môn**: Hiển thị đầy đủ 12 môn thi (Ngữ văn, Toán, Vật lí, Hóa học, Sinh học, Lịch sử, Địa lí, GD KTPL, Tin học, CNCN, CNNN, Ngoại ngữ).

### 2. 🏆 Tự Động Tính & Tổng Hợp Tổ Hợp Môn Chuẩn 2026
* **Bổ sung danh mục 33 tổ hợp xét tuyển 2026**: Hỗ trợ 33 tổ hợp xét tuyển (A00, A01, A02, A06, A07, B00, B02, B03, C00, C01, C02, C04, D01, D07, D08, D10, D14, D15, D66, D84, X01, X02, X06, X07, X10, X14, X21, X25, X26, X56, X70, X74, X78).
* **Dải Tag Liền Mạch 1 Dòng (Horizontal Tag Ribbon)**:
  * 👑 **Tag Tổ hợp cao nhất (Top 1)**: Nổi bật với huy hiệu xanh đại học, điểm số vàng hổ phách.
  * 🧮 **Tag Toán, Văn + 1 môn max**: Thể hiện điểm số nền tảng Toán + Văn.
  * 🏷️ **Dải tất cả tổ hợp**: Tự động tính toán và sắp xếp điểm từ cao xuống thấp, loại bỏ hoàn toàn sai số dấu phẩy động.
* **Hover Tooltip Chi Tiết**: Rê chuột vào bất kỳ tag tổ hợp nào để xem công thức và điểm số chi tiết từng môn cấu thành.

### 3. 📝 Bảng Tính Điểm Học Bạ 3 Năm Chuẩn Quy Chế Tuyển Sinh
* **Logic làm tròn chuẩn quy chế**:
  * ĐTB 3 năm từng môn làm tròn đến 2 chữ số thập phân (`.toFixed(2)`).
  * Tổng ĐTB chung 3 môn được tính bằng tổng của các ĐTB môn đã làm tròn (đảm bảo hiển thị toán học chính xác: VD `8.53 + 8.53 + 8.53 = 25.59`).
* **Gõ số thông minh**: 
  * Gõ 2 số tự động chuyển thành số thập phân (VD: `85` ➔ `8.5`, `05` hoặc `.5` ➔ `0.5`, `8.` ➔ `8.0`).
  * Gõ `10` ➔ `10.0` và tự động nhảy sang ô tiếp theo.
  * Rời ô (`blur`): gõ `8` ➔ tự động thành `8.0`.
* **Điều hướng phím tắt**: Hỗ trợ đầy đủ phím mũi tên (↑ ↓ ← →), <kbd>Enter</kbd>, <kbd>Space</kbd>, <kbd>Backspace</kbd>.
* **Chân bảng chuẩn mực (Success Theme)**: Đồng bộ độ cao `h-9` với thân bảng, 4 ô điểm trung bình và tổng điểm xét tuyển học bạ nổi bật với tông màu xanh lá **Emerald Success**.

### 4. ⚡ Luồng Focus Siêu Tốc & Nút "Nhập lại"
* **Tự động chuyển focus sau khi nhập xong**: Nhập xong ô thứ 9 (Môn 3 Lớp 12) hệ thống tự động lưu lịch sử và nhảy focus tới nút **"Nhập lại"** (Clear / Reset) có viền sáng nhận diện.
* **Nhấn <kbd>Enter</kbd> (hoặc <kbd>Space</kbd> / phím tắt <kbd>Esc</kbd>)**: Xóa trắng 100% dữ liệu và **tự động focus ngay về ô Tra Cứu SBD** (`sbdInput`), bôi đen sẵn sàng để nhập lượt tiếp theo siêu tốc.

### 5. 🕒 Quản Lý Lịch Sử Tra Cứu (LocalStorage)
* Tự động lưu trữ tối đa 50 lượt tra cứu / tính điểm gần nhất.
* Nạp lại dữ liệu hoặc xóa lịch sử chỉ với 1 cú click.

---

## 🚀 Hướng Dẫn Sử Dụng Trong Mạng LAN Nội Bộ

### Bước 1: Khởi động máy chủ (Trên máy Host)
Chỉ cần nhấp đúp vào **1 trong các file sau**:

* **🌟 Cách Khuyến Nghị (1-Click: Cài Tự Động Khởi Động & Chạy Ngầm Ngay)**:
  * Nhấp đúp vào file **`install_autostart.bat`** (hoặc `start_background.bat`).
  * ⚡ **Tác dụng kép**: Vừa thêm vào Windows Startup / Task Scheduler (mở máy là tự chạy), vừa bật server chạy ngầm ngay lập tức trên cổng `8080`.
  * 🛡️ **Hoàn toàn độc lập**: Bạn có thể tắt Antigravity, tắt IDE hoặc đóng cửa sổ console thoải mái, server vẫn hoạt động ngầm 24/7.
* **Cách Xem Log Trực Tiếp (Console Mode)**:
  * Nhấp đúp vào file **`run.bat`** (hiển thị toàn bộ log truy cập trực tiếp trên màn hình CMD).

> 💡 **Để tắt Server khi đang chạy ngầm**:
> * Nhấp đúp vào file **`stop_server.bat`**.
> 
> 🗑️ **Để gỡ bỏ tính năng tự khởi động cùng Windows**:
> * Nhấp đúp vào file **`uninstall_autostart.bat`**.

---

### Bước 2: Sử dụng trên các máy tính / điện thoại khác cùng mạng Wi-Fi / LAN
* **Mở khóa tường lửa (chỉ cần chạy 1 lần nếu máy khác không vào được)**:
  * Nhấp chuột phải vào file **`open_firewall_lan.bat`** và chọn **Run as administrator**.
* **Cách 1 (Mở tự động)**: Gửi file **[`ToolTS2026.html`](./ToolTS2026.html)** sang máy khác (qua Zalo, USB...). Người nhận chỉ cần nhấp đúp mở file `ToolTS2026.html`, trình duyệt sẽ tự động kết nối và mở trang web!
* **Cách 2 (Nhập trực tiếp trên trình duyệt máy tính hoặc điện thoại)**:
  Mở trình duyệt (Chrome, Safari, Edge...) và gõ địa chỉ IP máy chủ:
  👉 **`http://192.168.1.4:8080/`**

---

## 📁 Cấu Trúc Thư Mục Dự Án

```text
ts2026/
├── index.html               # Giao diện chính của ứng dụng tra cứu & tính điểm
├── ToolTS2026.html          # File launcher gửi cho máy khác để mở web tự động trong LAN
├── server.py                # Backend Python đa luồng xử lý API và đồng bộ IP mạng LAN
├── start_background.bat     # Khởi động server chạy ngầm không hiện cửa sổ console (1-click)
├── run_background.vbs       # Script VBS kích hoạt pythonw server.py
├── run.bat                  # Khởi động server trực tiếp xem console log
├── install_autostart.bat    # Cài đặt server tự động khởi động ngầm cùng Windows
├── stop_server.bat          # Dừng server đang chạy trên cổng 8080
├── uninstall_autostart.bat  # Gỡ bỏ tính năng tự khởi động cùng Windows
├── open_firewall_lan.bat    # Mở khóa tường lửa Windows (Firewall) cho mạng LAN
├── .gitignore               # Cấu hình bỏ qua các file tạm của Python
└── README.md                # Tài liệu hướng dẫn sử dụng chi tiết
```

---

## 🌐 Triển Khai Trực Tuyến
* Ứng dụng cũng đã được triển khai tự động qua GitHub Pages:
  👉 **`https://linhsama.github.io/ts2026/`**

---

© 2026 Tuyển Sinh Đại Học - Thiết kế tinh gọn, hiệu năng cao, tối ưu cho máy tính và thiết bị di động.

