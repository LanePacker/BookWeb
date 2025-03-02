from BookStoreApp import db, BookModel, CategoryModel, ManufacturerModel, PreviewModel

# Lấy thông tin của sách dựa vào tên sách
def get_books_by_name(book_name):
    books = db.session.query(
        BookModel.book_id,
        BookModel.name.label('book_name'),
        BookModel.image.label('book_image'),
        BookModel.price.label('book_price'),  # Thêm giá sách
        CategoryModel.name.label('category_name'),
        ManufacturerModel.name.label('manufacturer_name')
    ).select_from(BookModel) \
        .join(CategoryModel, BookModel.category_id == CategoryModel.category_id) \
        .join(ManufacturerModel, BookModel.manufacturer_id == ManufacturerModel.manufacturer_id) \
        .filter(BookModel.name.ilike(f'%{book_name}%')).all()

    return [{
        'book_id': book[0],
        'book_name': book[1],
        'book_image': book[2],
        'book_price': book[3],  # Giá sách
        'category_name': book[4],
        'manufacturer_name': book[5]
    } for book in books]