$(document).ready(function(){
    $.ajax({
        type: 'GET',
        url:'/book/categories?all=false',
        data: null,
        contentType: 'application/json'
      }).done(function(responses) {
            var cat_item_html = $("#category-item-template").html();
            var cat_items = $(".category-items");
            responses.forEach(element => {
                var cat_item_html_tmp = cat_item_html;
                cat_item_html_tmp = cat_item_html_tmp.replaceAll("@@category.id@@", element.id)
                                                    .replaceAll("@@category.thumbnail@@", element.thumbnail)
                                                    .replaceAll("@@category.name@@", element.name)
                                                    .replaceAll("@@category.short_description@@", element.short_description)

                cat_items.append(cat_item_html_tmp);
            });
      }).fail(function(msg){
          console.error(msg);
      }).always(function(){
        $('#cat-loading-icon').hide();
      });
})