
from flask import jsonify, request, json

from BookStoreApp import app
from BookStoreApp.service.admin.statistic_service import get_statistic_data as gsd, get_book_name


# Lấy thông tin dữ liệu thống kê
@app.route('/admin/statistic/api/data', methods=['post'])
def get_statistic_data():
    statistic_type = request.json.get('statistic_type')
    statistic_condition = request.json.get('statistic_condition')
    from_time = request.json.get('from_time')
    to_time = request.json.get('to_time')
    book_name = request.json.get('book_name')
    return jsonify(gsd(statistic_type=statistic_type,
                       statistic_condition=statistic_condition,
                       from_time=from_time,
                       to_time=to_time,
                       book_name=book_name))


# Lấy thông tin danh sách tên sách trùng với từ khóa
@app.route('/admin/statistic/api/book-name', methods=['post'])
def get_book_name_hint():
    keyword = request.json.get('keyword')
    book_names = []
    for book_name in get_book_name(keyword=keyword):
        book_names.append({
            'book_name': book_name[0]
        })
    return json.dumps(book_names)

