(function () {
  'use strict'

  $(document).ready(function(){
    $(".remove-from-wishlist").on('click', function(){
        var self = $(this);
        var bookId = self.data('id');
        debugger;
        $.ajax({
          type: 'POST',
          url: '/book/remove-wishlist',
          contentType: 'application/json',
          data: JSON.stringify({ "book_id": bookId }),
        }).done(function (response) {
            if(response.success){
              self.parent().parent().parent().parent().remove();
            }
        }).fail(function (msg) {
            console.table(msg);
        });
    });
  });
  
})()
