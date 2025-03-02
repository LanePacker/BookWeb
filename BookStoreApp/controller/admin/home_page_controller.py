from flask import jsonify, json

from BookStoreApp import app
from BookStoreApp.service.admin.home_page_service import get_general_statistic as ggs, \
    get_revenue as gr, get_cart_amount_in_month as gcm, get_top_book_selling as gtb


# Lấy thông tin thống kê tổng quan
@app.route('/admin/home-page/api/general-statistic', methods=['get'])
def get_general_statistic():
    return jsonify(ggs())


# Lấy thông tin thống kê doanh thu ngày hiện tại và ngày trước đó
@app.route('/admin/home-page/api/revenue', methods=['get'])
def get_revenue():
    return jsonify(gr())


# Lấy thông tin thống kê đơn hàng trong tháng
@app.route('/admin/home-page/api/cart-amount-month', methods=['get'])
def get_cart_amount_in_month():
    return jsonify(gcm())


# Lấy thông tin thống kê top các sách bán chạy nhất
@app.route('/admin/home-page/api/top-book', methods=['get'])
def get_top_book_selling():
    return json.dumps(gtb())
