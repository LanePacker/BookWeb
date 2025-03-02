from BookStoreApp import CustomerModel
from BookStoreApp import db
from BookStoreApp.model.account_model import AccountModel


# Tạo tài khoản
def set_sign_up(data=None, **kwargs):
    id = get_latest_account_id()[0] + 1
    if id:
        customer = CustomerModel(account_id=id,
                                 first_name=data['first_name'],
                                 last_name=data['last_name'],
                                 phone_number=data['phone_number'],
                                 city=data['city'],
                                 district=data['district'],
                                 address=data['address'],
                                 date_of_birth=data['date_of_birth'],
                                 accumulated_point=0,
                                 gmail=data['email'],
                                 type='customer',
                                 role_id=2,
                                 username=data['username'],
                                 password=data['password'])
        db.session.add(customer)
        db.session.commit()


# Lấy account_id moi nhat
def get_latest_account_id(name=None, **kwargs):
    query = db.session.query(AccountModel.account_id).order_by(AccountModel.account_id.desc())
    return query.first()


# kiểm tra tên tài khoản chưa
def is_username_exactly(username=None):
    user = AccountModel.query.filter(AccountModel.username.__eq__(username)).first()
    if user:
        return True
    return False
