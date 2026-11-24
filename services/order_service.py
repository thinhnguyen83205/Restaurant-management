"""Xử lý hóa đơn mở và quản lý bàn ăn."""

from datetime import datetime

from models.order import Order, OrderItem
from models.table import DiningTable, STATUS_EMPTY, STATUS_SERVING
from services import menu_service, payment_service


MAX_TABLES = 10
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

_tables = [DiningTable(number) for number in range(1, MAX_TABLES + 1)]
_open_orders = {}


def _validate_table_number(table_number):
    """Kiểm tra số bàn hợp lệ."""
    if not isinstance(table_number, int) or isinstance(table_number, bool):
        raise ValueError("Số bàn không hợp lệ.")
    if table_number < 1 or table_number > MAX_TABLES:
        raise ValueError("Số bàn không hợp lệ.")


def get_all_tables():
    """
    Lấy danh sách tất cả các bàn.
    - Trả về: danh sách DiningTable
    """
    return list(_tables)


def get_table(table_number):
    """
    Lấy thông tin một bàn.
    - table_number: số bàn cần lấy
    - Trả về: DiningTable tương ứng
    - Ném ValueError nếu số bàn không hợp lệ
    """
    _validate_table_number(table_number)
    return _tables[table_number - 1]


def get_open_order(table_number):
    """
    Lấy hóa đơn đang mở của một bàn.
    - table_number: số bàn cần lấy hóa đơn
    - Trả về: Order hoặc None nếu bàn chưa có hóa đơn
    - Ném ValueError nếu số bàn không hợp lệ
    """
    _validate_table_number(table_number)
    return _open_orders.get(table_number)


def generate_order_id():
    """
    Sinh mã hóa đơn mới theo thứ tự tăng dần.
    - Trả về: mã hóa đơn dạng HD0001
    - Ném ValueError nếu lịch sử hóa đơn không đọc được
    """
    if hasattr(payment_service, "load_paid_orders"):
        paid_orders = payment_service.load_paid_orders()
    else:
        paid_orders = []
    numbers = []

    for order in paid_orders:
        order_id = (
            order.order_id
            if hasattr(order, "order_id")
            else order.get("order_id", "")
        )
        if str(order_id).startswith("HD"):
            try:
                numbers.append(int(order_id[2:]))
            except (TypeError, ValueError):
                continue

    open_numbers = []
    for order in _open_orders.values():
        order_id = order.order_id
        if str(order_id).startswith("HD"):
            try:
                open_numbers.append(int(order_id[2:]))
            except (TypeError, ValueError):
                continue

    next_number = max(numbers + open_numbers + [0]) + 1
    return "HD{:04d}".format(next_number)


def open_order(table_number):
    """
    Mở hóa đơn mới cho một bàn trống.
    - table_number: số bàn cần mở
    - Trả về: Order vừa tạo
    - Ném ValueError nếu bàn không hợp lệ hoặc đang phục vụ
    """
    table = get_table(table_number)

    if table.status == STATUS_SERVING:
        raise ValueError("Bàn {} đang phục vụ.".format(table_number))

    order = Order(
        order_id=generate_order_id(),
        table_number=table_number,
        created_at=datetime.now().strftime(DATETIME_FORMAT),
    )
    _open_orders[table_number] = order
    table.status = STATUS_SERVING
    return order


def release_table(table_number):
    """
    Trả bàn về trạng thái trống và hủy hóa đơn đang mở.
    - table_number: số bàn cần trả
    - Trả về: True
    - Ném ValueError nếu số bàn không hợp lệ hoặc bàn đang trống
    """
    table = get_table(table_number)

    if table.status == STATUS_EMPTY:
        raise ValueError("Bàn {} đang trống.".format(table_number))

    _open_orders.pop(table_number, None)
    table.status = STATUS_EMPTY
    return True


def transfer_table(from_table_number, to_table_number):
    """
    Chuyển hóa đơn từ một bàn sang bàn trống.
    - from_table_number: bàn nguồn
    - to_table_number: bàn đích
    - Trả về: Order sau khi chuyển
    - Ném ValueError nếu bàn không hợp lệ hoặc trạng thái không phù hợp
    """
    source = get_table(from_table_number)
    destination = get_table(to_table_number)

    if source.status != STATUS_SERVING:
        raise ValueError("Bàn {} không có hóa đơn đang phục vụ.".format(
            from_table_number
        ))
    if destination.status != STATUS_EMPTY:
        raise ValueError("Bàn {} không đang trống.".format(to_table_number))

    order = _open_orders.pop(from_table_number)
    order.table_number = to_table_number
    _open_orders[to_table_number] = order
    source.status = STATUS_EMPTY
    destination.status = STATUS_SERVING
    return order


