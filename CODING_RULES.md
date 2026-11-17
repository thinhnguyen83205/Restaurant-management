Quy Tắc Viết Code — Dự Án Quản Lý Nhà Hàng

Tài liệu này quy định cách đặt tên, tổ chức thư mục, viết code và xử lý lỗi để mã nguồn luôn đồng nhất, dễ đọc và dễ bảo trì. Mọi thành viên cần đọc kỹ trước khi thêm tính năng mới.

1. Quy tắc đặt tên
Thành phần	Kiểu viết	Đúng	Sai
Tệp, thư mục	snake_case	menu_service.py, orders.json	MenuService.py, Order-History.json
Biến, hàm	snake_case	total_price, def add_new_dish():	TotalPrice, def Bill():
Lớp (class)	PascalCase	Dish, DiningTable, OrderItem	dish, dining_table
Hằng số	UPPER_SNAKE_CASE	MAX_TABLES = 10, MENU_FILE_PATH	maxTables
Hàm/biến nội bộ của module	Thêm _ ở đầu	_open_orders	—
Tên hàm bắt đầu bằng động từ: get_, find_, add_, update_, remove_, calculate_, load_, save_.
Hàm trả về True/False bắt đầu bằng is_ hoặc has_: is_empty(), is_available.
Toàn bộ tên tệp, biến, hàm, lớp viết bằng tiếng Anh không dấu.
Định dạng mã dữ liệu
Dữ liệu	Định dạng	Ví dụ
Mã món	M + 3 chữ số	M001, M012
Mã hóa đơn	HD + 4 chữ số	HD0001
Ngày	YYYY-MM-DD	2026-11-17
Ngày giờ	YYYY-MM-DD HH:MM:SS (hằng DATETIME_FORMAT)	2026-11-17 12:30:00
Tiền	Số nguyên, đơn vị VNĐ	65000
2. Cấu trúc và phân chia trách nhiệm

Dự án chia làm 3 tầng. Tầng trên chỉ được gọi tầng dưới, không gọi ngược lại.

text
main.py  ──►  services/  ──►  models/
(giao diện)   (nghiệp vụ)     (dữ liệu)
                  │
                  └──►  data/*.json
Thư mục / tệp	Được làm	Không được làm
models/	Khai báo thuộc tính, to_dict(), from_dict(), hàm kiểm tra đơn giản (is_empty())	Đọc/ghi file, tính toán nghiệp vụ, print(), input()
services/	Toàn bộ logic: thêm/sửa/xóa, tính tiền, đọc/ghi JSON, kiểm tra dữ liệu	print(), input()
main.py	Hiển thị menu, nhận input(), gọi service, in kết quả, bắt lỗi	Tính tiền, đọc/ghi file trực tiếp
data/	Chỉ chứa tệp JSON	Chứa code
Mỗi thư mục chứa code Python (models/, services/) phải có tệp __init__.py (có thể để trống).
Mỗi model phải có cặp hàm to_dict() và from_dict() (dùng @classmethod) để chuyển đổi với JSON.
Giá trị cố định (trạng thái bàn, nhóm món, số bàn tối đa…) khai báo thành hằng số ở đầu tệp, không viết trực tiếp chuỗi/số trong code.
3. Import
Đặt toàn bộ import ở đầu tệp, chia 3 nhóm, mỗi nhóm cách nhau 1 dòng trống:
Thư viện chuẩn (json, os, datetime)
Thư viện cài thêm (nếu có)
Module của dự án (models, services)
Dùng import tuyệt đối tính từ thư mục gốc dự án:
python
import json
import os

from models.dish import Dish
from services import menu_service
Không dùng from module import *.
4. Định dạng code
Thụt lề: 4 dấu cách, không dùng Tab.
Độ dài dòng: tối đa 79 ký tự (theo PEP 8). Xuống dòng bên trong dấu ngoặc khi quá dài.
Khoảng trắng: 1 dấu cách quanh toán tử (a = b + c), không đặt dấu cách ngay trong ngoặc (print("Hello")).
Dòng trống: 2 dòng trước/sau class hoặc hàm cấp cao; 1 dòng giữa các method trong class.
Chuỗi: dùng dấu nháy kép "...".
Tệp JSON thụt lề 4 dấu cách, giữ nguyên tiếng Việt có dấu (ensure_ascii=False).
5. Chú thích và docstring
Comment và nội dung hiển thị cho người dùng viết bằng tiếng Việt.
Mỗi tệp .py có docstring 1 dòng ở đầu tệp mô tả mục đích.
Mọi hàm public trong services/ phải có docstring gồm: chức năng, tham số, giá trị trả về và lỗi có thể ném ra.
python
def add_new_dish(name, category, price):
    """
    Thêm món mới vào thực đơn.
    - name: tên món
    - category: nhóm món, phải thuộc CATEGORIES
    - price: đơn giá (VNĐ)
    - Trả về: Dish vừa thêm
    - Ném ValueError nếu dữ liệu không hợp lệ
    """
6. Xử lý lỗi
Trong services/: khi dữ liệu sai (không tìm thấy món, số lượng âm, bàn đang bận…), ném ValueError kèm thông báo tiếng Việt. Không in lỗi, không trả về None để báo lỗi.
python
if quantity <= 0:
    raise ValueError("Số lượng phải lớn hơn 0.")
Trong main.py: bọc lời gọi service bằng try...except ValueError và in thông báo cho người dùng. Chương trình không được dừng đột ngột vì nhập sai.
python
try:
    order_service.open_order(table_number)
except ValueError as error:
    print("Lỗi: {}".format(error))
Ép kiểu dữ liệu nhập: dùng hàm input_int() trong main.py thay vì gọi int(input()) trực tiếp.
7. Đọc và ghi tệp
Luôn dùng with open(..., encoding="utf-8").
Đường dẫn tệp dữ liệu khai báo bằng hằng số, tính từ vị trí tệp code (chạy được ở bất kỳ thư mục nào):
python
MENU_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "menu.json",
)
Hàm đọc phải xử lý được trường hợp tệp chưa tồn tại hoặc rỗng (trả về danh sách rỗng).
8. Quy trình Git
Không commit venv/, __pycache__/ (đã khai báo trong .gitignore).
Mỗi commit làm một việc, thông điệp ngắn gọn theo mẫu <loại>: <mô tả>:
Loại	Dùng khi	Ví dụ
feat	Thêm tính năng	feat: thêm chức năng gộp bàn
fix	Sửa lỗi	fix: sai tổng tiền khi giảm giá 100%
docs	Sửa tài liệu	docs: cập nhật README
refactor	Sửa code không đổi chức năng	refactor: tách hàm tính tiền
Chạy thử python main.py trước khi commit.