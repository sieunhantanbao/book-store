(function () {
    'use strict'

    $("#frmCreateCategory").validate({
      rules: {
        name: {
            required: true,
        },
        short_description: {
            required: true,
        },
      },
      messages: {
        name: "Category name is required",
        short_description: "Short description is required",
      }
    });

    Dropzone.options.frmCreateCategory = {
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
                 if($("#frmCreateCategory").valid()){
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
               window.location.href = '/admin/category';
            });
            this.on("errormultiple", function(files, response) {
            // Gets triggered when there was an error sending the files.
            // Maybe show form again, and notify user of error
            });
        }
    };

    $("#frmEditCategory").validate({
      rules: {
        name: {
            required: true,
        },
        short_description: {
        required: true,
        },
      },
      messages: {
        name: "Category name is required",
        short_description: "Short description is required",
      }
    });

    Dropzone.options.frmEditCategory = {
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
               if($("#frmEditCategory").valid()){
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
              window.location.href = '/admin/category';
          });
          this.on("errormultiple", function(files, response) {
          // Gets triggered when there was an error sending the files.
          // Maybe show form again, and notify user of error
          });
      }
  };

    Dropzone.discover();

  })()  