def merge_tables(source_table_number, destination_table_number):
    """
    Gộp hóa đơn bàn nguồn vào bàn đích.
    - source_table_number: bàn nguồn
    - destination_table_number: bàn đích
    - Trả về: Order của bàn đích
    - Ném ValueError nếu hai bàn không hợp lệ hoặc không đang phục vụ
    """
    source = get_table(source_table_number)
    destination = get_table(destination_table_number)

    if source_table_number == destination_table_number:
        raise ValueError("Hai bàn gộp phải khác nhau.")
    if source.status != STATUS_SERVING:
        raise ValueError("Bàn {} không có hóa đơn đang phục vụ.".format(
            source_table_number
        ))
    if destination.status != STATUS_SERVING:
        raise ValueError("Bàn {} không có hóa đơn đang phục vụ.".format(
            destination_table_number
        ))

    source_order = _open_orders[source_table_number]
    destination_order = _open_orders[destination_table_number]

    for source_item in source_order.items:
        matching_item = next(
            (
                item for item in destination_order.items
                if item.dish_id == source_item.dish_id
            ),
            None,
        )
        if matching_item is not None:
            matching_item.quantity += source_item.quantity
        else:
            destination_order.items.append(source_item)

    _open_orders.pop(source_table_number)
    source.status = STATUS_EMPTY

    if hasattr(payment_service, "recalculate_order"):
        payment_service.recalculate_order(destination_order)
    else:
        destination_order.subtotal = sum(
            item.unit_price * item.quantity
            for item in destination_order.items
        )
        destination_order.total = destination_order.subtotal

    return destination_order


# ---------- Gọi món ----------

def _validate_quantity(quantity):
    """Đảm bảo số lượng món là số nguyên dương."""
    # bool là kiểu con của int trong Python nên cần loại riêng.
    if (not isinstance(quantity, int) or isinstance(quantity, bool)
            or quantity <= 0):
        raise ValueError("Số lượng phải là số nguyên lớn hơn 0.")


def _get_open_order_or_raise(table_number):
    """Lấy hóa đơn đang mở hoặc báo lỗi nếu bàn chưa có hóa đơn."""
    order = get_open_order(table_number)
    if order is None:
        raise ValueError(
            "Bàn {} chưa có hóa đơn đang mở.".format(table_number)
        )
    return order


def merge_item(order, dish, quantity):
    """
    Thêm món vào hóa đơn hoặc cộng dồn số lượng món đã có.
    - order: hóa đơn cần cập nhật
    - dish: món ăn cần thêm
    - quantity: số lượng cần thêm
    - Trả về: dòng món vừa thêm hoặc cập nhật
    - Ném ValueError nếu số lượng không hợp lệ
    """
    _validate_quantity(quantity)

    for item in order.items:
        if item.dish_id == dish.dish_id:
            item.quantity += quantity
            return item

    # Lưu tên và giá hiện tại để hóa đơn không đổi theo thực đơn sau này.
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
    - dish_id: mã món cần thêm
    - quantity: số lượng cần thêm
    - Trả về: hóa đơn sau khi cập nhật
    - Ném ValueError nếu bàn, món hoặc số lượng không hợp lệ
    """
    _validate_quantity(quantity)
    order = _get_open_order_or_raise(table_number)
    dish = menu_service.find_dish_by_id(dish_id)

    if not dish.is_available:
        raise ValueError("Món {} đã ngừng phục vụ.".format(dish_id))

    merge_item(order, dish, quantity)
    return payment_service.recalculate_order(order)


def remove_item_from_order(table_number, dish_id, quantity):
    """
    Bớt món khỏi hóa đơn; xóa dòng nếu số lượng còn bằng 0.
    - table_number: số bàn đang phục vụ
    - dish_id: mã món cần bớt
    - quantity: số lượng cần bớt
    - Trả về: hóa đơn sau khi cập nhật
    - Ném ValueError nếu bàn, món hoặc số lượng không hợp lệ
    """
    _validate_quantity(quantity)
    order = _get_open_order_or_raise(table_number)

    for item in order.items:
        if item.dish_id == dish_id:
            if quantity > item.quantity:
                raise ValueError("Số lượng món trong hóa đơn không đủ.")

            item.quantity -= quantity
            if item.quantity == 0:
                order.items.remove(item)

            return payment_service.recalculate_order(order)

    raise ValueError("Món {} không có trong hóa đơn.".format(dish_id))


# ---------- Thanh toán theo bàn ----------

def apply_discount(table_number, discount):
    """
    Áp dụng mức giảm giá cho hóa đơn của bàn.
    - table_number: số bàn đang phục vụ
    - discount: phần trăm giảm giá từ 0 đến 100
    - Trả về: hóa đơn sau khi tính lại tiền
    - Ném ValueError nếu không có hóa đơn hoặc mức giảm sai
    """
    order = _get_open_order_or_raise(table_number)
    return payment_service.set_order_discount(order, discount)


def checkout(table_number):
    """
    Thanh toán hóa đơn rồi trả bàn về trạng thái trống.
    - table_number: số bàn cần thanh toán
    - Trả về: hóa đơn đã thanh toán
    - Ném ValueError nếu không có hóa đơn hoặc không thể thanh toán
    """
    order = _get_open_order_or_raise(table_number)

    # Chỉ trả bàn sau khi lưu hóa đơn thanh toán thành công.
    paid_order = payment_service.pay_order(order)
    release_table(table_number)
    return paid_order


def cancel_order(table_number):
    """
    Hủy hóa đơn chưa thanh toán và trả bàn về trạng thái trống.
    - table_number: số bàn cần hủy hóa đơn
    - Trả về: hóa đơn đã hủy
    - Ném ValueError nếu bàn chưa có hóa đơn đang mở
    """
    order = _get_open_order_or_raise(table_number)
    release_table(table_number)
    return order
