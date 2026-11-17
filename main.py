"""Tệp khởi chạy chính: giao diện dòng lệnh của hệ thống quản lý nhà hàng."""


# ---------- Màn hình con (các thành viên thay bằng code thật) ----------

def show_menu_management():
    """Màn hình quản lý thực đơn — TV2 viết."""
    print("Chức năng đang phát triển.")


def show_table_management():
    """Màn hình quản lý bàn ăn — TV3 viết."""
    print("Chức năng đang phát triển.")


def show_order_management():
    """Màn hình gọi món & thanh toán — TV4 viết."""
    print("Chức năng đang phát triển.")


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