// Hiển thi form đăng nhập hoặc đăng ký
function getForm(status = true, isAuthenticated = false) {
    isAuthenticated = isAuthenticated == 'True'
    if (!isAuthenticated) {
        if (status) {
            $('#loginBtn').addClass('active')
            $('#registerBtn').removeClass('active')
            $('#login-form').modal('show')
            $('#register-form').modal('hide')
            $('.login-tab').addClass('active')
            $('.register-tab').removeClass('active')
        } else {
            $('#registerBtn').addClass('active')
            $('#loginBtn').removeClass('active')
            $('#register-form').modal('show')
            $('#login-form').modal('hide')
            $('.login-tab').removeClass('active')
            $('.register-tab').addClass('active')
        }
    }
}

// Lấy thông tin sách trong đơn hàng
function getBookInCart() {
    fetch('/gio-hang/api/books')
        .then(res => res.json()).then(books => {
            setCartDetail(books)
            getMoneyTotalInCart()
        })
}

// Lấy thông tin tổng giá trị đơn hàng trong đơn hàng
function getMoneyTotalInCart() {
    fetch('/gio-hang/api/money_total')
        .then(res => res.json()).then(moneyTotal => {
            setMoneyTotal(moneyTotal)
        })
}

// Thiết lập hiển thị danh sách các sách trong đơn hàng
function setCartDetail(books) {
    $('#bookList').html('')
    htmlData = `
        <h6 class="cart-header font-weight-bold">GIỎ HÀNG CỦA BẠN <span>(${books.length} sản phẩm)</span></h6>
        <div class="cart-list-items mt-3">
    `
    for (let i = 0; i < books.length; i++)
        htmlData += `
                <div class="cart-item d-flex mb-4">
                    <a href="/chi-tiet-sach?book_id=${books[i]['book_id']}" class="img">
                        <img src="${books[i]['book_image']}" class="img-fluid" alt="${books[i]['book_name']}" style="margin:unset;">
                    </a>
                    <div class="item-caption d-flex w-100">
                        <div class="item-info ml-3">
                            <a href="/chi-tiet-sach?book_id=${books[i]['book_id']}" class="book-name mb-3">${books[i]['book_name']}</a>
                            <div class="amount d-flex">
                                <div class="input-number input-group mb-3">
                                    <div class="input-group-prepend">
                                        <span class="input-group-text btn-spin btn-dec"
                                            onclick="subtractBook('${books[i]['book_id']}')">-</span>
                                    </div>
                                    <input type="number" value="${books[i]['book_amount']}"
                                    readonly class="amount-product text-right" id="input${books[i]['book_id']}">
                                    <div class="input-group-append">
                                        <span class="input-group-text btn-spin btn-inc" 
                                            onclick="addBook('${books[i]['book_id']}')">+</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="item-price ml-auto d-flex flex-column align-items-end">
                        <div class="d-flex">
                            <div class="new-price">${books[i]['book_sale_price']} ₫</div>
                            <div class="old-price">${books[i]['book_price']} ₫</div></div>
                            <span class="remove mt-auto"><i class="far fa-trash-alt"
                                onclick ="deleteBook('${books[i]['book_id']}')"></i></span>
                        </div>
                    </div>
            </div>
        `
    htmlData += '</div>'
    $('#bookList').html(htmlData)
}

// Thiết lập hiển thị tổng tiền trong đơn hàng
function setMoneyTotal(moneyTotal) {
    $('#totalPrice').html('')
    htmlData = `
        <div class="row">
            <div class="col-md-3">
                <a href="/" class="btn buy-more">Mua thêm</a>
            </div>
            <div class="col-md-5 offset-md-4">
                <div class="total-price">
                    <div class="group d-flex justify-content-between">
                        <p class="label">Tạm tính:</p>
                        <p class="tamtinh">${moneyTotal['cost_total']} ₫</p>
                    </div>
                    <div class="group d-flex justify-content-between">
                        <p class="label">Giảm giá:</p>
                        <p class="giamgia">${moneyTotal['saving_total']} ₫</p>
                    </div>
                    <div class="group d-flex justify-content-between align-items-center">
                        <strong class="text-uppercase">Tổng cộng:</strong>
                        <p class="total">${moneyTotal['sale_price_total']} ₫</p>
                    </div>
                    <small class="note d-flex justify-content-end text-muted">
                        (Giá đã bao gồm VAT)
                    </small>
                </div>
            </div>
        </div>
    `

    $('#totalPrice').html(htmlData)
}

