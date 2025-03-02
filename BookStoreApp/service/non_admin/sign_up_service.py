import hashlib
from random import randint
from BookStoreApp.repository.non_admin.sign_up_repository import set_sign_up as siu, is_username_exactly as iue


# xử lí dữ liệu để gửi qua repository
def set_sign_up(data=None, **kwargs):
    if get_null_in_data(data):
        data['password'] = hashlib.md5(data['password'].encode('utf8')).hexdigest()
        data['username'] = data['username'].strip()
        siu(data)


# Kiểm tra danh sách có tồn tại null
def get_null_in_data(data):
    flag = True
    for d in data.values():
        if d == "":
            flag = False
    return flag





# lấy kết quả từ repository về  tên tài khoản đã tồn tại hay chưa
def is_username_exactly(username=None):
    if username:
        return iue(username)
    return
