from BookStoreApp.repository.admin.cart_repository import get_book_in_cart as gbic, get_info_user_in_cart as info_user, \
    get_cart_model as gcm, get_total_by_cart_id as gtbc


# Lấy thông tin giỏ hàng
def get_cart_model():
    return gcm()


# Lấy thông tin của khách hàng thông qua repository
def get_info_user_in_cart():
    return info_user()


# Lấy thông tin sách trong giỏ hàng thông qua repository
def get_book_in_cart(**kwargs):
    return gbic()


# Lấy tổng tiền theo cartId thông qua repository
def get_total_by_cart_id(cartID=None, **kwargs):
    if cartID:
        return gtbc(cart_id=cartID)
    return


# Chuyển thông tyin người dùng sang dạng dictionary
def get_info_user_data(data=None, **kwargs):
    if data is None:
        return []

    report_data = []

    for value in data:
        report_data.append({
            'cart_id': value[0],
            'username': value[1],
            'first_name': value[2],
            'last_name': value[3],
            'phone_number': value[4],
            'total_money': float(get_total_by_cart_id(value[0]))
        })

    return report_data


# Chuyển thông tin sang dictionary
def get_book(data=None, **kwargs):
    if data is None:
        return []

    report_data = []

    for value in data:
        report_data.append({
            'cart_id': value[0],
            'name_book': value[1],
            'name_category': value[2],
            'image': value[3],
            'amount': value[4],
            'money': float(value[5])
        })

    return report_data


# Lấy danh sách tổng tiền để hổ trợ code
def get_list_total_money_by_cart_id(data=None, **kwargs):
    if data is None:
        return []

    list = []

    for value in data:
        list.append(float(get_total_by_cart_id(value[0])))

    return list
