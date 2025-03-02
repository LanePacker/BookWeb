import datetime

from sqlalchemy import desc, func

from BookStoreApp import db, BookModel, SaleModel, PointModel, ManufacturerModel, CategoryModel, AttachmentModel, \
    PreviewModel, viewed_book_model, cart_detail_model


# Lấy thông tin của sách dựa vào id sách
def get_book_detail_by_id(book_id=None, **kwargs):
    return db.session.query(BookModel.book_id,
                            BookModel.name,
                            BookModel.image,
                            BookModel.price,
                            BookModel.publish_date,
                            BookModel.like_amount,
                            BookModel.author,
                            BookModel.is_free_ship,
                            BookModel.cover_page_type,
                            BookModel.weight,
                            BookModel.translator,
                            BookModel.page_number,
                            BookModel.description,
                            SaleModel.percent,
                            PointModel.amount,
                            ManufacturerModel.name,
                            CategoryModel.name) \
        .select_from(BookModel) \
        .join(SaleModel, BookModel.sale_id.__eq__(SaleModel.sale_id), isouter=True) \
        .join(PointModel, BookModel.point_id.__eq__(PointModel.point_id)) \
        .join(ManufacturerModel, BookModel.manufacturer_id.__eq__(ManufacturerModel.manufacturer_id)) \
        .join(CategoryModel, BookModel.category_id.__eq__(CategoryModel.category_id)) \
        .filter(BookModel.book_id.__eq__(book_id)).first()


# Lấy thông tin các bản xem trước của sách dựa vào id sách
def get_book_preview_by_book_id(book_id=None, **kwargs):
    return db.session.query(PreviewModel.image) \
        .filter(PreviewModel.book_id.__eq__(book_id)) \
        .all()


# Lấy thông tin bản đính kèm sách dựa vào id sách
def get_book_attachment_by_book_id(book_id=None, **kwargs):
    return db.session.query(AttachmentModel.attachment_id,
                            AttachmentModel.name) \
        .join(BookModel) \
        .filter(AttachmentModel.attachment_id.__eq__(BookModel.attachment_id),
                BookModel.book_id.__eq__(book_id)).first()


# Lấy thông tin bản đính kèm sách dựa vào id bản đính kèm
def get_attachment_by_id(attachment_id=None, **kwargs):
    return db.session.query(BookModel.book_id,
                            BookModel.image,
                            BookModel.price,
                            BookModel.name,
                            SaleModel.percent,
                            BookModel.author) \
        .select_from(BookModel) \
        .join(SaleModel, BookModel.sale_id.__eq__(SaleModel.sale_id), isouter=True) \
        .join(AttachmentModel, BookModel.attachment_id.__eq__(AttachmentModel.attachment_id)) \
        .filter(AttachmentModel.attachment_id.__eq__(attachment_id)) \
        .group_by(BookModel.book_id,
                  BookModel.image,
                  BookModel.price,
                  BookModel.name,
                  SaleModel.percent) \
        .all()


# Lấy thông tin sách trong 1 danh mục cụ thể
def get_book_in_category(category_name=None, **kwargs):
    return db.session.query(BookModel.book_id,
                            BookModel.name,
                            BookModel.image,
                            BookModel.author,
                            BookModel.price,
                            SaleModel.percent) \
        .select_from(BookModel) \
        .join(SaleModel, BookModel.sale_id.__eq__(SaleModel.sale_id), isouter=True) \
        .join(CategoryModel, BookModel.category_id.__eq__(CategoryModel.category_id)) \
        .filter(CategoryModel.name.__eq__(category_name)).all()


# Lấy thông tin những cuốn sách mà khách hàng đã xem qua
def get_viewed_book_of_user(account_id=None, **kwargs):
    return db.session.query(BookModel.book_id,
                            BookModel.name,
                            BookModel.image,
                            BookModel.author,
                            BookModel.price,
                            SaleModel.percent) \
        .select_from(BookModel) \
        .join(viewed_book_model, BookModel.book_id.__eq__(viewed_book_model.c.book_id)) \
        .join(SaleModel, BookModel.sale_id.__eq__(SaleModel.sale_id), isouter=True) \
        .filter(viewed_book_model.c.customer_id.__eq__(account_id)).all()


# Thêm sách đã xem qua
def add_viewed_book(book_id=None, account_id=None, **kwargs):
    book = BookModel.query.get(book_id)
    if book is None:
        return False
    try:
        statement = viewed_book_model.insert() \
            .values(book_id=book.book_id, customer_id=account_id)
        db.session.execute(statement)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False



