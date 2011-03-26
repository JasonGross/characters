(function ($, jQuery, undefined) {
  var dataLoader;
  var tasks;
  var calibrationTasks;
  var afterCalibrationInstructionsDiv;

  var allUrlParameters = ['numberOfAlphabets', 'exampleCharactersPerAlphabet',
    'sameTestCharactersPerAlphabet', 'differentTestCharactersPerAlphabet',
    'differentAlphabetTestCharactersPerAlphabet', 'distractWithAll',
    'tasksPerFeedbackGroup', 'displayProgressBarDuringTask',
    'pauseToGroup', 'random', 'characterSet',
    'trialsPerExperiment', 'fractionSame', 'calibrationTaskCount'];

  $(function () {
    afterCalibrationInstructionsDiv = $('#after-calibration-instructions').hide();
  });

  function retrieveData(loadData) {
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

  function onDoneTasks() {
    $('.tasks').hide();
    $('.post-task').show();
  }

  function onDoneCalibration() {
    afterCalibrationInstructionsDiv.show();
    $('#continue-after-calibration').click(function () {
        afterCalibrationInstructionsDiv.remove();
        tasks.startTasks();
      });
  }

  function doLoadData(data) {
    saveUrlParameters(data);
    $(function () {
      $('.num-calibration-trials').html(data['calibrationTaskCount']);
      $('.num-trials').html(data['tasks'].length);
    });
    tasks = new RecognitionRTTasks(data, data['tasks'].length, dataLoader,
        onDoneTasks);
    calibrationTasks = new CalibrationTasks(onDoneCalibration,
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
