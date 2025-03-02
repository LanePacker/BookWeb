from flask_admin import AdminIndexView, expose
from flask_login import current_user


# Lớp tượng trưng cho trang home page
class HomeView(AdminIndexView):
    def is_accessible(self):
        access_result = False
        if current_user.is_authenticated and \
                current_user.role.name.lower().__contains__('admin'):
            access_result = True

        if not current_user.is_authenticated:
            access_result = True
        return access_result

    def is_visible(self):
        return not current_user.is_authenticated

    @expose('/')
    def index(self):
        return self.render('/admin/home_page.html')
