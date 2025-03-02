let gChartBackground = {
    backgroundColor: null
}

// Lấy thông tin thống kê tổng quan
function getGeneralStatistic() {
    fetch('/admin/home-page/api/general-statistic')
        .then(res => res.json()).then(generalStatisticData => {
            $('#bookAmount').text(generalStatisticData['book_amount'])
            $('#customerAmount').text(generalStatisticData['customer_amount'])
            $('#categoryAmount').text(generalStatisticData['category_amount'])
            $('#manufacturerAmount').text(generalStatisticData['manufacturer_amount'])
            $('#cartAmount').text(generalStatisticData['cart_amount'])
            $('#commentAmount').text(generalStatisticData['comment_amount'])
        })
}

// Lấy thông tin thống kê đơn hàng trong tháng
function getCartAmountInMonth(chartBackground) {
    fetch('/admin/home-page/api/cart-amount-month')
        .then(res => res.json()).then(cartAmount => {
            var chartInfo = {
                type: null,
                label: null,
                data: null,
                labels: null,
                backgroundColor: chartBackground.backgroundColor
            }
            setCartAmountInMonthChartData(cartAmount, chartInfo)
            setChart('amountCartChart', chartInfo)
        })
}

// Lấy thông tin thống kê doanh thu ngày hiện tại và ngày trước đó
function getRevenue(chartBackground) {
    fetch('/admin/home-page/api/revenue')
        .then(res => res.json()).then(revenue => {
            var chartInfo = {
                type: null,
                label: null,
                data: null,
                labels: null,
                backgroundColor: chartBackground.backgroundColor
            }
            setRevenueChartData(revenue, chartInfo)
            setChart('totalIncomeChart', chartInfo, isChangeBackground = false)
        })
}
// Lấy thông tin thống kê top các sách bán chạy nhất
function getTopBookSelling(chartBackground) {
    fetch('/admin/home-page/api/top-book')
        .then(res => res.json()).then(topBooks => {
            var chartInfo = {
                type: null,
                label: null,
                data: null,
                labels: null,
                backgroundColor: chartBackground.backgroundColor,
            }
            setTopBookSellingTableData(topBooks)
            setTopBookSellingChartData(topBooks, chartInfo)
            setChart('topBookChart', chartInfo)
        })
}

// Thiết lập cho chart dựa vào màu nên của trang web
function setBackgroundChart(chartBackground) {
    switch ($('body').attr('data-background-color')) {
        case 'bg1':
            chartBackground.backgroundColor = '#e0f7fa'; // Màu xanh nhạt
            break
        case 'bg2':
            chartBackground.backgroundColor = '#b2ebf2'; // Màu xanh nhạt hơn
            break
        case 'bg3':
            chartBackground.backgroundColor = '#80deea'; // Màu xanh đậm hơn
            break
        default:
            chartBackground.backgroundColor = '#009688'; // Màu xanh lam
    }
}

// Thiết lập dữ liệu cho biểu đồ doanh thu
function setRevenueChartData(revenue, chartInfo) {
    $('#todayRevenue').text(revenue['today_revenue'])
    $('#yesterdayRevenue').text(revenue['yesterday_revenue'])
    chartInfo.labels = ['Doanh thu hôm qua', 'Doanh thu hôm nay']
    chartInfo.data = []
    chartInfo.data.push(
        revenue['yesterday_revenue']
            .substring(0, revenue['yesterday_revenue'].indexOf(' '))
            .replaceAll(',', '')
    )
    chartInfo.data.push(
        revenue['today_revenue']
            .substring(0, revenue['today_revenue'].indexOf(' '))
            .replaceAll(',', '')
    )
    chartInfo.type = 'pie'
    chartInfo.label = 'Doanh thu'

}

// Thiết lập dữ liệu cho biểu đồ thống kê đơn hàng trong tháng
function setCartAmountInMonthChartData(cartAmount, chartInfo) {
    $('#month').text(cartAmount['month'])
    $('#year').text(cartAmount['year'])
    chartInfo.labels = cartAmount['days']
    chartInfo.data = cartAmount['datas']
    chartInfo.type = 'bar'
    chartInfo.label = `Tần suất đơn hàng trong tháng ${cartAmount['month']} / ${cartAmount['year']}`
}

