(function ($, jQuery, undefined) {
  var dataLoader;
  var tasks;

  var allUrlParameters = ['taskCount', 'anchorCount', 'classCount',
    'experimentGroup', 'displayProgressBarDuringTask',
    'unique', 'tasksPerFeedbackGroup', 'anchorPosition',
    'pauseToFirstHint', 'pauseToSecondHint', 'pauseToAnchor', 'pauseToNoise', 'pauseToTest', 'pauseToNextGroup',
    'confirmToContinue',
    'allowDidNotSeeCount', 'sameAlphabetClassCount'];

  function retrieveData(loadData) {
    $.getJSON("../scripts/python/classification-characters.py",
      urlParameters.getURLParameters(allUrlParameters),
      loadData);
  }

  function getTotalCount(data) {
    return data['tasks'].length * data['imagesPerTask'];
  }

  function onAccept() {
    tasks.startTasks();
  };

  function onDoneTasks() {
    $('.tasks').hide();
    $('.post-task').show();
  }

  function doLoadData(data) {
    saveUrlParameters(data);
    $(function () {
      $('.task-count').html(data['tasks'].length);
      $('.n').html(data['tasks'][0]['classes'].length);
      if (data['tasks'][0]['anchors'].length > 1) $('.s-if-multiple-anchors').html('s');
    });
    tasks = new ClassificationTasks(data, data['tasks'].length, dataLoader,
        onDoneTasks);
    doneLoading();
  };
  notYetLoaded();

  function saveUrlParameters(data) {
    var hiddenInputs = $('#hidden-inputs');
    jQuery.each(allUrlParameters, function (index, parameter) {
      if (parameter in data)
        hiddenInputs.append(makeInput('url-parameter-' + parameter)
            .attr('value', data[parameter])
          );
    });
  }

  dataLoader = new DataLoader(retrieveData, getTotalCount, onAccept, doLoadData);
})($, jQuery);
