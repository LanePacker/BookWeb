import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime

from BookStoreApp import db

# Biến này tượng trưng cho bảng cart_detail_model dưới database
# chứa các thông tin chi tiết của giỏ hàng
cart_detail_model = db.Table('cart_detail_model',
                             Column('cart_id', Integer,
                                    ForeignKey('cart_model.cart_id'), primary_key=True),
                             Column('book_id', Integer,
                                    ForeignKey('book_model.book_id'), primary_key=True),
                             Column('ordered_date', DateTime, default=datetime.datetime.now()),
                             Column('amount', Integer, default=1),
                             keep_existing=True)
