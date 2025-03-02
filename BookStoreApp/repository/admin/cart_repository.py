from BookStoreApp import CustomerModel, BookModel, CartModel, CategoryModel
from BookStoreApp import cart_detail_model
from BookStoreApp import db
from BookStoreApp.model.account_model import AccountModel


# Lấy tất cả dữ liệu trong giỏ hàng đã thanh toán
def get_cart_model(**kwargs):
    return CartModel.query.filter(CartModel.is_paid == True).all()  # Assuming is_paid is a boolean field


# Lấy thông tin người dùng trong giỏ hàng đã thanh toán
def get_info_user_in_cart(**kwargs):
    query = db.session.query(CartModel.cart_id, AccountModel.username, AccountModel.first_name, AccountModel.last_name,
                             CustomerModel.phone_number) \
        .filter(CartModel.customer_id == CustomerModel.account_id) \
        .filter(CustomerModel.account_id == AccountModel.account_id) \
        .filter(CartModel.is_paid == True)  # Filter for paid carts
    return query.all()


# Lấy sách trong giỏ hàng đã thanh toán
def get_book_in_cart(**kwargs):
    query = db.session.query(CartModel.cart_id, BookModel.name, CategoryModel.name, BookModel.image, \
                             cart_detail_model.c.amount, BookModel.price * cart_detail_model.c.amount) \
        .filter(CartModel.cart_id == cart_detail_model.c.cart_id) \
        .filter(cart_detail_model.c.book_id == BookModel.book_id) \
        .filter(cart_detail_model.c.cart_id == CartModel.cart_id) \
        .filter(BookModel.category_id == CategoryModel.category_id) \
        .filter(CartModel.is_paid == True)  # Filter for paid carts
    return query.all()


# Tổng tiền của 1 giỏ hàng đã thanh toán
def get_total_by_cart_id(cart_id=0, **kwargs):
    query = db.session.query(BookModel.price, cart_detail_model.c.amount) \
        .filter(cart_detail_model.c.book_id == BookModel.book_id) \
        .filter(cart_detail_model.c.cart_id == cart_id) \
        .filter(CartModel.is_paid == True)  # Ensure the cart is paid

    list = query.all()
    total = 0
    for l in list:
        total += l.price * l.amount
    return total
