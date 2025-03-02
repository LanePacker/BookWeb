from BookStoreApp import db, BookModel, CategoryModel, ManufacturerModel, PreviewModel


# Lấy thông tin của sách dựa vào tên sách
def get_book_info_by_name(book_name=None, **kwargs):
    if book_name is None:
        return None
    return db.session.query(BookModel.name,
                            CategoryModel.name,
                            ManufacturerModel.name,
                            BookModel.image) \
        .select_from(BookModel) \
        .join(CategoryModel) \
        .join(ManufacturerModel) \
        .filter(BookModel.name.__eq__(str(book_name).strip())) \
        .first()


# Lấy thông tin của sách dựa vào tên sách
def get_book_by_name(book_name=None, **kwargs):
    if book_name is None:
        return None
    return BookModel.query.filter(BookModel.name.__eq__(book_name)).first()


# Lấy thông tin các bản xem trước của sách
def get_preview_of_book(book_name=None, **kwargs):
    if book_name is None:
        return None
    return db.session.query(PreviewModel.preview_id,
                            PreviewModel.image) \
        .join(BookModel) \
        .filter(BookModel.book_id.__eq__(PreviewModel.book_id),
                BookModel.name.__eq__(str(book_name).strip())) \
        .all()


# Lưu bản xem trước vào database
def add_preview(preview=None, **kwargs):
    if preview is None:
        return False
    try:
        db.session.add(preview)
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True


# Xóa bản xem trước
def delete_preview(preview=None, **kwargs):
    if preview is None:
        return False
    try:
        db.session.delete(preview)
        db.session.commit()
    except:
        db.session.rollback()
        return False
    return True


# Lấy thông tin bản xem trước dựa vào id
def get_preview_by_id(preview_id=None, **kwargs):
    if preview_id is None:
        return None
    return PreviewModel.query.get(preview_id)
