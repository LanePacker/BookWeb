from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect


# Lớp tượng trưng cho trang chức năng đăng xuất
class LogOutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

    def is_visible(self):
        return False
