import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime

from BookStoreApp import db

# Biến này tượng trưng cho bảng viewed_book_model dưới database
# Chứa các thông tin của những sách khách hàng đã xem qua
viewed_book_model = db.Table('viewed_book_model',
                             Column('customer_id', Integer,
                                    ForeignKey('customer_model.account_id'), primary_key=True),
                             Column('book_id', Integer,
                                    ForeignKey('book_model.book_id'), primary_key=True),
                             Column('viewed_date', DateTime, default=datetime.datetime.now()),
                             keep_existing=True)
