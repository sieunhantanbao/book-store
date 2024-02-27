$(document).ready(function(){
    $.ajax({
        type: 'GET',
        url:'/book/api/featured-books',
        data: null,
        contentType: 'application/json'
      }).done(function(responses) {
           var carousel_indicators_template = $("#book-carousel-indicators-template").html();
           var carousel_inner_template = $("#book-carousel-inner-template").html();
           var carousel_indicators = $("#book-carousel-indicators");
           var carousel_inner = $("#book-carousel-inner");
           var featured_books_carousel_img_bg = $("#featured-books-carousel-img-bg");
            responses.forEach((element, index) => {
                let new_index = index + 1;

                var style = `<style>
                                .carousel-item:nth-child(@@index@@) {
                                background-image: url('data:image/gif;base64, @@featured_book.thumbnail@@');
                                background-repeat: no-repeat;
                                background-size: cover;
                                background-position: center center;
                                }
                            </style>`;
                style = style.replaceAll("@@index@@", new_index)
                             .replaceAll("@@featured_book.thumbnail@@", element.thumbnail);
                featured_books_carousel_img_bg.append(style);


                var carousel_indicators_template_temp = carousel_indicators_template;
                if(new_index > 1){
                    carousel_indicators_template_temp = carousel_indicators_template_temp.replaceAll("@@slideIndexMinus1@@", new_index - 1)
                            .replaceAll("@@slideIndex@@", new_index)
                            .replaceAll("@@isActive@@", "")
                            .replaceAll("@@isAriaCurrent@@","");
                }else{
                    carousel_indicators_template_temp = carousel_indicators_template_temp.replaceAll("@@slideIndexMinus1@@", 0)
                            .replaceAll("@@slideIndex@@", 1)
                            .replaceAll("@@isActive@@", "active")
                            .replaceAll("@@isAriaCurrent@@","true");
                }
                carousel_indicators.append(carousel_indicators_template_temp);

                var carousel_inner_template_temp = carousel_inner_template;
                carousel_inner_template_temp = carousel_inner_template_temp.replaceAll("@@isActive@@", index == 0?"active":"")
                            .replaceAll("@@featured_book.title@@", element.title)
                            .replaceAll("@@featured_book.short_description@@", element.short_description)
                            .replaceAll("@@featured_book.slug@@", element.slug)
                carousel_inner.append(carousel_inner_template_temp);
            });
            var myCarousel = document.querySelector('#carouselBookFeatured');
            new bootstrap.Carousel(myCarousel);
      }).fail(function(msg){
          console.error(msg);
      }).always(function(){
        $('#featured-book-loading-icon').hide();
      });
})