(function () {
  'use strict'

  $(document).ready(function(){
    var htmlTemplate = $('div#popover-template').html();
    $('[data-toggle="popover"]').on('click', function(){
      var self = this;
      var popoverInstance = bootstrap.Popover.getInstance(self);
      if (popoverInstance) {
          popoverInstance.show();
      } else {
        var star_rating_div = $(self).clone();
        star_rating_div.find('div.score').remove();
        var star_rating_html = star_rating_div.html();
        var book_id = $(self).data('id');
        $.ajax({
          type: 'GET',
          url:'/book/api/star_rating_statistic/' + book_id,
          data: null,
          contentType: 'application/json'
        }).done(function(response) {
            if(response.success){
                popoverInstance = new bootstrap.Popover(self, {
                  html: true,
                  trigger: 'manual',
                  content: fillRatingTemplate(htmlTemplate, star_rating_html, book_id, response.data)
                });
                popoverInstance.show();
                // Close popover on click outside the button
                document.addEventListener('click', function (event) {
                    var isClickInsideButton = self.contains(event.target);
                    if (!isClickInsideButton) {
                        var popoverInstance = bootstrap.Popover.getInstance(self);
                        if (popoverInstance) {
                            popoverInstance.hide();
                        }
                    }
                });
            }else{
              console.error('Error while fetching data');
            }
        }).fail(function(msg){
            console.error(msg);
        });
      }
    });

    loadStarRatingDetail();
});

function fillRatingTemplate(html, start_rating_html, book_id, data){
  html = html.replaceAll("#star_rating#", start_rating_html)
            .replaceAll("#book_id#", book_id)
            .replaceAll("#progress_bar_1#", data.total_ratings> 0? Math.round((data.total_rating_1/data.total_ratings)*100): 0)
            .replaceAll("#progress_bar_2#", data.total_ratings> 0? Math.round((data.total_rating_2/data.total_ratings)*100): 0)
            .replaceAll("#progress_bar_3#", data.total_ratings> 0? Math.round((data.total_rating_3/data.total_ratings)*100): 0)
            .replaceAll("#progress_bar_4#", data.total_ratings> 0? Math.round((data.total_rating_4/data.total_ratings)*100): 0)
            .replaceAll("#progress_bar_5#", data.total_ratings> 0? Math.round((data.total_rating_5/data.total_ratings)*100): 0)
            .replaceAll("#progress_percent_1#", data.total_ratings> 0? (data.total_rating_1 >0? ((data.total_rating_1/data.total_ratings)*100).toFixed(1) + "%":""):"")
            .replaceAll("#progress_percent_2#", data.total_ratings> 0? (data.total_rating_2 >0? ((data.total_rating_2/data.total_ratings)*100).toFixed(1) + "%":""):"")
            .replaceAll("#progress_percent_3#", data.total_ratings> 0? (data.total_rating_3 >0? ((data.total_rating_3/data.total_ratings)*100).toFixed(1) + "%":""):"")
            .replaceAll("#progress_percent_4#", data.total_ratings> 0? (data.total_rating_4 >0? ((data.total_rating_4/data.total_ratings)*100).toFixed(1) + "%":""):"")
            .replaceAll("#progress_percent_5#", data.total_ratings> 0? (data.total_rating_5 >0? ((data.total_rating_5/data.total_ratings)*100).toFixed(1) + "%":""):"")
            .replaceAll("#total_vote_1#", data.total_rating_1)
            .replaceAll("#total_vote_2#", data.total_rating_2)
            .replaceAll("#total_vote_3#", data.total_rating_3)
            .replaceAll("#total_vote_4#", data.total_rating_4)
            .replaceAll("#total_vote_5#", data.total_rating_5)
            .replaceAll("#total_global_ratings#", data.total_ratings)
            .replaceAll("#average_rating#", data.average_rating.toFixed(2));
  return html;
}

function loadStarRatingDetail(){
  var rating_detail_div = $('div#rating_detail');
  console.log(rating_detail_div.html())
  var book_id = $('[data-toggle="popover"]').data('id');
  var star_rating_html = $('[data-toggle="popover"]').clone();
  star_rating_html.find('div.score').remove();
  var star_rating_html_final = star_rating_html.html();
  if(rating_detail_div.length > 0){
    $.ajax({
      type: 'GET',
      url:'/book/api/star_rating_statistic/' + book_id,
      data: null,
      contentType: 'application/json'
    }).done(function(response) {
        if(response.success){
          var filledHtml = fillRatingTemplate(rating_detail_div.html(), star_rating_html_final, book_id, response.data);
          rating_detail_div.html(filledHtml);
        }else{
          console.error('Error while fetching data');
        }
    }).fail(function(msg){
        console.error(msg);
    });
  }
}

  $(function() {
    $('.custom-star').click(function() {
      $(this).children('.selected').addClass('is-animated');
      $(this).children('.selected').addClass('pulse');
      var target = this;
      setTimeout(function() {
        $(target).children('.selected').removeClass('is-animated');
        $(target).children('.selected').removeClass('pulse');
      }, 1000);
    })
    $('.star-full').click(function() {
      setFullStarState(this);
    })

    $("input#submit-review").click(function(){
      var self = $(this);
      var book_id = $("#hdf_book_id").val();
      var rating_value = $("#hdf_rating_value").val();
      var rating_value_int = parseInt(rating_value);
      $("#book-review-form-message").text('');
      $("#book-review-form-message").removeClass("text-danger text-success");
      if(rating_value_int == NaN || rating_value_int < 1 || rating_value_int > 5){
        $("#book-review-form-message").addClass("text-danger");
        $("#book-review-form-message").text("Invalid rating value");
        return;
      }
      var review_comment = $("#customer_review").val();
      $.ajax({
        type: 'POST',
        url: '/book/api/add-review',
        contentType: 'application/json',
        data: JSON.stringify({ "book_id": book_id, "rating_value": rating_value, "review_comment": review_comment }),
      }).done(function (response) {
          if(response.success){
            $('input#submit-review').addClass('disabled');
            $("#book-review-form-message").addClass("text-success");
            $("#book-review-form-message").text("Thank you for your valuable feedback. We'll review and populate it later.");
          }else{
           // window.location.href = '/auth/login';
          }
      }).fail(function (msg) {
          // window.location.href = '/auth/login';
          alert('Failed');
      });
    });
  })

  function updateStarState(target) {
    $(target).parent().prevAll().addClass('animate');
    $(target).parent().prevAll().children().addClass('star-colour');
    $(target).parent().nextAll().removeClass('animate');
    $(target).parent().nextAll().children().removeClass('star-colour');
  }

  function setFullStarState(target) {
    $(target).addClass('star-colour');
    $(target).parent().addClass('animate');
    updateRating(target);
  }

  function updateRating(target) {
    updateStarState(target);
    $('input#submit-review').removeClass('disabled');
    var rating_value = $(target).data('value');
    $("#hdf_rating_value").val(rating_value);
  }

})()
