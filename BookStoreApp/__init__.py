import cloudinary
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from BookStoreApp.model_view.home_page_view import HomeView
from twilio.rest import Client

app = Flask(__name__)

# thông tin database
USERNAME_DB = 'root'
PASSWORD_DB = 'tuoide0961872374'
NAME_DB = 'BookStore'
IP_DB = 'localhost'

# Thông tin cloudinary
CLOUD_NAME = 'attt92bookstore'
API_KEY = '718111144413712'
API_SECRET = 'QBWH4PeSsQKyl4Elx1alQiWEhzs'

# Cấu hình flask
app.config['SQLALCHEMY_DATABASE_URI'] = \
    str.format(f'mysql+pymysql://{USERNAME_DB}:{PASSWORD_DB}@{IP_DB}/{NAME_DB}?charset=utf8mb4')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = b'21137afa59a4dd08b708dcf106c724f9'

# Khởi tạo cấu hình
db = SQLAlchemy(app=app)
admin = Admin(app=app, name='Cửa hàng sách', template_mode='bootstrap4',
              index_view=HomeView(name='Trang chủ'))
login = LoginManager(app=app)
cloudinary.config(cloud_name=CLOUD_NAME,
                  api_key=API_KEY,
                  api_secret=API_SECRET)



# thanh toán momo
API_URL = 'https://test-payment.momo.vn/v2/gateway/api/create'
SECRET_KEY = 'NsyubDwquURwV46FycWCxdCqYsB8HUEd'
ACCESS_KEY = 'zvdfoutMBqzlawgZ'
PARTNER_CODE = 'MOMOO5NG20220325'

# Import model database
from model.book_model import BookModel
from model.cart_model import CartModel
from model.category_model import CategoryModel
from model.customer_model import CustomerModel
from model.manufacturer_model import ManufacturerModel
from model.point_model import PointModel
from model.preview_model import PreviewModel
from model.role_model import RoleModel
from model.sale_model import SaleModel
from model.attachment_model import AttachmentModel
from model.cart_detail_model import cart_detail_model
from model.comment_book_model import comment_book_model
from model.customer_sale_model import customer_sale_model
from model.love_book_model import love_book_model
from model.viewed_book_model import viewed_book_model

# Import view
from BookStoreApp.model_view.book_view import BookView
from BookStoreApp.model_view.category_view import CategoryView
from BookStoreApp.model_view.customer_view import CustomerView
from BookStoreApp.model_view.manufacturer_view import ManufacturerView
from BookStoreApp.model_view.point_view import PointView
from BookStoreApp.model_view.role_view import RoleView
from BookStoreApp.model_view.sale_view import SaleView
from BookStoreApp.model_view.cart_view import CartView
from BookStoreApp.model_view.change_password_view import ChangePasswordView
from BookStoreApp.model_view.log_out_view import LogOutView
from BookStoreApp.model_view.preview_view import PreviewView
from BookStoreApp.model_view.profile_view import ProfileView
from BookStoreApp.model_view.report_view import ReportView
from BookStoreApp.model_view.statistic_view import StatisticView
from BookStoreApp.model_view.attachment_view import AttachmentView

# Import controller
from controller.non_admin.home_controller import *
from controller.non_admin.cart_controller import *
from controller.non_admin.book_detail_controller import *
from controller.non_admin.category_controller import *
from controller.non_admin.sign_up_controller import *
from controller.non_admin.sign_in_controller import *
from controller.non_admin.account_info_controller import *
from controller.non_admin.cart_detail_controller import *
from controller.admin.account_controller import *
from controller.admin.cart_controller import *
from controller.admin.change_password_controller import *
from controller.admin.home_page_controller import *
from controller.admin.profile_controller import *
from controller.admin.report_controller import *
from controller.admin.statistic_controller import *
from controller.admin.preview_controller import *


# Tạo bảng database
def init_tables():
    try:
        db.create_all()
    except:
        db.session.rollback()


# Tạo view phía admin
def init_admin():
    admin.add_view(CustomerView(CustomerModel, db.session, name='Khách hàng'))
    admin.add_view(CartView(name='Giỏ hàng khách'))
    admin.add_view(BookView(BookModel, db.session, name='Sách'))
    admin.add_view(PreviewView(name='Bản xem trước sách'))
    admin.add_view(AttachmentView(AttachmentModel, db.session, name='Sách đính kèm', category='Thông tin bổ sung sách'))
    admin.add_view(CategoryView(CategoryModel, db.session, name='Loại sách', category='Thông tin bổ sung sách'))
    admin.add_view(ManufacturerView(ManufacturerModel, db.session, name='Nhà xuất bản',
                                    category='Thông tin bổ sung sách'))
    admin.add_view(StatisticView(name='Thống kê'))
    admin.add_view(ReportView(name='Báo cáo'))
    admin.add_view(SaleView(SaleModel, db.session, name='Giảm giá', category='Khác'))
    admin.add_view(PointView(PointModel, db.session, name='Điểm', category='Khác'))
    admin.add_view(RoleView(RoleModel, db.session, name='Vai trò tài khoản', category='Khác'))
    admin.add_view(ProfileView(name='Thông tin cá nhân'))
    admin.add_view(ChangePasswordView(name='Đổi mật khẩu'))
    admin.add_view(LogOutView(name='Đăng xuất'))
