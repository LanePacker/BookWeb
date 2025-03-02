from BookStoreApp import db
from BookStoreApp import CartModel, cart_detail_model, BookModel


# lay gio hang theo account id
def get_cart_detail(id=None, **kwargs):
    query = db.session.query(CartModel.cart_id,
                             CartModel.created_date,
                             CartModel.is_paid) \
        .filter(CartModel.customer_id == id)
    return query.all()


# Tổng tiên của 1 giỏ hàng
def get_total_by_cart_id(cart_id=0, **kwargs):
    query = db.session.query(BookModel.price, cart_detail_model.c.amount) \
        .filter(cart_detail_model.c.book_id == BookModel.book_id) \
        .filter(cart_detail_model.c.cart_id == cart_id)

    list = query.all()
    total = 0
    for l in list:
        total += l.price * l.amount
    return total


# lấy danh sách book theo cart id
def get_book_by_cart_id(cart_id=None, **kwargs):
    query = db.session.query(BookModel.name) \
        .join(cart_detail_model, BookModel.book_id.__eq__(cart_detail_model.c.book_id))\
        .filter(cart_detail_model.c.cart_id == cart_id)
    return query.all()