// Thêm sách vào đơn hàng
function addBook(bookId) {
    var id = `#input${bookId}`
    var value = parseInt($(id).val()) + 1
    $(id).val(value.toString())
    fetch('/gio-hang/api/add-to-cart', {
        method: 'post',
        body: JSON.stringify({
            'book_id': bookId,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(result => {
        if (result['result']) {
            getMoneyTotalInCart()
            getCartDetailAmount()
        } else
            Swal.fire({
                title: 'Thêm thất bại',
                text: 'Xin vui lòng kiểm tra lại',
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Ok',
            })
    })
}

// Giảm sách trong đơn hàng
function subtractBook(bookId) {
    var id = `#input${bookId}`
    var value = parseInt($(id).val()) - 1
    if (value <= 0) {
        $(id).val(1)
        return
    }
    $(id).val(value.toString())
    fetch('/gio-hang/api/subtract-to-cart', {
        method: 'post',
        body: JSON.stringify({
            'book_id': bookId,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(result => {
        if (result['result']) {
            getMoneyTotalInCart()
            getCartDetailAmount()
        } else
            Swal.fire({
                title: 'Giảm thất bại',
                text: 'Xin vui lòng kiểm tra lại',
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Ok',
            })
    })
}

// Xóa sách khỏi đơn hàng
function deleteBook(bookId) {
    Swal.fire({
        title: 'Bạn có chắc chắn muốn xóa sản phẩm này khỏi giỏ hàng?',
        text: 'Mọi thao tác sau khi thực hiện không thể phục hồi lại',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Xác nhận',
        cancelButtonText: 'Huỷ bỏ'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch('/gio-hang/api/delete-to-cart', {
                method: 'post',
                body: JSON.stringify({
                    'book_id': bookId,
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(result => {
                if (result['result']) {
                    Swal.fire(
                        'Xóa thành công',
                        'Giỏ hàng của bạn đã được cập nhật.',
                        'success'
                    ).then(function () {
                        getBookInCart()
                        getCartDetailAmount()
                    })

                } else
                    Swal.fire({
                        title: 'Xóa thất bại',
                        text: 'Xin vui lòng kiểm tra lại',
                        icon: 'warning',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'Ok',
                    })
            })
        }
    })

}

// Lấy số lượng sản phẩm trong đơn hàng
function getCartDetailAmount() {
    fetch('/gio-hang/api/amount-book').then(res => res.json()).then(result => {
        $('#cartDetailAmount').text(result['amount'])
    })
}

// Gửi thông tin đặt hàng xuống server
function setShipInfo() {
    fetch('/gio-hang/api/ship-info', {
        method: 'post',
        body: JSON.stringify({
            'customer_fullname': $('#nameShip').val(),
            'customer_phone_number': $('#phoneNumberShip').val(),
            'customer_address': $('#addressShip').val(),
            'customer_note': $('#noteShip').val(),
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(cartOTP => {
        // console.info(cartOTP)
        $('#otpModal').modal('toggle')
        countDown()
        $('#otpInput').on('input', () => {
            if ($('#otpInput').val() == cartOTP['cart_otp']) {
                $('#countDown').text(90)
                // payCart()
                window.location.href = '/thanh-toan'
            }
        })

    })
}

// Kiểm tra thông tin đặt hàng
function checkCartInformation() {
    if (parseInt($('#cartDetailAmount').text()) <= 0) {
        Swal.fire({
            title: 'Giỏ hàng không được trống',
            text: 'Xin vui lòng kiểm tra lại',
            icon: 'warning',
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Ok',
        })
        return false
    }
    if ($('#nameShip').val().length <= 0 ||
        $('#phoneNumberShip').val().length <= 0 ||
        $('#addressShip').val().length <= 0) {
        Swal.fire({
            title: 'Thông tin đặt hàng chưa đầy đủ hoặc chưa hợp lệ',
            text: 'Xin vui lòng kiểm tra lại',
            icon: 'warning',
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Ok',
        })
        return false
    }
    return true
}

// Xác nhận đặt hàng
// Xác nhận đặt hàng
function confirmOrder() {
    Swal.fire({
        title: 'Bạn xác nhận muốn thanh toán đơn hàng này',
        text: 'Mọi thao tác sau khi thực hiện không thể phục hồi lại',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Xác nhận',
        cancelButtonText: 'Huỷ bỏ'
    }).then((result) => {
        if (result.isConfirmed && checkCartInformation()) {
            // Gọi hàm thanh toán ngay lập tức
            payCart();
        }
    })
}

// Gửi yêu cầu thanh toán
function payCart() {
    fetch('/gio-hang/api/pay', {
        method: 'GET', // Hoặc 'POST' nếu cần thiết
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(result => {
        if (result['result']) {
            Swal.fire({
                title: 'Đặt hàng thành công!',
                icon: 'success',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Ok',
            }).then(() => {
                window.location.href = '/gio-hang'; // Chuyển hướng đến trang thanh toán
            });
        } else {
            Swal.fire({
                title: 'Đặt hàng thất bại',
                text: 'Xin vui lòng kiểm tra lại',
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Ok',
            });
        }
    }).catch(error => {
        console.error('Error:', error);
        Swal.fire({
            title: 'Có lỗi xảy ra',
            text: 'Xin vui lòng thử lại sau',
            icon: 'error',
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Ok',
        });
    });
}

$(document).ready(function () {
    getBookInCart()
    $('#buyButton').click(function () {
        $('#countDown').text('90')
        confirmOrder()
    })
    $('#customerBuyButton').click(function () {
        Swal.fire({
            title: 'Chỉ có khách hàng mới có thể đặt hàng',
            text: 'Xin vui lòng kiểm tra lại',
            icon: 'warning',
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Ok',
        })
    })

    checkPaymentResult();
})