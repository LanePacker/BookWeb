var url; // update 17/03/2022

// Xử lý sự kiện khi người dùng nhấn nút đăng nhập
$('#btnSignIn').click(function () {
    url = location.href; // Lưu URL hiện tại
    if (isExactlyDataSignIn() == true) {
        fetch('/client/api/sign-in', {
            method: 'post',
            body: JSON.stringify({
                'username': document.getElementById('usernameSignIn').value,
                'password': document.getElementById('passwordSignIn').value
            }),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json', // Sửa 'Context-Type' thành 'Content-Type'
            }
        }).then(res => res.json()).then(data => {
            if (data == 'error') {
                Swal.fire({
                    title: 'Tên đăng nhập hoặc mật khẩu sai !',
                    text: 'Xin vui lòng kiểm tra lại',
                    icon: 'warning',
                    confirmButtonColor: '#3085d6',
                    confirmButtonText: 'Ok',
                });
            } else {
                window.location = url; // Chuyển hướng về URL đã lưu
            }
        }).catch(error => {
            console.error('Có lỗi xảy ra:', error); // Xử lý lỗi nếu có
        });
    }
});

// Kiểm tra thông tin nhập
function isExactlyDataSignIn() {
    if (document.getElementById('usernameSignIn').value == '' || document.getElementById('passwordSignIn').value == '') {
        Swal.fire({
            title: 'Vui lòng kiểm tra lại !!!',
            text: '',
            icon: 'warning',
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Ok',
        });
        return false; // Ngăn chặn việc gửi yêu cầu nếu thông tin không hợp lệ
    }
    return true; // Trả về true nếu thông tin hợp lệ
}