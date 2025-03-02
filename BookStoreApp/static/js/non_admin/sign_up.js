let listCountry = {}
// Lấy dữ liệu các tỉnh/thành API
window.onload = function () {
    fetch("https://provinces.open-api.vn/api/?depth=2")
        .then(res => res.json())
        .then(data => {
            listCountry = data
            setCountry(data)
            setDistrictsDefault()
        })
}

// Đổ dữ liệu tỉnh/thành ra client
function setCountry(data) {
    let options = ``
    for (let c = 0; c < data.length; c++) {
        options += `<option id='${data[c].codename}' >${data[c].name}</option>`
    }
    document.getElementById('city').insertAdjacentHTML('beforeend', options)

}

//   Xuất quận/huyện mặc định
function setDistrictsDefault() {
    $("#district option[class='flag']").remove();
    let district = listCountry[0].districts
    let options = ``
    if (district != null)
        for (let i = 0; i < district.length; i++) {
            options += `<option class="flag">${district[i].name}</option>`
        }
    document.getElementById('district').insertAdjacentHTML('beforeend', options)
}

// Đổ dữ liệu quận/ huyện
function setDistricts() {
    $("#district option[class='flag']").remove();
    let district = getCountryDataByValue()
    let options = ``
    if (district != null)
        for (let i = 0; i < district.length; i++) {
            options += `<option class="flag">${district[i].name}</option>`
        }
    document.getElementById('district').insertAdjacentHTML('beforeend', options)
}

// Lấy danh sách cái quận/huyện
function getCountryDataByValue() {
    for (let i = 0; i < listCountry.length; i++) {
        if (document.getElementById('city').value == listCountry[i].name)
            return listCountry[i].districts
    }
    return null
}

let numberConfirm;
// Đưa dữ liệu xuống server để tiến hành gửi mật mã xác nhận qua email
function setConfirmEmail() {
    setSignup()
}



// Lấy thông tin tiến hành tạo tài khoản
function setSignup() {
    fetch("/client/api/sign-up", {
        method: 'post',
        body: JSON.stringify({
            'last_name': document.getElementById('lastName').value,
            'first_name': document.getElementById('firstName').value,
            'date_of_birth': document.getElementById('dateOfBirth').value,
            'phone_number': document.getElementById('phoneNumber').value,
            'email': document.getElementById('email').value,
            'city': document.getElementById('city').value,
            'district': document.getElementById('district').value,
            'address': document.getElementById('address').value,
            'username': document.getElementById('username').value,
            'password': document.getElementById('inputPassword').value
        }),
        headers: {
            'Accept': 'application/json',
            'Context-Type': 'application/json',
        }
    }).then(res => res.json()).then(data => {
        if (data == 'error') {
            Swal.fire({
                title: 'Thông tin bạn nhập không hợp lệ !!!',
                text: 'Xin vui lòng thử lại',
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Ok',
            })
            $('#login-form').removeClass("fade")
            $('#register-form').removeClass("fade")
            $('#login-form').modal("hide")
            $('#register-form').modal("hide")

            setDisabledInput()
            setResetValueInput()
            $('#city').val('Thành phố Hà Nội')
            setDistrictsDefault()
        }
        else if (data == 'exist') {
            Swal.fire({
                title: 'Tên đăng nhập đã tồn tại !!!',
                text: '',
                icon: 'warning',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Ok',
            })
            setDisabledInput()
        }
        else {
            Swal.fire(
                'Đăng kí thành công',
                'Tài khoản của bạn đã được kích hoạt!',
                'success'
            )
            $('#login-form').removeClass("fade")
            $('#register-form').removeClass("fade")
            $('#login-form').modal("hide")
            $('#register-form').modal("hide")
            setDisabledInput()
            setResetValueInput()
            $('#city').val('Thành phố Hà Nội')
            setDistrictsDefault()
        }
    })
}
// xóa disabled của các thẻ input
function setDisabledInput() {
    document.getElementById('city').disabled = false
    document.getElementById('district').disabled = false
    document.getElementById('btn-sign-up').disabled = false
    document.getElementById('numberEmail').value = ''
    document.getElementById('confirmEmail').style.display = "none"
    $("#form-signup input").removeAttr('disabled');
}
// cho dữ liệu rỗng như ban đầu ở client
function setResetValueInput() {
    $("#form-signup input").val('')
    document.getElementById('confirmEmail').style.display = "none"
}

// xóa dữ liệu khi đóng modal
$(".close").click(function () {
    Swal.fire({
        title: 'Bạn có chắc chắn muốn đóng?',
        text: 'Dữ liệu sẽ bị xóa nếu bạn nhấn "OK"',
        showDenyButton: true,
        denyButtonText: `Không`,
    }).then((result) => {
        if (result.isConfirmed) {
            $('#login-form').removeClass("fade")
            $('#register-form').removeClass("fade")
            $('#login-form').modal("hide")
            $('#register-form').modal("hide")
            setDisabledInput()
            setResetValueInput()
            $('#city').val('Thành phố Hà Nội')
            setDistrictsDefault()
        } else {
            $("ul.tabs .register-tab").addClass("active")
            $('#register-form').modal("show")
        }
    });

})

