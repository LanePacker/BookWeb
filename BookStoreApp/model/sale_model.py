from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from BookStoreApp import db


# Lớp này tượng trưng cho bảng sale_model dưới database
# Chứa các thông tin của giảm giá
class SaleModel(db.Model):
    __tablename__ = 'sale_model'
    __table_args__ = {'keep_existing': True}

    # Khóa chính
    sale_id = Column(Integer, primary_key=True, autoincrement=True)

    # Thuộc tính
    percent = Column(Integer, nullable=False, unique=True)

    # Khóa ngoại
    point_id = Column(Integer, ForeignKey('point_model.point_id'))

    # Quan hệ
    books = relationship('BookModel', backref='sale', lazy=True,
                         foreign_keys='[BookModel.sale_id]')
