from flask_admin import BaseView
from flask_login import current_user


# Lớp cơ sở dành cho những trang phía admin có custom từ đầu
class CustomBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.role.name.lower().__contains__('admin')
