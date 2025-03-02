from flask_admin import expose
from flask_login import current_user

from BookStoreApp.model_view.base_view import CustomBaseView
from BookStoreApp.controller.utils.utils_controller import get_data_json_file as gdjf


# Lớp tượng trưng cho trang chức năng báo cáo phía admin
class ReportView(CustomBaseView):
    @expose('/')
    def index(self):
        selections = gdjf('report_data.json')
        return self.render('/admin/report.html', selections=selections)

    def is_accessible(self):
        return current_user.is_authenticated

    def is_visible(self):
        return True
