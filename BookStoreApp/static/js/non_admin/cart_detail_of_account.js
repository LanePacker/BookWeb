$('#accountCD').ready(function () {
    fetch('/client/api/cart-detail', {
        method: 'post',
        body: JSON.stringify({
        }),
        headers: {
            'Accept': 'application/json',
            'Context-Type': 'application/json',
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
         if(data != 'error')
            setCartDetail(data)
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
})

// đổ dữ liệu ra client
function setCartDetail(data){
    if(isData(data) == true){
        html =``
        for(let i =0; i < data.length; i++){
            html +=`<tr >
                        <td class ='text-primary font-weight-bold'>${data[i]['id']}</td>
                        <td >${data[i]['date']}</td>
                        <td >${data[i]['books']}</td>
                        <td >${format(data[i]['total'])}</td>
                        <td >${data[i]['status']}</td>
                  </tr>`
        }
        document.getElementById('cartDetailAccount').insertAdjacentHTML('beforeend', html)
    }

}

// kiểm tra có đơn hàng hay không
function isData(data){
    if(data.length < 1){
        html =`<h5 style="text-align: center; margin-top: 50px; margin-bottom: 50px">Chưa có đơn hàng nào!!!</h5>`
        document.getElementById('cartDetailAccount').insertAdjacentHTML('afterend', html)
        document.getElementById('cartDetailAccount').style.display = 'none'
        return false
    }
    return true
}

// format theo tiền tệ(VNĐ)
function format(n) {
    return n.toFixed(0).replace(/./g, function (c, i, a) {
        return i > 0 && c !== "." && (a.length - i) % 3 === 0 ? "," + c : c
    }) + ' VNĐ'
}