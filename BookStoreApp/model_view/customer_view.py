from flask_admin.contrib.sqla.filters import FilterLike, FilterNotLike, BooleanEqualFilter, \
    BooleanNotEqualFilter, DateEqualFilter, DateNotEqualFilter, DateGreaterFilter, DateSmallerFilter, DateBetweenFilter, \
    DateNotBetweenFilter, IntEqualFilter, IntNotEqualFilter, IntGreaterFilter, IntSmallerFilter

from BookStoreApp import CustomerModel
from BookStoreApp.model_view.base_model_view import BaseModelView


# Lóp này tượng trưng cho trang quản lý thông tin khách hàng phía admin
class CustomerView(BaseModelView):
    can_edit = False
    can_create = False

    # Thuộc tính hiển thị
    column_sortable_list = ['account_id',
                            'username',
                            'joined_date',
                            'lass_access',
                            'first_name',
                            'last_name',
                            'phone_number',
                            'gmail',
                            'city',
                            'district',
                            'address',
                            'date_of_birth',
                            'accumulated_point']
    column_default_sort = 'account_id'
    column_labels = dict(account_id='Mã khách hàng',
                         username='Tên đăng nhập',
                         password='Mật khẩu',
                         avatar='Ảnh đại diện',
                         is_active='Trạng thái',
                         joined_date='Ngày tạo',
                         lass_access='Truy cập lần cuối',
                         first_name='Tên',
                         last_name='Họ và tên đệm',
                         phone_number='Số điện thoại',
                         gmail='Gmail',
                         city='Thành phố',
                         district='Quận/Huyện',
                         address='Địa chỉ',
                         date_of_birth='Ngày sinh',
                         accumulated_point='Điểm tích lũy')

    # Lọc dữ liệu
    column_filters = (FilterLike(CustomerModel.username, name='Tên đăng nhập'),
                      FilterNotLike(CustomerModel.username, name='Tên đăng nhập'),
                      FilterLike(CustomerModel.first_name, name='Tên'),
                      FilterNotLike(CustomerModel.first_name, name='Tên'),
                      FilterLike(CustomerModel.last_name, name='Họ và tên đệm'),
                      FilterNotLike(CustomerModel.last_name, name='Họ và tên đệm'),
                      DateEqualFilter(CustomerModel.date_of_birth, name='Ngày sinh'),
                      DateNotEqualFilter(CustomerModel.date_of_birth, name='Ngày sinh'),
                      DateGreaterFilter(CustomerModel.date_of_birth, name='Ngày sinh'),
                      DateSmallerFilter(CustomerModel.date_of_birth, name='Ngày sinh'),
                      DateBetweenFilter(CustomerModel.date_of_birth, name='Ngày sinh'),
                      DateNotBetweenFilter(CustomerModel.date_of_birth, name='Ngày sinh'),
                      FilterLike(CustomerModel.phone_number, name='Số điện thoại'),
                      FilterNotLike(CustomerModel.phone_number, name='Số điện thoại'),
                      FilterLike(CustomerModel.gmail, name='Gmail'),
                      FilterNotLike(CustomerModel.gmail, name='Gmail'),
                      FilterLike(CustomerModel.city, name='Thành phố'),
                      FilterNotLike(CustomerModel.city, name='Thành phố'),
                      FilterLike(CustomerModel.district, name='Quận/Huyện'),
                      FilterNotLike(CustomerModel.district, name='Quận/Huyện'),
                      FilterLike(CustomerModel.address, name='Địa chỉ'),
                      FilterNotLike(CustomerModel.address, name='Địa chỉ'),
                      IntEqualFilter(CustomerModel.accumulated_point, name='Điểm tích lũy'),
                      IntNotEqualFilter(CustomerModel.accumulated_point, name='Điểm tích lũy'),
                      IntGreaterFilter(CustomerModel.accumulated_point, name='Điểm tích lũy'),
                      IntSmallerFilter(CustomerModel.accumulated_point, name='Điểm tích lũy'),
                      BooleanEqualFilter(CustomerModel.is_active, name='Trạng thái'),
                      BooleanNotEqualFilter(CustomerModel.is_active, name='Trạng thái'),
                      DateEqualFilter(CustomerModel.joined_date, name='Ngày tạo'),
                      DateNotEqualFilter(CustomerModel.joined_date, name='Ngày tạo'),
                      DateGreaterFilter(CustomerModel.joined_date, name='Ngày tạo'),
                      DateSmallerFilter(CustomerModel.joined_date, name='Ngày tạo'),
                      DateBetweenFilter(CustomerModel.joined_date, name='Ngày tạo'),
                      DateNotBetweenFilter(CustomerModel.joined_date, name='Ngày tạo'),
                      DateEqualFilter(CustomerModel.lass_access, name='Truy cập lần cuối'),
                      DateNotEqualFilter(CustomerModel.lass_access, name='Truy cập lần cuối'),
                      DateGreaterFilter(CustomerModel.lass_access, name='Truy cập lần cuối'),
                      DateSmallerFilter(CustomerModel.lass_access, name='Truy cập lần cuối'),
                      DateBetweenFilter(CustomerModel.lass_access, name='Truy cập lần cuối'),
                      DateNotBetweenFilter(CustomerModel.lass_access, name='Truy cập lần cuối'))

    # Danh sách các cột hiển thị
    def scaffold_list_columns(self):
        return ['account_id',
                'username',
                'password',
                'first_name',
                'last_name',
                'date_of_birth',
                'accumulated_point',
                'city',
                'district',
                'address',
                'phone_number',
                'gmail',
                'avatar',
                'joined_date',
                'lass_access',
                'is_active']