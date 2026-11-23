"""Xử lý hóa đơn mở và quản lý bàn ăn."""

from datetime import datetime

from models.order import Order
from models.table import DiningTable, STATUS_EMPTY, STATUS_SERVING
from services import payment_service


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
