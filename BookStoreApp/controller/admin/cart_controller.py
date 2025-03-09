import json
from flask import request, jsonify
from BookStoreApp import app
from BookStoreApp.service.admin.cart_service import (
    get_info_user_in_cart as info_user,
    get_book_in_cart as gbic,
    get_info_user_data as giud,
    get_book as gb,
    get_list_total_money_by_cart_id as gltmbc,
    delete_cart_item_by_id
)

# Lấy thông tin giỏ hàng của khách
@app.route('/admin/api/cart', methods=['POST'])
def get_cart():
    try:
        data = json.loads(request.data)
        arr = data.get('typeArrange', 0)  # Mặc định là 0 nếu không có

        # Lấy thông tin người dùng và sách trong giỏ hàng
        user_info = giud(info_user())
        books_in_cart = gb(gbic())
        total_money_list = gltmbc(info_user())
        

        if arr == 0:
            return jsonify(user_info, books_in_cart, total_money_list, total_money_list)
        elif arr == 1:
            return jsonify(user_info, books_in_cart, sorted(total_money_list))
        else:
            return jsonify(user_info, books_in_cart, sorted(total_money_list, reverse=True))
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Trả về lỗi nếu có

# Xóa đơn hàng theo ID
@app.route('/admin/api/cart/<int:cart_id>', methods=['DELETE'])
def delete_cart_item(cart_id):
    try:
        result = delete_cart_item_by_id(cart_id)
        if result:
            return jsonify({"message": "Tất cả các mục trong giỏ hàng đã được xóa thành công"}), 200
        else:
            return jsonify({"message": "Không tìm thấy mục nào trong giỏ hàng"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Trả về lỗi nếu có