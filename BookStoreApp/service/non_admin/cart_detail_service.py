from BookStoreApp.repository.non_admin.cart_detail_repository import get_book_by_cart_id as gbbc, \
    get_cart_detail as gcd, get_total_by_cart_id as gt
from BookStoreApp.controller.utils.utils_controller import encode_vigenere


# lấy thông tin từ tầng repository và chuyển sang dạng danh sách từ điển
def get_cart_detail(account_id=None, **kwargs):
    account_data = []
    if account_id:
        cart = gcd(account_id)
        for c in cart:
            books = ''
            status = ''
            list_book = gbbc(c[0])
            if list_book:
                for lb in list_book:
                    books += lb[0] + '</br>'
            if c[2]:
                status = '<span class="font-weight-bold text-success">Đã thanh toán</span>'
            else:
                status = '<span class="font-weight-bold text-danger">Chưa thanh toán</span>'

            account_data.append({
                'id': encode_vigenere(c[0]),
                'date': c[1].strftime("%m/%d/%Y, %H:%M:%S"),
                'books': books,
                'total': float(gt(c[0])),
                'status': status
            })

    return account_data
