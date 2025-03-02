$(function () {
    $('.block-product').slick({
        dots: false,
        infinite: false,
        autoplay: true,
        autoplaySpeed: 3000,
        speed: 300,
        slidesToShow: 5,
        slidesToScroll: 1,
        responsive: [{
            breakpoint: 1200,
            settings: {
                slidesToShow: 3,
                slidesToScroll: 1,
                infinite: true,
                dots: true
            }
        },
        {
            breakpoint: 800,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 1
            }
        },
        {
            breakpoint: 480,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1
            }
        }
        ]
    });

    //hieu ung header va nut backtotop
    $("#backtotop").click(function () {
        $("html, body").animate({
            scrollTop: 0
        }, 400);
    });

    $(window).scroll(function () {
        if ($("body,html").scrollTop() > 150) {
            $(".navbar").addClass("fixed-top");
        } else {
            $(".navbar").removeClass("fixed-top");
        }
    });

    $(window).scroll(function () {
        if ($("body,html").scrollTop() > 400) {
            $(".scroll-up").addClass("show");
        } else {
            $(".scroll-up").removeClass("show");
        }
    });

    // header form dangnhap dangky
    $(".btn-login").click(function (e) {
        $("ul.tabs .login-tab").addClass("active");
    });
    $(".btn-register").click(function (e) {
        $("ul.tabs .register-tab").addClass("active");
    });

    $("ul.tabs .login-tab").click(function (e) {
        $("ul.tabs .login-tab").addClass("active");
        $("ul.tabs .register-tab").removeClass("active");
    });

    $("ul.tabs .register-tab").click(function (e) {
        $("ul.tabs .register-tab").addClass("active");
        $("ul.tabs .login-tab").removeClass("active");
    });

    // form dangnhap dangky 
    $(".register-tab").click(function (e) {
        $('#login-form').removeClass("fade");
        $('#register-form').removeClass("fade");
        $('#login-form').modal("hide");
        $('#register-form').modal("show");
    });
    $(".login-tab").click(function (e) {
        $('#login-form').removeClass("fade");
        $('#register-form').removeClass("fade");
        $('#register-form').modal("hide");
        $('#login-form').modal("show");
    });
    $(".close").click(function (e) {
        $('.modal').addClass("fade");
        $("ul.tabs .login-tab").removeClass("active");
        $("ul.tabs .register-tab").removeClass("active");
    });

    $("#book-list-btn").click(function (e) {
        $(".category-content").toggleClass("show");
    });

    // thumb-img
    $(".thumb-img.thumb1").addClass('vienvang');
    $('.thumb-img').click(function (e) {
        $('.product-image').attr('src', this.src);
    });

    $('.thumb-img').click(function (e) {
        $('.thumb-img:not(:hover)').removeClass('vienvang');
        $(this).addClass('vienvang');
    });

    //btn-spin
    $(".btn-inc").click(function (e) {
        var strval = $(this).parent().prev().val();
        var val = parseInt(strval) + 1;
        $(this).parent().prev().attr('value', val);
    });
    $(".btn-dec").click(function (e) {
        var strval = $(this).parent().next().val();
        var val = parseInt(strval) - 1;
        if (val < 1) {
            $(this).parent().next().attr('value', 1);
        } else {
            $(this).parent().next().attr('value', val);
        }
    });

    // gui danh gia
    $(".vote-form").hide(200);
    $(".write-form").click(function (e) {
        $(".vote-form").toggle(200);
    });

    //rotate chevron
    $('#step1contentid').on('show.bs.collapse', function () {
        $(this).prev().addClass("active");
    })
    $('#step1contentid').on('hide.bs.collapse', function () {
        $(this).prev().removeClass("active");
    })
    $('#step2contentid').on('show.bs.collapse', function () {
        $(this).prev().addClass("active");
    })
    $('#step2contentid').on('hide.bs.collapse', function () {
        $(this).prev().removeClass("active");
    })
    $('#step3contentid').on('show.bs.collapse', function () {
        $(this).prev().addClass("active");
    })
    $('#step3contentid').on('hide.bs.collapse', function () {
        $(this).prev().removeClass("active");
    })

    // nut btn-shopping-without-signup
    $("#step1contentid").collapse('show');
    $(".btn-shopping-without-signup").click(function (e) {
        $("#step1contentid").collapse('hide');
        $("#step2contentid").collapse('show');
    });

    // validate
    $("#form-signup").validate({
        rules: {
            last_name: {
                required: true,
            },
            first_name: {
                required: true,
            },
            dateOfBirth: {
                required: true,
            },
            address: {
                required: true,
            },
            phone: {
                required: true,
                minlength: 10,
                maxlength: 10,
            },
            username: {
                required: true,
            },
            password: {
                required: true,
                minlength: 6
            },
            confirm_password: {
                required: true,
                minlength: 6,
                equalTo: "#inputPassword"
            },
            email: {
                required: true,
                email: true
            }
        },
        messages: {
            last_name: {
                required: "Vui lòng nhập họ",
            },
            first_name: {
                required: "Vui lòng nhập tên",
            },
            dateOfBirth: {
                required: "Vui lòng nhập ngày sinh",
            },
            address: {
                required: "Vui lòng nhập địa chỉ",
            },
            phone: {
                required: "Vui lòng nhập số điện thoại",
                minlength: "Số máy quý khách vừa nhập là số không có thực",
                maxlength: "Vui lòng nhập đúng 10 kí tự"
            },
            username: {
                required: "Vui lòng nhập tên tài khoản",
            },
            password: {
                required: 'Vui lòng nhập mật khẩu',
                minlength: 'Vui lòng nhập ít nhất 6 kí tự'
            },
            confirm_password: {
                required: 'Vui lòng nhập lại mật khẩu',
                minlength: 'Vui lòng nhập ít nhất 6 kí tự',
                equalTo: 'Mật khẩu không trùng'
            },
            email: {
                required: "Vui lòng nhập email",
                minlength: "Email không hợp lệ",
                email: "Vui lòng nhập email",
            }
        }
    });

    // $("#form-signin").validate({
    //     rules: {
    //         password: {
    //             required: true,
    //             minlength: 6
    //         },
    //         email: {
    //             required: true,
    //             email: true
    //         }
    //     },
    //     messages: {
    //         password: {
    //             required: 'Vui lòng nhập mật khẩu',
    //             minlength: 'Vui lòng nhập ít nhất 6 kí tự'
    //         },
    //         email: {
    //             required: "Vui lòng nhập email",
    //             minlength: "Email không hợp lệ",
    //             email: "Vui lòng nhập email",
    //         }
    //     }
    // });

    $("#form-signup-cart").validate({
        rules: {
            name: {
                required: true,
            },
            phone: {
                required: true,
                minlength: 8
            },
            password: {
                required: true,
                minlength: 6
            },
            confirm_password: {
                required: true,
                minlength: 6,
                equalTo: "#inputPassword"
            },
            email: {
                required: true,
                email: true
            }
        },
        messages: {
            name: {
                required: "Vui lòng nhập họ và tên",
            },
            phone: {
                required: "Vui lòng nhập số điện thoại",
                minlength: "Số máy quý khách vừa nhập là số không có thực"
            },
            password: {
                required: 'Vui lòng nhập mật khẩu',
                minlength: 'Vui lòng nhập ít nhất 6 kí tự'
            },
            confirm_password: {
                required: 'Vui lòng nhập lại mật khẩu',
                minlength: 'Vui lòng nhập ít nhất 6 kí tự',
                equalTo: 'Mật khẩu không trùng'
            },
            email: {
                required: "Vui lòng nhập email",
                minlength: "Email không hợp lệ",
                email: "Vui lòng nhập email",
            }
        }
    });

    $("#form-signin-cart").validate({
        rules: {
            password: {
                required: true,
                minlength: 6
            },
            email: {
                required: true,
                email: true
            }
        },
        messages: {
            password: {
                required: 'Vui lòng nhập mật khẩu',
                minlength: 'Vui lòng nhập ít nhất 6 kí tự'
            },
            email: {
                required: "Vui lòng nhập email",
                minlength: "Email không hợp lệ",
                email: "Vui lòng nhập email",
            }
        }
    })

    $('.items .row').isotope({
        itemSelector: '.item',
    })

    $('.tag a').click(function (e) {
        var author = $(this).data('author');

        if (author == 'all') {
            $('.items .row').isotope({
                filter: '*'
            })
        } else {
            $('.items .row').isotope({
                filter: author
            });
        }
        return false;
    });

    $('.thay-doi-mk').hide();
    $("#changepass").click(function (e) {
        $('.thay-doi-mk').toggle(200);
    });

});

