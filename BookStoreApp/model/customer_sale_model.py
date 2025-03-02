from sqlalchemy import Column, ForeignKey, Integer
from BookStoreApp import db

# Biến này tượng trưng cho bảng customer_sale_model dưới database
# Chứa các thông tin phiếu giảm giá của khách hàng
customer_sale_model = db.Table('customer_sale_model',
                               Column('customer_id', Integer,
                                      ForeignKey('customer_model.account_id'), primary_key=True),
                               Column('sale_id', Integer,
                                      ForeignKey('sale_model.sale_id'), primary_key=True),
                               Column('amount', Integer, default=1),
                               keep_existing=True)
