import datetime

from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from BookStoreApp.model.account_model import AccountModel


# Lớp này tượng trưng cho bảng customer_model dưới database
# Chứa các thông tin của khách hàng
class CustomerModel(AccountModel):
    __tablename__ = 'customer_model'
    __table_args__ = {'keep_existing': True}
    # Khóa chính
    account_id = Column(Integer, ForeignKey('account_model.account_id'), primary_key=True)

    # Thuộc tính
    phone_number = Column(String(10), nullable=False)
    city = Column(String(30), nullable=False)
    district = Column(String(30), nullable=False)
    address = Column(String(50), nullable=False)
    date_of_birth = Column(DateTime, nullable=False, default=datetime.datetime.now())
    accumulated_point = Column(Integer, default=0)

    # Quan hệ
    carts = relationship('CartModel', backref='customer', lazy=True,
                         foreign_keys='[CartModel.customer_id]')
    sales = relationship('SaleModel', secondary='customer_sale_model',
                         backref=backref('customers', lazy=True), lazy=True)
    love_books = relationship('BookModel', secondary='love_book_model',
                              backref=backref('love_customers', lazy=True), lazy=True)
    viewed_books = relationship('BookModel', secondary='viewed_book_model',
                                backref=backref('viewed_customers', lazy=True), lazy=True)
    comment_books = relationship('BookModel', secondary='comment_book_model',
                                 backref=backref('comment_customers', lazy=True), lazy=True)

    # Ánh xạ
    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }