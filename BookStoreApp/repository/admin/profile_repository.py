from BookStoreApp import db
from BookStoreApp.model.account_model import AccountModel
from BookStoreApp import RoleModel


# Lấy thông tin account dựa vào id
def get_info_user_by_account_id(id=0):
    query = db.session.query(AccountModel.username,
                             AccountModel.first_name,
                             AccountModel.last_name,
                             AccountModel.joined_date,
                             AccountModel.avatar,
                             AccountModel.gmail,
                             RoleModel.name,
                             AccountModel.lass_access) \
        .filter(AccountModel.role_id == RoleModel.role_id) \
        .filter(AccountModel.account_id == id)
    return query.first()
