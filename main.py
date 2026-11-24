"""Tệp khởi chạy chính: giao diện dòng lệnh của hệ thống quản lý nhà hàng."""

from datetime import datetime

from services import menu_service, order_service, report_service


# ---------- Tiện ích chung ----------

def input_int(prompt):
    """Đọc một số nguyên; ném ValueError nếu dữ liệu nhập không hợp lệ."""
    try:
        # Bỏ khoảng trắng ở đầu/cuối rồi chuyển chuỗi người dùng nhập thành int.
        value = int(input(prompt).strip())
        return value
    except (EOFError, KeyboardInterrupt):
        # Báo cho màn hình đang gọi biết người dùng đã hủy thao tác nhập.
        raise ValueError("Đã hủy nhập dữ liệu.")
    except ValueError:
        # Màn hình sẽ bắt lỗi này, báo cho người dùng và tiếp tục chạy.
        raise ValueError("Vui lòng nhập số nguyên.")


def format_money(amount):
    """Định dạng số tiền theo đơn vị VNĐ."""
    return "{:,.0f}đ".format(amount).replace(",", ".")


def print_order(order):
    """In các món và tổng tiền của một hóa đơn."""
    print("\n" + "=" * 60)
    print("HÓA ĐƠN {} | Bàn {}".format(
        order.order_id, order.table_number
    ))
    print("Lập lúc: {}".format(order.created_at))
    if order.paid_at is not None:
        print("Thanh toán: {}".format(order.paid_at))

    print("-" * 60)
    for item in order.items:
        item_total = item.unit_price * item.quantity
        print("{} | {} | {} x {} = {}".format(
            item.dish_id,
            item.dish_name,
            format_money(item.unit_price),
            item.quantity,
            format_money(item_total),
        ))

    print("-" * 60)
    print("Tạm tính: {}".format(format_money(order.subtotal)))
    print("Giảm giá: {}%".format(order.discount))
    print("Tổng cộng: {}".format(format_money(order.total)))
    print("=" * 60)


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


# ---------- Quản lý thực đơn ----------

def print_dishes(dishes):
    """In danh sách món ra màn hình dạng bảng."""
    if len(dishes) == 0:
        print("(Chưa có món nào.)")
        return

    print("-" * 60)
    print("{:<6} {:<24} {:<10} {:>10}  {}".format(
        "Mã", "Tên món", "Nhóm", "Giá", "Trạng thái"
    ))
    print("-" * 60)
    for dish in dishes:
        status = "Đang bán" if dish.is_available else "Ngừng bán"
        print("{:<6} {:<24} {:<10} {:>10}  {}".format(
            dish.dish_id, dish.name, dish.category,
            format_money(dish.price), status
        ))
    print("-" * 60)


def choose_category():
    """Cho người dùng chọn nhóm món."""
    categories = menu_service.CATEGORIES
    for index, category in enumerate(categories, start=1):
        print("{}. {}".format(index, category))
    number = input_int("Chọn nhóm món: ")

    if 1 <= number <= len(categories):
        return categories[number - 1]
    print("Nhóm món không hợp lệ.")
    return None


def _view_dishes_by_category():
    category = choose_category()
    if category is not None:
        print_dishes(menu_service.get_dishes_by_category(category))


def _add_dish():
    name = input("Tên món: ").strip()
    category = choose_category()
    if category is None:
        return
    price = input_int("Giá (VNĐ): ")
    dish = menu_service.add_new_dish(name, category, price)
    print("Đã thêm món {} - {} ({}).".format(
        dish.dish_id, dish.name, format_money(dish.price)
    ))


def _update_price():
    dish_id = input("Mã món cần sửa giá (vd M004): ")
    dish = menu_service.find_dish_by_id(dish_id)
    print("Món hiện tại: {} - giá {}".format(
        dish.name, format_money(dish.price)
    ))
    new_price = input_int("Giá mới (VNĐ): ")
    dish = menu_service.update_dish_price(dish_id, new_price)
    print("Đã cập nhật giá {} thành {}.".format(
        dish.name, format_money(dish.price)
    ))


def _change_availability():
    dish_id = input("Mã món (vd M004): ")
    dish = menu_service.find_dish_by_id(dish_id)
    print("Món {} đang ở trạng thái: {}".format(
        dish.name, "Đang bán" if dish.is_available else "Ngừng bán"
    ))
    print("1. Mở bán")
    print("2. Ngừng bán")
    choice = input("Chọn: ").strip()

    if choice == "1":
        menu_service.set_dish_availability(dish_id, True)
        print("Đã mở bán món {}.".format(dish.name))
    elif choice == "2":
        menu_service.set_dish_availability(dish_id, False)
        print("Đã ngừng bán món {}.".format(dish.name))
    else:
        print("Lựa chọn không hợp lệ.")


