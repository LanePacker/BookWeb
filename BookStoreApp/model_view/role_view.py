from flask_admin.contrib.sqla.filters import FilterLike, FilterNotLike
from flask_admin.form import rules
from wtforms import validators
from wtforms.validators import DataRequired

from BookStoreApp import RoleModel
from BookStoreApp.model_view.base_model_view import BaseModelView


# Lớp này tượng trưng cho trang quản lý vai trò tài khoản phía admin
class RoleView(BaseModelView):
    # Thuộc tính hiển thị
    column_sortable_list = ['role_id',
                            'name']
    column_searchable_list = ['name']
    column_default_sort = 'role_id'
    column_labels = dict(role_id='Mã vai trò',
                         name='Tên vai trò')

    # Lọc dữ liệu
    column_filters = (FilterLike(RoleModel.name, name='Tên vai trò'),
                      FilterNotLike(RoleModel.name, name='Tên vai trò'))

    # Form nhập thông tin
    form_rules = [
        rules.FieldSet(('name',), 'Thông tin vai trò'),
        rules.FieldSet(('accounts',), 'Thông tin khác có liên quan')
    ]
    form_args = dict(
        name=dict(validators=[DataRequired(), validators.Length(max=20)],
                  render_kw={
                      'placeholder': 'Tên vai trò...'
                  }),
    )

    # Danh sách các cột hiển thị
    def scaffold_list_columns(self):
        return ['role_id',
                'name']
