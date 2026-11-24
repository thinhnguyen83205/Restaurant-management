# Phân Công Công Việc — Dự Án Quản Lý Nhà Hàng

Tài liệu này chia công việc cho 6 thành viên, quy định thứ tự làm và quy trình Git. Mỗi người phụ trách trọn một chức năng (service + màn hình trong `main.py`) để có thể tự trình bày phần của mình.

> Đọc kỹ [`CODING_RULES.md`](CODING_RULES.md) trước khi bắt đầu viết code.

---

## 1. Thành viên và vai trò

| Mã | Họ tên | Vai trò | Nhánh Git |
|---|---|---|---|
| NT | Nguyễn Tiến Thịnh | Nhóm trưởng — Quản lý Git, review code, làm nền tảng | `feature/models` |
| TV2 | Thu Huyền | Thực đơn | `feature/menu` |
| TV3 | Lý Minh Đức | Bàn ăn | `feature/table` |
| TV4 | Trần Đức Minh | Gọi món | `feature/order` |
| TV5 | Nguyễn Đại Ân | Thống kê, kiểm thử, tài liệu | `feature/report` |
| TV6 | Nguyễn Quốc Huy | Thanh toán | `feature/payment` |

---

## 2. Bảng phân công chi tiết

### Nhóm trưởng — Quản lý Git, review code, làm nền tảng

**File phụ trách:**
- `models/dish.py`, `models/table.py`, `models/order.py`
- `models/__init__.py`, `services/__init__.py`
- `.gitignore`, `requirements.txt`
- `main.py` — chỉ hàm `main()`

