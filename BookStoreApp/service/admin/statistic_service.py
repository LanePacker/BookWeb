from BookStoreApp.repository.admin.statistic_repository import get_statistic_revenue_month, \
    get_statistic_revenue_quarter, get_statistic_revenue_year, get_statistic_frequently_book_selling_month, \
    get_statistic_frequently_book_selling_quarter, get_statistic_frequently_book_selling_year, get_book_name as gbn


# Chuyển dữ liệu thống kê doanh thu thành mảng các từ dictionary
def get_revenue_statistic_data(data=None, **kwargs):
    if data is None:
        return []

    statistic_data = []

    for value in data:
        statistic_data.append({
            'time': value[0],
            'revenue_total': '{:,.0f} VND'.format(float(value[1]))
        })

    return statistic_data


# Chuyển dữ liệu thống kê tần suất bán sách thành mảng các dictionary
def get_frequently_book_selling_statistic_data(data=None, **kwargs):
    if data is None:
        return []

    statistic_data = []

    for value in data:
        statistic_data.append({
            'time': value[0],
            'amount_total': value[1]
        })

    return statistic_data


# Lấy thông tin thống kê doanh thu
def get_statistic_revenue(statistic_condition, **kwargs):
    if statistic_condition.__contains__('month'):
        return get_statistic_revenue_month(from_month=kwargs.get('from_time'),
                                           to_month=kwargs.get('to_time'))

    if statistic_condition.__contains__('quarter'):
        return get_statistic_revenue_quarter(from_quarter=kwargs.get('from_time'),
                                             to_quarter=kwargs.get('to_time'))

    if statistic_condition.__contains__('year'):
        return get_statistic_revenue_year(from_year=kwargs.get('from_time'),
                                          to_year=kwargs.get('to_time'))


# Lấy thông tin tần suất bán sách
def get_statistic_frequently_book_selling(statistic_condition, **kwargs):
    if not kwargs.get('book_name'):
        return []

    if statistic_condition.__contains__('month'):
        return get_statistic_frequently_book_selling_month(from_month=kwargs.get('from_time'),
                                                           to_month=kwargs.get('to_time'),
                                                           book_name=kwargs.get('book_name'))
    if statistic_condition.__contains__('quarter'):
        return get_statistic_frequently_book_selling_quarter(from_quarter=kwargs.get('from_time'),
                                                             to_quarter=kwargs.get('to_time'),
                                                             book_name=kwargs.get('book_name'))
    if statistic_condition.__contains__('year'):
        return get_statistic_frequently_book_selling_year(from_year=kwargs.get('from_time'),
                                                          to_year=kwargs.get('to_time'),
                                                          book_name=kwargs.get('book_name'))


# Lấy thông tin dữ liệu thống kê và trả về 1 mảng với mỗi phần từ là 1 dictionary
def get_statistic_data(statistic_type=None, statistic_condition=None, **kwargs):
    data = None
    if statistic_type == 'revenue':
        data = get_statistic_revenue(statistic_condition, **kwargs)
        data = get_revenue_statistic_data(data=data)

    if statistic_type == 'frequently_book_selling':
        data = get_statistic_frequently_book_selling(statistic_condition, **kwargs)
        data = get_frequently_book_selling_statistic_data(data=data)

    return data


# Lấy thông tin tên sách trùng với từ khóa
def get_book_name(keyword=None):
    book_names = gbn(keyword=keyword)
    return [] if book_names is None else book_names
