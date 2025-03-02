from BookStoreApp.repository.admin.profile_repository import get_info_user_by_account_id as giu


# Lấy thông tin account dựa vào id
def get_info_user_by_account_id(id=0):
    if id:
        return giu(id)


# Chuyển thông tin sang dictionary
def get_info(data=None, **kwargs):
    if data is None:
        return []

    profile_data = []

    profile_data.append({
        'username': data[0],
        'first_name': data[1],
        'last_name': data[2],
        'joined_date': data[3].strftime('%d/%m/%Y'),
        'avatar': data[4],
        'gmail': data[5],
        'role_name': data[6],
        'lass_access': data[7].strftime("%m/%d/%Y, %H:%M:%S")
    })

    return profile_data
