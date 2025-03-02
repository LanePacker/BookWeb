from operator import and_

from sqlalchemy import func

from BookStoreApp import db, BookModel, CartModel
from BookStoreApp.model.cart_detail_model import cart_detail_model


# Lấy thông tin thống kê doanh thu theo tháng, hoặc giữa 2 tháng
def get_statistic_revenue_month(from_month=None, to_month=None):
    data = db.session.query(func.month(cart_detail_model.c.ordered_date),
                            func.sum(cart_detail_model.c.amount * BookModel.price)) \
        .join(BookModel) \
        .filter(BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .join(CartModel) \
        .filter(CartModel.is_paid.__eq__(True)) \
        .group_by(func.month(cart_detail_model.c.ordered_date)) \
        .order_by(func.month(cart_detail_model.c.ordered_date))

    if from_month and to_month:
        data = data.filter(and_(func.month(cart_detail_model.c.ordered_date) >= from_month,
                                func.month(cart_detail_model.c.ordered_date) <= to_month))
    return data.all()


# Lấy thông tin thống kê doanh thu theo quý, hoặc giữa 2 quý
def get_statistic_revenue_quarter(from_quarter=None, to_quarter=None):
    data = db.session.query(func.quarter(cart_detail_model.c.ordered_date),
                            func.sum(cart_detail_model.c.amount * BookModel.price)) \
        .join(BookModel) \
        .filter(BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .join(CartModel) \
        .filter(CartModel.is_paid.__eq__(True)) \
        .group_by(func.quarter(cart_detail_model.c.ordered_date)) \
        .order_by(func.quarter(cart_detail_model.c.ordered_date))

    if from_quarter and to_quarter:
        data = data.filter(and_(func.quarter(cart_detail_model.c.ordered_date) >= from_quarter,
                                func.quarter(cart_detail_model.c.ordered_date) <= to_quarter))
    return data.all()


# Lấy thông tin thống kê doanh thu theo năm, hoặc giữa 2 năm
def get_statistic_revenue_year(from_year=None, to_year=None):
    data = db.session.query(func.year(cart_detail_model.c.ordered_date),
                            func.sum(cart_detail_model.c.amount * BookModel.price)) \
        .join(BookModel) \
        .filter(BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .join(CartModel) \
        .filter(CartModel.is_paid.__eq__(True)) \
        .group_by(func.year(cart_detail_model.c.ordered_date)) \
        .order_by(func.year(cart_detail_model.c.ordered_date))

    if from_year and to_year:
        data = data.filter(and_(func.year(cart_detail_model.c.ordered_date) >= from_year,
                                func.year(cart_detail_model.c.ordered_date) <= to_year))
    return data.all()


# Lấy thông tin thống kê tần suất bán sách theo tháng, hoặc giữa 2 tháng
def get_statistic_frequently_book_selling_month(from_month=None, to_month=None, book_name=None):
    data = db.session.query(func.month(cart_detail_model.c.ordered_date),
                            func.sum(cart_detail_model.c.amount)) \
        .join(BookModel) \
        .filter(BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .join(CartModel) \
        .filter(CartModel.is_paid.__eq__(True)) \
        .group_by(func.month(cart_detail_model.c.ordered_date)) \
        .order_by(func.month(cart_detail_model.c.ordered_date))

    if book_name:
        data = data.filter(BookModel.name.__eq__(book_name.strip()))

    if from_month and to_month:
        data = data.filter(and_(func.month(cart_detail_model.c.ordered_date) >= from_month,
                                func.month(cart_detail_model.c.ordered_date) <= to_month))
    return data.all()


# Lấy thông tin thống kê tần suất bán sách theo quý, hoặc giữa 2 quý
def get_statistic_frequently_book_selling_quarter(from_quarter=None, to_quarter=None, book_name=None):
    data = db.session.query(func.quarter(cart_detail_model.c.ordered_date),
                            func.sum(cart_detail_model.c.amount)) \
        .join(BookModel) \
        .filter(BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .join(CartModel) \
        .filter(CartModel.is_paid.__eq__(True)) \
        .group_by(func.quarter(cart_detail_model.c.ordered_date)) \
        .order_by(func.quarter(cart_detail_model.c.ordered_date))

    if book_name:
        data = data.filter(BookModel.name.__eq__(book_name.strip()))

    if from_quarter and to_quarter:
        data = data.filter(and_(func.quarter(cart_detail_model.c.ordered_date) >= from_quarter,
                                func.quarter(cart_detail_model.c.ordered_date) <= to_quarter))
    return data.all()


# Lấy thông tin thống kê tần suất bán sách theo năm, hoặc giữa 2 năm
def get_statistic_frequently_book_selling_year(from_year=None, to_year=None, book_name=None):
    data = db.session.query(func.year(cart_detail_model.c.ordered_date),
                            func.sum(cart_detail_model.c.amount)) \
        .join(BookModel) \
        .filter(BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .join(CartModel) \
        .filter(CartModel.is_paid.__eq__(True)) \
        .group_by(func.year(cart_detail_model.c.ordered_date)) \
        .order_by(func.year(cart_detail_model.c.ordered_date))

    if book_name:
        data = data.filter(BookModel.name.__eq__(book_name.strip()))

    if from_year and to_year:
        data = data.filter(and_(func.year(cart_detail_model.c.ordered_date) >= from_year,
                                func.year(cart_detail_model.c.ordered_date) <= to_year))
    return data.all()


# Lấy thông tin danh sách tên sách dựa vào từ khóa
def get_book_name(keyword=None):
    if keyword is None:
        return None

    return db.session.query(BookModel.name) \
        .filter(BookModel.name.like('{}%'.format(keyword.strip()))) \
        .slice(0, 10) \
        .all()
