from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from BookStoreApp import db


# Lớp này tượng trưng cho bảng attachment_model dưới database
# Dùng chứa các thông tin của sách đính kèm
class AttachmentModel(db.Model):
    __tablename__ = 'attachment_model'
    __table_args__ = {'keep_existing': True}

    # Khóa chính
    attachment_id = Column(Integer, primary_key=True, autoincrement=True)

    # Thuộc tính
    name = Column(String(255), nullable=False, unique=True)

    # Quan hệ
    books = relationship('BookModel', backref='attachment', lazy=True,
                         foreign_keys='[BookModel.attachment_id]')
