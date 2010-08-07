var notYetLoaded, doneLoading;
(function (loadingSelector) {
  var loadingCount = 0;
  notYetLoaded = function () {
    loadingCount++;
  };
  doneLoading = function () {
    loadingCount--;
    if (loadingCount <= 0)
      $(loadingSelector).remove();
  };
})('#loading');
notYetLoaded();
$(doneLoading);
