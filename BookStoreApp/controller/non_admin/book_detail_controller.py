from flask import render_template, jsonify, request, redirect
from flask_login import current_user

from BookStoreApp import app
from BookStoreApp.controller.utils.utils_controller import decode_vigenere

from BookStoreApp.service.non_admin.book_detail_service import get_book_detail_by_id, get_book_preview_by_book_id, \
    get_attachment_by_book_id, get_book_in_category, get_viewed_book_of_current_user, add_viewed_book
from BookStoreApp.service.non_admin.cart_service import add_book_to_cart


# Lấy thông tin chi tiết của sách
@app.route('/chi-tiet-sach')
def get_book_detail_client():
    book_id = request.args.get('book_id')
    try:
        book_id = int(decode_vigenere(book_id))
        book_detail = get_book_detail_by_id(book_id=book_id)
        book_previews = get_book_preview_by_book_id(book_id=book_id)
        book_attachments = get_attachment_by_book_id(book_id=book_id)
        book_category = get_book_in_category(category_name=book_detail['category_name'])
        if current_user.is_authenticated:
            add_viewed_book(book_id=book_id, account_id=current_user.account_id)
        viewed_books = get_viewed_book_of_current_user(
            account_id=current_user.account_id if current_user.is_authenticated else None)
        return render_template('/non_admin/book-detail.html',
                               book_detail=book_detail,
                               book_previews=book_previews,
                               book_attachments=book_attachments,
                               book_category=book_category,
                               viewed_books=viewed_books)
    except:
        return redirect('/')


# Thêm sách vào giỏ hàng
@app.route('/book-detail/api/add-to-cart', methods=['post'])
def add_to_cart():
    book_id = request.json.get('book_id')
    amount = request.json.get('book_amount')
    if amount is None:
        amount = 1
    return jsonify(add_book_to_cart(book_id=decode_vigenere(book_id),
                                    account_id=current_user.account_id,
                                    amount=int(amount)))

