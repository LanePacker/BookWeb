from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from BookStoreApp import db


# Lớp này tượng trưng cho bảng manufacturer_model dưới database
# Dùng chứa các thông tin của nhà xuất bản
class ManufacturerModel(db.Model):
    __tablename__ = 'manufacturer_model'
    __table_args__ = {'keep_existing': True}

    # Khóa chính
    manufacturer_id = Column(Integer, primary_key=True, autoincrement=True)

    # Thuộc tính
    name = Column(String(255), nullable=False, unique=True)

    # Quan hệ
    books = relationship('BookModel', backref='manufacturer', lazy=True,
                         foreign_keys='[BookModel.manufacturer_id]')
