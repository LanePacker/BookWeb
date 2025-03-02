import json

from flask import request, jsonify

from BookStoreApp import app
from BookStoreApp.service.admin.cart_service import get_info_user_in_cart as info_user, get_book_in_cart as gbic, \
    get_info_user_data as giud, get_book as gb, get_list_total_money_by_cart_id as gltmbc


# Lấy thông tin giỏ hàng của khách
@app.route('/admin/api/cart', methods=['post'])
def get_cart():
    data = json.loads(request.data)
    arr = data.get('typeArrange')
    if arr == 0:
        return jsonify(giud(info_user()), gb(gbic()), gltmbc(info_user()), gltmbc(info_user()))
    if arr == 1:
        return jsonify(giud(info_user()), gb(gbic()), sorted(gltmbc(info_user())))
    else:
        return jsonify(giud(info_user()), gb(gbic()), sorted(gltmbc(info_user()), reverse=True))
