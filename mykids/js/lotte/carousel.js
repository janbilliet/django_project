var totalItems = $('.item').length;
var currentIndex = $('div.active').index() + 1;
$('.num').html(''+currentIndex+'/'+totalItems+'');

$('#myCarousel').carousel({
    interval: 2000
});

$('#myCarousel').on('slide.bs.carousel', function() {
    currentIndex = $('div.active').index() + 1;
   $('.num').html(''+currentIndex+'/'+totalItems+'');
});