"""Tạo báo cáo doanh thu và món bán chạy từ lịch sử hóa đơn."""

from datetime import datetime

from services import payment_service


DATE_FORMAT = "%Y-%m-%d"
DEFAULT_DISH_LIMIT = 5


def _validate_date(date):
    """Kiểm tra ngày theo định dạng YYYY-MM-DD."""
    if not isinstance(date, str):
        raise ValueError("Ngày phải có định dạng YYYY-MM-DD.")
    try:
        datetime.strptime(date, DATE_FORMAT)
    except ValueError as error:
        raise ValueError("Ngày phải có định dạng YYYY-MM-DD.") from error


def get_revenue_by_date(date):
    """
    Tính doanh thu đã thanh toán trong một ngày.
    - date: ngày cần xem theo định dạng YYYY-MM-DD
    - Trả về: doanh thu trong ngày (VNĐ)
    - Ném ValueError nếu ngày sai định dạng hoặc lịch sử không hợp lệ
    """
    _validate_date(date)
    return sum(
        order.total
        for order in payment_service.load_paid_orders()
        if order.paid_at and order.paid_at[:10] == date
    )


def get_daily_revenue_summary():
    """
    Tổng hợp doanh thu theo ngày thanh toán.
    - Trả về: dict ngày YYYY-MM-DD ánh xạ tới doanh thu (VNĐ)
    - Ném ValueError nếu lịch sử hóa đơn không hợp lệ
    """
    summary = {}
    for order in payment_service.load_paid_orders():
        if not order.paid_at:
            continue
        date = order.paid_at[:10]
        _validate_date(date)
        summary[date] = summary.get(date, 0) + order.total
    return dict(sorted(summary.items()))


def get_best_selling_dishes(limit=DEFAULT_DISH_LIMIT):
    """
    Xếp hạng món theo số lượng đã bán, từ cao xuống thấp.
    - limit: số món tối đa cần trả về, phải là số nguyên dương
    - Trả về: list dict gồm dish_id, dish_name, quantity và revenue
    - Ném ValueError nếu limit hoặc lịch sử hóa đơn không hợp lệ
    """
    if (not isinstance(limit, int) or isinstance(limit, bool)
            or limit <= 0):
        raise ValueError("Số món cần xem phải là số nguyên lớn hơn 0.")

    totals = {}
    for order in payment_service.load_paid_orders():
        for item in order.items:
            dish = totals.setdefault(
                item.dish_id,
                {
                    "dish_id": item.dish_id,
                    "dish_name": item.dish_name,
                    "quantity": 0,
                    "revenue": 0,
                },
            )
            dish["quantity"] += item.quantity
            dish["revenue"] += item.unit_price * item.quantity

    ranked_dishes = sorted(
        totals.values(),
        key=lambda dish: (-dish["quantity"], dish["dish_id"]),
    )
    return ranked_dishes[:limit]


def get_total_revenue():
    """
    Tính tổng doanh thu của tất cả hóa đơn đã thanh toán.
    - Trả về: tổng doanh thu (VNĐ)
    - Ném ValueError nếu lịch sử hóa đơn không hợp lệ
    """
    return sum(
        order.total for order in payment_service.load_paid_orders()
    )


# [SỬA LỖI #3] Hàm mới: README có tính năng "Xem lại hóa đơn cũ" nhưng
# chưa được làm. Hàm chỉ đọc lịch sử qua payment_service, không sửa gì.
def get_paid_order_by_id(order_id):
    """
    Tìm một hóa đơn đã thanh toán theo mã (không phân biệt hoa/thường).
    - order_id: mã hóa đơn, vd "HD0001"
    - Trả về: Order tìm được
    - Ném ValueError nếu không tìm thấy hoặc lịch sử không hợp lệ
    """
    wanted_id = str(order_id).strip().upper()
    for order in payment_service.load_paid_orders():
        if order.order_id == wanted_id:
            return order
    raise ValueError("Không tìm thấy hóa đơn có mã {}.".format(wanted_id))
