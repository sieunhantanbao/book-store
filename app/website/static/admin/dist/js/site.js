$(function(){
    $(".btn-image-delete").on("click", function(e){
        debugger;
        e.preventDefault();
        var self = $(this);
        var image_id = self.data('id');
        if (image_id){
            $.ajax({
                type: 'DELETE',
                url:'/admin/category/api/image/remove/' + image_id,
                data: null,
                contentType: 'application/json'
              }).done(function(responses) {
                    if(responses){
                        self.parent(".image-item").remove();
                    }
              }).fail(function(msg){
                  console.error(msg);
              });
        }
    })
})