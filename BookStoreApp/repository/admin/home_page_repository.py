import datetime

from sqlalchemy import func, desc

from BookStoreApp import db, BookModel, CategoryModel, cart_detail_model, CartModel, CustomerModel, ManufacturerModel, \
    comment_book_model


# Lấy thông tin top các sách bán chạy nhất
def get_top_book_selling(**kwargs):
    return db.session.query(BookModel.name,
                            CategoryModel.name,
                            ManufacturerModel.name,
                            BookModel.image,
                            func.sum(cart_detail_model.c.amount * BookModel.price)) \
        .select_from(BookModel) \
        .join(CategoryModel) \
        .join(ManufacturerModel) \
        .join(cart_detail_model) \
        .filter(CartModel.is_paid.__eq__(True)) \
        .group_by(BookModel.name,
                  CategoryModel.name,
                  ManufacturerModel.name,
                  BookModel.image) \
        .order_by(desc(func.sum(cart_detail_model.c.amount * BookModel.price))) \
        .slice(0, 15) \
        .all()


# Lấy thông tin số lượng đơn hàng trong tháng hiện tại
def get_cart_amount_in_month(days=None, month=None, year=None, **kwargs):
    datas = []
    for d in days:
        datas.append(db.session.query(func.count(CartModel.cart_id)) \
                     .filter(CartModel.is_paid.__eq__(True),
                             func.month(CartModel.created_date).__eq__(month),
                             func.year(CartModel.created_date).__eq__(year),
                             func.day(CartModel.created_date).__eq__(d)).first()[0])
    return datas


# Lấy thông tin doanh thu trong ngày hiện tại
def get_revenue_today(**kwargs):
    return db.session.query(func.sum(cart_detail_model.c.amount * BookModel.price)) \
        .select_from(cart_detail_model) \
        .join(BookModel) \
        .filter(func.month(cart_detail_model.c.ordered_date).__eq__(datetime.datetime.now().month),
                func.year(cart_detail_model.c.ordered_date).__eq__(datetime.datetime.now().year),
                func.day(cart_detail_model.c.ordered_date).__eq__(datetime.datetime.now().day)) \
        .first()[0]


# Lấy thông tin doanh thu trong ngày hôm qua
def get_revenue_yesterday(**kwargs):
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    return db.session.query(func.sum(cart_detail_model.c.amount * BookModel.price)) \
        .select_from(cart_detail_model) \
        .join(BookModel) \
        .join(CartModel) \
        .filter(func.month(cart_detail_model.c.ordered_date).__eq__(yesterday.month),
                func.year(cart_detail_model.c.ordered_date).__eq__(yesterday.year),
                func.day(cart_detail_model.c.ordered_date).__eq__(yesterday.day)).first()[0]


# Lấy thông tin số lượng sách
def get_book_amount(**kwargs):
    return db.session.query(func.count(BookModel.book_id)).first()[0]


# Lấy thông tin số lượng loại sách
def get_category_amount(**kwargs):
    return db.session.query(func.count(CategoryModel.category_id)).first()[0]


# Lấy thông tin số lượng đơn hàng
def get_cart_amount(**kwargs):
    return db.session.query(func.count(CartModel.cart_id)) \
        .filter(CartModel.is_paid.__eq__(True)).first()[0]


# Lấy thông tin số lượng khách hàng
def get_customer_amount(**kwargs):
    return db.session.query(func.count(CustomerModel.account_id)).first()[0]


# Lấy thông tin số lượng nhà xuất bản
def get_manufacturer_amount(**kwargs):
    return db.session.query(func.count(ManufacturerModel.manufacturer_id)).first()[0]


# Lấy thông tin số lượng đánh giá của khách hàng
def get_comment_amount(**kwargs):
    return db.session.query(comment_book_model).count()
