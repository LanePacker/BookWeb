// Thông tin dành cho phân trang
let gPageInfo = {
    pageSize: 10,
    beginIndex: null,
    endIndex: null,
    currentPage: null
}

// Thông tin các loại lựa chọn báo cáo
let gChoiceInfo = {
    reportType: 'revenue',
    month: null,
    quarter: null,
    year: null,
}

// Gửi các thông tin cần thiết lên server để lấy dữ liệu báo cáo
function getReportData(choiceInfo, pageInfo) {
    fetch('/admin/report/api/data', {
        method: 'post',
        body: JSON.stringify({
            'report_type': choiceInfo.reportType,
            'month': choiceInfo.month,
            'quarter': choiceInfo.quarter,
            'year': choiceInfo.year,
            'begin_index': pageInfo.beginIndex,
            'end_index': pageInfo.endIndex
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(reportDatas => {
        setReportDataTable(reportDatas)
    })
}

// Gửi các thông tin cần thiết lên server để lấy tổng số lượng bản báo cáo
function getAmountReportData(choiceInfo, pageInfo) {
    fetch('/admin/report/api/amount', {
        method: 'post',
        body: JSON.stringify({
            'report_type': choiceInfo.reportType,
            'month': choiceInfo.month,
            'quarter': choiceInfo.quarter,
            'year': choiceInfo.year
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(reportAmountData => {
        setPagination(reportAmountData['amount'], choiceInfo, pageInfo)
    })
}

// Gửi các thông tin cần thiết lên server để lấy thông tin report cho việc xuất pdf
function getExportReportData(choiceInfo) {
    fetch('/admin/report/api/all-data', {
        method: 'post',
        body: JSON.stringify({
            'report_type': choiceInfo.reportType,
            'month': choiceInfo.month,
            'quarter': choiceInfo.quarter,
            'year': choiceInfo.year,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(reportDatas => {
        if (reportDatas.length <= 0) {
            Swal.fire({
                title: 'Dữ liệu trống không thể xuất pdf. Vui lòng thử lại sau',
                icon: 'error',
                confirmButtonColor: '#3085d6',
                confirmButtonText: 'Ok',
            })
            return
        }
        getPdf(reportDatas)
    })
}

// Thiết lập phân trang
function setPagination(dataAmount, choiceInfo, pageInfo) {
    let page = ''
    let pageAmount = Math.ceil(dataAmount / pageInfo.pageSize)
    if (dataAmount <= pageInfo.pageSize) {
        $('#pagination').html(page)
        return
    }
    if (pageAmount != 1) {
        pageInfo.currentPage = 1
        $('#pagination').html('')
        page += `<li class="page-item" id ='previousItem'>
                <button class="page-link" onclick='setPrevious(${pageAmount})'><</button>
            </li>`
        for (let i = 1; i <= pageAmount; i++)
            page += `<li class="page-item ${i == 1 ? 'active' : ''}">
                    <button class="page-link" onclick='setPage(${i},${pageAmount})'>${i}</button>
                </li>`

        page += `<li class="page-item" id = 'nextItem'>
                <button class="page-link" onclick='setNext(${pageAmount}, ${dataAmount})'>></button>
            </li>`
        $('#pagination').html(page)
    }
}

// Xử lý nút trở về phía trước trong phân trang
function setPrevious(pageAmount) {
    if (gPageInfo.beginIndex - gPageInfo.pageSize >= 0) {
        $('#previousItem').show()
        gPageInfo.currentPage--;
        if (gPageInfo.currentPage == 1)
            $('#previousItem').hide()

        if (gPageInfo.currentPage == 1 && gPageInfo.currentPage != pageAmount)
            $('#nextItem').show()

        gPageInfo.beginIndex -= gPageInfo.pageSize
        gPageInfo.endIndex = gPageInfo.beginIndex + gPageInfo.pageSize
        getReportData(gChoiceInfo, gPageInfo)
    } else {
        $('#previousItem').hide()
    }
    $('#pagination').children().removeClass('active')
    $(`#pagination li:nth-child(${gPageInfo.currentPage + 1})`).addClass('active')
}

// Xử lý nút kế tiếp của phân trang
function setNext(pageAmount, dataAmount) {

    if (gPageInfo.beginIndex + gPageInfo.pageSize <= dataAmount) {
        $('#nextItem').show()
        gPageInfo.currentPage++;
        if (gPageInfo.currentPage == pageAmount)
            $('#nextItem').hide()
        if (gPageInfo.currentPage == pageAmount && gPageInfo.currentPage != 1)
            $('#previousItem').show()

        gPageInfo.beginIndex += gPageInfo.pageSize
        gPageInfo.endIndex = gPageInfo.beginIndex + gPageInfo.pageSize

        getReportData(gChoiceInfo, gPageInfo)
    } else {
        $('#nextItem').hide()
    }
    $('#pagination').children().removeClass('active')
    $(`#pagination li:nth-child(${gPageInfo.currentPage + 1})`).addClass('active')
}

// Xử lý khi chọn trang cụ thể
function setPage(itemIndex, pageAmount) {
    gPageInfo.currentPage = itemIndex
    if (itemIndex == pageAmount) {
        $('#nextItem').hide()
        if (itemIndex != 1)
            $('#previousItem').show()
    } else
        if (itemIndex == 1) {
            $('#previousItem').hide()
            if (itemIndex != pageAmount)
                $('#nextItem').show()
        } else {
            $('#previousItem').show()
            $('#nextItem').show()
        }
    gPageInfo.beginIndex = (itemIndex - 1) * gPageInfo.pageSize
    gPageInfo.endIndex = gPageInfo.beginIndex + gPageInfo.pageSize

    getReportData(gChoiceInfo, gPageInfo)
    $('#pagination').children().removeClass('active')
    $(`#pagination li:nth-child(${gPageInfo.currentPage + 1})`).addClass('active')
}

// Thiết lập dữ liệu các điều kiện tháng, quý, năm
function setTimeSelections() {
    var options = ''
    for (let i = 1; i <= 12; i++)
        options += `<option value=${i}>${i}</option>`
    $('#monthInput').html(options)
    options = ''
    for (let i = 1; i <= 4; i++)
        options += `<option value=${i}>${i}</option>`
    $('#quarterInput').html(options)
    options = ''
    for (let i = 2018; i <= 2100; i++)
        options += `<option value=${i}>${i}</option>`
    $('#yearInput').html(options)
}


// Thiết lập bảng dữ liệu báo cáo kết quả
function setReportDataTable(reportDatas) {

    if (reportDatas == undefined)
        return
    var headers = ''
    var rows = ''
    var total = ''

    $('#titleReportTable').html('')
    $('#reportDataTable').html('')
    $('#total').text('')

    sum = 0
    if ($('#reportType').val() == 'revenue') {
        headers += `<tr>
                            <th> ${'Số thứ tự'}</th>
                            <th> ${'Ngày bán'}</th>
                            <th> ${'Doanh thu'}</th>
                        </tr>`
        for (let i = 0; i < reportDatas.length; i++) {
            rows += `<tr>
                            <td>${i + 1}</td>
                            <td>${reportDatas[i]['ordered_date']}</td>
                            <td>${reportDatas[i]['revenue_total']}</td>
                    </tr>`
            sum += parseInt(reportDatas[i]['revenue_total'].substring(0,
                reportDatas[i]['revenue_total'].indexOf(' ')).replaceAll(',', ''))
        }
        total = `Tổng doanh thu: ${sum} VNĐ`
    }

    if ($('#reportType').val() == 'frequently_book_selling') {
        headers += `<tr>
                            <th> ${'Số thứ tự'}</th>
                            <th> ${'Tên sách'}</th>
                            <th> ${'Số lượng'}</th>
                        </tr>`
        for (let i = 0; i < reportDatas.length; i++) {
            rows += `<tr>
                            <td>${i + 1}</td>
                            <td>${reportDatas[i]['book_name']}</td>
                            <td>${reportDatas[i]['amount_total']}</td>
                    </tr>`
            sum += parseInt(reportDatas[i]['amount_total'])
        }
        total = `Tổng số lượng sách đã bán: ${sum}`
    }

    $('#titleReportTable').html(headers)
    $('#dataReportTable').html(rows)
    $('#total').text(total)

}

// Thiết lập vị trí ban đầu của trang
function setIndexPagination(pageInfo) {
    pageInfo.beginIndex = 0
    pageInfo.endIndex = pageInfo.beginIndex + pageInfo.pageSize
}

// Thiết lập giá trị khởi tạo lúc load trang lần đầu
function setInitialData(choiceInfo, pageInfo) {
    setTimeSelections()
    choiceInfo.month = parseInt($('#monthInput').val())
    choiceInfo.year = parseInt($('#yearInput').val())
    setIndexPagination(pageInfo)
    getReportData(choiceInfo, pageInfo)
    getAmountReportData(choiceInfo, pageInfo)
}

// Tái thiết lập dữ liệu khi đổi lựa chọn
function resetData(choiceInfo, pageInfo) {
    choiceInfo.reportType = $('#reportType').val() == undefined ?
        'revenue' : $('#reportType').val()
    setIndexPagination(pageInfo)
    getReportData(choiceInfo, pageInfo)
    getAmountReportData(choiceInfo, pageInfo)
}

// Xuất pdf
function getPdf(reportDatas) {
    const pdf = new jsPDF({
        orientation: 'landscape',
        format: 'a4',
        putOnlyUsedFonts: true,
        floatPrecision: 16
    })

    pdf.setFontSize(13)
    var head = []
    var body = []
    var foot = ''
    var sum = 0

    if ($('#reportType option:selected').val() == 'revenue') {
        head = ['STT', 'Ngay ban', 'Doanh thu']
        for (let i = 0; i < reportDatas.length; i++) {
            temp = []
            temp.push(i + 1)
            temp.push(reportDatas[i]['ordered_date'])
            temp.push(reportDatas[i]['revenue_total'])
            body.push(temp)
            sum += parseFloat(reportDatas[i]['revenue_total'].slice(0,
                reportDatas[i]['revenue_total'].length - 4).replaceAll(',', ''))
        }
        foot = `Tong doanh thu: ${sum} VND`
    }

    if ($('#reportType option:selected').val() == 'frequently_book_selling') {
        head = ['STT', 'Ten sach', 'So luong']
        for (let i = 0; i < reportDatas.length; i++) {
            temp = []
            temp.push(i + 1)
            temp.push(reportDatas[i]['book_name'])
            temp.push(reportDatas[i]['amount_total'] + ' cuon')
            body.push(temp)
            sum += parseInt(reportDatas[i]['amount_total'])
        }
        foot = `Tong so thuoc: ${sum}`
    }
    var time = ''
    if ($('#reportCondition').val().includes('month'))
        time = 'THANG'
    else
        if ($('#reportCondition').val().includes('quarter'))
            time = 'QUY'
        else
            time = 'NAM'
    if ($('#reportType').val().includes('revenue'))
        pdf.text(`BAO CAO DOANH THU THEO ${time}`, 110, 10)
    else
        pdf.text('BAO CAO TAN SUAT BAN SACH', 110, 10)

    pdf.autoTable({
        head: [head],
        body: body,
        startY: 30,
        theme: 'grid',
        styles: {
            font: 'Arial',
            fontStyle: 'normal',
        },
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
    pdf.setFontSize(15)

    pdf.text(foot, 20, pdf.lastAutoTable.finalY + 15)

    pdf.autoPrint({
        variant: 'non-conform'
    });

    pdf.save('report.pdf')
    Swal.fire({
        title: 'Xuất phiếu thành công',
        icon: 'success',
        confirmButtonColor: '#3085d6',
        confirmButtonText: 'Ok',
    })
}

$(document).ready(function () {
    setInitialData(gChoiceInfo, gPageInfo)

    $('#quarterSelection').hide()

    $('#reportType').change(function () {
        resetData(gChoiceInfo, gPageInfo)
    })

    $('#reportCondition').change(function () {
        if ($(this).val() == 'month_report') {
            $('#monthSelection').show()
            $('#quarterSelection').hide()
            gChoiceInfo.month = parseInt($('#monthInput').val())
            gChoiceInfo.quarter = null
        }

        if ($(this).val() == 'quarter_report') {
            $('#monthSelection').hide()
            $('#quarterSelection').show()
            gChoiceInfo.month = null
            gChoiceInfo.quarter = parseInt($('#quarterInput').val())
        }

        if ($(this).val() == 'year_report') {
            $('#monthSelection').hide()
            $('#quarterSelection').hide()
            gChoiceInfo.month = null
            gChoiceInfo.quarter = null
        }

        gChoiceInfo.year = parseInt($('#yearInput').val())
        resetData(gChoiceInfo, gPageInfo)
    })

    $('#monthInput').change(function () {
        gChoiceInfo.month = parseInt($(this).val())
        resetData(gChoiceInfo, gPageInfo)
    })

    $('#quarterInput').change(function () {
        gChoiceInfo.quarter = parseInt($(this).val())
        resetData(gChoiceInfo, gPageInfo)

    })

    $('#yearInput').change(function () {
        gChoiceInfo.year = parseInt($(this).val())
        resetData(gChoiceInfo, gPageInfo)
    })
    $('#exportPdf').click(function () {
        getExportReportData(gChoiceInfo)
    })
})


