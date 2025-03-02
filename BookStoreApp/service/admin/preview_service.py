from BookStoreApp.repository.admin.preview_repository import get_preview_of_book as gpb \
    , get_book_info_by_name as gbn, get_book_by_name as gbbn, add_preview as ad, delete_preview as dp \
    , get_preview_by_id as gpi


# Lấy thông tin của sách dựa vào tên sách
def get_book_info_by_name(book_name=None, **kwargs):
    book_info = gbn(book_name=book_name)
    if book_info is None:
        return None
    return {
        'book_name': book_info[0],
        'category_name': book_info[1],
        'manufacturer_name': book_info[2],
        'book_image': book_info[3]
    }


# Lấy thông tin của sách dựa vào tên sách
def get_book_by_name(book_name=None, **kwargs):
    return gbbn(book_name=book_name)


# Lấy thông tin các bản xem trước của sách
def get_preview_of_book(book_name=None, **kwargs):
    data = gpb(book_name=book_name)
    previews = []
    if data is None:
        return previews
    for preview in data:
        previews.append({
            'preview_id': preview[0],
            'preview_image': preview[1]
        })
    return previews


# Lưu bản xem trước vào database
def add_preview(preview=None, **kwargs):
    return ad(preview=preview)


# Xóa bản xem trước
def delete_preview(preview=None, **kwargs):
    return dp(preview=preview)


# Lấy thông tin bản xem trước dựa vào id
def get_preview_by_id(preview_id=None, **kwargs):
    return gpi(preview_id=preview_id)
