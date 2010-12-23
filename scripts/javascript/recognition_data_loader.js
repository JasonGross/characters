function makeBoxForImage(image) {
  var imageBox = $('<div>')
    .addClass('image-box image-holder')
    .attr('id', 'image-box-for-' + image.attr('id'))
    .attr('name', 'image-box-for-' + image.attr('name'));
//  var imageInnerBox = $('<div>')
//    .addClass('image-inner-box image-holder');
  /*var imageHolder = $('<span>')
    .addClass('wraptocenter image-holder')
    .attr('id', 'image-holder-for-' + image.attr('id'))
    .attr('name', 'image-holder-for' + image.attr('name'));*/
  imageBox.append(image);
  //imageBox.append(imageHolder);
  //imageOuterBox.append(imageInnerBox);
  return imageBox;
}

var firstTask = null;

(function ($) {
  var progressHolder;
  var totalTasks;
  var progressBar;
  var progressMessage;
  var acceptButton;
  var removeOnAccept;
  var tasksContainer;
  var tasks = [];
  $(function () {
    progressHolder = $('#loading-progress');
    progressBar = $('#loading_progress').progressbar({value:0});
    acceptButton = $('#accept_task-button');
    removeOnAccept = $('.pre-task');
    tasksContainer = $('#all-tasks');
    var ellipsis = $('<span>').append('..');
    var count = 2;
    var maxCount = 3;
    progressMessage = $('#loading_message')
      .append($('<p>').append('Loading information about what tasks to give you').append(ellipsis));
    ellipsisTime = 500;
    ellipsisFunc = function () {
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
  });

  function loadImages(data) {
    imagePairs = data['tasks'];
    totalTasks = imagePairs.length;
    var totalImages = totalTasks * 3;
    refcounter.setCounter('image progress', totalImages);
    $(function () {
      progressMessage.children().remove();
      var progressLoaded = $('<span>').append('0')
      progressMessage
        .append('Loading images.  ')
        .append(progressLoaded)
        .append(' of ' + totalImages + ' done.');
      progressBar.progressbar('option', 'value', 0);
      refcounter.handleCounterChange('image progress', function (value) {
        progressBar.progressbar('option', 'value', 100 * (totalImages - value) / totalImages);
        progressLoaded.html(totalImages - value);
      });
      refcounter.handleCounterZero('image progress', function () {
        if ($('.warning .error').length == 0)
          acceptButton.attr('disabled', '');
        progressHolder.hide();
      });

      $('#accept_task-form').submit(function (ev) {
        ev.preventDefault();
        removeOnAccept.remove();
        tasksContainer.append(firstTask['dom-element']);
        firstTask['do-task']();
      });
    });

   var numRightWrong = {'right':0, 'wrong':0};

    jQuery.each(imagePairs, function (index, imagePair) {
      firstTask = makeTask(totalTasks - index - 1, imagePair[0], imagePair[1], imagePair[2], imagePair[3], firstTask, data, numRightWrong);
    });


  }

  function makeBreak(numRight, numWrong, breakTime, afterBreak) {
    var task = $('<div>')
      .attr('id', 'task-' + index)
      .hide();
    var taskFieldSet = $('<fieldset>')
      .append($('<legend>').append('Task ' + (index + 1) + ' of ' + totalTasks))
      .addClass('task-holder');
    var example = $('<div>')
      .addClass('example-holder');
    var test = $('<div>')
      .addClass('test-holder');
    var question = $('<div>')
      .addClass('question-holder')
      .hide();


  }

  function makeTask(index, exampleImageObject, testImageObject, noiseImageUrl, areSameCharacter, nextTask, data, numRightWrong) {
    var startTime;
    var endTime;
    var task = $('<div>')
      .attr('id', 'task-' + index)
      .hide();
    var taskFieldSet = $('<fieldset>')
      .append($('<legend>').append('Task ' + (index + 1) + ' of ' + totalTasks))
      .addClass('task-holder');
    var example = $('<div>')
      .addClass('example-holder');
    var test = $('<div>')
      .addClass('test-holder');
    var question = $('<div>')
      .addClass('question-holder')
      .hide();

    // Example
    var exampleImage = $('<img>')
        .attr('src', exampleImageObject['anonymous url'])
        .attr('alt', 'Example image for task ' + (index + 1) + '.')
        .addClass('example-image')
        .hide()
        .load(function () { refcounter.decrementCounter('image progress'); });
    var testImage = $('<img>')
        .attr('src', testImageObject['anonymous url'])
        .attr('alt', 'Test image for task ' + (index + 1) + '.')
        .addClass('test-image')
        .hide()
        .load(function () { refcounter.decrementCounter('image progress'); });
    var noiseImage = $('<img>')
        .attr('src', noiseImageUrl)
        .attr('alt', 'Noise image for task ' + (index + 1) + '.')
        .addClass('noise-image')
        .hide()
        .load(function () { refcounter.decrementCounter('image progress'); });

    var exampleHeader = $('<div>')
      .addClass('example-header')
      .append('Example Image');
    var testHeader = $('<div>')
      .addClass('example-header')
      .append('Test Image');
    var questionFields = $('<fieldset>');
    var questionLegend = $('<legend>').append('Are these images examples of the same character?');
    var questionTrueInputYes;
    var questionInputYes = $('<label>').append(
      questionTrueInputYes = $('<input>')
        .attr('type', 'radio')
        .attr('name', 'task-' + index + '_question')
        .attr('id', 'task-' + index + '_question-yes')
        .attr('value', 1)
        .attr('disabled', 'disabled')
      ).append(
        'Yes, they are the same.'
      );
    var questionInputNo = $('<label>').append(
      $('<input>')
        .attr('type', 'radio')
        .attr('name', 'task-' + index + '_question')
        .attr('id', 'task-' + index + '_question-no')
        .attr('value', 0)
        .attr('disabled', 'disabled')
      ).append(
        'No, they are different.'
      );

    var questionDurationInput = $('<input>')
        .attr('type', 'hidden')
        .attr('value', '')
        .attr('id', 'task-' + index + '-duration-of-see-test')
        .attr('name', 'task-' + index + '-duration-of-see-test');

    var questionIsCorrectInput = $('<input>')
        .attr('type', 'hidden')
        .attr('value', '')
        .attr('id', 'task-' + index + '-is-correct-answer')
        .attr('name', 'task-' + index + '-is-correct-answer');

    var questionExampleURLInput = $('<input>')
        .attr('type', 'hidden')
        .attr('value', exampleImageObject['anonymous url'])
        .attr('id', 'task-' + index + '-example-url')
        .attr('name', 'task-' + index + '-example-url');

    var questionTestURLInput = $('<input>')
        .attr('type', 'hidden')
        .attr('value', testImageObject['anonymous url'])
        .attr('id', 'task-' + index + '-test-url')
        .attr('name', 'task-' + index + '-test-url');





    var exampleImageHolder = $('<div>')
      .addClass('example-image-holder');
    var testImageHolder = $('<div>')
      .addClass('test-image-holder');

    example.append(exampleHeader).append(exampleImageHolder);
    test.append(testHeader).append(testImageHolder);

    questionFields.append(questionLegend).append(questionInputYes).append($('<br>')).append(questionInputNo).append(questionDurationInput);
    question.append(questionFields);
    taskFieldSet.append(example).append(test).append(question);
    task.append(taskFieldSet);

    tasksContainer.append(task);

    var timeOuts = {};
    jQuery.each(['pauseToFirstHint', 'pauseToSecondHint', 'pauseToExample', 'pauseToNoise', 'pauseToTest', 'tasksPerFeedbackGroup', 'tasksPerWaitGroup', 'pauseToGroup'],
                function (index, name) {
      timeOuts[name] = data[name];
      if (timeOuts[name].length > 1)
        timeOuts[name] = timeOuts[name][0] + (2 * Math.random() - 1) * timeOuts[name][1];
      else
        timeOuts[name] = timeOuts[name][0];
    });

    var doneTask = function () {
      endTime = dateUTC(new Date());
      questionDurationInput.value = endTime - startTime;
      questionIsCorrectInput.value = areSameCharacter == questionTrueInputYes.checked;
      if (areSameCharacter == questionTrueInputYes.checked)
        numRightWrong['right']++;
      else
        numRightWrong['wrong']++;
      example.remove();
      test.remove();
      task.hide();
      if (nextTask !== null) {
        var doNextTaskNow = function () {
            task.parent().append(nextTask['dom-element']);
            nextTask['do-task']();
        };
        if ((numRightWrong['right'] + numRightWrong['wrong']) % data['tasksPerFeedbackGroup'] == 0)
          makeBreak(numRightWrong['right'], numRightWrong['wrong'], timeOuts['pauseToGroup'], doNextTaskNow);
        else
          doNextTaskNow();
      } else {
        $('.post-task').show();
      }
    };

    var doTask = function () {
      task.show();
      window.location.hash = '';
      window.location.hash = 'task-' + index;
      exampleImageHolder.append(exampleImage).append(noiseImage);
      testImageHolder.append(testImage);
      window.setTimeout(showFirstHint, timeOuts['pauseToFirstHint']);
    };

    var showFirstHint = function () {
      window.setTimeout(showSecondHint, timeOuts['pauseToSecondHint']);
      exampleImageHolder.addClass('example-holder-long');
    };


    var showSecondHint = function () {
      window.setTimeout(showExample, timeOuts['pauseToExample']);
      exampleImageHolder.addClass('example-holder-short');
      exampleImageHolder.removeClass('example-holder-long');
    };


    var showExample = function () {
      if (timeOuts['pauseToNoise'] > 0)
        window.setTimeout(showNoise, timeOuts['pauseToNoise']);
      else
        window.setTimeout(showTest, timeOuts['pauseToTest']);
      //exampleImageHolder.append(exampleImage);
      exampleImage.show();
      exampleImageHolder.addClass('example-holder-doing');
      exampleImageHolder.removeClass('example-holder-short');
    };

    var showNoise = function () {
      window.setTimeout(showTest, timeOuts['pauseToTest']);
      exampleImage.remove();
      //exampleImageHolder.append(noiseImage);
      noiseImage.show();
      exampleImageHolder.addClass('example-holder-done');
      exampleImageHolder.removeClass('example-holder-doing');
    };

    var showTest = function () {
      exampleImageHolder.addClass('example-holder-done');
      exampleImageHolder.removeClass('example-holder-doing');
      //testImageHolder.append(testImage);
      testImage.show();
      question.show();
      startTime = dateUTC(new Date());
      jQuery.each([questionInputYes, questionInputNo], function (index, input) {
        input.children().attr('disabled', '')
          .change(function () {
            console.log(this);
            doneTask();
          });
      });
    };



    return {'dom-element':task, 'do-task':doTask};
  }

  function makeInputs(data) {

    loadImages(data);

    /*jQuery.each(tasks, function (index, task) {
      tasksContainer.append(task['dom-element']);
    });*/
    doneLoading();
  }
  notYetLoaded();
  $(function () {
      $.getJSON("../scripts/python/characters.py",
        urlParameters.getURLParameters(['numberOfAlphabets', 'exampleCharactersPerAlphabet', 'sameTestCharactersPerAlphabet',
                                        'differentTestCharactersPerAlphabet', 'differentAlphabetTestCharactersPerAlphabet', 'distractWithAll',
                                        'pauseToFirstHint', 'pauseToSecondHint', 'pauseToExample', 'pauseToNoise', 'pauseToTest', 'tasksPerFeedbackGroup', 'tasksPerWaitGroup', 'pauseToGroup']),
        makeInputs);
    });
})(jQuery);
