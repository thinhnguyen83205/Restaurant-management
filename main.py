"""Tệp khởi chạy chính: giao diện dòng lệnh của hệ thống quản lý nhà hàng."""

from services import order_service


# ---------- Tiện ích chung ----------

def input_int(prompt):
    """Đọc số nguyên; báo lỗi và không làm dừng chương trình."""
    try:
        value = int(input(prompt).strip())
        return value
    except (EOFError, KeyboardInterrupt):
        raise ValueError("Đã hủy nhập dữ liệu.")
    except ValueError:
        raise ValueError("Vui lòng nhập số nguyên.")


def format_money(amount):
    """Định dạng số tiền theo đơn vị VNĐ."""
    return "{:,.0f}đ".format(amount).replace(",", ".")


def print_tables():
    """In danh sách 10 bàn cùng trạng thái và tạm tính."""
    print("\n" + "-" * 70)
    print("{:<8} {:<20} {:>16}".format(
        "Bàn", "Trạng thái", "Tạm tính"
    ))
    print("-" * 70)
    for table in order_service.get_all_tables():
        if table.status == "serving":
            status = "Đang phục vụ"
        else:
            status = "Trống"

        order = order_service.get_open_order(table.table_number)
        subtotal = order.subtotal if order is not None else 0
        print("{:<8} {:<20} {:>16}".format(
            table.table_number,
            status,
            format_money(subtotal),
        ))
    print("-" * 70)


# ---------- Màn hình con (các thành viên thay bằng code thật) ----------

def show_menu_management():
    """Màn hình quản lý thực đơn — TV2 viết."""
    print("Chức năng đang phát triển.")


def show_table_management():
    """Màn hình quản lý bàn ăn."""
    while True:
        print("\n" + "=" * 60)
        print("QUẢN LÝ BÀN ĂN")
        print("=" * 60)
        print_tables()
        print("1. Mở hóa đơn")
        print("2. Chuyển bàn")
        print("3. Gộp bàn")
        print("4. Trả bàn")
        print("0. Quay lại")

        try:
            choice = input_int("Chọn chức năng: ")

            if choice == 1:
                table_number = input_int("Nhập số bàn: ")
                order = order_service.open_order(table_number)
                print("Đã mở {} cho bàn {}.".format(
                    order.order_id, table_number
                ))
            elif choice == 2:
                from_table = input_int("Bàn nguồn: ")
                to_table = input_int("Bàn đích: ")
                order_service.transfer_table(from_table, to_table)
                print("Đã chuyển bàn {} sang bàn {}.".format(
                    from_table, to_table
                ))
            elif choice == 3:
                source_table = input_int("Bàn nguồn cần gộp: ")
                destination_table = input_int("Bàn đích: ")
                order_service.merge_tables(
                    source_table, destination_table
                )
                print("Đã gộp bàn {} vào bàn {}.".format(
                    source_table, destination_table
                ))
            elif choice == 4:
                table_number = input_int("Nhập số bàn: ")
                order_service.release_table(table_number)
                print("Đã trả bàn {} về trạng thái trống.".format(
                    table_number
                ))
            elif choice == 0:
                break
            else:
                print("Lựa chọn không hợp lệ.")
        except ValueError as error:
            print("Lỗi: {}".format(error))


def show_order_management():
    """Màn hình gọi món & thanh toán — TV4 viết."""
    print("Chức năng đang phát triển.")


def show_reports():
    """Màn hình thống kê doanh thu — TV5 viết."""
    print("Chức năng đang phát triển.")


# ---------- Menu chính (nhóm trưởng) ----------

def prompt_choice():
    """Đọc lựa chọn người dùng, không để lỗi EOF làm vỡ chương trình."""
    try:
        return input("Chọn chức năng: ").strip()
    except EOFError:
        print("\nKhông nhận được dữ liệu đầu vào. Chương trình sẽ thoát.")
        return "0"
    except KeyboardInterrupt:
        print("\nĐã hủy chương trình.")
        return "0"


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
        choice = prompt_choice()

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
