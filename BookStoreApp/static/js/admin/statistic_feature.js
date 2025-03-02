let gChoiceInfo = {
  statisticType: 'revenue',
  statisticCondition: 'month_statistic',
  fromTime: null,
  toTime: null,
  bookName: null,
  hintIndex: null,
  flagTimeInput: null
}

let gChartInfo = {
  chart: null,
  type: null,
  data: null,
  backgroundColor: null,
  label: null,
  labels: null
}

// Thiết lập màu nên cho chart khi load trang lần đầu
window.onload = setBackgroundChart(gChartInfo)

// Gửi các thông tin lựa chọn lên server để lấy dữ liệu thống kê
function getStatisticData(choiceInfo, chartInfo) {
  choiceInfo.statisticType = $('#statisticType').val()
  var bookName = $('#bookName').val()
  bookName = (bookName == undefined || bookName.length <= 0) ? null : $('#bookName').val()
  choiceInfo.bookName = bookName
  choiceInfo.statisticCondition = $('#statisticCondition').val()

  fetch('/admin/statistic/api/data', {
    method: 'post',
    body: JSON.stringify({
      'statistic_type': choiceInfo.statisticType,
      'statistic_condition': choiceInfo.statisticCondition,
      'from_time': choiceInfo.fromTime,
      'to_time': choiceInfo.toTime,
      'book_name': choiceInfo.bookName
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(res => res.json()).then(statisticData => {
    setStatisticInput(choiceInfo, chartInfo)

    if (statisticData.length <= 0) {
      resetData(chartInfo)
      return
    }
    $('#pdfChart').show()
    $('#statisticTable').show()

    setStatisticDataTable(statisticData)
    setChartData(statisticData, chartInfo)
    chartInfo.label = $("#statisticType option:selected").text()
    setChart(chartInfo)

  })
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


// Thiết lập cho chart dựa vào màu nên của trang web
function setBackgroundChart(chartInfo) {
  switch ($('body').attr('data-background-color')) {
    case 'bg1':
      chartInfo.backgroundColor = '#fafafa'
      break
    case 'bg2':
      chartInfo.backgroundColor = '#ffffff'
      break
    case 'bg3':
      chartInfo.backgroundColor = '#f1f1f1'
      break
    default:
      chartInfo.backgroundColor = '#202940'
  }
  chartInfo.label = $('#statisticType option:selected').text()
  setChart(chartInfo)
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
  getStatisticData(gChoiceInfo, gChartInfo)
}

// Hiệu ứng khi hover qua danh sách gợi ý
function setOnMouseOverHint(position) {
  gChoiceInfo.hintIndex = position
  for (let i = 1; i <= $('#bookNameResultInput').children().length; i++)
    $(`.stats-choice .show-hint p:nth-child(${i})`).css('background-color', 'white');
  $(`.stats-choice .show-hint p:nth-child(${position})`).css('background-color', '#04a9f5');

}

// Thiết lập dữ liệu input cho chức năng thống kê
function setStatisticInput(choiceInfo, chartInfo) {
  var conditionSelect = $('#statisticCondition').val()
  var timeAreaInput = $('#timeInput')

  timeAreaInput.css('display', 'none')
  if (conditionSelect.indexOf('month') != conditionSelect.lastIndexOf('month') ||
    conditionSelect.indexOf('quarter') != conditionSelect.lastIndexOf('quarter') ||
    conditionSelect.indexOf('year') != conditionSelect.lastIndexOf('year')) {
    var minVal = null
    var maxVal = null
    if (conditionSelect.includes('month')) {
      minVal = 1
      maxVal = 12
    }

    if (conditionSelect.includes('quarter')) {
      minVal = 1
      maxVal = 4
    }

    if (conditionSelect.includes('year')) {
      minVal = 2018
      maxVal = 2100
    }

    timeAreaInput.css('display', 'flex')
    var selection = ''
    for (let i = minVal; i <= maxVal; i++)
      selection += `<option value=${i}>${i}</option>`

    if (!choiceInfo.flagTimeInput) {
      $('#leftTime').html(selection)
      $('#rightTime').html(selection)
      choiceInfo.flagTimeInput = true
      choiceInfo.fromTime = choiceInfo.toTime = minVal
      getStatisticData(choiceInfo, chartInfo)
    }
  }
}

// Khởi tạo dữ liệu
function setInitialData(chartInfo, choiceInfo) {
  chartInfo.type = 'pie'
  chartInfo.data = chartInfo.labels = []
  choiceInfo.flagTimeInput = false
  getStatisticData(choiceInfo, chartInfo)
}

// Tái thiết lập dữ liệu
function resetData(chartInfo) {
  chartInfo.data = []
  chartInfo.chart.destroy()
  $('#pdfChart').hide()
  $('#statisticTable').hide()
}

// Thiết lập label header cho bảng kết quả thống kê
function setLabelHeaderTable() {
  var conditionSelect = $('#statisticCondition').val()
  if (conditionSelect.includes('month'))
    return 'Tháng'

  if (conditionSelect.includes('quarter'))
    return 'Quý'
  return 'Năm'
}

// Thiết lập result header cho bảng kết quả thống kê
function setResultHeaderTable() {
  if ($('#statisticType').val().includes('revenue'))
    return 'Tổng doanh thu'
  return 'Tần suất bán sách'
}


// Thiết lập dữ liệu bảng kết quả thống kê
function setStatisticDataTable(statisticData) {
  var row = ''
  var header = `<tr>
                  <th>${'Số thứ tự'}</th>
                  <th>${setLabelHeaderTable()}</th>
                  <th>${setResultHeaderTable()}</th>
              </tr>`

  for (let i = 0; i < statisticData.length; i++)
    if ($('#statisticType').val().includes('revenue'))
      row += `<tr> 
                  <td>${i + 1}</td>
                  <td>${statisticData[i]['time']}</td>
                  <td>${statisticData[i]['revenue_total']}</td>
              </tr>`
  else
    row += `<tr> 
                  <td>${i + 1}</td>
                  <td>${statisticData[i]['time']}</td>
                  <td>${statisticData[i]['amount_total']}</td>
              </tr>`

  $('#titleStatisticTable').html(header)
  $('#dataStatisticTable').html(row)
}

//  Thiết lập dữ liệu cho chart
function setChartData(statisticData, chartInfo) {
  chartInfo.data = [];
  chartInfo.labels = [];
  var resultKey = $('#statisticType').val().includes('revenue') ? 'revenue_total' : 'amount_total'
  for (let i = 0; i < statisticData.length; i++) {

    chartInfo.labels.push(statisticData[i]['time'])
    data = statisticData[i][resultKey]
    if (resultKey == 'revenue_total')
      chartInfo.data.push(parseInt(data.substring(0, data.indexOf(' ')).replaceAll(',', '')))
    else
      chartInfo.data.push(data)
  }
}

// Thiết lập chart
function setChart(chartInfo) {
  var backgroundColor = [];
  var borderColor = [];
  if (chartInfo.data != null)
    for (let i = 0; i < chartInfo.data.length; i++) {
      r = Math.floor(Math.random() * 255 + 1);
      g = Math.floor(Math.random() * 255 + 1);
      b = Math.floor(Math.random() * 255 + 1);
      backgroundColor.push(`rgba(${r},${g}, ${b}, 0.7)`);
      borderColor.push(`rgba(${r},${g}, ${b}, 1)`);
    }
  else
    return
  const ctx = document.getElementById('chart').getContext('2d');

  if (chartInfo.chart != null)
    chartInfo.chart.destroy();

  const bgColorPDF = {
    id: 'bgColorPDF',
    beforeDraw: (chart) => {
      const {
        ctx,
        width,
        height
      } = chart
      ctx.fillStyle = chartInfo.backgroundColor
      ctx.fillRect(0, 0, width, height)
      ctx.restore()
    }
  }
  chartInfo.chart = new Chart(ctx, {
    type: chartInfo.type,
    data: {
      labels: chartInfo.labels,
      datasets: [{
        label: chartInfo.label,
        data: chartInfo.data,
        backgroundColor: backgroundColor,
        borderColor: borderColor,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    },
    plugins: [bgColorPDF]
  });
}

// Thiết lập dữ liệu cho pdf và xuất pdf
function setPdfExport() {

  const canvas = document.getElementById('chart')
  canvas.toDataURL('image/jpeg', 1.0)


  const pdf = new jsPDF({
    orientation: 'portrait',
    format: 'a4',
    putOnlyUsedFonts: true,
    floatPrecision: 16
  })
  pdf.setFontSize(13)
  pdf.text(`Bieu do thong ke ${$('#statisticType option:selected').text()}`.toUpperCase(), 10, 15)
  pdf.addImage({
    imageData: canvas,
    format: 'JPEG',
    x: 30,
    y: 45,
    width: 250,
    height: 200
  })
  pdf.addPage({
    format: 'a4',
    orientation: 'portrait'
  })
  pdf.autoTable({
    html: '#statisticTable',
    theme: 'grid',
    headStyles: {
      fontStyle: 'bold',
      halign: 'center',
      valign: 'middle',
      fontSize: 13,
      cellWidth: 'auto',
      minCellHeight: 15,
      lineWidth: 1,
      lineColor: [4, 41, 58]
    },
    bodyStyles: {
      halign: 'center',
      valign: 'center',
      lineColor: [4, 41, 58],
      cellPadding: {
        bottom: 5,
        top: 5
      }
    }
  })

  pdf.text('@CopyRight: Open University', 77, pdf.lastAutoTable.finalY + 10)

  pdf.autoPrint({
    variant: 'non-conform'
  });
  pdf.save('statistic.pdf')

  Swal.fire({
    title: 'Xuất phiếu thành công',
    icon: 'success',
    confirmButtonColor: '#3085d6',
    confirmButtonText: 'Ok',
  })
}

$(document).ready(() => {
  gChartInfo.backgroundColor = $('.card').css('background-color')
  setInitialData(gChartInfo, gChoiceInfo)

  // Bắt sự kiện khi nhập từ khóa tìm kiếm tên sách
  $('#bookName').keydown((event) => {
    if (gChoiceInfo.hintIndex == null)
      return;
    // Ấn enter
    if (event.keyCode == 13) {
      event.preventDefault()
      $('#bookName').val($(`.stats-choice .show-hint p:nth-child(${gChoiceInfo.hintIndex})`).text().trim())
      $('#bookNameResultInput').html('')
      getStatisticData(gChoiceInfo, gChartInfo)
    }

    // Ấn mũi tên đi xuống
    if (event.keyCode == 40) {
      for (let i = 1; i <= $('#bookNameResultInput').children().length; i++)
        $(`.stats-choice .show-hint p:nth-child(${i})`).css('background-color', 'white')
      if (++gChoiceInfo.hintIndex > $('#bookNameResultInput').children().length)
        gChoiceInfo.hintIndex = 1
      $(`.stats-choice .show-hint p:nth-child(${gChoiceInfo.hintIndex})`).css('background-color', '#04a9f5')
    }

    // Ấn mũi tên đi lên
    if (event.keyCode == 38) {
      for (let i = 1; i <= $('#bookNameResultInput').children().length; i++)
        $(`.stats-choice .show-hint p:nth-child(${i})`).css('background-color', 'white')
      if (--gChoiceInfo.hintIndex <= 0)
        gChoiceInfo.hintIndex = $('#bookNameResultInput').children().length
      $(`.stats-choice .show-hint p:nth-child(${gChoiceInfo.hintIndexxHint})`).css('background-color', '#04a9f5')
    }
  })

  $('.changeBackgroundColor').click(() => setBackgroundChart(gChartInfo))


  $('#timeInput').hide()
  $('#bookNameInput').hide()

  $('#bookName').on('input', () => {
    keyword = $('#bookName').val() == undefined ? null : $('#bookName').val()
    getBookNameHint(keyword, gChoiceInfo)
    getStatisticData(gChoiceInfo, gChartInfo)
  })

  $('#bookName').focus(() => {
    $('#bookNameResultInput').show()
    if (gChoiceInfo.hintIndex != null)
      $(`.stats-choice .show-hint p:nth-child(1)`).css('background-color', '#04a9f5')
  })

  $('#statisticType').change(() => {
    gChoiceInfo.statisticType = $('#statisticType').val()
    getStatisticData(gChoiceInfo, gChartInfo)
    if ($('#statisticType').val() == 'frequently_book_selling') {
      $('#bookNameInput').show()
    } else {
      $('#bookNameInput').hide()
      $('#bookName').val('')
      $('#bookNameResultInput').html('')
    }
  })

  $('#chartType').change(() => {
    gChartInfo.type = $('#chartType').val()
    getStatisticData(gChoiceInfo, gChartInfo)
  })

  $('#statisticCondition').change(function () {
    gChoiceInfo.flagTimeInput = false
    if ($(this).val().indexOf('month') != $(this).val().lastIndexOf('month') ||
      $(this).val().indexOf('quarter') != $(this).val().lastIndexOf('quarter') ||
      $(this).val().indexOf('year') != $(this).val().lastIndexOf('year')) {
      setStatisticInput(gChoiceInfo, gChartInfo)
      gChoiceInfo.fromTime = parseInt($('#leftTime').val())
      gChoiceInfo.toTime = parseInt($('#rightTime').val())
    } else {
      gChoiceInfo.fromTime = null
      gChoiceInfo.toTime = null
    }
    getStatisticData(gChoiceInfo, gChartInfo)
  })


  $('#leftTime').data('lastSelectedIndex', 0)

  $('#leftTime').click(function () {
    $(this).data('lastSelectedIndex', this.selectedIndex)
  })
  $('#rightTime').data('lastSelectedIndex', 0)

  $('#rightTime').click(function () {
    $(this).data('lastSelectedIndex', this.selectedIndex)
  })

  $('#leftTime').change(function () {
    if (parseInt($(this).val()) > parseInt($('#rightTime').val())) {
      this.selectedIndex = $(this).data('lastSelectedIndex')
    } else {
      gChoiceInfo.fromTime = parseInt($(this).val())
      getStatisticData(gChoiceInfo, gChartInfo)
    }
  })

  $('#rightTime').change(function () {
    if (parseInt($(this).val()) < parseInt($('#leftTime').val())) {
      this.selectedIndex = $(this).data('lastSelectedIndex')
    } else {
      gChoiceInfo.toTime = parseInt($(this).val())
      getStatisticData(gChoiceInfo, gChartInfo)
    }
  })

  $('#pdfChart').click(function () {
    setPdfExport()
  })
})