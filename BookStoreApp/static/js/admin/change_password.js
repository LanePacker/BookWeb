var numberFlag = false;
var lengthFlag = false;
var titleAlert = ''
var textAlert = ''

function passAccountData() {
    fetch('/admin/api/change-password', {
        method: 'post',
        body: JSON.stringify({
            'username': document.getElementById("username").innerText.slice('nguoi dung: '.length).trim(),
            'old_password': document.getElementById("oldPsw").value,
            'new_password': document.getElementById("newPsw").value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (res) {
        return res.json()
    }).then(function (datas) {
        if (datas['result']) {
            Swal.fire(
                'Đổi mật khẩu thành công!!!',
                'Mật khẩu của bạn đã được cập nhật.',
                'success'
            ).then(function () {
                window.location = '/admin/';
            })
        } else if (datas['wrong_password']) {
            Swal.fire({
                title: 'Nhập mật khẩu cũ sai!!!',
                text: 'Xin vui lòng kiểm tra lại',
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Ok',
            })
        } else {
            Swal.fire({
                title: 'Đổi mật khẩu thất bại!!!',
                text: 'Xin vui lòng kiểm tra lại',
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Ok',
            })
        }
    })
}

$(document).ready(function () {
    $('#cfm').click(function () {
        var flag = checkAlertWrong()
        if (!flag) {
            Swal.fire({
                title: titleAlert,
                text: textAlert,
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Ok',
            })
            return
        }
        Swal.fire({
            title: 'Bạn có chắc chắn đổi mật khẩu ?',
            text: 'Mọi thao tác sau khi thực hiện không thể phục hồi lại',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Xác nhận',
            cancelButtonText: 'Huỷ bỏ'
        }).then((result) => {
            if (result.isConfirmed) {
                passAccountData()
            }
        })
    })

    var numbers = /[0-9]/g;
    $('#oldPsw').keyup(function () {
        // Validate numbers
        if ($(this).val().match(numbers))
            numberFlag = true;
        // Validate length
        if ($(this).val().length >= 8 && $(this).val().length <= 12)
            lengthFlag = true;
    })
})

function checkCondition(element, text) {
    if (!(element.val().length >= 6 && element.val().length <= 8)) {
        titleAlert = `Độ dài của ${text} không hợp lệ`
        textAlert = 'Lưu ý: độ dài từ 6 đến 8 ký tự'
        return false
    }
    var numbers = /[0-9]/g;
    if (element.val().match(numbers) == null) {
        titleAlert = `${text} chỉ được nhập số`
        textAlert = 'Xin vui lòng kiểm tra lại!!!'
        return false
    }
    return true
}

function checkAlertWrong() {
    if (!checkCondition($('#oldPsw'))) {
        checkCondition($('#oldPsw'), 'Mật khẩu cũ')
        return false
    }

    if (!checkCondition($('#newPsw'))) {
        checkCondition($('#newPsw'), 'Mật khẩu mới')
        return false
    }
    if (!checkCondition($('#cfmNewPsw'))) {
        checkCondition($('#cfmNewPsw'), 'mật khẩu xác nhận')
        return false
    }
    if ($('#newPsw').val() != $('#cfmNewPsw').val()) {
        titleAlert = 'Mật khẩu xác nhận không trùng khớp với mật khẩu mới'
        return false
    }
    if ($('#newPsw').val() == $('#oldPsw').val()) {
        titleAlert = 'Mật khẩu mới trùng với mật khẩu cũ'
        return false
    }
    return true
}