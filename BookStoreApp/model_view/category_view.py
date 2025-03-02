from flask_admin.contrib.sqla.filters import FilterLike, FilterNotLike
from flask_admin.form import rules
from wtforms import validators
from wtforms.validators import DataRequired

from BookStoreApp import CategoryModel
from BookStoreApp.model_view.base_model_view import BaseModelView


# Lớp này tượng trưng cho trang quản lý loại sách phía admin
class CategoryView(BaseModelView):
    # Thuộc tính hiển thị
    column_sortable_list = ['category_id',
                            'name']
    column_searchable_list = ['name']
    column_default_sort = 'category_id'
    column_labels = dict(category_id='Mã loại sách',
                         name='Tên loại sách')

    # Lọc dữ liệu
    column_filters = (FilterLike(CategoryModel.name, name='Tên loại sách'),
                      FilterNotLike(CategoryModel.name, name='Tên loại sách'))

    # Form nhập thông tin
    form_rules = [
        rules.FieldSet(('name',), 'Thông tin loại sách'),
        rules.FieldSet(('books',), 'Thông tin khác có liên quan')
    ]
    form_args = dict(
        name=dict(validators=[DataRequired(), validators.Length(max=255)],
                  render_kw={
                      'placeholder': 'Tên loại sách...'
                  })
    )

    # Danh sách các cột hiển thị
    def scaffold_list_columns(self):
        return ['category_id',
                'name']
