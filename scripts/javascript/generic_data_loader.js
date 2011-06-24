var DataLoader;
(function (defaultProgressHolder, defaultProgressBar, defaultAcceptButton,
           defaultRemoveOnAccept, defaultProgressMessage, 
           defaultProgressMessageText, defaultEllipsisTime, 
           defaultLoadingTypeText, defaultNoErrors, defaultAcceptTaskForm,
           $, jQuery, undefined) {
  var dataLoaderId = 0;
  DataLoader = function DataLoader(retrieveData, getTotalCount, onAccept, doLoadData,
      autoLoadData, progressHolder, progressBar, acceptButton, removeOnAccept,
      progressMessage, progressMessageText, ellipsisTime, loadingTypeText, 
      noErrors, acceptTaskForm) {
    var thisDataLoaderId = dataLoaderId;
    var counterTag = 'DataLoader' + thisDataLoaderId; 
    dataLoaderId++;
    if (autoLoadData === undefined) autoLoadData = true;
    var self = this;

    var elipsis;

    this.preLoadData = function () {
      progressHolder = $(progressHolder || defaultProgressHolder);
      progressBar = $(progressBar || defaultProgressBar).progressbar({value:0});
      acceptButton = $(acceptButton || defaultAcceptButton);
      removeOnAccept = $(removeOnAccept || defaultRemoveOnAccept);

      ellipsis = $('<span>').append('..');
      var count = 2;
      var maxCount = 3;
    
      progressMessage = $(progressMessage || defaultProgressMessage)
        .append($('<p>')
          .append(progressMessageText || defaultProgressMessageText)
          .append(ellipsis));

      ellipsisTime = ellipsisTime || defaultEllipsisTime;
      var ellipsisFunc = function () {
        if (ellipsis) {
          if (count == maxCount) {
            count = 0;
            ellipsis.html('');
          } else {
            count++;
            ellipsis.append('.');
          }
          setTimeout(ellipsisFunc, ellipsisTime);
        }
      };
      ellipsisFunc();
      self.preLoadData = function () {};
    };

    this.retrieveData = function () { retrieveData(self.loadData); };
    
    this.loadData = function (data) {
      self.preLoadData();
      var totalCount = getTotalCount(data);
      refcounter.initCounter(counterTag, totalCount);
      $(function () {
        progressMessage.children().remove();
        ellipsis = undefined;
        var progressLoaded = $('<span>').append('0')
        progressMessage
          .append(loadingTypeText || defaultLoadingTypeText)
          .append(progressLoaded)
          .append(' of ' + totalCount  + ' done.');
        progressBar.progressbar('option', 'value', 0);
        refcounter.handleCounterChange(counterTag, function (value) {
          progressBar.progressbar('option', 'value', 
            100 * (totalCount - value) / totalCount);
          progressLoaded.html(totalCount - value);
        });
        refcounter.handleCounterZero(counterTag, function () {
          if ((noErrors || defaultNoErrors)())
            acceptButton.attr('disabled', '');
          progressHolder.hide();
        });

        $(acceptTaskForm || defaultAcceptTaskForm).submit(function (ev) {
          ev.preventDefault();
          removeOnAccept.remove();
          onAccept();
        });

        doLoadData(data);
      });
    };

    this.thingDone = function () {
      refcounter.decrementCounter(counterTag);
    };

    if (autoLoadData) {
      $(function () {
          self.preLoadData();
          self.retrieveData();
        });
    }
  };
})('#loading-progress', '#loading_progress','#accept_task-button', '.pre-task',
  '#loading_message', 'Loading information about what tasks to give you',
  500, 'Loading images.  ',
  function () { return $('.warning, .error').length == 0; }, 
  '#accept_task-form',
  jQuery, jQuery);
