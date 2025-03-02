import math

from BookStoreApp.repository.non_admin.book_detail_repository import get_book_detail_by_id as gbt, \
    get_book_preview_by_book_id as gbp, get_book_attachment_by_book_id as gab, get_attachment_by_id, \
    get_book_in_category as gbc, get_viewed_book_of_user as gvb, add_viewed_book as avb
from BookStoreApp.controller.utils.utils_controller import encode_vigenere


# Lấy thông tin của sách dựa vào id sách
def get_book_detail_by_id(book_id=None, **kwargs):
    book_detail = gbt(book_id=book_id)
    if book_detail is None:
        return {}
    book_sale_price = book_detail[3] if book_detail[13] is None else \
        math.floor(book_detail[3] * book_detail[13] / 100)
    return {
        'book_id': encode_vigenere(int(book_detail[0])),
        'book_name': book_detail[1],
        'book_image': book_detail[2],
        'book_price': '{:,.0f}'.format(book_detail[3]),
        'book_publish_date': book_detail[4].strftime('%d/%m/%Y'),
        'book_like_amount': book_detail[5],
        'book_author': book_detail[6],
        'book_is_free_ship': 'Có' if book_detail[7] else 'Không',
        'book_cover_page_type': book_detail[8],
        'book_weight': book_detail[9],
        'book_translator': book_detail[10],
        'book_page_number': book_detail[11],
        'book_description': '' if book_detail[12] is None else book_detail[12],
        'sale_percent': 0 if book_detail[13] is None else book_detail[13],
        'point_amount': book_detail[14],
        'manufacturer_name': book_detail[15],
        'category_name': book_detail[16],
        'book_price_sale': '{:,.0f}'.format(book_sale_price),
        'money_saving': '{:,.0f}'.format(book_detail[3] - book_sale_price)
    }


# Lấy thông tin các bản xem trước của sách dựa vào id sách
def get_book_preview_by_book_id(book_id=None, **kwargs):
    previews = gbp(book_id=book_id)
    datas = []
    if len(previews) == 0:
        return datas

    for preview in previews:
        datas.append({
            'preview_image': preview[0]
        })
    return datas


# Lấy thông tin bản đính kèm sách dựa vào id sách
def get_attachment_by_book_id(book_id=None, **kwargs):
    attachment = gab(book_id=book_id)
    datas = []
    if attachment is None:
        return datas

    book_attachments = get_attachment_by_id(attachment_id=attachment[0])
    if len(book_attachments) == 0:
        return datas

    for book_attachment in book_attachments:
        book_sale_price = book_attachment[2] if book_attachment[4] is None else \
            math.floor(book_attachment[2] * book_attachment[4] / 100)
        datas.append({
            'book_id': encode_vigenere(int(book_attachment[0])),
            'book_image': book_attachment[1],
            'book_price': '{:,.0f}'.format(book_attachment[2]),
            'book_name': book_attachment[3],
            'sale_percent': 0 if book_attachment[4] is None else book_attachment[4],
            'book_price_sale': '{:,.0f}'.format(book_sale_price),
            'money_saving': '{:,.0f}'.format(book_attachment[2] - book_sale_price),
            'book_author': book_attachment[5]
        })
    return datas


# Lấy thông tin sách trong 1 danh mục cụ thể
def get_book_in_category(category_name=None, **kwargs):
    books = gbc(category_name=category_name)
    datas = []
    if len(books) == 0:
        return datas

    for book in books:
        book_sale_price = book[4] if book[5] is None else \
            math.floor(book[4] * book[5] / 100)
        datas.append({
            'book_id': encode_vigenere(int(book[0])),
            'book_name': book[1],
            'book_image': book[2],
            'book_author': book[3],
            'book_price': '{:,.0f}'.format(book[4]),
            'sale_percent': 0 if book[5] is None else book[5],
            'book_sale_price': '{:,.0f}'.format(book_sale_price),
            'money_saving': '{:,.0f}'.format(book[4] - book_sale_price)
        })
    return datas


# Lấy thông tin những cuốn sách mà khách hàng đã xem qua
def get_viewed_book_of_current_user(account_id=None, **kwargs):
    datas = []
    if account_id is None:
        return datas
    viewed_books = gvb(account_id=account_id)
    if len(viewed_books) == 0:
        return datas

    for viewed_book in viewed_books:
        book_sale_price = viewed_book[4] if viewed_book[5] is None else \
            math.floor(viewed_book[4] * viewed_book[5] / 100)
        datas.append({
            'book_id': encode_vigenere(int(viewed_book[0])),
            'book_name': viewed_book[1],
            'book_image': viewed_book[2],
            'book_author': viewed_book[3],
            'book_price': '{:,.0f}'.format(viewed_book[4]),
            'sale_percent': 0 if viewed_book[5] is None else viewed_book[5],
            'book_sale_price': '{:,.0f}'.format(book_sale_price),
            'money_saving': '{:,.0f}'.format(viewed_book[4] - book_sale_price)
        })
    return datas


# Thêm sách đã xem qua
def add_viewed_book(book_id=None, account_id=None, **kwargs):
    return {
        'result': avb(book_id=book_id, account_id=account_id)
    }




