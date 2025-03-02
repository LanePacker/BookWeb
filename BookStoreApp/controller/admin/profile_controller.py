import json
from flask import request, jsonify
from sqlalchemy.sql.functions import current_user

from BookStoreApp import app
from BookStoreApp.service.admin.profile_service import get_info_user_by_account_id as giu,get_info
from flask_login import current_user

# Lấy thông tin giỏ hàng của khách
@app.route('/admin/profile/api/profile-info', methods=['post'])
def get_profile():
    account_id = current_user.account_id
    return jsonify(get_info(giu(account_id)))
