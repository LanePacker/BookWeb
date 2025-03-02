from BookStoreApp import db
from BookStoreApp import CustomerModel, RoleModel
from BookStoreApp.model.account_model import AccountModel


# Lấy thông tin account dựa vào id
def get_account_info_by_id(id=None, **kwargs):
    query = db.session.query(CustomerModel.username,
                             CustomerModel.last_name,
                             CustomerModel.first_name,
                             RoleModel.name,
                             CustomerModel.gmail,
                             CustomerModel.phone_number,
                             CustomerModel.address,
                             CustomerModel.district,
                             CustomerModel.city,
                             CustomerModel.joined_date,
                             CustomerModel.date_of_birth,
                             CustomerModel.accumulated_point) \
        .filter(CustomerModel.role_id == RoleModel.role_id) \
        .filter(CustomerModel.account_id == id)
    return query.first()


# Thay đổi mật khẩu
def set_change_password(new_password=None, account_id=None, **kwargs):
    account = get_account(account_id)
    account.password = new_password
    db.session.add(account)
    db.session.commit()


# Lấy thông tin từ database của account dựa vào username và password
def get_account(account_id=None, **kwargs):
    if account_id:
        return AccountModel.query.filter(AccountModel.account_id.__eq__(account_id)).first()
    return None
