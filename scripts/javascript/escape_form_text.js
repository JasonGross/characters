(function (jQuery, $, undefined) {
  $(function () {
    $('form').submit(function () {
      $('input[type="text"]').add('textarea').each(function () {
          $(this).attr('value', $(this).attr('value').replace(/\n/g, '\\n').replace(/\r/g, '\\r').replace(/\t/g, '\\t'));
        });
      return true;
    });
  });
})(jQuery, jQuery);
