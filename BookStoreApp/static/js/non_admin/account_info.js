$('#accountInfoClient').ready(function () {
           getAccountInfo()

})

function getAccountInfo() {
    fetch('/client/api/account-info', {
        method: 'post',
        body: JSON.stringify({
        }),
        headers: {
            'Accept': 'application/json',
            'Context-Type': 'application/json',
        }
    }).then(res => res.json()).then(data => {
         if(data != 'error')
            setAccountInfoData(data[0])
         else {
            Swal.fire({
                        title: 'Hệ thống đang bảo trì !',
                        text: 'Vui lòng quay lại sau',
                        icon: 'warning',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'Ok',
                    })
         }

    })
}

function setAccountInfoData(data){
    setData(data)
    var info = `<div class="my-3">
                    <div class="row">
                        <label class="col-md-2 offset-md-2" for="account-username">Tên tài khoản</label>
                        <input class="col-md-5" type="text" name="account-username" disabled="disabled"
                        value="${data['username']}">
                    </div>
                </div>
                <div class="my-3">
                    <div class="row">
                        <label class="col-md-2 offset-md-2" for="account-name">Họ tên</label>
                        <input class="col-md-5" type="text" name="account-name" disabled="disabled"
                        value="${data['name']}">
                    </div>
                </div>
                <div class="my-3">
                    <div class="row">
                        <label class="col-md-2 offset-md-2" for="account-role">Đối tượng</label>
                        <input class="col-md-5" type="text" name="account-role" disabled="disabled"
                        value="${data['role']}">
                    </div>
                </div>
                <div class="my-3">
                    <div class="row">
                        <label class="col-md-2 offset-md-2" for="account-email">Email</label>
                        <input class="col-md-5" type="text" name="account-email" disabled="disabled"
                        value="${data['gmail']}">
                    </div>
                </div>
                <div class="my-3">
                    <div class="row">
                        <label class="col-md-2 offset-md-2" for="account-phone">Số điện thoại</label>
                        <input class="col-md-5" type="text" name="account-phone" disabled="disabled"
                        value="${data['phone_number']}">
                    </div>
                </div>
                <div class="my-3">
                    <div class="row">
                        <label class="col-md-2 offset-md-2" for="account-address">Địa chỉ</label>
                        <input class="col-md-5" type="text" name="account-address" disabled="disabled"
                        value="${data['address']}">
                    </div>
                </div>
                <div class="my-3">
                    <div class="row">
                        <label class="col-md-2 offset-md-2" for="account-joined-date">Ngày tạo</label>
                        <input class="col-md-5" type="text" name="account-joined-date" disabled="disabled"
                        value="${data['joined_date']}">
                    </div>
                </div>
                <div class="my-3">
                    <div class="row">
                        <label class="col-md-2 offset-md-2" for="account-bd">Ngày sinh</label>
                        <input class="col-md-5" type="text" name="account-bd" disabled="disabled"
                        value="${data['date_of_birth']}">
                    </div>
                </div>
                <div class="my-3">
                    <div class="row">
                        <label class="col-md-2 offset-md-2" for="account-point">Điểm tích lũy</label>
                        <input class="col-md-5" type="text" name="account-point" disabled="disabled"
                        value="${data['accumulated_point']}">
                    </div>
                </div>`
    document.getElementById('accountInfoClient').insertAdjacentHTML('afterend', info)
}

function setData(data){
    for(let i in data){
        if (data[i] == '')
            data[i] = 'Thông tin chưa cập nhật'
    }
}

// Thay đổi mật khẩu
function setChangePassword(){
    if(isChangePassData() == true){
        fetch('/client/api/change-password', {
            method: 'post',
            body: JSON.stringify({
                'new_password': document.getElementById('accountNewPassword1').value,
                'old_password': document.getElementById('accountOldPassword').value
            }),
            headers: {
                'Accept': 'application/json',
                'Context-Type': 'application/json',
            }
            }).then(res => res.json()).then(data => {
                 if(data == 'wrong_password'){
                    Swal.fire({
                            title: 'Mật khẩu cũ sai !!!',
                            text: 'Vui lòng kiểm tra lại',
                            icon: 'warning',
                            confirmButtonColor: '#3085d6',
                            confirmButtonText: 'Ok',
                        })
                 }
                 else if(data == 'successful'){
                            Swal.fire(
                                'Đổi mật khẩu thành công',
                                '',
                                'success'
                            )
                            setDefaultChangePassword()
                        }
                        else {
                            Swal.fire({
                                        title: 'Hệ thống đang bảo trì !',
                                        text: 'Vui lòng quay lại sau',
                                        icon: 'warning',
                                        confirmButtonColor: '#3085d6',
                                        confirmButtonText: 'Ok',
                                    })
                        }

        })
    }
}

// kiểm tra dữ liệu nhập vào
function isChangePassData(){
    let oldPass = document.getElementById('accountOldPassword').value
    let newPass1 = document.getElementById('accountNewPassword1').value
    let newPass2 = document.getElementById('accountNewPassword2').value

    if (oldPass.length < 6 || newPass1.length < 6 || newPass2.length < 6){
        Swal.fire({
                        title: 'Độ dài mật khẩu phải ít nhất 6 kí tự !',
                        text: 'Vui lòng kiểm tra lại',
                        icon: 'warning',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'Ok',
                    })
        return false
    }
    else if (newPass1 != newPass2){
            Swal.fire({
                        title: 'Mật khẩu mới không trùng !',
                        text: 'Vui lòng kiểm tra lại',
                        icon: 'warning',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'Ok',
                    })
               return false
          }
          else if(oldPass ==newPass1){
                Swal.fire({
                        title: 'Mật khẩu mới trùng với mật khẩu cũ !',
                        text: 'Vui lòng kiểm tra lại',
                        icon: 'warning',
                        confirmButtonColor: '#3085d6',
                        confirmButtonText: 'Ok',
                    })
                return false
          }
    return true
}

// thiết lập giá trị mặc định của thay đổi mật khẩu
function setDefaultChangePassword(){
    document.getElementById('accountOldPassword').value = ''
    document.getElementById('accountNewPassword1').value = ''
    document.getElementById('accountNewPassword2').value = ''
    $('.thay-doi-mk').hide()
    document.getElementById('changepass').checked = false
}

