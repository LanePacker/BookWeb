from sqlalchemy import func

from BookStoreApp import db, BookModel, CartModel
from BookStoreApp.model.cart_detail_model import cart_detail_model


# Tạo câu truy vấn khi lấy báo cáo doanh thu
def get_revenue_query(**kwargs):
    return db.session.query(cart_detail_model.c.ordered_date,
                            func.sum(cart_detail_model.c.amount * BookModel.price)) \
        .join(BookModel) \
        .filter(BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .join(CartModel)\
        .filter(CartModel.is_paid.__eq__(True))\
        .group_by(cart_detail_model.c.ordered_date) \
        .order_by(cart_detail_model.c.ordered_date)


# Tạo câu truy vấn khi báo cáo tần suất bán sách
def get_frequently_book_selling_query(**kwargs):
    return db.session.query(BookModel.name,
                            func.sum(cart_detail_model.c.amount)) \
        .join(BookModel)\
        .filter(BookModel.book_id == cart_detail_model.c.book_id) \
        .join(CartModel) \
        .filter(CartModel.is_paid.__eq__(True)) \
        .group_by(BookModel.name) \
        .order_by(BookModel.name)


# Lọc sữ liệu báo cáo theo điều kiện
def get_report_data(query=None, **kwargs):
    if query is None:
        return None

    month = kwargs.get('month')
    quarter = kwargs.get('quarter')
    year = kwargs.get('year')

    if month:
        query = query.filter(func.month(cart_detail_model.c.ordered_date) == month)

    if quarter:
        query = query.filter(func.quarter(cart_detail_model.c.ordered_date) == quarter)

    if year:
        query = query.filter(func.year(cart_detail_model.c.ordered_date) == year)

    if kwargs.get('begin_index') is not None and kwargs.get('begin_index') is not None:
        query = query.slice(int(kwargs.get('begin_index')), int(kwargs.get('end_index')))

    return query.all()
