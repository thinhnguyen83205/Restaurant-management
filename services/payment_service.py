"""Tính tiền, áp dụng giảm giá và lưu lịch sử hóa đơn đã thanh toán."""

import json
import os
from datetime import datetime

from models.order import Order


ORDERS_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "orders.json",
)
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def load_paid_orders():
    """Đọc lịch sử; trả về list[Order], hoặc [] nếu tệp thiếu/rỗng."""
    if not os.path.exists(ORDERS_FILE_PATH):
        return []
    with open(ORDERS_FILE_PATH, "r", encoding="utf-8") as file:
        content = file.read().strip()
    if not content:
        return []
    try:
        data = json.loads(content)
        if not isinstance(data, list):
            raise ValueError("Lịch sử hóa đơn phải là một danh sách.")
        return [Order.from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise ValueError("Dữ liệu lịch sử hóa đơn không hợp lệ.") from error


def save_paid_orders(orders):
    """Ghi list[Order] vào JSON; ném ValueError nếu dữ liệu sai."""
    try:
        data = [order.to_dict() for order in orders]
    except (TypeError, AttributeError) as error:
        raise ValueError("Danh sách hóa đơn không hợp lệ.") from error
    os.makedirs(os.path.dirname(ORDERS_FILE_PATH), exist_ok=True)
    with open(ORDERS_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.write("\n")


def calculate_subtotal(order):
    """Tính tổng giá món theo số lượng; trả về VNĐ; lỗi nếu giá trị sai."""
    subtotal = 0
    for item in order.items:
        if (not isinstance(item.unit_price, int)
                or isinstance(item.unit_price, bool)
                or not isinstance(item.quantity, int)
                or isinstance(item.quantity, bool)
                or item.unit_price < 0 or item.quantity <= 0):
            raise ValueError("Giá món hoặc số lượng không hợp lệ.")
        subtotal += item.unit_price * item.quantity
    return subtotal


def calculate_total(subtotal, discount):
    """Tính số tiền sau giảm giá; trả về VNĐ; lỗi nếu ngoài 0–100%."""
    if (not isinstance(subtotal, int) or isinstance(subtotal, bool)
            or subtotal < 0):
        raise ValueError("Tạm tính phải là số nguyên không âm.")
    if (not isinstance(discount, (int, float))
            or isinstance(discount, bool) or not 0 <= discount <= 100):
        raise ValueError("Giảm giá phải nằm trong khoảng 0–100%.")
    return round(subtotal * (100 - discount) / 100)


def recalculate_order(order):
    """Cập nhật subtotal và total của Order; trả về Order; lỗi nếu sai."""
    order.subtotal = calculate_subtotal(order)
    order.total = calculate_total(order.subtotal, order.discount)
    return order


def set_order_discount(order, discount):
    """Áp dụng phần trăm giảm giá; trả về Order; lỗi nếu đã trả/sai %."""
    if order.paid_at is not None:
        raise ValueError("Hóa đơn đã thanh toán.")
    calculate_total(0, discount)
    order.discount = discount
    return recalculate_order(order)


def pay_order(order):
    """Chốt Order, ghi thời gian và lịch sử; lỗi nếu rỗng/đã trả."""
    if order.paid_at is not None:
        raise ValueError("Hóa đơn đã thanh toán.")
    if not order.items:
        raise ValueError("Không thể thanh toán hóa đơn chưa có món.")
    recalculate_order(order)
    paid_orders = load_paid_orders()
    if any(saved.order_id == order.order_id for saved in paid_orders):
        raise ValueError("Mã hóa đơn đã tồn tại trong lịch sử.")
    order.paid_at = datetime.now().strftime(DATETIME_FORMAT)
    paid_orders.append(order)
    try:
        save_paid_orders(paid_orders)
    except Exception:
        order.paid_at = None
        raise
    return order
