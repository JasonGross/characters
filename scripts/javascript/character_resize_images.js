var setupResizeImages
(function (defaultCheckBoxSelector, $, jQuery, undefined) {
  var baseSize = 80, offset = 125, count = 5, min = 20;
  var calcNewHolderSize = function (width) {
    console.log(width);
    if ((width - offset) / count > baseSize)
      return baseSize;
    else if ((width - offset) / count < min)
      return min;
    else
      return (width - offset) / count;
  };
  setupResizeImages = function setupResizeImages(changeImageSizeFunc, resetDefaultFunc, checkBoxSelector) {
    $window = $(window);
    if (resetDefaultFunc === undefined)
      resetDefaultFunc = function defaultResetDefaultFunc() { changeImageSizeFunc(baseSize + 'px', baseSize + 'px'); };
    var actualResizeFunc = function () {};
    var checkBox = $(checkBoxSelector || defaultCheckBoxSelector)
      .change(function () {
        if (checkBox.attr('checked')) {
          actualResizeFunc = onResize;
          $window.resize();
        } else {
          actualResizeFunc = function resizeNop() {};
          resetDefaultFunc();
        }
      });

    function onResize(ev) {
      var newSize = calcNewHolderSize($window.width()) + 'px';
      console.log(newSize);
      changeImageSizeFunc(newSize, newSize);
    }

    $window.resize(function () { actualResizeFunc.apply(this, arguments); } );

    if (checkBox.attr('checked'))
      checkBox.change();

    return checkBox;
  };
})('#resize-images-on-page-resize',
   jQuery, jQuery);
