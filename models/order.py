"""Định nghĩa đối tượng Hóa đơn (Order) và Món trong hóa đơn (OrderItem)."""


class OrderItem:
    """Một dòng món ăn trong hóa đơn."""

    def __init__(self, dish_id, dish_name, unit_price, quantity):
        self.dish_id = dish_id
        self.dish_name = dish_name
        self.unit_price = unit_price
        self.quantity = quantity

    def to_dict(self):
        """Chuyển đối tượng sang từ điển."""
        return {
            "dish_id": self.dish_id,
            "dish_name": self.dish_name,
            "unit_price": self.unit_price,
            "quantity": self.quantity,
        }

    @classmethod
    def from_dict(cls, data):
        """Tạo đối tượng OrderItem từ từ điển."""
        return cls(
            dish_id=data["dish_id"],
            dish_name=data["dish_name"],
            unit_price=data["unit_price"],
            quantity=data["quantity"],
        )


class Order:
    """Hóa đơn của một bàn ăn."""

    def __init__(self, order_id, table_number, created_at, items=None,
                 discount=0, subtotal=0, total=0, paid_at=None):
        self.order_id = order_id
        self.table_number = table_number
        self.created_at = created_at
        self.items = items if items is not None else []
        self.discount = discount        # phần trăm giảm giá (0 - 100)
        self.subtotal = subtotal        # tổng tiền trước giảm giá
        self.total = total              # tổng tiền phải trả
        self.paid_at = paid_at          # None nếu chưa thanh toán

    def to_dict(self):
        """Chuyển đối tượng sang từ điển để ghi ra JSON."""
        return {
            "order_id": self.order_id,
            "table_number": self.table_number,
            "created_at": self.created_at,
            "paid_at": self.paid_at,
            "items": [item.to_dict() for item in self.items],
            "discount": self.discount,
            "subtotal": self.subtotal,
            "total": self.total,
        }

    @classmethod
    def from_dict(cls, data):
        """Tạo đối tượng Order từ từ điển đọc từ JSON."""
        return cls(
            order_id=data["order_id"],
            table_number=data["table_number"],
            created_at=data["created_at"],
            items=[OrderItem.from_dict(i) for i in data.get("items", [])],
            discount=data.get("discount", 0),
            subtotal=data.get("subtotal", 0),
            total=data.get("total", 0),
            paid_at=data.get("paid_at"),
        )