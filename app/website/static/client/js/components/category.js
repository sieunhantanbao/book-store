$(document).ready(function(){
    var is_get_full_cats = $("#is_get_full_cats").val();
    $.ajax({
        type: 'GET',
        url:'/book/api/categories?all='+ is_get_full_cats,
        data: null,
        contentType: 'application/json'
      }).done(function(responses) {
            var cat_item_html = $("#category-item-template").html();
            var cat_items = $(".category-items");
            responses.forEach(element => {
                var cat_item_html_tmp = cat_item_html;
                cat_item_html_tmp = cat_item_html_tmp.replaceAll("@@category.slug@@", element.slug)
                                                    .replaceAll("@@category.thumbnail_url@@", element.thumbnail_url)
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