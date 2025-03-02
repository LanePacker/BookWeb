import calendar
import datetime

from BookStoreApp.repository.admin.home_page_repository import get_book_amount, get_category_amount, get_cart_amount, \
    get_customer_amount, get_manufacturer_amount, get_comment_amount, get_revenue_yesterday, get_revenue_today, \
    get_cart_amount_in_month as gcm, get_top_book_selling as gtb


# lấy thông tin thống kê tổng quan
def get_general_statistic(**kwargs):
    return {
        'book_amount': get_book_amount(),
        'category_amount': get_category_amount(),
        'cart_amount': get_cart_amount(),
        'customer_amount': get_customer_amount(),
        'manufacturer_amount': get_manufacturer_amount(),
        'comment_amount': get_comment_amount()
    }


# Lấy thông tin thống kê doanh thu ngày hiện tại và ngày trước đó
def get_revenue(**kwargs):
    return {
        'yesterday_revenue': '{:,.0f} VNĐ'.format(0 if get_revenue_yesterday() is None else get_revenue_yesterday()),
        'today_revenue': '{:,.0f} VNĐ'.format(0 if get_revenue_today() is None else get_revenue_today())
    }


# Lấy thông tin thống kê số lượng đơn hàng trong tháng
def get_cart_amount_in_month(**kwargs):
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    days = [day for day in range(1, calendar.monthrange(year, month)[1] + 1)]
    return {
        'month': month,
        'year': year,
        'days': days,
        'datas': gcm(days=days, month=month, year=year)
    }


# Lấy thông tin top các sách bán chạy nhất
def get_top_book_selling(**kwargs):
    data = []
    books = gtb()
    for book in books:
        data.append({
            'book_name': book[0],
            'category_name': book[1],
            'manufacturer_name': book[2],
            'book_image': book[3],
            'revenue_total': '{:,.0f} VNĐ'.format(book[4]), })
    return data
