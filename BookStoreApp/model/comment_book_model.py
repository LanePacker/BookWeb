import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime, Text

from BookStoreApp import db

# Biến này tượng trưng cho bảng comment_book_model dưới database
# Chứa các thông tin comment của khách hàng cho sách
comment_book_model = db.Table('comment_book_model',
                              Column('customer_id', Integer,
                                     ForeignKey('customer_model.account_id'), primary_key=True),
                              Column('book_id', Integer,
                                     ForeignKey('book_model.book_id'), primary_key=True),
                              Column('created_date', DateTime, default=datetime.datetime.now()),
                              Column('content', Text, default=''),
                              keep_existing=True)
