(function () {
  'use strict'

  $(document).ready(function(){
    $(".add-to-wishlist").on('click', function(){
        var self = $(this);
        var bookId = self.data('id');
        $.ajax({
          type: 'POST',
          url: '/book/add-wishlist',
          contentType: 'application/json',
          data: JSON.stringify({ "book_id": bookId }),
        }).done(function (response) {
            if(response.success){
              //self.text('Added to wishlist');
              self.removeClass('btn-outline-success').addClass('disabled btn-danger');
            }
        }).fail(function (msg) {
            console.table(msg);
        });

    });
  });
  
})()
