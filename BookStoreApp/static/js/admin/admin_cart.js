var val = 0;
window.onload = function () {
    var x = location.href;
    if (x.indexOf('admin/cartview') != -1) {
        getCartData();
    }
}

// Gửi thông tin lên server
function getCartData() {
    val = getPriceRange();
    setDeleteData();
    fetch('/admin/api/cart', {
        method: 'post',
        body: JSON.stringify({
            'typeArrange': getTypeArrange()
        }),
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    }).then(res => res.json()).then(data => {
        console.info(data);

        if (getTypeArrange() == 0 && val == 0) // Sắp xếp mặc định
            setCartData(data[0], data[1]);
        else if (val == 0)
            setCartDataArrange(data[0], data[1], data[2]);
        else
            setCartByPrice(data[0], data[1], data[2]);
    }).catch(err => {
        console.log(err);
    });
}

// Đưa dữ liệu lên client
function setCartData(cart, book) {
    var cartId = 1;
    for (let i = 0; i < cart.length; i++) {
        // Kiểm tra tổng tiền của giỏ hàng
        if (!cart[i]['is_paid'] == 1 || cart[i]['total_money'] <= 0) {
            continue; // Bỏ qua giỏ hàng không hợp lệ
        }
        // Kiểm tra xem giỏ hàng có sách nào không
        const hasBooks = book.some(b => b.cart_id === cart[i].cart_id);
        if (!hasBooks) {
            continue; // Bỏ qua giỏ hàng không có sách
        }

        var parent = `<div id='c${cartId}' class='cart-id col-12'></div>`;
        document.getElementById('cart-admin').insertAdjacentHTML('beforeend', parent);

        var bookId = 1;
        var bookx = `
        <div class="card col-12">
            <div class="card-header">
                <div class="card-title">Thông tin giỏ hàng thứ ${cartId}</div>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group-default">
                            <div class="pt-2 pb-2">
                                <span class="text-success fw-bold">Tên tài khoản:</span>
                                <span>${cart[i]['username']}</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group-default">
                            <div class="pt-2 pb-2">
                                <span class="text-success fw-bold">Họ tên:</span>
                                <span>${cart[i]['last_name']} ${cart[i]['first_name']}</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group-default">
                            <div class="pt-2 pb-2">
                                <span class="text-success fw-bold">Số điện thoại:</span>
                                <span>${cart[i]['phone_number']}</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group-default">
                            <div class="pt-2 pb-2">
                                <span class="text-success fw-bold">Tổng tiền:</span>
                                <span>${format(cart[i]['total_money'])}</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group-default">
                            <div class="pt-2 pb-2">
                                <span class="text-success fw-bold">Thời gian tạo:</span>
                                <span>${new Date(cart[i]['created_date']).toLocaleString()}</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <button class="btn btn-danger" onclick="xoaDonHang(${cart[i]['cart_id']})">Xóa</button>
                    </div>
                </div>
            </div>
        </div>
        `;
        var listBook = `<div id='b${cartId++}' class='row'></div>`;
        document.getElementById(`c${cartId - 1}`).insertAdjacentHTML('beforeend', listBook);
        for (let j = 0; j < book.length; j++) {
            if (cart[i]['cart_id'] == book[j]['cart_id']) {
                bookx += `
                <div class="col-12 col-sm-6 col-md-4 col-lg-3">
                    <div class="card">
                        <div class="card-header">
                            <div class="card-head-row">
                                <div class="">${bookId++}. ${book[j]['name_book']}</div>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="img-book">
                                <img src="${book[j]['image']}" alt="${book[j]['image']}">
                            </div>
                            <div class="book-info">
                                <p><span class="text-success fw-bold">Loại sách:</span> ${book[j]['name_category']}</p
                                <p><span class="text-success fw-bold">Số lượng:</span> ${book[j]['amount']}</p>
                                <p><span class="text-warning fw-bold">Thành tiền:</span> ${format(book[j]['money'])}</p>
                            </div>
                        </div>
                    </div>
                </div>
                `;
            }
        }
        document.getElementById(`b${cartId - 1}`).insertAdjacentHTML('afterbegin', bookx);
    }
}

// Hàm xóa đơn hàng
function xoaDonHang(cartId) {
    if (confirm("Bạn có chắc chắn muốn xóa tất cả các mục trong giỏ hàng này không?")) {
        fetch(`/admin/api/cart/${cartId}`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
        })
        .then(res => {
            if (!res.ok) {
                throw new Error('Lỗi khi xóa đơn hàng');
            }
            return res.json();
        })
        .then(data => {
            // Cập nhật giao diện người dùng
            const cartItem = document.getElementById(`c${cartId}`);
            if (cartItem) {
                cartItem.remove(); // Xóa phần tử khỏi DOM
                updateCartSummary(); // Cập nhật tổng số tiền và số lượng
            }
            console.log('Đơn hàng đã được xóa thành công:', data);
            alert('Tất cả các mục trong giỏ hàng đã được xóa thành công!'); // Thông báo cho người dùng

            // Quay lại trang trước
            window.location = '/admin/cartview/'; // Quay lại trang trước
        })
        .catch(err => {
            console.error('Có lỗi xảy ra:', err);
            alert('Có lỗi xảy ra khi xóa đơn hàng. Vui lòng thử lại.');
        });
    }
}

