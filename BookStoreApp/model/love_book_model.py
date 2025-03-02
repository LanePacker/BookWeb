from sqlalchemy import Column, Integer, ForeignKey

from BookStoreApp import db

# Biến này tượng trưng cho bảng love_book_model dưới database
# Chứa thông tin sách yêu thích của khách hàng
love_book_model = db.Table('love_book_model',
                           Column('customer_id', Integer,
                                  ForeignKey('customer_model.account_id'), primary_key=True),
                           Column('book_id', Integer,
                                  ForeignKey('book_model.book_id'), primary_key=True),
                           keep_existing=True)
