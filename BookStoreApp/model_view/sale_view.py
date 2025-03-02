from flask_admin.contrib.sqla.filters import IntEqualFilter, IntNotEqualFilter, \
    IntGreaterFilter, IntSmallerFilter
from flask_admin.form import rules
from wtforms import validators
from wtforms.validators import DataRequired

from BookStoreApp import SaleModel
from BookStoreApp.model_view.base_model_view import BaseModelView


# Lớp này tượng trưng cho trang quản lý giảm giá phía admin
class SaleView(BaseModelView):
    # Thuộc tính hiển thị
    column_sortable_list = ['sale_id',
                            'percent']
    column_searchable_list = ['percent']
    column_default_sort = 'sale_id'
    column_labels = dict(sale_id='Mã giảm giá',
                         percent='Phần trăm giảm giá')

    # Lọc dữ liệu
    column_filters = (IntEqualFilter(SaleModel.percent, name='Phần trăm giảm giá'),
                      IntNotEqualFilter(SaleModel.percent, name='Phần trăm giảm giá'),
                      IntGreaterFilter(SaleModel.percent, name='Phần trăm giảm giá'),
                      IntSmallerFilter(SaleModel.percent, name='Phần trăm giảm giá'))

    # Form nhập thông tin
    form_rules = [
        rules.FieldSet(('percent',), 'Thông tin giảm giá'),
        rules.FieldSet(('point', 'books'), 'Thông tin khác có liên quan')
    ]
    form_args = dict(
        percent=dict(validators=[DataRequired(), validators.NumberRange(max=99)],),
    )

    # Danh sách các cột hiển thị
    def scaffold_list_columns(self):
        return ['sale_id',
                'percent']
