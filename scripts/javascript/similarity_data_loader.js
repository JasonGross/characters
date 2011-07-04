(function ($, jQuery, undefined) {
  var dataLoader;
  var tasks;

  var allUrlParameters = ['taskCount', 'displayProgressBarDuringTask', 'unique', 'tasksPerFeedbackGroup', 'pauseToNextGroup',
                          'characterSize', 'characterSet', 'allowDidNotSeeCount', 'sameFraction', 'differentAlphabetFraction'];

  function retrieveData(loadData) {
    $.getJSON("../scripts/python/similarity-characters.py",
      urlParameters.getURLParameters(allUrlParameters),
      loadData);
  }

  function getTotalCount(data) {
    return data['tasks'].length * data['imagesPerTask'];
  }

  function onAccept() {
    tasks.startTasks();
    $('#extra-options-form').show();
  };

  function onDoneTasks() {
    $('.tasks').hide();
    $('.post-task').show();
  }

  function doLoadData(data) {
    saveUrlParameters(data);
    $(function () {
      $('.task-count').html(data['tasks'].length);
    });
    tasks = new SimilarityTasks(data, data['tasks'].length, dataLoader, onDoneTasks);
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
