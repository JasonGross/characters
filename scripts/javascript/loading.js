var notYetLoaded, doneLoading, formFinishedLoadingTime;
(function (loadingSelector, doOnDoneLoading) {
  var startTime;
  var loadingCount = 0;
  notYetLoaded = function () {
    loadingCount++;
  };
  doneLoading = function () {
    loadingCount--;
    if (loadingCount <= 0) {
      $(loadingSelector).remove();
      if (doOnDoneLoading)
        doOnDoneLoading();
      formFinishedLoadingTime = new Date();
    }
  };
})('.loading, #loading');
notYetLoaded();
$(doneLoading);
