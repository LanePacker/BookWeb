from flask_admin import expose
from flask_login import current_user
from BookStoreApp.model_view.base_view import CustomBaseView
from BookStoreApp.service.admin.cart_service import get_book_in_cart,get_cart_model,get_info_user_in_cart


# Lớp tượng trưng cho trang chức năng thông tin giỏ hàng khách hàng phía admin
class CartView(CustomBaseView):
    @expose('/')
    def index(self):
        return self.render('/admin/cart.html', total=len(get_cart_model()),
                           cart=get_info_user_in_cart(), book=get_book_in_cart())

    def is_accessible(self):
        return current_user.is_authenticated

    def is_visible(self):
        return True

