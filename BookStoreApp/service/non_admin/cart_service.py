import math

from BookStoreApp.controller.utils.utils_controller import encode_vigenere
from BookStoreApp.repository.non_admin.cart_repository import add_to_cart, \
    get_book_in_not_paid_cart as gnc, delete_to_cart, get_amount_book_in_cart as gac, \
    update_ship_info as usi, pay_cart as pc


# Thêm sản phẩm vào giỏ hàng
def add_book_to_cart(book_id=None, account_id=None, amount=None, **kwargs):
    return {
        'result': add_to_cart(book_id=book_id, account_id=account_id, amount=amount)
    }


# Lấy sách trong giỏ hàng
def get_book_in_not_paid_cart(account_id=None, **kwargs):
    books = gnc(account_id=account_id)

    datas = []
    if books is None or len(books) == 0:
        return datas

    for book in books:
        book_sale_price = book[3] if book[4] is None else \
            math.floor(book[3] * book[4] / 100)
        datas.append({
            'book_id': encode_vigenere(int(book[0])),
            'book_name': book[1],
            'book_image': book[2],
            'book_price': '{:,.0f}'.format(book[3]),
            'book_sale_price': '{:,.0f}'.format(book_sale_price),
            'book_amount': book[5]
        })
    return datas


# Lấy giá trị đơn hàng
def get_money_total(account_id=None, **kwargs):
    books = gnc(account_id=account_id)
    if books is None or len(books) == 0:
        return {
            'cost_total': '{:,.0f}'.format(0),
            'saving_total': '{:,.0f}'.format(0),
            'sale_price_total': '{:,.0f}'.format(0)
        }
    cost_total = 0
    sale_price_total = 0
    for book in books:
        book_cost = book[3] * book[5]
        book_sale_price = book_cost if book[4] is None else \
            math.floor(book_cost * book[4] / 100)
        cost_total += book_cost
        sale_price_total += book_sale_price
    saving_total = cost_total - sale_price_total
    return {
        'cost_total': '{:,.0f}'.format(cost_total),
        'saving_total': '{:,.0f}'.format(saving_total),
        'sale_price_total': '{:,.0f}'.format(sale_price_total)
    }


# Xóa sách trong giỏ hàng
def delete_book_in_cart(book_id=None, account_id=None, **kwargs):
    return {
        'result': delete_to_cart(account_id=account_id, book_id=book_id)
    }


# Lấy số lượng sách trong đơn hàng
def get_amount_book_in_cart(account_id=None, **kwargs):
    return {
        'amount': gac(account_id=account_id)
    }


# Cập nhật thông tin ship hàng
def update_ship_info(account_id=None, **kwargs):
    return {
        'result': usi(account_id=account_id, **kwargs)
    }


# Thanh toán giỏ hàng
def pay_cart(account_id=None, **kwargs):
    return {
        'result': pc(account_id=account_id, **kwargs)
    }