**Công việc:**
- [x] Viết các lớp `Dish`, `DiningTable`, `Order`, `OrderItem` (thuộc tính, `to_dict()`, `from_dict()`)
- [x] Viết hàm `main()`: menu chính nối 4 màn hình con
- [x] Tạo nhánh, mời thành viên, bật bảo vệ nhánh `main` *(nhánh và thành viên: đã có; bảo vệ nhánh `main`: cần tự kiểm tra lại trên GitHub)*
- [x] Review và merge Pull Request của các thành viên *(đã merge PR #1 – #12)*

---

### TV2 — Thực đơn

**File phụ trách:**
- `services/menu_service.py`
- `data/menu.json`

**Công việc:**
- [x] `load_menu()`, `save_menu()` — đọc/ghi `menu.json`
- [x] `find_dish_by_id()` — **làm đầu tiên**, TV4 cần dùng
- [x] `add_new_dish()` — thêm món
- [x] `update_dish_price()` — sửa giá
- [x] `set_dish_availability()` — ngừng / mở bán món
- [x] `get_all_dishes()`, `get_dishes_by_category()` — lọc theo nhóm
- [x] Nhập thực đơn mẫu vào `data/menu.json`
- [x] Trong `main.py`: `show_menu_management()`, `print_dishes()`, `choose_category()`

---

### TV3 — Bàn ăn

**File phụ trách:**
- `services/order_service.py` — **chỉ phần `# ---------- Quản lý bàn ----------`**

**Công việc:**
- [x] `get_all_tables()`, `get_table()` — lấy danh sách / một bàn
- [x] `get_open_order()` — lấy hóa đơn đang mở của bàn (TV4 dùng)
- [x] `generate_order_id()` — sinh mã hóa đơn `HD0001` (dùng `load_paid_orders()` của TV6)
- [x] `open_order()` — mở hóa đơn, chuyển bàn sang *Đang phục vụ*
- [x] `release_table()` — trả bàn về trạng thái trống
- [x] `transfer_table()` — chuyển bàn
- [x] `merge_tables()` — gộp bàn
- [x] Trong `main.py`: `show_table_management()`, `print_tables()`

---

### TV4 — Gọi món

**File phụ trách:**
- `services/order_service.py` — **chỉ phần `# ---------- Gọi món ----------` và `# ---------- Thanh toán theo bàn ----------`**

**Công việc:**
- [x] `merge_item()` — cộng dồn số lượng nếu món đã có trong hóa đơn
- [x] `add_item_to_order()` — thêm món (dùng `find_dish_by_id()` của TV2)
- [x] `remove_item_from_order()` — bớt món, xóa dòng khi số lượng về 0
- [x] `apply_discount()`, `checkout()`, `cancel_order()` — hàm theo số bàn, gọi sang `payment_service` của TV6
- [x] Trong `main.py`: `show_order_management()` (màn hình chung, gọi hàm của TV3 và TV6), `input_int()`

---

### TV5 — Thống kê, kiểm thử, tài liệu

**File phụ trách:**
- `services/report_service.py`
- `README.md`

**Công việc:**
- [x] `get_revenue_by_date()` — doanh thu theo ngày
- [x] `get_daily_revenue_summary()` — tổng hợp theo từng ngày
- [x] `get_best_selling_dishes()` — món bán chạy
- [x] `get_total_revenue()` — tổng doanh thu
- [x] Trong `main.py`: `show_reports()`
- [x] Viết kịch bản kiểm thử (mục 6) và chạy thử toàn bộ chương trình trước khi nộp *(đã chạy 17/17 kịch bản đạt)*
- [x] Cập nhật `README.md` khi có thay đổi

---

### TV6 — Thanh toán

**File phụ trách:**
- `services/payment_service.py` — **toàn bộ file**
- `data/orders.json`

**Công việc:**
- [x] `load_paid_orders()`, `save_paid_orders()` — đọc/ghi `orders.json` — **làm đầu tiên**, TV3 và TV5 cần dùng
- [x] `calculate_subtotal()`, `calculate_total()`, `recalculate_order()` — tính tiền
- [x] `set_order_discount()` — kiểm tra và áp dụng giảm giá theo %
- [x] `pay_order()` — chốt tiền, ghi thời điểm thanh toán, lưu lịch sử
- [x] Trong `main.py`: `print_order()`, `format_money()` — **làm sớm**, TV3, TV4, TV5 đều dùng để in

> `payment_service.py` **không** được import `order_service` để tránh lỗi import vòng.

---

## 3. Thứ tự thực hiện

| Giai đoạn | Ai làm | Nội dung | Điều kiện để sang giai đoạn sau |
|---|---|---|---|
| **1. Nền tảng** | Nhóm trưởng | Viết `models/`, `__init__.py`, `.gitignore`, hàm `main()`; đẩy lên `main` | `models/` đã có trên nhánh `main` |
| **2. Song song** | TV2 – TV6 | Mỗi người làm trên nhánh riêng | Mỗi người tạo Pull Request |
| **3. Ghép & kiểm thử** | Cả nhóm | Nhóm trưởng merge; TV5 chạy thử toàn bộ; cả nhóm sửa lỗi | Chạy hết kịch bản kiểm thử không lỗi |

**Thứ tự merge:** `models` → `menu` → `payment` → `table` → `order` → `report`

---

## 4. Quy trình Git

### Sơ đồ nhánh

```text
main                 ← chỉ nhóm trưởng merge vào
├── feature/models   ← Nhóm trưởng
├── feature/menu     ← TV2
├── feature/table    ← TV3
├── feature/order    ← TV4
├── feature/report   ← TV5
└── feature/payment  ← TV6
```

### Nhóm trưởng thiết lập (làm 1 lần)

1. GitHub → *Settings → Collaborators* → mời 4 thành viên.
2. GitHub → *Settings → Branches* → bảo vệ nhánh `main`, bắt buộc qua Pull Request.

### Thành viên làm hằng ngày

```bash
# Lần đầu
git clone https://github.com/thinhnguyen83205/Restaurant-management.git
cd Restaurant-management
git checkout -b feature/menu          # đổi theo nhánh của mình

# Mỗi lần làm việc
git pull origin main                  # lấy code mới nhất đã merge
# ... viết code, chạy thử: python main.py ...
git add services/menu_service.py main.py
git commit -m "feat: thêm chức năng cập nhật giá món"
git push -u origin feature/menu
# → lên GitHub tạo Pull Request vào main
```

### Mẫu commit

| Loại | Dùng khi | Ví dụ |
|---|---|---|
| `feat` | Thêm tính năng | `feat: thêm chức năng gộp bàn` |
| `fix` | Sửa lỗi | `fix: sai tổng tiền khi giảm giá` |
| `docs` | Sửa tài liệu | `docs: cập nhật README` |
| `refactor` | Sửa code, không đổi chức năng | `refactor: tách hàm tính tiền` |

### Checklist review Pull Request (nhóm trưởng)

- [x] Chạy `python main.py` không lỗi
- [x] Không có `print()` / `input()` trong `services/`
- [x] Lỗi được báo bằng `raise ValueError(...)`
- [x] Tên biến, hàm theo `snake_case`; lớp theo `PascalCase`
- [x] Hàm trong `services/` có docstring
- [x] Chỉ sửa trong file / khu vực được phân công
- [x] Không commit `venv/`, `__pycache__/`

---

## 5. Quy tắc tránh conflict

* **Chỉ viết trong khu vực của mình.** `order_service.py` (TV3, TV4) và `main.py` (cả nhóm) có nhiều người cùng sửa — mỗi người chỉ thêm code trong phần được đánh dấu `# ---------- ... ----------` của mình.
* **Không tự ý sửa code của người khác.** Thấy lỗi → báo người phụ trách hoặc nhóm trưởng.
* **Pull thường xuyên.** Sau mỗi lần nhóm trưởng merge, các thành viên chạy `git pull origin main` vào nhánh của mình.
* **Commit nhỏ, thường xuyên.** Mỗi commit làm một việc, dễ review và dễ sửa khi có conflict.

---

## 6. Kịch bản kiểm thử (TV5 phụ trách)

| # | Chức năng | Thao tác | Kết quả mong đợi | Đạt |
|---|---|---|---|---|
| 1 | Thực đơn | Thêm món "Bánh flan", nhóm Khai vị, giá 20000 | Món mới có mã `M011` | [x] |
| 2 | Thực đơn | Thêm món với giá `-5000` hoặc `abc` | Báo lỗi, chương trình không dừng | [x] |
| 3 | Thực đơn | Ngừng bán `M004` rồi gọi món `M004` | Báo "đã ngừng phục vụ" | [x] |
| 4 | Bàn | Mở hóa đơn bàn 1 | Bàn 1 chuyển *Đang phục vụ* | [x] |
| 5 | Bàn | Mở hóa đơn bàn 1 lần nữa | Báo "Bàn 1 đang phục vụ" | [x] |
| 6 | Bàn | Nhập bàn số 99 | Báo số bàn không hợp lệ | [x] |
| 7 | Bàn | Chuyển bàn 1 → bàn 5 | Bàn 1 trống, bàn 5 đang phục vụ | [x] |
| 8 | Bàn | Gộp bàn 2 vào bàn 5 | Món cộng dồn, bàn 2 trống | [x] |
| 9 | Gọi món | Gọi `M004` x2, gọi thêm `M004` x1 | Một dòng `M004` số lượng 3 | [x] |
| 10 | Gọi món | Bớt món đến số lượng 0 | Dòng món bị xóa khỏi hóa đơn | [x] |
| 11 | Thanh toán | Giảm giá 10% cho hóa đơn 145,000đ | Tổng cộng 130,500đ | [x] |
| 12 | Thanh toán | Giảm giá 150% | Báo lỗi 0 – 100% | [x] |
| 13 | Thanh toán | Thanh toán hóa đơn chưa có món | Báo không thể thanh toán | [x] |
| 14 | Thanh toán | Thanh toán bình thường | In hóa đơn, lưu vào `orders.json`, bàn trở về trống | [x] |
| 15 | Thống kê | Xem doanh thu hôm nay sau bước 14 | Đúng số hóa đơn và tổng tiền | [x] |
| 16 | Thống kê | Xem món bán chạy | Sắp xếp theo số lượng giảm dần | [x] |
| 17 | Thống kê | Tắt và mở lại chương trình, xem lịch sử | Hóa đơn cũ vẫn còn | [x] |

---

## 7. Theo dõi tiến độ

| Thành viên | Phần việc | Trạng thái | Hạn | Ghi chú |
|---|---|---|---|---|
| Nhóm trưởng | `models/`, `main()`, Git | done | | |
| TV2 | Thực đơn | done | | |
| TV3 | Bàn ăn | done | | |
| TV4 | Gọi món | done | | |
| TV5 | Thống kê, kiểm thử, tài liệu | done | | |
| TV6 | Thanh toán | done | | |

*Trạng thái:* cl: Chưa làm · dl: Đang làm · rv Chờ review · done:Đã merge