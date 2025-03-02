from flask_admin.contrib.sqla.filters import FilterLike, FilterNotLike
from flask_admin.form import rules
from wtforms import validators
from wtforms.validators import DataRequired

from BookStoreApp import ManufacturerModel
from BookStoreApp.model_view.base_model_view import BaseModelView


# Lớp này tượng trưng cho trang quản lý nhà xuất bản phía admin
class ManufacturerView(BaseModelView):
    # Thuộc tính hiển thị
    column_sortable_list = ['manufacturer_id',
                            'name']
    column_searchable_list = ['name']
    column_default_sort = 'manufacturer_id'
    column_labels = dict(manufacturer_id='Mã nhà xuất bản',
                         name='Tên nhà xuất bản')

    # Lọc dữ liệu
    column_filters = (FilterLike(ManufacturerModel.name, name='Tên nhà xuất bản'),
                      FilterNotLike(ManufacturerModel.name, name='Tên nhà xuất bản'))

    # Form nhập thông tin
    form_rules = [
        rules.FieldSet(('name',), 'Thông tin nhà xuất bản'),
        rules.FieldSet(('books',), 'Thông tin khác có liên quan')
    ]
    form_args = dict(
        name=dict(validators=[DataRequired(), validators.Length(max=255)],
                  render_kw={
                      'placeholder': 'Tên nhà xuất bản...'
                  }),
    )

    # Danh sách các cột hiển thị
    def scaffold_list_columns(self):
        return ['manufacturer_id',
                'name']
