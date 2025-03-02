from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from BookStoreApp import db


# Lớp này tượng trưng cho bảng point_model dưới database
# Chứa các thông tin điểm
class PointModel(db.Model):
    __tablename__ = 'point_model'
    __table_args__ = {'keep_existing': True}

    # Khóa chính
    point_id = Column(Integer, primary_key=True, autoincrement=True)

    # Thuộc tính
    amount = Column(Integer, default=0, nullable=False)

    # Quan hệ
    sales = relationship('SaleModel', backref='point', lazy=True,
                         foreign_keys='[SaleModel.point_id]')
    books = relationship('BookModel', backref='point', lazy=True,
                         foreign_keys='[BookModel.point_id]')
