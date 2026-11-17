"""Định nghĩa đối tượng Món ăn (Dish)."""


class Dish:
    """Một món ăn trong thực đơn."""

    def __init__(self, dish_id, name, category, price, is_available=True):
        self.dish_id = dish_id
        self.name = name
        self.category = category
        self.price = price
        self.is_available = is_available

    def to_dict(self):
        """Chuyển đối tượng sang từ điển để ghi ra JSON."""
        return {
            "dish_id": self.dish_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "is_available": self.is_available,
        }

    @classmethod
    def from_dict(cls, data):
        """Tạo đối tượng Dish từ từ điển đọc từ JSON."""
        return cls(
            dish_id=data["dish_id"],
            name=data["name"],
            category=data["category"],
            price=data["price"],
            is_available=data.get("is_available", True),
        )