import datetime

from sqlalchemy import func, desc

from BookStoreApp import db, CategoryModel, BookModel, SaleModel, cart_detail_model, CartModel, AttachmentModel


# Lấy thông tin tất cả các category
def get_all_category(**kwargs):
    return db.session.query(CategoryModel.category_id,
                            CategoryModel.name) \
        .order_by(CategoryModel.name).all()


# Lấy thông tin sách trong category cụ thể
def get_book_in_category(category_id=None, **kwargs):
    return db.session.query(BookModel.book_id,
                            BookModel.name,
                            BookModel.image,
                            BookModel.price,
                            BookModel.author,
                            SaleModel.percent) \
        .join(SaleModel, BookModel.sale_id.__eq__(SaleModel.sale_id), isouter=True) \
        .join(CategoryModel, BookModel.category_id.__eq__(CategoryModel.category_id)) \
        .filter(CategoryModel.category_id.__eq__(category_id)).all()


# Lấy thông tin top 10 sách bán chạy nhất của trong category
def get_top_selling_book_category(category_id=None, **kwargs):
    return db.session.query(BookModel.book_id,
                            BookModel.name,
                            BookModel.image) \
        .join(CategoryModel, BookModel.category_id.__eq__(CategoryModel.category_id)) \
        .join(cart_detail_model, BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .join(CartModel, cart_detail_model.c.cart_id.__eq__(CartModel.cart_id)) \
        .filter(CategoryModel.category_id.__eq__(category_id),
                CartModel.is_paid.__eq__(True)) \
        .group_by(BookModel.book_id,
                  BookModel.image,
                  BookModel.name) \
        .order_by(desc(func.sum(cart_detail_model.c.amount))) \
        .slice(0, 10) \
        .all()


# Lấy thông tin tất cả sách mới trong tháng
def get_newest_book():
    return db.session.query(BookModel.book_id,
                            BookModel.name,
                            BookModel.image,
                            BookModel.price,
                            BookModel.author,
                            SaleModel.percent) \
        .join(SaleModel, BookModel.sale_id.__eq__(SaleModel.sale_id), isouter=True) \
        .join(CategoryModel, BookModel.category_id.__eq__(CategoryModel.category_id)) \
        .filter(func.month(BookModel.publish_date).__eq__(datetime.datetime.now().month)) \
        .all()


# Lấy tất cả các combo sách
def get_all_attachment():
    return db.session.query(AttachmentModel.attachment_id,
                            AttachmentModel.name,
                            func.sum(BookModel.price)) \
        .select_from(AttachmentModel) \
        .join(BookModel, AttachmentModel.attachment_id.__eq__(BookModel.book_id)) \
        .group_by(AttachmentModel.attachment_id,
                  AttachmentModel.name) \
        .order_by(AttachmentModel.name).all()


# Lấy những sách sắp phát hành
def get_coming_book():
    return db.session.query(BookModel.book_id,
                            BookModel.name,
                            BookModel.image,
                            BookModel.author,
                            BookModel.price,
                            SaleModel.percent) \
        .select_from(BookModel) \
        .join(SaleModel, BookModel.sale_id.__eq__(SaleModel.sale_id), isouter=True) \
        .join(cart_detail_model, BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .filter(BookModel.publish_date.__gt__(datetime.datetime.today())) \
        .group_by(BookModel.book_id,
                  BookModel.name,
                  BookModel.image,
                  BookModel.author,
                  BookModel.price,
                  SaleModel.percent) \
        .order_by(desc(func.sum(cart_detail_model.c.amount * BookModel.price))) \
        .all()


# Lấy thông tin sách đề xuất
def get_recommend_book():
    return db.session.query(BookModel.book_id,
                            BookModel.name,
                            BookModel.image,
                            BookModel.publish_date) \
        .join(cart_detail_model, BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .group_by(BookModel.book_id,
                  BookModel.name,
                  BookModel.image,
                  BookModel.publish_date) \
        .order_by(desc(func.sum(cart_detail_model.c.amount))) \
        .all()


# Láy top sách được bán
def get_top_selling_book():
    return db.session.query(BookModel.book_id,
                            BookModel.name,
                            BookModel.image,
                            BookModel.author,
                            BookModel.price,
                            SaleModel.percent) \
        .select_from(BookModel) \
        .join(SaleModel, BookModel.sale_id.__eq__(SaleModel.sale_id), isouter=True) \
        .join(cart_detail_model, BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .group_by(BookModel.book_id,
                  BookModel.name,
                  BookModel.image,
                  BookModel.author,
                  BookModel.price,
                  SaleModel.percent) \
        .order_by(desc(func.sum(cart_detail_model.c.amount * BookModel.price))) \
        .all()


# Lấy thông tin loại sách dựa vào id
def get_category_by_id(category_id=None, **kwargs):
    return CategoryModel.query.get(category_id)
