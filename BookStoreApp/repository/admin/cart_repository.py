from BookStoreApp import CustomerModel, BookModel, CartModel, CategoryModel
from BookStoreApp import cart_detail_model
from BookStoreApp import db
from BookStoreApp.model.account_model import AccountModel


# Lấy tất cả dữ liệu trong giỏ hàng đã thanh toán
def get_cart_model(**kwargs):
    return CartModel.query.filter(CartModel.is_paid == True).all()  # Assuming is_paid is a boolean field


# Lấy thông tin người dùng trong giỏ hàng đã thanh toán
def get_info_user_in_cart(**kwargs):
    query = db.session.query(
        CartModel.cart_id,
        AccountModel.username,
        AccountModel.first_name,
        AccountModel.last_name,
        CustomerModel.phone_number,
        CartModel.created_date,
    ) \
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
    """Tính tổng tiền của giỏ hàng đã thanh toán theo cart_id."""
    # Truy vấn để lấy giá sách và số lượng từ cart_detail_model
    query = db.session.query(BookModel.price, cart_detail_model.c.amount) \
        .join(cart_detail_model, cart_detail_model.c.book_id == BookModel.book_id) \
        .join(CartModel, cart_detail_model.c.cart_id == CartModel.cart_id) \
        .filter(cart_detail_model.c.cart_id == cart_id) \
        .filter(CartModel.is_paid == True)  # Đảm bảo giỏ hàng đã thanh toán

    results = query.all()  # Lấy tất cả kết quả
    total = 0
    for price, amount in results:
        total += price * amount  # Tính tổng tiền

    return total


# Xóa giỏ hàng theo ID
def delete_cart_by_id(cart_id):
    """Xóa giỏ hàng và tất cả các mục trong giỏ hàng theo cart_id."""
    try:
        # Xóa tất cả các mục trong bảng cart_detail_model dựa trên cart_id
        items_deleted = db.session.query(cart_detail_model).filter(
            cart_detail_model.c.cart_id == cart_id  # Sử dụng cart_detail_model.c để truy cập cột
        ).delete(synchronize_session='fetch')  # Xóa tất cả các mục

        # Xóa giỏ hàng khỏi bảng cart_model
        cart_deleted = db.session.query(CartModel).filter(
            CartModel.cart_id == cart_id  # Sử dụng trực tiếp thuộc tính cart_id
        ).delete(synchronize_session='fetch')  # Xóa giỏ hàng

        db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu

        if items_deleted > 0 or cart_deleted > 0:
            return True  # Trả về True nếu xóa thành công
        else:
            return False  # Trả về False nếu không tìm thấy mục nào để xóa
    except Exception as e:
        db.session.rollback()  # Hoàn tác nếu có lỗi
        print(f"Error deleting cart: {e}")
        return False  # Trả về False nếu có lỗi xảy ra