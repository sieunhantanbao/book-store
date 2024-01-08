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
})()
