import cloudinary.uploader

from BookStoreApp import app, PreviewModel
from flask import jsonify, request, redirect
from BookStoreApp.service.admin.preview_service import get_preview_of_book, \
    get_book_info_by_name, get_book_by_name, add_preview, get_preview_by_id, delete_preview as dp


# Lấy thông tin sách dựa trên tên
@app.route('/admin/previewview/api/book-name', methods=['post'])
def get_book_info():
    book_name = request.json.get('book_name')
    return jsonify(get_book_info_by_name(book_name=book_name))


# Lấy thông tin preview của sách dựa vào tên sách
@app.route('/admin/previewview/api/preview', methods=['post'])
def get_preview_info():
    book_name = request.json.get('book_name')
    return jsonify(get_preview_of_book(book_name=book_name))


# Thêm bản xem trước sách
@app.route('/admin/previewview/api/add-preview', methods=['post'])
def set_preview_info():
    preview_images = request.files.getlist('new_preview')
    book_name = request.form.get('book_name')
    book = get_book_by_name(book_name=book_name)
    for image in preview_images:
        path = cloudinary.uploader.upload(image, folder='preview')
        preview = PreviewModel(image=path['secure_url'], book=book)
        add_preview(preview=preview)

    return redirect('/admin/previewview')


# Xóa bản xem trước sách
@app.route('/admin/previewview/api/delete', methods=['post'])
def delete_preview():
    preview_id = request.json.get('preview_id')
    preview = get_preview_by_id(preview_id=preview_id)
    return jsonify(dp(preview=preview))
