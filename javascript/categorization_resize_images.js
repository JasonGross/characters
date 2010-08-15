(function () {
  var baseSize = 100, offset = 15;
  var calcNewColSize = function (width) {
    return ((width / 10 < baseSize + offset) ? ((width / 10) - offset) : baseSize);
  };
  var calcNewHolderSize = function (width) {
    return ((width / 10 < baseSize + offset) ? ((width / 10) - offset) : baseSize) - 20;
  };
  var calcNewImageSize = function (width) {
    return ((width / 10 < baseSize + offset) ? ((width / 10) - offset) : baseSize) - 25;
  };
  (function (checkBoxId, calcNewHolderSize, calcNewImageSize,
             calcNewColSize, calcNewImageBoxMargin) {
    var checkBox;
    $(function () {
      checkBox = $('#' + checkBoxId);
      if (checkBox.attr('checked'))
        $(window).resize();
      checkBox.change(function () {
        $(window).resize(); 
      });
    });
    $(window).resize(function (ev) {
      if (checkBox && checkBox.attr('checked')) {
        if (calcNewColSize) {
          var newWidth = calcNewColSize($(window).width());
          $('.alphabet-table-col').css({'width':newWidth});
        }
        if (calcNewHolderSize) {
          var newWidth = calcNewHolderSize($(window).width());
          $('.image-holder').css({'width':newWidth, 'height':newWidth});
        }
        if (calcNewImageSize) {
          var newWidth = calcNewImageSize($(window).width());
          $('img').width(newWidth).height(newWidth);
        }
        if (calcNewImageBoxMargin) {
          var newMargin = calcNewImageBoxMargin($(window).width());
          $('.image-holder').css('margin', newMargin);
        }
      } else {
        $('.alphabet-table-col').css({'width':100});
        $('.image-holder').css({'width':80, 'height':80});
        $('img').width(75).height(75);
        $('.image-holder').css('margin', '2.5px');
      }
    });
  })('resize-images-on-page-resize', calcNewHolderSize, calcNewImageSize,
      calcNewColSize);
})();
