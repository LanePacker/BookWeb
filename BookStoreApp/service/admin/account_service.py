import hashlib

from BookStoreApp.repository.admin.account_repository import \
    get_account as ga, get_account_by_id as gabi, set_last_access as sla, set_change_password as cp


# Lấy thông tin account từ tầng repository thông qua username và passwrod
def get_account(username=None, password=None, **kwargs):
    hash_password = hashlib.md5(password.encode('utf8')).hexdigest()
    return ga(username=username, password=hash_password, **kwargs)


# Lấy thông tin account từ tầng repository thông qua id
def get_account_by_id(account_id=None, **kwargs):
    return gabi(account_id=account_id, **kwargs)


# Thiết lập lần truy cập cuối cùng của account
def set_last_access(account=None):
    sla(account=account)


# Thiết lập thay đổi mật khẩu
def set_change_passwork(new_password=None, account=None):
    if new_password and account:
        hash_password = hashlib.md5(new_password.encode('utf8')).hexdigest()
        cp(new_password=hash_password, account=account)
