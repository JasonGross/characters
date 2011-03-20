(function ($, jQuery, undefined) {
  var dataLoader;
  var tasks;
  var calibrationTasks;

  var allUrlParameters = ['numberOfAlphabets', 'exampleCharactersPerAlphabet',
    'sameTestCharactersPerAlphabet', 'differentTestCharactersPerAlphabet',
    'differentAlphabetTestCharactersPerAlphabet', 'distractWithAll',
    'tasksPerFeedbackGroup', 'displayProgressBarDuringTask',
    'pauseToGroup', 'random', 'characterSet',
    'trialsPerExperiment', 'fractionSame', 'calibrationTaskCount'];


  function retrieveData (loadData) {
    $.getJSON("../scripts/python/characters.py",
      urlParameters.getURLParameters(allUrlParameters),
      loadData);
  }

  function getTotalCount(data) {
    return data['tasks'].length * 7;
  }

  function onAccept() {
    calibrationTasks.startTasks();
  };

  function onDoneTasks () {
    $('.tasks').hide();
    $('.post-task').show();
  }

  function doLoadData (data) {
    saveUrlParameters(data);
    tasks = new RecognitionRTTasks(data, data['tasks'].length, dataLoader,
        onDoneTasks);
    calibrationTasks = new CalibrationTasks(tasks.startTasks,
        data['calibrationTaskCount']);
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
