(function () {
    'use strict'
    var optSimple = {
      format: 'mm-dd-yyyy',
      todayHighlight: true,
      orientation: 'bottom right',
      autoclose: true,
      container: '#sandbox'
    };
  
    $('.datetime-picker').datepicker(optSimple);

    $('#book_description').summernote(
        {
        height: 150,
        focus: true
      });

    $("#frmCreateBook").validate({
      rules: {
        title: {
            required: true,
        },
        short_description: {
            required: true,
        },
        category_id: {
            required: true,
        },
        price: {
            required: true,
            min: 0,
            number: true,
        },
        isbn: {
            required: true
        },
        author: {
            required: true
        },
        pages: {
            required: true,
            min: 0,
            number: true,
        }
      },
      messages: {
        title: "Book title is required",
        short_description: "Short description is required",
        category_id: "Category is required",
        price: {
            required: "Price is required",
            min: "Price must be greater or equal 0",
            number: "Price should be a number",
        },
        isbn: "ISBN is required",
        author: "Author is required",
        pages: {
            required: "Total pages is required",
            min: "Total pages must be greater or equal 0",
            number: "Total pages should be a number",
        }
      }
    });

    Dropzone.options.frmCreateBook = {
        autoProcessQueue: false,
        uploadMultiple: true,
        maxFilesize: 2, // MB
        acceptedFiles: 'image/*', // Allow only image files
        addRemoveLinks: true, // Add remove links to uploaded files
        parallelUploads: 100,
        maxFiles: 5,
        // The setting up of the dropzone
        init: function() {
            var myDropzone = this;
            // First change the button to actually tell Dropzone to process the queue.
            $(":submit").click(function(e){
                 if($("#frmCreateBook").valid()){
                    if ($("#isFileAdded").val() == "true"){
                        e.preventDefault();
                        e.stopPropagation();
                        myDropzone.processQueue();
                    }
                 }
            });
            this.on("addedfile", function(file) { 
                $("#isFileAdded").val("true");
            });
            this.on("removedfile", function(file) { 
                $("#isFileAdded").val("false");
            });
            // Listen to the sendingmultiple event. In this case, it's the sendingmultiple event instead
            // of the sending event because uploadMultiple is set to true.
            this.on("sendingmultiple", function()  {
                // Append all form inputs to the formData Dropzone will POST
            });
            this.on("successmultiple", function(files, response) {
            // Gets triggered when the files have successfully been sent.
            // Redirect user or notify of success.
               window.location.href = '/admin/book';
            });
            this.on("errormultiple", function(files, response) {
            // Gets triggered when there was an error sending the files.
            // Maybe show form again, and notify user of error
            });
        }
    };

    $("#frmEditBook").validate({
      rules: {
        title: {
            required: true,
        },
        short_description: {
            required: true,
        },
        category_id: {
            required: true,
        },
        price: {
            required: true,
            min: 0,
            number: true,
        },
        isbn: {
            required: true
        },
        author: {
            required: true
        },
        pages: {
            required: true,
            min: 0,
            number: true,
        }
      },
      messages: {
        title: "Book title is required",
        short_description: "Short description is required",
        category_id: "Category is required",
        price: {
            required: "Price is required",
            min: "Price must be greater or equal 0",
            number: "Price should be a number",
        },
        isbn: "ISBN is required",
        author: "Author is required",
        pages: {
            required: "Total pages is required",
            min: "Total pages must be greater or equal 0",
            number: "Total pages should be a number",
        }
      }
    });

    Dropzone.options.frmEditBook = {
      autoProcessQueue: false,
      uploadMultiple: true,
      maxFilesize: 2, // MB
      acceptedFiles: 'image/*', // Allow only image files
      addRemoveLinks: true, // Add remove links to uploaded files
      parallelUploads: 100,
      maxFiles: 5,
      // The setting up of the dropzone
      init: function() {
          var myDropzone = this;
          // First change the button to actually tell Dropzone to process the queue.
          $(":submit").click(function(e){
               if($("#frmEditBook").valid()){
                if ($("#isFileAdded").val() == "true"){
                    e.preventDefault();
                    e.stopPropagation();
                    myDropzone.processQueue();
                }
               }
          });
          this.on("addedfile", function(file) { 
            $("#isFileAdded").val("true");
          });
          this.on("removedfile", function(file) { 
            $("#isFileAdded").val("false");
          });
          // Listen to the sendingmultiple event. In this case, it's the sendingmultiple event instead
          // of the sending event because uploadMultiple is set to true.
          this.on("sendingmultiple", function()  {
              // Append all form inputs to the formData Dropzone will POST
          });
          this.on("successmultiple", function(files, response) {
          // Gets triggered when the files have successfully been sent.
          // Redirect user or notify of success.
              window.location.href = '/admin/book';
          });
          this.on("errormultiple", function(files, response) {
          // Gets triggered when there was an error sending the files.
          // Maybe show form again, and notify user of error
          });
      }
  };

    Dropzone.discover();

  })()  