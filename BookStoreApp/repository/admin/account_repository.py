import datetime

from BookStoreApp import db
from BookStoreApp.model.account_model import AccountModel


# Lấy thông tin từ database của account dựa vào username và password
def get_account(username=None, password=None, **kwargs):
    if username and password:
        return AccountModel.query.filter(AccountModel.username.__eq__(username),
                                         AccountModel.password.__eq__(password)).first()
    return None


# Lấy thông tin từ database của account dựa vào id
def get_account_by_id(account_id=None, **kwargs):
    if account_id:
        return AccountModel.query.get(account_id)
    return None


# Thiết lập truy cập lần cuối cho account
def set_last_access(account=None):
    if account:
        account.last_access = datetime.datetime.now()
        db.session.add(account)
        db.session.commit()


# Thay đổi mật khẩu
def set_change_password(new_password=None, account=None):
    account.password = new_password
    db.session.add(account)
    db.session.commit()
