(function () {
  'use strict'

  $(function() {
    $('.star').click(function() {
      $(this).children('.selected').addClass('is-animated');
      $(this).children('.selected').addClass('pulse');
      var target = this;
      setTimeout(function() {
        $(target).children('.selected').removeClass('is-animated');
        $(target).children('.selected').removeClass('pulse');
      }, 1000);
    })
    $('.half').click(function() {
      setHalfStarState(this);
      $(this).closest('.rating').find('.js-score').text($(this).data('value'));
      $(this).closest('.rating').data('vote', $(this).data('value'));
    })
    $('.full').click(function() {
      setFullStarState(this);
      $(this).closest('.rating').find('.js-score').text($(this).data('value'));
      $(this).find('js-average').text(parseInt($(this).data('value')));
      $(this).closest('.rating').data('vote', $(this).data('value'));
    })
  })

  function updateStarState(target) {
    $(target).parent().prevAll().addClass('animate');
    $(target).parent().prevAll().children().addClass('star-colour');
    $(target).parent().nextAll().removeClass('animate');
    $(target).parent().nextAll().children().removeClass('star-colour');
  }

  function setHalfStarState(target) {
    $(target).addClass('star-colour');
    $(target).siblings('.full').removeClass('star-colour');
    updateRating(target);
  }

  function setFullStarState(target) {
    $(target).addClass('star-colour');
    $(target).parent().addClass('animate');
    $(target).siblings('.half').addClass('star-colour');
    updateRating(target);
  }

  function updateRating(target) {
    var rating_value = $(target).data('value');
    var book_id = $(target).parents('div.rating').data('id');
    $.ajax({
      type: 'POST',
      url: '/book/add-rating',
      contentType: 'application/json',
      data: JSON.stringify({ "book_id": book_id, "rating_value": rating_value }),
    }).done(function (response) {
        if(response.success){
          updateStarState(target);
          updateAverageRating(target, response.average_rating);
        }
    }).fail(function (msg) {
        console.table(msg);
    });
  }

  function updateAverageRating(target, average_rating) {
    $(target).parents('div.rating').find('div.score').find('span.js-score').text(average_rating);
  }

})()