// Thiết lập dữ liệu cho biểu đồ thống kê top sách bán chạy
function setTopBookSellingChartData(topBooks, chartInfo) {
    chartInfo.labels = []
    chartInfo.data = []
    for (let i = 0; i < topBooks.length; i++) {
        chartInfo.labels.push(topBooks[i]['book_name'])
        chartInfo.data.push(
            topBooks[i]['revenue_total']
                .substring(0, topBooks[i]['revenue_total'].indexOf(' '))
                .replaceAll(',', '')
        )
    }
    chartInfo.type = 'polarArea'
    chartInfo.label = 'Các loại sách bán chạy nhất'
}

function setTopBookSellingTableData(topBooks) {
    var rows = ''
    for (let i = 0; i < topBooks.length; i++) {
        var image = topBooks[i]['book_image']
        if (image == null || image.length == 0)
            image = 'https://res.cloudinary.com/attt92bookstore/image/upload/v1646019055/book/book_qmruxn.jpg'
        rows += ` <div class='d-flex pt-2 pl-3 pr-3'>
                    <div class='avatar'>
                        <img src=${image}
                            alt='book' class='avatar-img rounded-circle'>
                    </div>
                    <div class='flex-1 pt-1 ml-2'>
                        <h5 class='fw-bold mb-1'>${topBooks[i]['book_name']}</h5>
                        <small class='text-muted'>${topBooks[i]['category_name']}</small>
                        <small class='text-muted d-block' >${topBooks[i]['manufacturer_name']}</small>
                    </div>
                    <div class='d-flex ml-auto align-items-center'>
                        <span class='text-info fw-bold'>${topBooks[i]['revenue_total']}</span>
                    </div>
                </div>
                <div class='separator-dashed'></div>`
    }
    $('#topBookTable').html(rows)
}


// Tạo chart
function setChart(elementId, chartInfo, isChangeBackground = true) {
    var backgroundColor = ['#F25961', '#31CE36']
    var borderColor = ['#F25961', '#31CE36']
    if (isChangeBackground)
        for (let i = 0; i < chartInfo.data.length; i++) {
            r = Math.floor(Math.random() * 255 + 1)
            g = Math.floor(Math.random() * 255 + 1)
            b = Math.floor(Math.random() * 255 + 1)
            backgroundColor.push(`rgba(${r},${g}, ${b}, 0.7)`)
            borderColor.push(`rgba(${r},${g}, ${b}, 1)`)
        }

    for (let i = 0; i < $('.chart-container canvas').length; i++)
        if ($('.chart-container canvas')[i].id == elementId) {
            $('.chart-container')[i].innerHTML = `<canvas id='${elementId}'></canvas>`
            break
        }
    const ctx = document.getElementById(elementId).getContext('2d')

    const bgColorPDF = {
        id: "bgColorPDF",
        beforeDraw: (chart) => {
            const {
                ctx,
                width,
                height
            } = chart;
            ctx.fillStyle = chartInfo.backgroundColor;
            ctx.fillRect(0, 0, width, height);
            ctx.restore();
        },
    }
    new Chart(ctx, {
        type: chartInfo.type,
        data: {
            labels: chartInfo.labels,
            datasets: [{
                label: chartInfo.label,
                data: chartInfo.data,
                backgroundColor: backgroundColor,
                borderColor: borderColor,
                borderWidth: 1,
            },],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
        plugins: [bgColorPDF],
    })
}

$(document).ready(function () {

    setBackgroundChart(gChartBackground)
    getGeneralStatistic()
    getCartAmountInMonth(gChartBackground)
    getRevenue(gChartBackground)
    getTopBookSelling(gChartBackground)

    $('.changeBackgroundColor').click(function () {
        setBackgroundChart(gChartBackground)
        getCartAmountInMonth(gChartBackground)
        getRevenue(gChartBackground)
        getTopBookSelling(gChartBackground)
    })
})