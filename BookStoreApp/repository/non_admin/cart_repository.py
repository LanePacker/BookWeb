from sqlalchemy import func

from BookStoreApp import db, BookModel, SaleModel, CartModel, CustomerModel, cart_detail_model
from BookStoreApp.model.account_model import AccountModel


# Kiểm tra xem khách hàng có còn giỏ hàng nào chưa thanh toán hay không
def get_not_paid_cart(account_id=None, **kwargs):
    not_paid_cart = db.session.query(CartModel.cart_id) \
        .join(CustomerModel, CartModel.customer_id.__eq__(CustomerModel.account_id)) \
        .filter(CustomerModel.account_id.__eq__(account_id),
                CartModel.is_paid.__eq__(False)).first()
    return not_paid_cart


# Lấy sách trong giỏ hàng
def get_book_in_not_paid_cart(account_id=None, **kwargs):
    not_paid_cart = get_not_paid_cart(account_id=account_id)
    if not_paid_cart is None:
        return None

    return db.session.query(BookModel.book_id,
                            BookModel.name,
                            BookModel.image,
                            BookModel.price,
                            SaleModel.percent,
                            func.sum(cart_detail_model.c.amount)) \
        .select_from(BookModel) \
        .join(SaleModel, BookModel.sale_id.__eq__(SaleModel.sale_id), isouter=True) \
        .join(cart_detail_model, BookModel.book_id.__eq__(cart_detail_model.c.book_id)) \
        .join(CartModel, cart_detail_model.c.cart_id.__eq__(CartModel.cart_id)) \
        .group_by(BookModel.book_id,
                  BookModel.name,
                  BookModel.image,
                  BookModel.price,
                  SaleModel.percent) \
        .filter(CartModel.cart_id.__eq__(not_paid_cart[0])).all()


# Lấy thông tin của sách dựa trên id
def get_book_by_book_id(book_id=None):
    return BookModel.query.get(book_id)


# Lấy thông tin của đơn hàng dựa trên id
def get_cart_by_cart_id(cart_id=None):
    return CartModel.query.get(cart_id)


# Lấy thông tin của user dựa trên id
def get_user_by_account_id(account_id=None):
    return AccountModel.query.get(account_id)


# Thêm một giỏ hàng mới
def add_new_cart(cart=None):
    try:
        db.session.add(cart)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


# Lấy thông tin của cart detail
def get_cart_detail(cart_id=None, book_id=None, **kwargs):
    return db.session.query(cart_detail_model) \
        .filter(cart_detail_model.c.cart_id.__eq__(cart_id),
                cart_detail_model.c.book_id.__eq__(book_id)).first()


# Xoas giỏ hàng
def delete_cart(cart_id=None, **kwargs):
    try:
        db.session.delete(CartModel.query.get(cart_id))
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


# Xóa sản phẩm trong giỏ hàng
def delete_cart_detail(cart_id=None, book_id=None, **kwargs):
    try:
        statement = cart_detail_model.delete() \
            .where(cart_detail_model.c.cart_id.__eq__(cart_id),
                   cart_detail_model.c.book_id.__eq__(book_id))
        db.session.execute(statement)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


# Cập nhật thông tin cart detail
def update_cart_detail(cart_id=None, book_id=None, amount=None, **kwargs):
    if amount == 0:
        return delete_cart_detail(cart_id=cart_id, book_id=book_id)

    try:
        statement = cart_detail_model.update() \
            .where(cart_detail_model.c.cart_id.__eq__(cart_id),
                   cart_detail_model.c.book_id.__eq__(book_id)) \
            .values(amount=amount)
        db.session.execute(statement)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


# Thêm cart detail
def add_cart_detail(cart=None, book=None, amount=None):
    try:
        statement = cart_detail_model.insert().values(cart_id=cart.cart_id,
                                                      book_id=book.book_id,
                                                      amount=amount)
        db.session.execute(statement)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


# Thêm sản phẩm vào giỏ hàng
def add_to_cart(book_id=None, account_id=None, amount=None, **kwargs):
    if get_not_paid_cart(account_id=account_id) is None:
        customer = get_user_by_account_id(account_id=account_id)
        cart = CartModel(customer_id=customer.account_id)
        if not add_new_cart(cart=cart)  :
            return False

    book = get_book_by_book_id(book_id=book_id)
    cart = get_cart_by_cart_id(get_not_paid_cart(account_id=account_id)[0])
    cart_detail = get_cart_detail(cart_id=cart.cart_id,
                                  book_id=book.book_id)

    if cart_detail is not None:
        return update_cart_detail(cart_id=cart.cart_id,
                                  book_id=book.book_id,
                                  amount=amount + cart_detail[3])
    return add_cart_detail(cart=cart, book=book, amount=amount)


# Xóa sách trong giỏ hàng
def delete_to_cart(book_id=None, account_id=None, **kwargs):
    book = get_book_by_book_id(book_id=book_id)
    cart = get_cart_by_cart_id(get_not_paid_cart(account_id=account_id)[0])
    return delete_cart_detail(cart_id=cart.cart_id, book_id=book.book_id)


# Lấy số lượng chi tiết đơn hàng
def get_amount_cart_detail_by_cart_id(cart_id=None, **kwargs):
    data = db.session.query(func.sum(cart_detail_model.c.amount)) \
        .filter(cart_detail_model.c.cart_id.__eq__(cart_id)).first()
    if data is None:
        return 0
    return data[0]


# Lấy số lượng sách trong đơn hàng
def get_amount_book_in_cart(account_id=None, **kwargs):
    if account_id is None:
        return 0
    not_paid_cart = get_not_paid_cart(account_id=account_id)
    if not_paid_cart is None:
        return 0
    amount = get_amount_cart_detail_by_cart_id(cart_id=not_paid_cart[0])
    if amount is None:
        return 0
    return amount


# Cập nhật thông tin ship hàng
def update_ship_info(account_id=None, **kwargs):
    if account_id is None:
        return False

    not_paid_cart = get_not_paid_cart(account_id=account_id)
    if not_paid_cart is None:
        return False

    customer_fullname = kwargs.get('customer_fullname')
    customer_phone_number = kwargs.get('customer_phone_number')
    customer_address = kwargs.get('customer_address')
    customer_note = kwargs.get('customer_note')
    cart_otp = kwargs.get('cart_otp')
    try:
        cart = get_cart_by_cart_id(cart_id=not_paid_cart[0])
        cart.customer_fullname = customer_fullname
        cart.customer_phone_number = customer_phone_number
        cart.customer_address = customer_address
        cart.customer_note = customer_note
        cart.cart_otp = cart_otp
        db.session.add(cart)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


# Thanh toán giỏ hàng
def pay_cart(account_id=None, **kwargs):
    if account_id is None:
        return False

    not_paid_cart = get_not_paid_cart(account_id=account_id)
    if not_paid_cart is None:
        return False

    try:
        cart = get_cart_by_cart_id(cart_id=not_paid_cart[0])
        cart.is_paid = True
        db.session.add(cart)
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False
