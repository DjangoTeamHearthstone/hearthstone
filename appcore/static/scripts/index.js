var path = window.location.pathname
if(path === '/tableau-de-bord/') {
    $("#return").css('display', 'none')
    $("#logout").css('display', 'auto')
} else {
    $("#return").css('display', 'auto')
    $("#logout").css('display', 'none')
}

// body style register, welcome, login
if(path === '/' || path === '/inscription/' || path === '/connexion/') {
    $('body').css('display', 'flex')
    $('body').css('height', '100%')
} else {
    $('body').css('display', 'auto')
    $('body').css('height', 'auto')
}

// btn
var width_btn = 176
$('button').mouseleave(function() {
    $(this).css('background-position', 0)
})
$('button').mouseenter(function() {
    $(this).css('background-position', (width_btn * -1))
})
$('button').mouseup(function() {
    $(this).css('background-position', (width_btn * -1))
})
$('button').mousedown(function() {
    $(this).css('background-position', (width_btn * -2))
})

// small_btn
var width_towelcome_btn = 155
$('.small_btn').mouseleave(function() {
    $(this).css('background-position', 0)
})
$('.small_btn').mouseenter(function() {
    $(this).css('background-position', (width_towelcome_btn * -1))
})
$('.small_btn').mouseup(function() {
    $(this).css('background-position', (width_towelcome_btn * -1))
})
$('.small_btn').mousedown(function() {
    $(this).css('background-position', (width_towelcome_btn * -2))
})
$('.panel').mouseleave(function() {
    $(this).find('.small_btn').css('background-position', 0)
})
$('.panel').mouseenter(function() {
    $(this).find('.small_btn').css('background-position', (width_towelcome_btn * -1))
})

// checkbox
$("input[type='checkbox']").on('mouseenter', function() {
    $(this).css('background-position', '-25px')
})
$("input[type='checkbox']").on('mouseleave', function() {
    if($(this).attr('checked')) {
        $(this).css('background-position', '-75px')
    } else {
        $(this).css('background-position', '0px')
    }
})
$("input[type='checkbox']").on('mousedown', function() {
    $(this).css('background-position', '-50px')
})
$("input[type='checkbox']").on('click',function(){
    if($(this).attr('checked')) {
        $(this).removeAttr('checked')
        $(this).css('background-position', '0')
    } else {
        $(this).attr('checked', true)
        $(this).css('background-position', '-75px')
    }
})