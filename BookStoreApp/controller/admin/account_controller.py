from flask import request, redirect
from flask_login import login_user, current_user, logout_user
from BookStoreApp import login, app
from BookStoreApp.service.admin.account_service import get_account as ga, \
    get_account_by_id as gabi, set_last_access as sla


# Lấy thông tin tài khoản, dùng cho phân quyền
@login.user_loader
def load_account(account_id):
    return gabi(account_id=account_id)


# Lấy thông tin đăng nhập từ web để kiểm tra tài khoản
@app.route('/admin-login', methods=['POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            account = ga(username=username, password=password)
        else:
            account = None
        if account and account.is_active == True and account.role_id == 1:
            login_user(user=account)
            sla(account=account)
    return redirect('/admin')

