window.onload = function () {
    getProfileData()
}
// Lấy thông tin người dùng
function getProfileData() {
    fetch('/admin/profile/api/profile-info', {
        method: 'post',
        body: JSON.stringify({}),
        headers: {
            'Accept': 'application/json',
            'Context-Type': 'application/json',
        }
    }).then(res => res.json()).then(data => {
        setProfileData(data[0])
    }).catch(err => {
        console.log(err)
    });
}

// Gán dữ liệu ra html
function setProfileData(data) {
    // last_name
    if (data['last_name'] != '')
        document.getElementById('lastName').innerHTML = data['last_name']
    else
        document.getElementById('lastName').innerHTML = 'Thông tin chưa cập nhật'

    // first_name
    if (data['first_name'] != '')
        document.getElementById('firstName').innerHTML = data['first_name']
    else
        document.getElementById('firstName').innerHTML = 'Thông tin chưa cập nhật'

    // joined_date
    if (data['joined_date'] != '')
        document.getElementById('joinedDate').innerHTML = data['joined_date']
    else
        document.getElementById('joinedDate').innerHTML = 'Thông tin chưa cập nhật'

    // gmail
    if (data['gmail'] != '')
        document.getElementById('gmail').innerHTML = data['gmail']
    else
        document.getElementById('gmail').innerHTML = 'Thông tin chưa cập nhật'

    // lass_access
    if (data['lass_access'] != '')
        document.getElementById('lassAccess').innerHTML = data['lass_access']
    else
        document.getElementById('lassAccess').innerHTML = 'Thông tin chưa cập nhật'

    // username
    if (data['username'] != '')
        document.getElementById('username').innerHTML = data['username']
    else
        document.getElementById('username').innerHTML = 'Thông tin chưa cập nhật'

    // role
    if (data['role_name'] != '')
        document.getElementById('role').innerHTML = data['role_name']
    else
        document.getElementById('role').innerHTML = 'Thông tin chưa cập nhật'

}