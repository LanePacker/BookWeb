import datetime

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime, Float
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.orm import relationship

from BookStoreApp import db


# Lớp này tượng trưng cho bảng book_model dưới database
# Dùng để lưu thông tin của sách
class BookModel(db.Model):
    __tablename__ = 'book_model'
    __table_args__ = {'keep_existing': True}

    # Khóa chính
    book_id = Column(Integer, primary_key=True, autoincrement=True)

    # Thuộc tính
    name = Column(String(100), nullable=False)
    price = Column(DECIMAL, default=0.0)
    image = Column(String(255), default='')
    like_amount = Column(Integer, default=0)
    is_free_ship = Column(Boolean, default=False)
    description = Column(Text, default='')
    created_date = Column(DateTime, default=datetime.datetime.now())
    publish_date = Column(DateTime, default=datetime.datetime.now())
    author = Column(String(100), default='', nullable=False)
    page_number = Column(Integer, default=0)
    weight = Column(Float, default=0.0)
    cover_page_type = Column(String(50), default='')
    translator = Column(String(100), default='')

    # Khóa ngoại
    sale_id = Column(Integer, ForeignKey('sale_model.sale_id'))
    point_id = Column(Integer, ForeignKey('point_model.point_id'))
    manufacturer_id = Column(Integer, ForeignKey('manufacturer_model.manufacturer_id'))
    category_id = Column(Integer, ForeignKey('category_model.category_id'))
    attachment_id = Column(Integer, ForeignKey('attachment_model.attachment_id'))

    # Quan hệ
    previews = relationship('PreviewModel', backref='book', lazy=True,
                            foreign_keys='[PreviewModel.book_id]')

    def __str__(self):
        return '{}'.format(self.name)

    def set_image(self, url):
        self.image = url