// Cập nhật tổng số tiền và số lượng đơn hàng
function updateCartSummary() {
    const cartItems = document.querySelectorAll('.cart-id');
    let totalAmount = 0;
    let totalPrice = 0;

    cartItems.forEach(item => {
        const price = parseFloat(item.querySelector('.total-price').textContent.replace(' VNĐ', '').replace(/,/g, ''));
        totalPrice += price;
        totalAmount += 1; // Hoặc tính toán số lượng cụ thể nếu cần
    });

    document.getElementById('total-amount').textContent = totalAmount;
    document.getElementById('total-price').textContent = format(totalPrice);
}

// Sắp xếp tăng/giảm dần
function setCartDataArrange(cart, book, listTotal) {
    var cartId = 1;
    for (let i = 0; i < listTotal.length; i++) {
        for (let c = 0; c < cart.length; c++) {
            if (cart[c]['total_money'] == listTotal[i]) {
                var parent = `<div id='c${cartId}' class='cart-id col-12'></div>`;
                document.getElementById('cart-admin').insertAdjacentHTML('beforeend', parent);

                var child = `
                <div class="card col-12">
                    <div class="card-header">
                        <div class="card-title">Thông tin giỏ hàng thứ ${cartId}</div>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group-default">
                                    <div class="pt-2 pb-2">
                                        <span class="text-success fw-bold">Tên tài khoản:</span>
                                        <span>${cart[c]['username']}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group-default">
                                    <div class="pt-2 pb-2">
                                        <span class="text-success fw-bold">Họ tên:</span>
                                        <span>${cart[c]['last_name']} ${cart[c]['first_name']}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group-default">
                                    <div class="pt-2 pb-2">
                                        <span class="text-success fw-bold">Số điện thoại:</span>
                                        <span>${cart[c]['phone_number']}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group-default">
                                    <div class="pt-2 pb-2">
                                        <span class="text-success fw-bold">Tổng tiền:</span>
                                        <span>${format(cart[c]['total_money'])}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group-default">
                                    <div class="pt-2 pb-2">
                                        <span class="text-success fw-bold">Thời gian tạo:</span>
                                        <span>${new Date(cart[c]['created_date']).toLocaleString()}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <button class="btn btn-danger" onclick="xoaDonHang(${cart[c]['cart_id']})">Xóa</button>
                            </div>
                        </div>
                    </div>
                </div>
                `;
                document.getElementById(`c${cartId}`).insertAdjacentHTML('afterbegin', child);

                var bookId = 1;
                var bookx = ``;
                var listBook = `<div id='b${cartId++}' class='row'></div>`;
                document.getElementById(`c${cartId - 1}`).insertAdjacentHTML('beforeend', listBook);
                for (let j = 0; j < book.length; j++) {
                    if (cart[c]['cart_id'] == book[j]['cart_id']) {
                        bookx += `
                        <div class="col-12 col-sm-6 col-md-4 col-lg-3">
                            <div class="card">
                                <div class="card-header">
                                    <div class="card-head-row">
                                        <div class="">${bookId++}. ${book[j]['name_book']}</div>
                                    </div>
                                </div>
                                <div class="card-body">
                                    <div class="img-book">
                                        <img src="${book[j]['image']}" alt="${book[j]['image']}">
                                    </div>
                                    <div class="book-info">
                                        <p><span class="text-success fw-bold">Loại sách:</span> ${book[j]['name_category']}</p>
                                        <p><span class="text-success fw-bold">Số lượng:</span> ${book[j]['amount']}</p>
                                        <p><span class="text-warning fw-bold">Thành tiền:</span> ${format(book[j]['money'])}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        `;
                    }
                }
                document.getElementById(`b${cartId - 1}`).insertAdjacentHTML('afterbegin', bookx);
            }
        }
    }
}

// Xóa
function setDeleteData() {
    document.querySelectorAll('.cart-id').forEach(element => element.remove());
}

// Qui ước sắp xếp
function getTypeArrange() {
    if (document.getElementById('input-asc').checked) // Sắp xếp tăng dần
        return 1;
    if (document.getElementById('input-desc').checked) // Sắp xếp giảm dần
        return -1;
    else // Mặc định
        return 0;
}

function getPriceRange() {
    if (document.getElementById('selectPrice').value != 'select-all') {
        if (document.getElementById('selectPrice').value == 'select-1') // Dưới 1 triệu
            return 1;
        else if (document.getElementById('selectPrice').value == 'select-2') // Từ 1 - 2 triệu
            return 2;
        else return 3; // Trên 2 triệu
    } else return 0; // Mặc định
}

// Lọc danh sách từ mảng
function getListCart(list) {
    let listRemove = [];
    for (let i = 0; i < list.length; i++) {
        if (val == 1 && list[i] > 1000000) {
            listRemove.push(list[i]);
        }
        if (val == 2 && (list[i] < 1000000 || list[i] > 2000000)) {
            listRemove.push(list[i]);
        }
        if (val == 3 && list[i] < 2000000) {
            listRemove.push(list[i]);
        }
    }
    for (let i = 0; i < listRemove.length; i++) {
        list.splice(list.indexOf(listRemove[i]), 1);
    }

    return list;
}

// Sắp xếp theo giá
function setCartByPrice(cart, book, listTotal) {
    if (listTotal.length != 0)
        setCartDataArrange(cart, book, getListCart(listTotal));
}

// Format theo tiền tệ (VNĐ)
function format(n) {
    return n.toFixed(0).replace(/./g, function (c, i, a) {
        return i > 0 && c !== "." && (a.length - i) % 3 === 0 ? "," + c : c;
    }) + ' VNĐ';
}