# Quy Tắc Viết Code (Coding Conventions) - Dự Án Quản Lý Nhà Hàng

Tài liệu này quy định cách đặt tên, tổ chức tệp và viết mã nguồn để giữ cho dự án luôn đồng nhất và dễ bảo trì.

---

## 1. Quy Tắc Đặt Tên (Naming Conventions)

* **Tên tệp và thư mục:** Dùng chữ thường và dấu gạch dưới (`snake_case`).
  * *Đúng:* `menu_service.py`, `order_history.json`
  * *Sai:* `MenuService.py`, `Order-History.json`
* **Tên biến và tên hàm:** Dùng chữ thường và dấu gạch dưới (`snake_case`). Tên hàm nên bắt đầu bằng một động từ.
  * *Đúng:* `total_price = 0`, `def calculate_bill():`, `def add_new_dish():`
  * *Sai:* `TotalPrice = 0`, `def Bill():`
* **Tên Class (Lớp đối tượng):** Viết hoa chữ cái đầu mỗi từ (`PascalCase`).
  * *Đúng:* `class Dish:`, `class DiningTable:`, `class OrderItem:`
  * *Sai:* `class dish:`, `class dining_table:`
* **Tên Hằng số (Constants):** Viết hoa toàn bộ và nối bằng dấu gạch dưới (`UPPER_SNAKE_CASE`).
  * *Đúng:* `TAX_RATE = 0.08`, `MAX_TABLES = 20`, `MENU_FILE_PATH = "data/menu.json"`

---

## 2. Cấu Trúc và Phân Chia Trách Nhiệm

* **Thư mục `models/`:** Chỉ chứa các lớp định nghĩa dữ liệu (thuộc tính và hàm chuyển đổi sang từ điển/JSON). Không viết logic nhập xuất hay tính toán phức tạp ở đây.
* **Thư mục `services/`:** Chứa toàn bộ logic xử lý (thêm, sửa, xóa, tính tiền, đọc/ghi file). Không dùng lệnh `print()` hoặc `input()` bên trong các file service để tách biệt phần xử lý và giao diện.
* **Tệp `main.py`:** Chỉ làm nhiệm vụ hiển thị menu, nhận dữ liệu từ `input()`, gọi các hàm từ `services/` và in kết quả ra màn hình.

---

## 3. Quy Tắc Định Dạng Code (Formatting)

* **Thụt đầu dòng (Indentation):** Sử dụng **4 dấu cách (4 spaces)** cho mỗi cấp thụt lề. Không dùng phím Tab lẫn lộn với dấu cách.
* **Độ dài dòng:** Mỗi dòng code không nên dài quá **80 - 100 ký tự** để dễ đọc trên màn hình.
* **Khoảng trắng:**
  * Đặt 1 dấu cách xung quanh các toán tử (`a = b + c`, `price >= 10000`).
  * Không đặt dấu cách ngay bên trong dấu ngoặc (`print("Hello")`, không viết `print( "Hello" )`).
* **Dòng trống:**
  * Cách **2 dòng trống** trước và sau khi định nghĩa một `class` hoặc một hàm cấp cao.
  * Cách **1 dòng trống** giữa các phương thức (method) bên trong một `class`.

---

## 4. Chú Thích và Ghi Chú Hàm (Comments & Docstrings)

* **Ngôn ngữ:** Toàn bộ tên biến, tên hàm và tên file phải viết bằng **tiếng Anh** không dấu. Phần chú thích (comment) và nội dung hiển thị cho người dùng có thể viết bằng **tiếng Việt**.
* **Docstring cho hàm:** Mọi hàm xử lý quan trọng trong `services/` cần có mô tả ngắn gọn chức năng, tham số đầu vào và giá trị trả về.
  ```python
  def calculate_total(order_items, discount=0):
      """
      Tính tổng tiền hóa đơn sau khi trừ giảm giá.
      - order_items: danh sách các món đã gọi
      - discount: phần trăm giảm giá (0 - 100)
      """
      pass
  ```

---

## 5. Xử Lý Lỗi và Dữ Liệu (Error Handling)

* **Bắt lỗi nhập liệu:** Luôn dùng khối `try...except ValueError` khi ép kiểu dữ liệu người dùng nhập vào (ví dụ: nhập giá tiền hoặc chọn số menu) để tránh chương trình bị sập đột ngột.
* **Xử lý tệp tin:** Luôn dùng từ khóa `with open(..., encoding="utf-8")` khi đọc hoặc ghi tệp JSON/CSV để tránh lỗi font tiếng Việt và đảm bảo tệp luôn được đóng an toàn.
