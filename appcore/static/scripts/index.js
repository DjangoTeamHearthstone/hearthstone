var path = window.location.pathname
if(path === '/tableau-de-bord/') {
    $("#return").css('display', 'none')
    $("#logout").css('display', 'auto')
} else {
    $("#return").css('display', 'auto')
    $("#logout").css('display', 'none')
}

// if(path === '/' || path === '/connexion/' || path === '/inscription/') {
//     $("#header").css('display', 'none')
// } else {
//     $("#header").css('display', 'block')
// }

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