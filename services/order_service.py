"""Xử lý gọi món và thanh toán theo bàn."""

from models.order import OrderItem
from services import menu_service, payment_service


# ---------- Gọi món ----------

def _validate_quantity(quantity):
    """Đảm bảo số lượng là số nguyên dương trước khi cập nhật hóa đơn."""
    # Trong Python, bool cũng được xem là int, nên cần loại True/False riêng.
    if (not isinstance(quantity, int) or isinstance(quantity, bool)
            or quantity <= 0):
        raise ValueError("Số lượng phải là số nguyên lớn hơn 0.")


def merge_item(order, dish, quantity):
    """
    Thêm món vào hóa đơn hoặc cộng dồn số lượng món đã có.
    - order: hóa đơn đang mở
    - dish: món ăn cần thêm
    - quantity: số lượng cần thêm
    - Trả về: OrderItem được thêm hoặc cập nhật
    - Ném ValueError nếu số lượng không hợp lệ
    """
    _validate_quantity(quantity)

    # Nếu món đã có trong hóa đơn, chỉ cần cộng thêm số lượng.
    for item in order.items:
        if item.dish_id == dish.dish_id:
            item.quantity += quantity
            return item

    # Lưu tên và giá tại thời điểm gọi món để hóa đơn không đổi
    # nếu thực đơn được cập nhật sau đó.
    item = OrderItem(
        dish_id=dish.dish_id,
        dish_name=dish.name,
        unit_price=dish.price,
        quantity=quantity,
    )
    order.items.append(item)
    return item


def add_item_to_order(table_number, dish_id, quantity):
    """
    Thêm món đang bán vào hóa đơn của bàn.
    - table_number: số bàn đang phục vụ
    - dish_id: mã món trong thực đơn
    - quantity: số lượng cần thêm
    - Trả về: hóa đơn sau khi thêm món
    - Ném ValueError nếu dữ liệu sai, không tìm thấy món hoặc bàn
    """
    _validate_quantity(quantity)

    # TV3 cung cấp hàm này để lấy hóa đơn đang mở của bàn.
    order = get_open_order(table_number)
    dish = menu_service.find_dish_by_id(dish_id)
    if dish is None:
        raise ValueError("Không tìm thấy món {}.".format(dish_id))
    if not dish.is_available:
        raise ValueError("Món {} đã ngừng phục vụ.".format(dish_id))

    # Gộp món trùng, rồi tính lại tạm tính và tổng tiền.
    merge_item(order, dish, quantity)
    return payment_service.recalculate_order(order)


def remove_item_from_order(table_number, dish_id, quantity):
    """
    Bớt số lượng món khỏi hóa đơn; xóa dòng nếu số lượng còn bằng 0.
    - table_number: số bàn đang phục vụ
    - dish_id: mã món cần bớt
    - quantity: số lượng cần bớt
    - Trả về: hóa đơn sau khi cập nhật
    - Ném ValueError nếu dữ liệu sai hoặc món không có đủ số lượng
    """
    _validate_quantity(quantity)
    order = get_open_order(table_number)

    # Tìm món cần bớt trong các món của hóa đơn.
    for item in order.items:
        if item.dish_id == dish_id:
            if quantity > item.quantity:
                raise ValueError("Số lượng món trong hóa đơn không đủ.")

            # Trừ số lượng; nếu hết thì bỏ hẳn dòng món khỏi hóa đơn.
            item.quantity -= quantity
            if item.quantity == 0:
                order.items.remove(item)

            # Cập nhật lại tiền sau khi thay đổi số lượng.
            return payment_service.recalculate_order(order)
    raise ValueError("Món {} không có trong hóa đơn.".format(dish_id))


# ---------- Thanh toán theo bàn ----------

def apply_discount(table_number, discount):
    """
    Áp dụng mức giảm giá theo phần trăm cho hóa đơn của bàn.
    - table_number: số bàn đang phục vụ
    - discount: phần trăm giảm giá từ 0 đến 100
    - Trả về: hóa đơn sau khi tính lại tiền
    - Ném ValueError nếu bàn không có hóa đơn hoặc mức giảm sai
    """
    order = get_open_order(table_number)

    # Payment service kiểm tra mức giảm giá và tính lại tổng tiền.
    return payment_service.set_order_discount(order, discount)


def checkout(table_number):
    """
    Thanh toán hóa đơn và trả bàn về trạng thái trống.
    - table_number: số bàn cần thanh toán
    - Trả về: hóa đơn đã thanh toán
    - Ném ValueError nếu bàn không có hóa đơn hoặc hóa đơn không thể trả
    """
    order = get_open_order(table_number)

    # Chỉ trả bàn về trống sau khi thanh toán và lưu lịch sử thành công.
    paid_order = payment_service.pay_order(order)
    release_table(table_number)
    return paid_order


def cancel_order(table_number):
    """
    Hủy hóa đơn chưa thanh toán và trả bàn về trạng thái trống.
    - table_number: số bàn cần hủy hóa đơn
    - Trả về: hóa đơn đã hủy
    - Ném ValueError nếu bàn không có hóa đơn
    """
    order = get_open_order(table_number)

    # Giao việc cập nhật trạng thái bàn cho phần quản lý bàn của TV3.
    release_table(table_number)
    return order
