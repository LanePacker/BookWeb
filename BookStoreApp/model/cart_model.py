import datetime

from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, String, Text
from sqlalchemy.orm import relationship, backref

from BookStoreApp import db


# Lớp này tượng trưng cho bảng cart_model dưới database
# Chứa các thông tin của giỏ hàng
class CartModel(db.Model):
    __tablename__ = 'cart_model'
    __table_args__ = {'keep_existing': True}
    # Khóa chính
    cart_id = Column(Integer, primary_key=True, autoincrement=True)

    # Thuộc tính
    is_paid = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.datetime.now())
    customer_fullname = Column(String(100), default=None)
    customer_phone_number = Column(String(10), default=None)
    customer_address = Column(String(100), default=None)
    customer_note = Column(Text, default=None)
    cart_otp = Column(String(6), default=None)
    # Khóa ngoại
    customer_id = Column(Integer, ForeignKey('customer_model.account_id'))

    # Quan hệ
    books = relationship('BookModel', secondary='cart_detail_model',
                         backref=backref('carts', lazy=True), lazy=True)
