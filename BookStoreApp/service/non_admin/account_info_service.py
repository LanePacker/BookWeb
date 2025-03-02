import hashlib
from BookStoreApp.repository.non_admin.account_info_repository import get_account_info_by_id as gaibi, \
                    set_change_password as scp


# Lấy thông tin từ repository
def get_account_info_by_id(id=None, **kwargs):
    if id:
        return gaibi(id)
    return

# Chuyển thông tin sang dictionary
def get_dictionary(data=None, **kwargs):
    if data is None:
        return []

    account_data = []

    account_data.append({
        'username': data[0],
        'name': data[1] + ' ' + data[2],
        'role' : data[3],
        'gmail' : data[4],
        'phone_number' : data[5],
        'address' : data[6]+ ', ' + data[7] + ', ' + data[8],
        'joined_date' : data[9].strftime("%m/%d/%Y, %H:%M:%S"),
        'date_of_birth' : data[10].strftime('%d/%m/%Y'),
        'accumulated_point' : data[11]
    })

    return account_data


# Thiết lập thay đổi mật khẩu
def set_change_password(new_password=None, account_id=None):
    if new_password and account_id:
        hash_password = hashlib.md5(new_password.encode('utf8')).hexdigest()
        scp(new_password=hash_password, account_id=account_id)


