(function ($, jQuery, undefined) {
  var dataLoader;
  var tasks;

  var allUrlParameters = ['taskCount', 'exampleClassCount', 'examplePerClassCount', 'uniqueClasses',
    'pauseToFirstHint', 'pauseToSecondHint', 'pauseToExample', 'pauseToNoise',
    'characterSize', 'canvasSize', 'characterSet'];

  function retrieveData(loadData) {
    $.getJSON("../scripts/python/duplication-characters.py",
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
//      $('.expected-duration').html((data['tasks'].length / 10) + '-' + (Math.floor(data['tasks'].length / 2.5))); // minutes
      $('.example-class-count').html(data['exampleClassCount']);
      $('.example-per-class-count').html(data['examplePerClassCount']);
      if (data['examplePerClassCount'] <= 1) $('.show-if-multiple-per-class').remove();
    });
    tasks = new DuplicationTasks(data, data['tasks'].length, dataLoader, onDoneTasks);
    var checkBox = setupResizeImages(tasks.resizeImages, tasks.resetImageSizes);
    tasks.extraTaskInfo = function () {
        var rtn = {
                    'resized-images-checked':checkBox.attr('checked'),
                    'window-width':$(window).width(),
                    'window-height':$(window).height()
                  };
        return rtn;
      };
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
