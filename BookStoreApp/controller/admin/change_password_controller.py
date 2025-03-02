import json

from flask import request, jsonify
from BookStoreApp import app
from BookStoreApp.service.admin.account_service import get_account as ga, set_change_passwork as scp


# Đổi mật khẩu
@app.route('/admin/api/change-password', methods=['post'])
def set_change_passwork():
    result = True
    wrong_password = False
    if request.method.__eq__('POST'):
        data = json.loads(request.data)
        username = str(data.get('username'))
        old_password = str(data.get('old_password'))
        if username and old_password:
            if ga(username=username, password=old_password) is None:
                result = False
                wrong_password = True
            else:
                account = ga(username=username, password=old_password)
                new_password = str(data.get("new_password"))
                scp(new_password=new_password, account=account)
        else:
            result = False
    return jsonify(result=result, wrong_password=wrong_password)
