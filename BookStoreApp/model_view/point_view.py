from flask_admin.contrib.sqla.filters import IntEqualFilter, IntNotEqualFilter, IntGreaterFilter, IntSmallerFilter
from flask_admin.form import rules
from wtforms import validators
from wtforms.validators import DataRequired

from BookStoreApp import PointModel
from BookStoreApp.model_view.base_model_view import BaseModelView


# Lớp này tượng trưng cho trang quản lý điểm phía admin
class PointView(BaseModelView):
    # Thuộc tính hiển thị
    column_sortable_list = ['point_id',
                            'amount']
    column_searchable_list = ['amount']
    column_default_sort = 'point_id'
    column_labels = dict(point_id='Mã điểm',
                         amount='Số lượng')

    # Lọc dữ liệu
    column_filters = (IntEqualFilter(PointModel.amount, name='Số lượng'),
                      IntNotEqualFilter(PointModel.amount, name='Số lượng'),
                      IntGreaterFilter(PointModel.amount, name='Số lượng'),
                      IntSmallerFilter(PointModel.amount, name='Số lượng'))

    # Form nhập thông tin
    form_rules = [
        rules.FieldSet(('amount',), 'Thông tin điểm'),
        rules.FieldSet(('books', 'sales'), 'Thông tin khác có liên quan')
    ]
    form_args = dict(
        amount=dict(validators=[DataRequired(), validators.NumberRange(min=1, max=1000)]),
    )

    # Danh sách các cột hiển thị
    def scaffold_list_columns(self):
        return ['point_id',
                'amount']
