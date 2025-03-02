from flask import request, redirect, jsonify, json
from flask_login import login_user
from BookStoreApp import app
from BookStoreApp.service.admin.account_service import get_account as ga, \
    set_last_access as sla


# Lấy thông tin đăng nhập từ web để kiểm tra tài khoản
@app.route('/client/api/sign-in', methods=['POST'])
def login_client():
    if request.method == 'POST':
        data = json.loads(request.data)
        username = data.get('username')
        password = data.get('password')
        if username and password:
            account = ga(username=username, password=password)
        else:
            account = None
        if account and account.is_active == True:
            login_user(user=account)
            sla(account=account)
            return jsonify("successful")
        else:
            return jsonify("error")
    return redirect('/')

