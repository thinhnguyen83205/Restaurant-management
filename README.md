# Hệ Thống Quản Lý Nhà Hàng (Restaurant Management System)

Dự án phần mềm **Quản lý nhà hàng** được xây dựng bằng ngôn ngữ **Python**, giúp số hóa quy trình vận hành cơ bản tại quán ăn hoặc nhà hàng nhỏ như quản lý thực đơn, theo dõi bàn ăn, gọi món, tính tiền và báo cáo doanh thu.

---

## Bài Toán & Mục Tiêu Dự Án

Trong quá trình vận hành thủ công, nhà hàng thường gặp khó khăn trong việc theo dõi bàn trống, nhầm lẫn khi ghi nhận món ăn và mất thời gian cộng sổ cuối ngày. Phần mềm này giải quyết các vấn đề trên thông qua 4 nhóm nghiệp vụ chính:

* **Quản lý thực đơn (Menu):** Thêm món mới, cập nhật giá bán, ngừng phục vụ món và phân loại theo nhóm (Khai vị, Món chính, Đồ uống).
* **Quản lý bàn ăn (Tables):** Kiểm soát trạng thái từng bàn theo thời gian thực (**Trống** / **Đang phục vụ**), hỗ trợ chuyển bàn hoặc gộp bàn linh hoạt.
* **Gọi món & Thanh toán (Orders):** Mở hóa đơn cho từng bàn, thêm/bớt số lượng món ăn, tự động tính tổng tiền, áp dụng giảm giá và xuất hóa đơn chi tiết.
* **Thống kê doanh thu (Reports):** Lưu trữ toàn bộ lịch sử hóa đơn và tính tổng doanh thu theo ngày hoặc theo món bán chạy.

---

## Cấu Trúc Thư Mục Dự Án

```text
project/
├── venv/                  # Môi trường ảo Python
├── data/                  # Cơ sở dữ liệu lưu trữ dạng JSON
│   ├── menu.json          # Danh sách món ăn và đơn giá
│   └── orders.json        # Lịch sử các hóa đơn đã thanh toán
├── models/                # Các lớp định nghĩa đối tượng dữ liệu
│   ├── dish.py            # Đối tượng Món ăn
│   ├── table.py           # Đối tượng Bàn ăn
│   └── order.py           # Đối tượng Hóa đơn
├── services/              # Xử lý logic nghiệp vụ
│   ├── menu_service.py    # Nghiệp vụ quản lý thực đơn
│   ├── order_service.py   # Nghiệp vụ gọi món và thanh toán
│   └── report_service.py  # Nghiệp vụ thống kê doanh thu
├── main.py                # Tệp khởi chạy chính (Giao diện menu)
├── requirements.txt       # Danh sách thư viện cài đặt thêm
├── CODING_RULES.md        # Quy chuẩn viết code của dự án
└── README.md              # Tài liệu mô tả và hướng dẫn sử dụng
```

---

## Yêu Cầu Cài Đặt

* **Ngôn ngữ:** Python 3.8 trở lên.
* **Trình soạn thảo:** Visual Studio Code hoặc PyCharm.

---

## Hướng Dẫn Khởi Chạy

### Bước 1: Kích hoạt môi trường ảo
Mở Terminal tại thư mục gốc của dự án và chạy lệnh tương ứng:

* **Windows:**
  ```bash
  venv\Scripts\activate
  ```
* **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### Bước 2: Cài đặt thư viện phụ thuộc (nếu có)
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy chương trình
```bash
python main.py
```

---

## Quy Chuẩn Phát Triển

Vui lòng đọc kỹ tệp `CODING_RULES.md` trước khi bổ sung tính năng mới để đảm bảo mã nguồn thống nhất và dễ bảo trì.