// init cursor
var cursors = [{
    cursor_id: "3",
    cursor_type: "0",
    cursor_shape: "15",
    cursor_image: "",
    default_cursor: "auto",
    hover_effect: "plugin",
    body_activation: "1",
    element_activation: "0",
    selector_type: "tag",
    selector_data: "body",
    color: "#cc3a3b",
    width: "30",
    blending_mode: "normal"
}];

function getCartDetailAmount() {
    fetch('/gio-hang/api/amount-book').then(res => res.json()).then(result => {
        $('#cartDetailAmount').text(result['amount'])
    })
}

getCartDetailAmount()

$('#form-signup').on('submit', function (e) {
    e.preventDefault(); // Now nothing will happen
});

// Show Password
function showPassword(button) {
    var inputPassword = $(button).parent().find('input');
    if (inputPassword.attr('type') === "password") {
        inputPassword.attr('type', 'text');
        $(".show-password i").removeClass("far fa-eye");
        $(".show-password i").addClass("far fa-eye-slash");
    } else {
        inputPassword.attr('type', 'password');
        $(".show-password i").removeClass("far fa-eye-slash");
        $(".show-password i").addClass("far fa-eye");
    }
}

$('.show-password').on('click', function () {
    showPassword(this);
})
$('#bookSearchBtn').on('click', function () {
    var query = $('#bookTitleInput').val().trim(); // Lấy giá trị từ trường nhập liệu

    if (query) {
        // Chuyển hướng đến trang tìm kiếm với từ khóa
        window.location.href = '/search?query=' + encodeURIComponent(query);
    } else {
        Swal.fire({
            title: 'Vui lòng nhập tên sách!',
            icon: 'warning',
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Ok',
        });
    }
});
