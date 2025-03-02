from flask import render_template, request, redirect
from BookStoreApp.controller.utils.utils_controller import decode_vigenere
from BookStoreApp.service.non_admin.category_service import get_book_in_category, get_top_selling_book_category, \
    get_category_name_by_id
from BookStoreApp import app


# Thông tin chi tiết các sách trong category
@app.route('/chi-tiet-loai-sach')
def category():
    category_id = request.args.get('category_id')
    try:
        category_id = int(decode_vigenere(category_id))
        top_selling_books = get_top_selling_book_category(category_id=category_id)
        books_in_category = get_book_in_category(category_id=category_id)
        category_name = get_category_name_by_id(category_id=category_id)
        return render_template('/non_admin/category_detail.html',
                               top_selling_books=top_selling_books,
                               books_in_category=books_in_category,
                               category_name=category_name)
    except:
        return redirect('/')
