let gChoiceInfo = {
  hintIndex: null
}

// Gửi thông tin từ khóa tìm kiếm tên sách lên server và nhận về danh sách tên sách tìm được
function getBookNameHint(keyword, choiceInfo) {
  fetch('/admin/statistic/api/book-name', {
    method: 'post',
    body: JSON.stringify({
      'keyword': keyword
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(function (res) {
    return res.json()
  }).then(function (hintResult) {
    setHintResult(hintResult, choiceInfo)
  })
}

// Lấy thông tin của sách
function getBookInfo(bookName) {
  fetch('/admin/previewview/api/book-name', {
      method: 'post',
      body: JSON.stringify({
        'book_name': bookName
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(res => res.json()).then(bookInfo => {
      setBookInfoData(bookInfo)
    })
}

// Lấy thông tin các bản preview của sách
function getPreviewBookInfo(bookName) {
  fetch('/admin/previewview/api/preview', {
      method: 'post',
      body: JSON.stringify({
        'book_name': bookName
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(res => res.json()).then(previewInfo => {
      setPreviewInfoData(previewInfo, bookName)
    })
}

// Xóa bản xem trước
function deletePreview(previewId, bookName) {
  fetch('/admin/previewview/api/delete', {
      method: 'post',
      body: JSON.stringify({
        'preview_id': previewId
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(res => res.json()).then(result => {
      if (result)
        Swal.fire(
          'Xóa thành công!!!',
          `Bản xem trước đã có mã ${previewId} đã bị xóa`,
          'success'
        ).then(function () {
          getBookInfo(bookName)
          getPreviewBookInfo(bookName)
        })

      else
        Swal.fire({
          title: 'Xóa thất bại!!!',
          text: 'Xin vui lòng thử lại',
          icon: 'warning',
          confirmButtonColor: '#3085d6',
          confirmButtonText: 'Ok',
        })

    })
}

// Thiết lập hiển thị gợi ý khi tìm
function setHintResult(hintResult, choiceInfo) {
  if (hintResult.length > 0)
    choiceInfo.hintIndex = 1
  var row = ''
  for (let i = 0; i < hintResult.length; i++)
    row += `<p onclick = "setOnClickHint('${hintResult[i]['book_name']}')"
      onmouseover='setOnMouseOverHint(${i + 1})'>${hintResult[i]['book_name']}</p>`

  $('#bookNameResultInput').html(row)
}

// Chọn gợi ý
function setOnClickHint(hint) {
  $('#bookName').val(hint.trim())
  $('#bookNameResultInput').html('')
}

// Hiệu ứng khi hover qua danh sách gợi ý
function setOnMouseOverHint(position) {
  gChoiceInfo.hintIndex = position
  for (let i = 1; i <= $('#bookNameResultInput').children().length; i++)
    $(`.show-hint p:nth-child(${i})`).css('background-color', 'white');
  $(`.show-hint p:nth-child(${position})`).css('background-color', '#04a9f5');
}

// Thiết lập thông tin sách
function setBookInfoData(bookInfo) {
  if (bookInfo == null) {
    Swal.fire({
      title: 'Thông báo',
      text: 'Sách không tồn tại',
      icon: 'warning',
      confirmButtonColor: '#3085d6',
      confirmButtonText: 'Ok',
    })
    $('#previewAddition').hide()
    return
  }
  var image = bookInfo['book_image']
  if (image == null || image.length == 0)
  image = 'https://res.cloudinary.com/attt92bookstore/image/upload/v1646019055/book/book_qmruxn.jpg'
  var data = `
      <div class="card">
      <div class="card-header">
          <div class="card-head-row">
              <div class="card-title">Thông tin sách</div>
          </div>
      </div>
      <div class="card-body d-flex align-items-center justify-content-center flex-wrap text-center">
          <div class="img-book col-12 col-md-3">
          <img src='${image}'/>
          </div>
          <div class="book-info col-12 col-md-6">
              <p><span class="text-success fw-bold">Tên sách: </span> ${bookInfo['book_name']}</p>
              <p><span class="text-success fw-bold">Loại sách:</span>  ${bookInfo['category_name']}</p>
              <p><span class="text-warning fw-bold">Nhà xuất bản:</span> ${bookInfo['manufacturer_name']}</p>
          </div>
      </div>
  </div>
  `
  $('#bookInfo').html(data)
  $('#bookNameData').val(`${bookInfo['book_name']}`)
  $('#previewAddition').show()
}


// Thiết lập dữ liệu cho bản xem trước
function setPreviewInfoData(previewData, bookName) {

  var data = `
  <div class="card-header">
  <div class="card-head-row">
      <div class="card-title">Thông tin các bản xem trước của sách</div>
  </div>
</div>
<div class="row my-4 justify-content-center">`
  if (previewData.length == 0) {
    data += '<p class="text-danger fw-bold mt-3">Không có bản xem trước nào</p>'
    $('#previewInfo').html(data)
    return
  }

  for (let i = 0; i < previewData.length; i++) {
    var image = previewData[i]['preview_image']
    if (image == null || image.length == 0)
    image = 'https://res.cloudinary.com/attt92bookstore/image/upload/v1646019055/book/book_qmruxn.jpg'

    data += `
    <div class="img-book col-12 col-md-3 position-relative">
    <img id='${previewData[i]['preview_id']}' src='${image}'/>
    <button class="btn btn-primary btn-sm btn-delete"onclick= "deletePreview('${previewData[i]['preview_id']}', '${bookName}')">Xóa</button>
    </div>
      `
  }
  data += `</div>`
  $('#previewInfo').html(data)
}

$(document).ready(() => {
  $('#previewAddition').hide()
  $('#bookName').keydown((event) => {
    if (gChoiceInfo.hintIndex == null)
      return;
    // Ấn enter
    if (event.keyCode == 13) {
      event.preventDefault()
      $('#bookName').val($(`.show-hint p:nth-child(${gChoiceInfo.hintIndex})`).text().trim())
      $('#bookNameResultInput').html('')
    }

    // Ấn mũi tên đi xuống
    if (event.keyCode == 40) {
      for (let i = 1; i <= $('#bookNameResultInput').children().length; i++)
        $(`.show-hint p:nth-child(${i})`).css('background-color', 'white')
      if (++gChoiceInfo.hintIndex > $('#bookNameResultInput').children().length)
        gChoiceInfo.hintIndex = 1
      $(`.show-hint p:nth-child(${gChoiceInfo.hintIndex})`).css('background-color', '#04a9f5')
    }

    // Ấn mũi tên đi lên
    if (event.keyCode == 38) {
      for (let i = 1; i <= $('#bookNameResultInput').children().length; i++)
        $(`.show-hint p:nth-child(${i})`).css('background-color', 'white')
      if (--gChoiceInfo.hintIndex <= 0)
        gChoiceInfo.hintIndex = $('#bookNameResultInput').children().length
      $(`.show-hint p:nth-child(${gChoiceInfo.hintIndexxHint})`).css('background-color', '#04a9f5')
    }
  })
  $('#bookName').on('input', () => {
    keyword = $('#bookName').val() == undefined ? null : $('#bookName').val()
    getBookNameHint(keyword, gChoiceInfo)
  })

  $('#bookName').focus(() => {
    $('#bookNameResultInput').show()
    if (gChoiceInfo.hintIndex != null)
      $(`.show-hint p:nth-child(1)`).css('background-color', '#04a9f5')
  })

  $('#searchBookName').click(() => {
    var bookName = $('#bookName').val()
    if (bookName.length == 0) {
      Swal.fire({
        title: 'Thông báo',
        text: 'Thông tin tên sách không được để trống',
        icon: 'warning',
        confirmButtonColor: '#3085d6',
        confirmButtonText: 'Ok',
      })
      return
    }
    getBookInfo(bookName)
    getPreviewBookInfo(bookName)
  })
})