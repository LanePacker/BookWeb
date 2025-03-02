from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from BookStoreApp import db


# Lớp này tượng trưng cho bảng role_model dưới database
# Chứa các thông tin vai trò của tài khoản
class RoleModel(db.Model):
    __tablename__ = 'role_model'
    __table_args__ = {'keep_existing': True}

    # Khóa chính
    role_id = Column(Integer, primary_key=True, autoincrement=True)

    # Thuộc tính
    name = Column(String(20), nullable=False, unique=True)

    # Quan hệ
    accounts = relationship('AccountModel', backref='role', lazy=True,
                            foreign_keys='[AccountModel.role_id]')
