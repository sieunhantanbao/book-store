(function () {
  'use strict'

  $(document).ready(function(){
    
    $(".add-to-wishlist").on('click', function(){
      var self = $(this);
      var bookId = self.data('id');
      $.ajax({
        type: 'POST',
        url: '/book/api/add-wishlist',
        contentType: 'application/json',
        data: JSON.stringify({ "book_id": bookId }),
      }).done(function (response) {
          if(response.success){
            self.removeClass('btn-outline-success').addClass('disabled btn-danger');
          }else{
            window.location.href = '/auth/login';
          }
      }).fail(function (msg) {
          console.error(msg);
          window.location.href = '/auth/login';
        });
    });

    $(".remove-from-wishlist").on('click', function(){
        var self = $(this);
        var bookId = self.data('id');
        $.ajax({
          type: 'POST',
          url: '/book/api/remove-wishlist',
          contentType: 'application/json',
          data: JSON.stringify({ "book_id": bookId }),
        }).done(function (response) {
            if(response.success){
              self.parent().parent().parent().parent().remove();
            }else{
              window.location.href = '/auth/login';
            }
        }).fail(function (msg) {
            console.error(msg);
            window.location.href = '/auth/login';
        });
    });
  });
  
})()