def show_menu_management():
    """Màn hình quản lý thực đơn."""
    while True:
        print("\n--- QUẢN LÝ THỰC ĐƠN ---")
        print("1. Xem toàn bộ thực đơn")
        print("2. Xem theo nhóm món")
        print("3. Thêm món mới")
        print("4. Cập nhật giá món")
        print("5. Ngừng bán / mở bán lại")
        print("0. Quay lại")
        choice = input("Chọn chức năng: ").strip()

        if choice == "0":
            break

        try:
            if choice == "1":
                print_dishes(menu_service.get_all_dishes())
            elif choice == "2":
                _view_dishes_by_category()
            elif choice == "3":
                _add_dish()
            elif choice == "4":
                _update_price()
            elif choice == "5":
                _change_availability()
            else:
                print("Lựa chọn không hợp lệ.")
        except ValueError as error:
            print("Lỗi: {}".format(error))


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
    """
    Hiển thị menu gọi món và thanh toán cho người dùng.

    Hàm này chỉ nhận dữ liệu, gọi order_service xử lý nghiệp vụ
    và in kết quả:
    - 1: mở hóa đơn cho bàn
    - 2: thêm món vào hóa đơn
    - 3: bớt món khỏi hóa đơn
    - 4: hủy hóa đơn và trả bàn
    - 5: áp dụng giảm giá
    - 6: thanh toán và in hóa đơn
    - 0: quay lại menu chính

    Nếu service báo ValueError, thông báo lỗi được in ra và menu
    tiếp tục hiển thị để người dùng thao tác lại.
    """
    # Lặp lại để người dùng có thể thực hiện nhiều thao tác liên tiếp.
    while True:
        print("\n--- GỌI MÓN & THANH TOÁN ---")
        print("1. Mở hóa đơn")
        print("2. Thêm món")
        print("3. Bớt món")
        print("4. Hủy hóa đơn")
        print("5. Giảm giá")
        print("6. Thanh toán")
        print("0. Quay lại")

        try:
            # Dùng input_int để lựa chọn luôn là số nguyên.
            choice = input_int("Chọn chức năng: ")
            if choice == 0:
                # Thoát khỏi menu này và quay về menu chính.
                break
            if choice not in (1, 2, 3, 4, 5, 6):
                print("Lựa chọn không hợp lệ.")
                continue

            if choice == 1:
                # Việc tạo hóa đơn và đổi trạng thái bàn do service xử lý.
                table_number = input_int("Nhập số bàn: ")
                order = order_service.open_order(table_number)
                print("Đã mở hóa đơn {}.".format(order.order_id))
            elif choice == 2:
                table_number = input_int("Nhập số bàn: ")
                # In thực đơn để người dùng biết mã món trước khi nhập.
                print_dishes(menu_service.get_all_dishes())
                dish_id = input("Nhập mã món: ").strip()
                quantity = input_int("Nhập số lượng: ")
                # Service kiểm tra bàn, món và số lượng, rồi cập nhật tiền.
                order = order_service.add_item_to_order(
                    table_number, dish_id, quantity
                )
                print_order(order)
            elif choice == 3:
                table_number = input_int("Nhập số bàn: ")
                dish_id = input("Nhập mã món cần bớt: ").strip()
                quantity = input_int("Nhập số lượng cần bớt: ")
                # Service sẽ báo lỗi nếu món không có hoặc số lượng bớt quá lớn.
                order = order_service.remove_item_from_order(
                    table_number, dish_id, quantity
                )
                print_order(order)
            elif choice == 4:
                table_number = input_int("Nhập số bàn: ")
                # Hủy hóa đơn đồng thời trả bàn về trạng thái trống.
                order_service.cancel_order(table_number)
                print("Đã hủy hóa đơn bàn {}.".format(table_number))
            elif choice == 5:
                table_number = input_int("Nhập số bàn: ")
                discount = input_int("Nhập phần trăm giảm giá: ")
                # Service kiểm tra phần trăm giảm giá và tính lại tổng tiền.
                order = order_service.apply_discount(
                    table_number, discount
                )
                print_order(order)
            else:
                table_number = input_int("Nhập số bàn: ")
                # Thanh toán và lưu lịch sử trước khi hiển thị hóa đơn đã chốt.
                order = order_service.checkout(table_number)
                print_order(order)
        except ValueError as error:
            # Hiển thị lỗi nghiệp vụ mà không làm dừng vòng lặp giao diện.
            print("Lỗi: {}".format(error))


def show_reports():
    """Hiển thị các báo cáo doanh thu và món bán chạy."""
    while True:
        print("\n--- Thống kê doanh thu ---")
        print("1. Doanh thu hôm nay")
        print("2. Doanh thu theo ngày")
        print("3. Tổng hợp doanh thu từng ngày")
        print("4. Top món bán chạy")
        print("5. Tổng doanh thu")
        print("0. Quay lại")
        choice = prompt_choice()

        if choice == "0":
            return

        try:
            if choice == "1":
                today = datetime.now().strftime("%Y-%m-%d")
                revenue = report_service.get_revenue_by_date(today)
                print("Doanh thu ngày {}: {}".format(
                    today, format_money(revenue)
                ))
            elif choice == "2":
                date = input("Nhập ngày (YYYY-MM-DD): ").strip()
                revenue = report_service.get_revenue_by_date(date)
                print("Doanh thu ngày {}: {}".format(
                    date, format_money(revenue)
                ))
            elif choice == "3":
                summary = report_service.get_daily_revenue_summary()
                if not summary:
                    print("Chưa có dữ liệu doanh thu.")
                else:
                    print("\nDoanh thu theo ngày:")
                    for date, revenue in summary.items():
                        print("{}: {}".format(date, format_money(revenue)))
            elif choice == "4":
                dishes = report_service.get_best_selling_dishes()
                if not dishes:
                    print("Chưa có dữ liệu món đã bán.")
                else:
                    print("\nTop món bán chạy:")
                    for rank, dish in enumerate(dishes, start=1):
                        print(
                            "{}. {} - {} ({} phần)".format(
                                rank,
                                dish["dish_name"],
                                dish["dish_id"],
                                dish["quantity"],
                            )
                        )
            elif choice == "5":
                revenue = report_service.get_total_revenue()
                print("Tổng doanh thu: {}".format(format_money(revenue)))
            else:
                print("Lựa chọn không hợp lệ.")
        except ValueError as error:
            print("Lỗi: {}".format(error))


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
