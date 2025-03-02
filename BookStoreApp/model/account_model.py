import datetime
import hashlib

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from BookStoreApp import db


# Lớp tượng trưng cho bảng account_model dưới database
# Chứa các thông tin của tài khoản
class AccountModel(db.Model, UserMixin):
    __tablename__ = 'account_model'
    __table_args__ = {'keep_existing': True}

    # khóa chính
    account_id = Column(Integer, primary_key=True, autoincrement=True)

    # thuộc tính
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(40), nullable=False)
    avatar = Column(String(200), default='https://res.cloudinary.com/attt92bookstore/image/upload/v1646017546/account'
                                         '/default_ho5q85.png')
    is_active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.datetime.now())
    lass_access = Column(DateTime, default=datetime.datetime.now())
    first_name = Column(String(20), default='', nullable=False)
    last_name = Column(String(40), default='', nullable=False)
    gmail = Column(String(50), nullable=False)
    type = Column(String(20), default='admin')

    # Khóa ngoại
    role_id = Column(Integer, ForeignKey('role_model.role_id'))

    # Ánh xạ
    __mapper_args__ = {
        'polymorphic_on': type
    }

    # Ánh xạ
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def __str__(self):
        return self.username

    def get_id(self):
        return self.account_id

    def set_avatar(self, url):
        self.avatar = url

    def set_password(self, password):
        self.password = hashlib.md5(password.encode('utf8')).hexdigest()
