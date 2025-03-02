from flask import jsonify, request

from BookStoreApp import app
from BookStoreApp.service.admin.report_service import get_report_data as grd, \
    get_amount_report_data as gard


# Lấy thông tin dữ liệu báo cáo
@app.route('/admin/report/api/data', methods=['post'])
def get_report_data():
    report_type = request.json.get('report_type')
    month = request.json.get('month')
    quarter = request.json.get('quarter')
    year = request.json.get('year')
    begin_index = request.json.get('begin_index')
    end_index = request.json.get('end_index')
    return jsonify(grd(report_type=report_type,
                       month=month,
                       quarter=quarter,
                       year=year,
                       begin_index=begin_index,
                       end_index=end_index))


@app.route('/admin/report/api/all-data', methods=['post'])
def get_report_export_data():
    report_type = request.json.get('report_type')
    month = request.json.get('month')
    quarter = request.json.get('quarter')
    year = request.json.get('year')
    return jsonify(grd(report_type=report_type,
                       month=month,
                       quarter=quarter,
                       year=year))


# Lấy số lượng tổng báo cáo
@app.route('/admin/report/api/amount', methods=['post'])
def get_amount_report_data():
    report_type = request.json.get('report_type')
    month = request.json.get('month')
    quarter = request.json.get('quarter')
    year = request.json.get('year')
    return jsonify(gard(report_type=report_type,
                        month=month,
                        quarter=quarter,
                        year=year))


