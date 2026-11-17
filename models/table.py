"""Định nghĩa đối tượng Bàn ăn (DiningTable)."""

STATUS_EMPTY = "empty"
STATUS_SERVING = "serving"


class DiningTable:
    """Một bàn ăn trong nhà hàng."""

    def __init__(self, table_number, status=STATUS_EMPTY):
        self.table_number = table_number
        self.status = status

    def is_empty(self):
        """Trả về True nếu bàn đang trống."""
        return self.status == STATUS_EMPTY

    def to_dict(self):
        """Chuyển đối tượng sang từ điển."""
        return {"table_number": self.table_number, "status": self.status}

    @classmethod
    def from_dict(cls, data):
        """Tạo đối tượng DiningTable từ từ điển."""
        return cls(data["table_number"], data.get("status", STATUS_EMPTY))