from BookStoreApp.repository.admin.report_repository import get_revenue_query as grq, \
    get_frequently_book_selling_query as gfb, get_report_data as grd


# Chuyển dữ liệu báo cáo doanh thu thành mảng các từ dictionary
def get_revenue_report_data(data=None, **kwargs):
    if data is None:
        return []

    report_data = []

    for value in data:
        report_data.append({
            'ordered_date': value[0].strftime('%d/%m/%Y'),
            'revenue_total': '{:,.0f} VND'.format(float(value[1]))
        })

    return report_data


# Chuyển dữ liệu báo cáo tần suất bán sách thành mảng các dictionary
def get_frequently_book_selling_report_data(data=None, **kwargs):
    if data is None:
        return []

    report_data = []

    for value in data:
        report_data.append({
            'book_name': value[0],
            'amount_total': value[1]
        })

    return report_data


# Lấy thông tin dữ liệu báo cáo và trả về 1 mảng với mỗi phần từ là 1 dictionary
def get_report_data(report_type=None, **kwargs):
    query = None

    if report_type == 'revenue':
        query = grq()

    if report_type == 'frequently_book_selling':
        query = gfb()

    data = grd(query=query,
               month=kwargs.get('month'),
               quarter=kwargs.get('quarter'),
               year=kwargs.get('year'),
               begin_index=kwargs.get('begin_index'),
               end_index=kwargs.get('end_index'))

    if report_type == 'revenue':
        return get_revenue_report_data(data=data)

    if report_type == 'frequently_book_selling':
        return get_frequently_book_selling_report_data(data=data)


# Lấy thông tin số lượng báo cáo trả về đói tượng từ điển tương ứng
def get_amount_report_data(report_type=None, **kwargs):
    return {
        'amount': len(get_report_data(report_type=report_type, **kwargs))
    }
