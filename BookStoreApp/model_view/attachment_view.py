from flask_admin.contrib.sqla.filters import FilterLike, FilterNotLike
from flask_admin.form import rules
from wtforms import validators
from wtforms.validators import DataRequired

from BookStoreApp import AttachmentModel
from BookStoreApp.model_view.base_model_view import BaseModelView


# Lớp này tượng trưng cho trang quản lý sách đính kèm phía admin
class AttachmentView(BaseModelView):
    # Thuộc tính hiển thị
    column_sortable_list = ['attachment_id',
                            'name']
    column_searchable_list = ['name']
    column_default_sort = 'attachment_id'
    column_labels = dict(attachment_id='Mã bộ đính kèm',
                         name='Tên bộ đính kèm')

    # Lọc dữ liệu
    column_filters = (FilterLike(AttachmentModel.name, name='Tên bộ đính kèm'),
                      FilterNotLike(AttachmentModel.name, name='Tên bộ đính kèm'))

    # Form nhập thông tin
    form_rules = [
        rules.FieldSet(('name',), 'Thông tin bộ đính kèm'),
        rules.FieldSet(('books',), 'Thông tin khác có liên quan')
    ]
    form_args = dict(
        name=dict(validators=[DataRequired(), validators.Length(max=255)],
                  render_kw={
                      'placeholder': 'Tên bộ đính kèm...'
                  }),
    )

    # Danh sách các cột hiển thị
    def scaffold_list_columns(self):
        return ['attachment_id',
                'name']
