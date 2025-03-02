from flask import jsonify
from flask_login import current_user

from BookStoreApp import app
from BookStoreApp.service.non_admin.cart_detail_service import get_cart_detail as gcd


#  xuất thông tin tài khoản
@app.route('/client/api/cart-detail', methods=['POST'])
def cart_detail_account():
    if current_user.is_authenticated:
        return jsonify(gcd(current_user.account_id))
    return jsonify('0')

