"""Tệp khởi chạy chính: giao diện dòng lệnh của hệ thống quản lý nhà hàng."""

from services import order_service


def format_money(amount):
    """Định dạng số tiền VNĐ cho giao diện dòng lệnh."""
    return "{:,.0f}đ".format(amount)


def print_order(order):
    """In hóa đơn chi tiết từ các giá trị đã được service tính."""
    print("\n" + "=" * 60)
    print("HÓA ĐƠN {} | Bàn {}".format(order.order_id, order.table_number))
    print("Lập lúc: {}".format(order.created_at))
    if order.paid_at:
        print("Thanh toán: {}".format(order.paid_at))
    print("-" * 60)
    for item in order.items:
        print("{} | {} | {} x {} = {}".format(
            item.dish_id, item.dish_name, format_money(item.unit_price),
            item.quantity, format_money(item.unit_price * item.quantity),
        ))
    print("-" * 60)
    print("Tạm tính: {}".format(format_money(order.subtotal)))
    print("Giảm giá: {}%".format(order.discount))
    print("Tổng cộng: {}".format(format_money(order.total)))
    print("=" * 60)


# ---------- Màn hình con (các thành viên thay bằng code thật) ----------

def show_menu_management():
    """Màn hình quản lý thực đơn — TV2 viết."""
    print("Chức năng đang phát triển.")


def show_table_management():
    """Màn hình quản lý bàn ăn — TV3 viết."""
    print("Chức năng đang phát triển.")


def show_order_management():
    """Màn hình gọi món & thanh toán — TV4 viết."""
    # Lặp lại màn hình cho đến khi người dùng chọn quay lại.
    while True:
        print("\n--- GỌI MÓN & THANH TOÁN ---")
        print("1. Mở hóa đơn")
        print("2. Thêm món")
        print("3. Bớt món")
        print("4. Hủy hóa đơn")
        print("5. Giảm giá")
        print("6. Thanh toán")
        print("0. Quay lại")
        choice = input_int("Chọn chức năng: ")

        if choice == 0:
            break
        if choice not in (1, 2, 3, 4, 5, 6):
            print("Lựa chọn không hợp lệ.")
            continue

        # Service kiểm tra nghiệp vụ và báo lỗi bằng ValueError.
        try:
            if choice == 1:
                table_number = input_int("Nhập số bàn: ")
                # TV3 xử lý việc tạo hóa đơn và cập nhật trạng thái bàn.
                order_service.open_order(table_number)
                print("Đã mở hóa đơn bàn {}.".format(table_number))
            elif choice == 2:
                table_number = input_int("Nhập số bàn: ")
                dish_id = input("Nhập mã món: ").strip()
                quantity = input_int("Nhập số lượng: ")
                # Service kiểm tra món, rồi gộp món trùng nếu cần.
                order = order_service.add_item_to_order(
                    table_number, dish_id, quantity
                )
                print_order(order)
            elif choice == 3:
                table_number = input_int("Nhập số bàn: ")
                dish_id = input("Nhập mã món: ").strip()
                quantity = input_int("Nhập số lượng cần bớt: ")
                # Nếu số lượng còn bằng 0, service sẽ xóa dòng món.
                order = order_service.remove_item_from_order(
                    table_number, dish_id, quantity
                )
                print_order(order)
            elif choice == 4:
                table_number = input_int("Nhập số bàn: ")
                order_service.cancel_order(table_number)
                print("Đã hủy hóa đơn bàn {}.".format(table_number))
            elif choice == 5:
                table_number = input_int("Nhập số bàn: ")
                discount = input_int("Nhập phần trăm giảm giá: ")
                # Payment service kiểm tra mức giảm và tính lại tiền.
                order = order_service.apply_discount(
                    table_number, discount
                )
                print_order(order)
            else:
                table_number = input_int("Nhập số bàn: ")
                # Thanh toán thành công mới in hóa đơn đã chốt.
                order = order_service.checkout(table_number)
                print_order(order)
        except ValueError as error:
            print("Lỗi: {}".format(error))


def input_int(prompt):
    """Nhận số nguyên; hỏi lại nếu người dùng nhập sai."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            # Giữ người dùng ở bước nhập cho đến khi nhận được số nguyên.
            print("Lỗi: vui lòng nhập số nguyên.")


def show_reports():
    """Màn hình thống kê doanh thu — TV5 viết."""
    print("Chức năng đang phát triển.")


# ---------- Menu chính (nhóm trưởng) ----------

def main():
    """Vòng lặp menu chính của chương trình."""
    while True:
        print("\n" + "=" * 60)
        print("      HỆ THỐNG QUẢN LÝ NHÀ HÀNG")
        print("=" * 60)
        print("1. Quản lý thực đơn")
        print("2. Quản lý bàn ăn")
        print("3. Gọi món & thanh toán")
        print("4. Thống kê doanh thu")
        print("0. Thoát")
        choice = input("Chọn chức năng: ").strip()

        if choice == "1":
            show_menu_management()
        elif choice == "2":
            show_table_management()
        elif choice == "3":
            show_order_management()
        elif choice == "4":
            show_reports()
        elif choice == "0":
            print("Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
