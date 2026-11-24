"""Quản lý thực đơn: đọc/ghi menu.json, thêm món, sửa giá, ngừng bán."""
# [SỬA QUY TẮC] Thêm docstring đầu tệp ở dòng trên (trước đây dòng 1 để
# trống). CODING_RULES mục 5: mỗi tệp .py có docstring 1 dòng ở đầu tệp.

import json
import os

from models.dish import Dish


MENU_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "menu.json",
)

CATEGORY_APPETIZER = "Khai vị"
CATEGORY_MAIN = "Món chính"
CATEGORY_DRINK = "Đồ uống"
CATEGORIES = [CATEGORY_APPETIZER, CATEGORY_MAIN, CATEGORY_DRINK]

DISH_ID_PREFIX = "M"   # mã món có dạng M001, M002, ...
DISH_ID_DIGITS = 3     # số chữ số sau chữ M



def load_menu():
    """
    Đọc toàn bộ thực đơn từ menu.json.
    - Trả về: danh sách Dish (danh sách rỗng nếu tệp chưa có hoặc rỗng)
    - Ném ValueError nếu nội dung tệp bị sai định dạng
    """
    # Tệp chưa tồn tại -> chưa có món nào
    if not os.path.exists(MENU_FILE_PATH):
        return []

    with open(MENU_FILE_PATH, "r", encoding="utf-8") as file:
        content = file.read().strip()

    # Tệp rỗng -> chưa có món nào
    if content == "":
        return []

    try:
        data = json.loads(content)
        if not isinstance(data, list):
            raise ValueError("Thực đơn phải là một danh sách.")
        dishes = []
        for item in data:
            dishes.append(Dish.from_dict(item))
        return dishes
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise ValueError("Dữ liệu thực đơn không hợp lệ.") from error


def save_menu(dishes):
    """
    Ghi danh sách món vào menu.json.
    - dishes: danh sách Dish
    - Ném ValueError nếu danh sách không hợp lệ
    """
    try:
        data = []
        for dish in dishes:
            data.append(dish.to_dict())
    except (TypeError, AttributeError) as error:
        raise ValueError("Danh sách món không hợp lệ.") from error

    # Tạo thư mục data/ nếu chưa có
    os.makedirs(os.path.dirname(MENU_FILE_PATH), exist_ok=True)
    with open(MENU_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)



def _check_price(price):
    """Kiểm tra đơn giá: phải là số nguyên lớn hơn 0."""
    # bool cũng là int trong Python (True == 1) nên phải loại ra
    if isinstance(price, bool) or not isinstance(price, int):
        raise ValueError("Giá phải là số nguyên.")
    if price <= 0:
        raise ValueError("Giá phải lớn hơn 0.")


def _check_category(category):
    """Kiểm tra nhóm món phải nằm trong CATEGORIES."""
    if category not in CATEGORIES:
        raise ValueError(
            "Nhóm món không hợp lệ. Chọn: {}.".format(", ".join(CATEGORIES))
        )


def _generate_dish_id(dishes):
    """Sinh mã món mới = số lớn nhất hiện có + 1 (vd M010 -> M011)."""
    biggest_number = 0
    for dish in dishes:
        number_part = dish.dish_id[len(DISH_ID_PREFIX):]
        if number_part.isdigit() and int(number_part) > biggest_number:
            biggest_number = int(number_part)
    return "{}{:0{}d}".format(
        DISH_ID_PREFIX, biggest_number + 1, DISH_ID_DIGITS
    )




def get_all_dishes():
    """Trả về danh sách tất cả món (kể cả món đã ngừng bán)."""
    return load_menu()


def get_dishes_by_category(category):
    """
    Lấy các món thuộc một nhóm.
    - category: nhóm món, phải thuộc CATEGORIES
    - Trả về: danh sách Dish của nhóm đó
    - Ném ValueError nếu nhóm không hợp lệ
    """
    _check_category(category)
    result = []
    for dish in load_menu():
        if dish.category == category:
            result.append(dish)
    return result


def find_dish_by_id(dish_id):
    """
    Tìm một món theo mã (không phân biệt hoa/thường, vd "m004").
    - dish_id: mã món, vd "M004"
    - Trả về: Dish tìm được
    - Ném ValueError nếu không tìm thấy món
    """
    wanted_id = str(dish_id).strip().upper()
    for dish in load_menu():
        if dish.dish_id == wanted_id:
            return dish
    raise ValueError("Không tìm thấy món có mã {}.".format(wanted_id))




def add_new_dish(name, category, price):
    """
    Thêm món mới vào thực đơn (mã món tự sinh, mặc định đang bán).
    - name: tên món
    - category: nhóm món, phải thuộc CATEGORIES
    - price: đơn giá (VNĐ), số nguyên > 0
    - Trả về: Dish vừa thêm
    - Ném ValueError nếu tên trống/trùng, nhóm hoặc giá không hợp lệ
    """
    name = str(name).strip()
    if name == "":
        raise ValueError("Tên món không được để trống.")
    _check_category(category)
    _check_price(price)

    dishes = load_menu()
    for dish in dishes:
        if dish.name.lower() == name.lower():
            raise ValueError("Món \"{}\" đã có trong thực đơn.".format(name))

    new_dish = Dish(_generate_dish_id(dishes), name, category, price)
    dishes.append(new_dish)
    save_menu(dishes)
    return new_dish


def update_dish_price(dish_id, new_price):
    """
    Cập nhật giá một món.
    - dish_id: mã món cần sửa
    - new_price: giá mới (VNĐ), số nguyên > 0
    - Trả về: Dish sau khi sửa
    - Ném ValueError nếu không tìm thấy món hoặc giá không hợp lệ
    """
    _check_price(new_price)
    return _change_dish(dish_id, price=new_price)


def set_dish_availability(dish_id, is_available):
    """
    Ngừng bán hoặc mở bán lại một món.
    - dish_id: mã món cần đổi
    - is_available: True = mở bán, False = ngừng bán
    - Trả về: Dish sau khi sửa
    - Ném ValueError nếu không tìm thấy món
    """
    return _change_dish(dish_id, is_available=bool(is_available))


def _change_dish(dish_id, price=None, is_available=None):
    """Tìm món, đổi giá và/hoặc trạng thái rồi lưu lại tệp."""
    wanted_id = str(dish_id).strip().upper()
    dishes = load_menu()
    for dish in dishes:
        if dish.dish_id == wanted_id:
            if price is not None:
                dish.price = price
            if is_available is not None:
                dish.is_available = is_available
            save_menu(dishes)
            return dish
    raise ValueError("Không tìm thấy món có mã {}.".format(wanted_id))
