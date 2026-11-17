# Hệ Thống Quản Lý Nhà Hàng

Ứng dụng dòng lệnh viết bằng **Python** giúp quán ăn, nhà hàng nhỏ quản lý **thực đơn**, **bàn ăn**, **gọi món**, **thanh toán** và **thống kê doanh thu**, thay cho việc ghi chép bằng sổ tay.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Thư viện ngoài](https://img.shields.io/badge/th%C6%B0%20vi%E1%BB%87n%20ngo%C3%A0i-kh%C3%B4ng-brightgreen)

---

##  Mục lục

1. [Bài toán](#-bài-toán)
2. [Tính năng](#-tính-năng)
3. [Cài đặt và chạy](#-cài-đặt-và-chạy)
4. [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
5. [Cấu trúc dự án](#-cấu-trúc-dự-án)
6. [Kiến trúc](#-kiến-trúc)
7. [Dữ liệu](#-dữ-liệu)
8. [Lỗi thường gặp](#-lỗi-thường-gặp)
9. [Giới hạn và hướng phát triển](#-giới-hạn-và-hướng-phát-triển)
10. [Thành viên nhóm](#-thành-viên-nhóm)

---

## Bài toán

Khi vận hành thủ công, nhà hàng thường gặp các vấn đề:

* Khó biết bàn nào đang trống, bàn nào đang có khách.
* Ghi nhầm món, tính sai tiền khi khách gọi thêm hoặc bớt món.
* Mất thời gian cộng sổ cuối ngày, không biết món nào bán chạy.

Phần mềm giải quyết các vấn đề trên bằng cách số hóa toàn bộ quy trình từ lúc khách vào bàn đến khi thanh toán, đồng thời lưu lại lịch sử để thống kê.

---

## Tính năng

| Nhóm | Chức năng |
|---|---|
| **Thực đơn** | Xem toàn bộ hoặc theo nhóm (Khai vị, Món chính, Đồ uống) · Thêm món mới · Cập nhật giá · Ngừng bán / mở bán lại |
| **Bàn ăn** | Xem trạng thái 10 bàn (*Trống* / *Đang phục vụ*) kèm tạm tính · Chuyển bàn · Gộp bàn |
| **Gọi món** | Mở hóa đơn cho bàn · Thêm / bớt món (tự cộng dồn món trùng) · Hủy hóa đơn |
| **Thanh toán** | Tự động tính tiền · Giảm giá theo % · In hóa đơn chi tiết · Lưu lịch sử |
| **Thống kê** | Doanh thu hôm nay / theo ngày · Tổng hợp theo từng ngày · Top món bán chạy · Xem lại hóa đơn cũ |

---

## Cài đặt và chạy

**Yêu cầu:** Python 3.8 trở lên ([tải tại đây](https://www.python.org/downloads/)). Không cần cài thêm thư viện.

### Bước 1: Tải mã nguồn

```bash
git clone https://github.com/thinhnguyen83205/Restaurant-management.git
cd Restaurant-management
```

### Bước 2: Tạo và kích hoạt môi trường ảo *(tùy chọn)*

```bash
python -m venv venv
```

| Hệ điều hành | Lệnh kích hoạt |
|---|---|
| Windows | `venv\Scripts\activate` |
| macOS / Linux | `source venv/bin/activate` |

Kích hoạt thành công khi đầu dòng Terminal hiện `(venv)`.

### Bước 3: Cài thư viện

```bash
pip install -r requirements.txt
```

> Hiện dự án chỉ dùng thư viện chuẩn của Python nên bước này không cài gì thêm.

### Bước 4: Chạy chương trình

```bash
python main.py
```

---

## Hướng dẫn sử dụng

### Màn hình chính

```text
============================================================
      HỆ THỐNG QUẢN LÝ NHÀ HÀNG
============================================================
1. Quản lý thực đơn
2. Quản lý bàn ăn
3. Gọi món & thanh toán
4. Thống kê doanh thu
0. Thoát
```

### Quy trình phục vụ một bàn

| Bước | Thao tác | Kết quả |
|---|---|---|
| 1. Mở hóa đơn | `3` → `1` → nhập số bàn | Bàn chuyển sang *Đang phục vụ* |
| 2. Gọi món | `3` → `2` → số bàn → mã món (vd `M004`) → số lượng | Món được thêm vào hóa đơn; gọi lại món cũ sẽ cộng dồn số lượng |
| 3. Bớt món *(nếu cần)* | `3` → `3` → số bàn → mã món → số lượng bớt | Số lượng về 0 thì món bị xóa khỏi hóa đơn |
| 4. Giảm giá *(nếu có)* | `3` → `5` → số bàn → phần trăm (0 – 100) | Tổng tiền được tính lại |
| 5. Thanh toán | `3` → `6` → số bàn | In hóa đơn, lưu vào lịch sử, bàn trở về *Trống* |

### Hóa đơn mẫu

```text
------------------------------------------------------------
HÓA ĐƠN HD0001  |  Bàn 1
Giờ vào: 2026-11-17 12:30:05
Thanh toán: 2026-11-17 13:10:42
------------------------------------------------------------
M004   Phở bò tái                 2 x    65,000đ =    130,000đ
M008   Trà đá                     3 x     5,000đ =     15,000đ
------------------------------------------------------------
Tạm tính:                                           145,000đ
Giảm giá (10%):                                     -14,500đ
TỔNG CỘNG:                                          130,500đ
------------------------------------------------------------
```

### Chuyển bàn và gộp bàn

| Chức năng | Thao tác | Điều kiện |
|---|---|---|
| **Chuyển bàn** | `2` → `2` → bàn cũ → bàn mới | Bàn mới phải **đang trống** |
| **Gộp bàn** | `2` → `3` → bàn nguồn → bàn đích | Cả hai bàn **đang phục vụ**; bàn nguồn trở về trống |

---

## Cấu trúc dự án

```text
Restaurant-management/
├── data/                      # Dữ liệu lưu dạng JSON
│   ├── menu.json              # Danh sách món ăn và đơn giá
│   └── orders.json            # Lịch sử hóa đơn đã thanh toán
├── models/                    # Lớp định nghĩa dữ liệu
│   ├── __init__.py            # Gom các lớp để import gọn
│   ├── dish.py                # Dish: món ăn
│   ├── table.py               # DiningTable: bàn ăn
│   └── order.py               # Order, OrderItem: hóa đơn
├── services/                  # Xử lý nghiệp vụ
│   ├── __init__.py
│   ├── menu_service.py        # Quản lý thực đơn
│   ├── order_service.py       # Quản lý bàn, gọi món
│   ├── payment_service.py     # Tính tiền, giảm giá, lưu hóa đơn
│   └── report_service.py      # Thống kê doanh thu
├── main.py                    # Điểm khởi chạy, giao diện menu
├── requirements.txt           # Thư viện cần cài (hiện không có)
├── .gitignore                 # Bỏ qua venv/, __pycache__/ khi commit
├── CODING_RULES.md            # Quy tắc viết code
├── TEAM_TASKS.md              # Phân công công việc nhóm
└── README.md                  # Tài liệu này
```

---

## Kiến trúc

Dự án chia làm 3 tầng, **tầng trên chỉ gọi tầng dưới**:

```text
┌────────────────────────────────────────────────┐
│  main.py          Giao diện: nhập / in kết quả │
└───────────────────────┬────────────────────────┘
                        ▼
┌────────────────────────────────────────────────┐
│  services/        Nghiệp vụ: xử lý, tính toán, │
│                   đọc / ghi file JSON          │
└───────────────────────┬────────────────────────┘
                        ▼
┌────────────────────────────────────────────────┐
│  models/          Dữ liệu: Dish, DiningTable,  │
│                   Order, OrderItem             │
└────────────────────────────────────────────────┘
```

Quan hệ giữa các service (một chiều, không import vòng):

```text
order_service ──► menu_service
      │
      └────────► payment_service ◄── report_service
```

* `services/` **không** dùng `print()` / `input()`; khi dữ liệu sai sẽ `raise ValueError` để `main.py` hiển thị lỗi.
* Chi tiết quy ước xem tại [`CODING_RULES.md`](CODING_RULES.md).

---

## Dữ liệu

### `data/menu.json`

```json
{
    "dish_id": "M004",
    "name": "Phở bò tái",
    "category": "Món chính",
    "price": 65000,
    "is_available": true
}
```

| Trường | Ý nghĩa |
|---|---|
| `dish_id` | Mã món, dạng `M001`, tự sinh khi thêm món |
| `name` | Tên món |
| `category` | `Khai vị`, `Món chính` hoặc `Đồ uống` |
| `price` | Đơn giá (VNĐ) |
| `is_available` | `true` đang bán, `false` ngừng bán |

### `data/orders.json`

Mỗi hóa đơn đã thanh toán gồm: `order_id` (dạng `HD0001`), `table_number`, `created_at`, `paid_at`, `items` (danh sách món), `discount` (%), `subtotal` (trước giảm giá), `total` (phải trả).

**Mẹo:**
* Sửa trực tiếp `menu.json` để nhập thực đơn ban đầu.
* Xóa lịch sử doanh thu: thay nội dung `orders.json` bằng `[]`.

---

## Lỗi thường gặp

| Lỗi | Cách khắc phục |
|---|---|
| `'python' is not recognized...` | Dùng `py main.py`, hoặc cài lại Python và tích **Add Python to PATH** |
| `running scripts is disabled on this system` khi kích hoạt `venv` | Chạy `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` rồi kích hoạt lại |
| `ModuleNotFoundError: No module named 'models'` | Chạy lệnh tại **thư mục gốc** dự án (cùng chỗ với `main.py`) |
| Tiếng Việt bị lỗi font trong Terminal | Chạy `chcp 65001` trước khi chạy chương trình (Windows) |

---

## Giới hạn và hướng phát triển

**Giới hạn hiện tại:**

* Trạng thái bàn và hóa đơn **chưa thanh toán** chỉ lưu trong bộ nhớ; thoát chương trình sẽ mất.
* Số bàn cố định là 10 (đổi bằng hằng `MAX_TABLES` trong `services/order_service.py`).
* Chưa tính thuế VAT, chưa có đăng nhập / phân quyền.

**Hướng phát triển:**

- [ ] Lưu trạng thái bàn ra `data/tables.json`
- [ ] Thêm thuế VAT (`TAX_RATE`)
- [ ] Xuất hóa đơn ra file `.txt` / `.pdf`
- [ ] Viết unit test trong thư mục `tests/`
- [ ] Làm giao diện đồ họa (Tkinter) hoặc web

---

## Thành viên nhóm

| Thành viên | Phụ trách |
|---|---|
| Nguyễn Tiến Thịnh | Quản lý Git, `models/`, menu chính |
| Thu Huyền | Thực đơn: `menu_service.py` |
| Lý Minh Đức| Bàn ăn: `order_service.py` (phần quản lý bàn) |
| Trần Đức Minh | Gọi món: `order_service.py` (phần gọi món) |
| Nguyễn Đại Ân | Thống kê, kiểm thử: `report_service.py` |
| Nguyễn Quốc Huy | Thanh toán: `payment_service.py` |

Phân công chi tiết và quy trình Git xem tại [`TEAM_TASKS.md`](TEAM_TASKS.md).

### Đóng góp

1. Đọc [`CODING_RULES.md`](CODING_RULES.md) trước khi viết code.
2. Tạo nhánh riêng: `git checkout -b feature/<tên-chức-năng>`.
3. Commit theo mẫu: `feat: ...`, `fix: ...`, `docs: ...`.
4. Tạo Pull Request vào `main` để nhóm trưởng review.