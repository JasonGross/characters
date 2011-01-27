function makeBoxForImage(image) {
  var imageBox = $('<div>')
    .addClass('image-box image-holder')
    .attr('id', 'image-box-for-' + image.attr('id'))
    .attr('name', 'image-box-for-' + image.attr('name'));
  imageBox.append(image);
  return imageBox;
}

var firstTask = null;

var makeTask;

(function ($) {
  var progressHolder;
  var totalTasks;
  var progressBar;
  var progressMessage;
  var acceptButton;
  var removeOnAccept;
  var tasksContainer;
  var tasks = [];
  var taskProgress;
  var taskProgressMessage;
  var taskProgressBarHolder;
  var taskActualProgressBar;
  var taskOverlayProgressBar;
  var taskCorrectProgressBar;
  var taskIncorrectProgressBar;
  var taskCorrectText;
  var taskIncorrectText;
  var taskScoredText;
  var allUrlParameters = ['numberOfAlphabets', 'exampleCharactersPerAlphabet', 'sameTestCharactersPerAlphabet',
                          'differentTestCharactersPerAlphabet', 'differentAlphabetTestCharactersPerAlphabet', 'distractWithAll',
                          'pauseToFirstHint', 'pauseToSecondHint', 'pauseToExample', 'pauseToNoise', 'pauseToTest', 
                          'tasksPerFeedbackGroup', 'tasksPerWaitGroup', 'pauseToGroup', 'displayProgressBarDuringTask',
                          'random', 'characterSet', 'trialsPerExperiment', 'fractionSame'];
  var hiddenInputs;

  var makeTaskData;

  $(function () { 

    $('.task-progress').html($('.task-progress').html().replace(/>(\s|\n)+</g, '><'));

    progressHolder = $('#loading-progress');
    progressBar = $('#loading_progress').progressbar({value:0});
    acceptButton = $('#accept_task-button');
    removeOnAccept = $('.pre-task');
    tasksContainer = $('#all-tasks');
    hiddenInputs = $('#hidden-inputs');

    taskProgress = $('.task-progress').hide();
    taskProgressMessage = $('.task-message');
    taskProgressBarHolder = $('.task-progress-bar-holder');
    taskActualProgressBar = $('.task-actual-progress-bar').progressbar({value:0});
    taskOverlayProgressBar = $('.task-overlay-progress-bar-holder');
    taskCorrectProgressBar = $('.task-correct-progress-bar');
    taskIncorrectProgressBar = $('.task-incorrect-progress-bar');

    taskCorrectText = $('#task-progress-message-num-tasks-correct');
    taskIncorrectText = $('#task-progress-message-num-tasks-incorrect');
    taskScoredText = $('#task-progress-message-num-tasks-known');

    breakDiv = $('.task-break').hide();

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
        
    if (data['pauseToNoise'] !== undefined) {
      if (data['pauseToNoise'][0] > 0) {
        $('.show-if-untimed').hide();
        $('.show-if-timed').show();
      } else {
        $('.show-if-timed').hide();
        $('.show-if-untimed').show();
      }
    }
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
        if ($('.warning, .error').length == 0)
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

    var numRightWrong = {'right':0, 'wrong':0, 'did not see':0};

    firstTask = {'do-task': function () {
        updateProgress(numRightWrong['right'], numRightWrong['wrong'], numRightWrong['did not see']);
        taskProgress.show();
        $('.tasks').hide();
        $('.post-task').show();
      }};

    makeTaskData = data;
    startExampleTask();

    if (data['pauseToGroup'][0] < 0) {
      breakDiv.append($('<p>').html('You have completed a group of tasks.  You may take a short break and see your progress, below.  When you are ready to move on, click ')
          .append($('<input>')
            .attr('type', 'submit')
            .attr('name', 'finish_break')
            .attr('id', 'finish_break')
            .attr('value', 'here')
            .click(function (ev) { breakDiv.afterBreak(); }))
          .append('.'));
    } else {
      breakDiv.append($('<p>').html('You have completed a group of tasks.  You may take a short break of about ' +
            data['pauseToGroup'][0] + ' milliseconds and see your progress below.'));
    }

    $('#num-trials').html(totalTasks);
    
    jQuery.each(imagePairs, function (index, imagePair) {
      firstTask = makeTask(totalTasks - index - 1, imagePair[0], imagePair[1], imagePair[2], imagePair[3], firstTask, data, numRightWrong);
    });
    firstTask['do-task'] = (function (doFirstTask) {
      return function () {
        taskProgress.show();
        taskCorrectProgressBar.height(taskActualProgressBar.height());
        taskIncorrectProgressBar.height(taskActualProgressBar.height());
        taskOverlayProgressBar.height(taskActualProgressBar.height());
        if (!data['displayProgressBarDuringTask'])
          taskProgress.hide();
        doFirstTask();
      };
    })(firstTask['do-task']);
  }

  function makeBreak(breakTime, afterBreak, data, tasksProgress, breakDiv) {
    if (!data['displayProgressBarDuringTask']) {
      tasksProgress.show();
      var oldAfterBreak = afterBreak;
      afterBreak = function () {
        tasksProgress.hide();
        oldAfterBreak();
      };
    }
    if (breakDiv !== undefined) {
      breakDiv.afterBreak = function () {
        breakDiv.afterBreak = undefined;
        breakDiv.hide();
        afterBreak();
      };
      breakDiv.show();
    }
    if (breakTime >= 0)
      window.setTimeout(afterBreak, breakTime);
  }

  function updateProgress(numRight, numWrong, numDidNotSee) {
    taskCorrectProgressBar.width(numRight * 100.0 / totalTasks + '%');
    taskIncorrectProgressBar.width(numWrong * 100.0 / totalTasks + '%');
    taskCorrectText.html(numRight);
    taskIncorrectText.html(numWrong);
    taskScoredText.html(numRight + numWrong + numDidNotSee);
  }

  
  makeTask = function (index, exampleImageObject, testImageObject, noiseImageUrl, areSameCharacter, nextTask, data, numRightWrong, taskLabel, onLoadImage,
                       doGlobalUpdates, localTasksContainer, taskProgressBar, doRepeat, doUserInput, jumpToTask) {
    if (taskLabel === undefined) taskLabel = 'Task ' + (index + 1) + ' of ' + totalTasks;
    if (onLoadImage === undefined) onLoadImage = function () { refcounter.decrementCounter('image progress'); };
    if (doGlobalUpdates === undefined) doGlobalUpdates = true;
    if (localTasksContainer === undefined) localTasksContainer = tasksContainer;
    if (taskProgressBar === undefined) taskProgressBar = taskActualProgressBar;
    if (doRepeat === undefined) doRepeat = false;
    if (data === undefined) data = makeTaskData;
    if (jumpToTask === undefined) jumpToTask = true;
    var startTime;
    var endTime;
    var task = $('<div>')
      .attr('id', 'task-' + index)
      .hide();
    var taskFieldSet = $('<fieldset>')
      .append($('<legend>').append(taskLabel))
      .addClass('task-holder');
    var example = $('<div>')
      .addClass('example-holder');
    var test = $('<div>')
      .addClass('test-holder');
    var question = $('<div>')
      .addClass('question-holder')
      .css({'display':'inline-block'}) // Why the heck do I need this?  The css class should take care of it.  It works in chrome, but not firefox.
      .hide();
    
    // Example
    var exampleImage = $('<img>')
        .attr('src', exampleImageObject['anonymous url'])
        .attr('alt', 'Example image for task ' + (index + 1) + '.')
        .addClass('example-image')
        .hide()
        .load(onLoadImage);
    var testImage = $('<img>')
        .attr('src', testImageObject['anonymous url'])
        .attr('alt', 'Test image for task ' + (index + 1) + '.')
        .addClass('test-image')
        .hide()
        .load(onLoadImage);
    var noiseImage = $('<img>')
        .attr('src', noiseImageUrl)
        .attr('alt', 'Noise image for task ' + (index + 1) + '.')
        .addClass('noise-image')
        .hide()
        .load(onLoadImage);
    
    var exampleHeader = $('<div>')
      .addClass('example-header')
      .append('Example Image');
    var testHeader = $('<div>')
      .addClass('example-header')
      .append('Test Image');
    var questionFields = $('<fieldset>');
    var questionLegend = $('<legend>').append('Are these images examples of the same character?');
    var extraInstructions = $('<p>')
      .append($('<strong>')
          .append("Don't worry if the Example Image was hard to see, it flashes very quickly."))
      .append($('<br>'))
      .append($('<strong>').append("Please respond as quickly as possible."));
    var questionTrueInputYes, questionTrueInputNo, questionTrueInputDidNotSee;
    var questionInputYes = $('<label>').append(
      questionTrueInputYes = $('<input>')
        .attr('type', 'radio')
        .attr('name', 'task-' + index + '_question')
        .attr('id', 'task-' + index + '_question-yes')
        .attr('value', 1)
        .attr('disabled', 'disabled')
//        .css({'width':'64px', 'height':'64px', 'zoom':2})
      ).append(
        'Yes, they are the same.'
      );
    var questionInputNo = $('<label>').append(
      questionTrueInputNo = $('<input>')
        .attr('type', 'radio')
        .attr('name', 'task-' + index + '_question')
        .attr('id', 'task-' + index + '_question-no')
        .attr('value', 0)
        .attr('disabled', 'disabled')
      ).append(
        'No, they are different.'
      );
    var questionInputDidNotSee = $('<label>').append(
        questionTrueInputDidNotSee = $('<input>')
          .attr('type', 'radio')
          .attr('name', 'task-' + index + '_question')
          .attr('id', 'task-' + index + '_question-did_not_see')
          .attr('value', 1)
          .attr('disabled', 'disabled')
        ).append(
          'I did not see the example character.'
        );

    var questionDidNotSeeButton;
    var questionDidNotSeeHolder = $('<div>').append(
        questionDidNotSeeButton = $('<button>')
          .attr('type', 'button')
          .attr('value', 'I did not see the test image.'));
    var questionDidNotSeeUseCount = $('<input>')
      .attr('type', 'hidden')
      .attr('value', 0)
      .attr('id', 'task-' + index + '-did_not_see-count')
      .attr('name', 'task-' + index + '-did_not_see-count');
      
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

    var questionTimes = {};
    jQuery.each(['doneTask', 'doTask', 'showFirstHint', 'showSecondHint', 'showExample', 'showNoise', 'showTest'], 
                function (questionIndex, name) {
      questionTimes[name] = $('<input>')
        .attr('type', 'hidden')
        .attr('value', '')
        .attr('id', 'task-' + index + '-time-of-' + name)
        .attr('name', 'task-' + index + '-time-of-' + name);
      questionFields.append(questionTimes[name]);
    });
    questionFields.append(questionDurationInput).append(questionIsCorrectInput).append(questionExampleURLInput).append(questionTestURLInput).append(questionDidNotSeeUseCount);
      
    var exampleImageHolder = $('<div>')
      .addClass('example-image-holder');
    var testImageHolder = $('<div>')
      .addClass('test-image-holder');
      
    example.append(exampleHeader).append(exampleImageHolder);    
    test.append(testHeader).append(testImageHolder);
   
    var timeOuts = {};
    jQuery.each(['pauseToFirstHint', 'pauseToSecondHint', 'pauseToExample', 'pauseToNoise', 'pauseToTest', 'tasksPerFeedbackGroup', 'tasksPerWaitGroup', 'pauseToGroup'],
                function (index, name) {
      timeOuts[name] = data[name];
      if (timeOuts[name].length > 1)
        timeOuts[name] = timeOuts[name][0] + (2 * Math.random() - 1) * timeOuts[name][1];
      else
        timeOuts[name] = timeOuts[name][0];
    });

    questionFields.append(questionLegend).append(questionInputYes).append($('<br>')).append(questionInputNo).append(questionDurationInput);
    if (timeOuts['pauseToNoise'] > 0)
      questionFields.append($('<br>')).append(questionInputDidNotSee).append(questionDurationInput);
    
    question.append(questionFields);
    taskFieldSet.append(example).append(test).append(question);
    task.append(taskFieldSet);

    localTasksContainer.append(task);


    var didNotSee = function () {
    };

    questionDidNotSeeButton.click(didNotSee);

    var redoTask = function () {
    };


    var doneTask = function () {
      endTime = dateUTC(new Date());
      questionDurationInput.attr('value', endTime - startTime);
      questionTimes['doneTask'].attr('value', endTime);
      if (questionTrueInputDidNotSee.attr('checked'))
        questionIsCorrectInput.attr('value', 'Did Not See');
      else
        questionIsCorrectInput.attr('value', areSameCharacter == questionTrueInputYes.attr('checked'));
      if ((areSameCharacter && questionTrueInputYes.attr('checked')) || 
          (!areSameCharacter && questionTrueInputNo.attr('checked')))
        numRightWrong['right']++;
      else if (questionTrueInputYes.attr('checked') || questionTrueInputNo.attr('checked'))
        numRightWrong['wrong']++;
      else
        numRightWrong['did not see']++;
      if (doRepeat) {
        testImage.hide();
        noiseImage.hide();
        exampleImage.hide();
        questionTrueInputYes.attr('checked', '');
        questionTrueInputNo.attr('checked', '');
        questionTrueInputDidNotSee.attr('checked', '')
        question.hide();
        exampleImageHolder.removeClass('example-holder-done');
        example.css({'opacity':0, 'filter':'alpha(opacity=0)', '-moz-opacity':0});
        test.css({'opacity':0, 'filter':'alpha(opacity=0)', '-moz-opacity':0});
      } else {
        example.remove();
        test.remove();
        task.hide()
      }
      if (taskProgressBar !== null)
        taskProgressBar.progressbar('option', 'value', 100 * (numRightWrong['right'] + numRightWrong['wrong'] + numRightWrong['did not see']) / totalTasks);
      if (nextTask !== null) {
        var doNextTaskNow = function () {
            if ('dom-element' in nextTask && nextTask['dom-element'] !== null)
              task.parent().append(nextTask['dom-element']);
            nextTask['do-task']();
        };
        if (doGlobalUpdates && (numRightWrong['right'] + numRightWrong['wrong'] + numRightWrong['did not see']) % data['tasksPerFeedbackGroup'][0] == 0)
          updateProgress(numRightWrong['right'], numRightWrong['wrong'], numRightWrong['did not see']);
        if (doGlobalUpdates && (numRightWrong['right'] + numRightWrong['wrong'] + numRightWrong['did not see']) % data['tasksPerWaitGroup'][0] == 0)
          makeBreak(timeOuts['pauseToGroup'], doNextTaskNow, data, taskProgress, breakDiv);
        else
          doNextTaskNow();
      }
    };
    
    var doTask = function () {
      task.show();
      example.css({'opacity':1, 'filter':'alpha(opacity=100)', '-moz-opacity':1});
      test.css({'opacity':1, 'filter':'alpha(opacity=100)', '-moz-opacity':1});
      if (jumpToTask) {
        window.location.hash = '';
        window.location.hash = 'task-' + index;
      }
      exampleImageHolder.append(exampleImage.hide()).append(noiseImage.hide());
      testImageHolder.append(testImage.hide());
      questionTimes['doTask'].attr('value', dateUTC(new Date()));
      window.setTimeout(showFirstHint, timeOuts['pauseToFirstHint']);
    };
    
    var showFirstHint = function () {
      window.setTimeout(showSecondHint, timeOuts['pauseToSecondHint']);
      exampleImageHolder.addClass('example-holder-long');
      questionTimes['showFirstHint'].attr('value', dateUTC(new Date()));
    };

    
    var showSecondHint = function () {
      window.setTimeout(showExample, timeOuts['pauseToExample']);
      exampleImageHolder.addClass('example-holder-short');
      exampleImageHolder.removeClass('example-holder-long');
      questionTimes['showSecondHint'].attr('value', dateUTC(new Date()));
    };

    
    var showExample = function () {
      if (timeOuts['pauseToNoise'] > 0)
        window.setTimeout(showNoise, timeOuts['pauseToNoise']);
      else
        window.setTimeout(showTest, timeOuts['pauseToTest']);
      //exampleImageHolder.append(exampleImage);
      exampleImage.show();
      questionTimes['showExample'].attr('value', dateUTC(new Date()));
      exampleImageHolder.addClass('example-holder-doing');
      exampleImageHolder.removeClass('example-holder-short');
    };
    
    var showNoise = function () {
      window.setTimeout(showTest, timeOuts['pauseToTest']);
      if (doRepeat)
        exampleImage.hide();
      else
        exampleImage.remove();
      //exampleImageHolder.append(noiseImage);
      noiseImage.show();
      questionTimes['showNoise'].attr('value', dateUTC(new Date()));
      exampleImageHolder.addClass('example-holder-done');
      exampleImageHolder.removeClass('example-holder-doing');
    };
    
    var showTest = function () {
      exampleImageHolder.addClass('example-holder-done');
      exampleImageHolder.removeClass('example-holder-doing');
      //testImageHolder.append(testImage);
      testImage.show();

      // On the first two trials (until they answer two trials), show extra instructions
      if (numRightWrong['right'] + numRightWrong['wrong'] < 2 && timeOuts['pauseToNoise'] > 0)
        questionFields.prepend(extraInstructions);


      question.show();
      questionTimes['showTest'].attr('value', dateUTC(new Date()));
      startTime = dateUTC(new Date());
      jQuery.each([questionInputYes, questionInputNo, questionInputDidNotSee], function (index, input) {
        input.children().attr('disabled', '')
          .one('change', function () {
            //console.log(this);
            doneTask();
          });
      });
      if (doUserInput !== undefined)
        doUserInput();
    };
    
    

    return {'dom-element':task, 'do-task':doTask, 'questionInputYes':questionTrueInputYes, 'questionInputNo':questionTrueInputNo, 'questionInputDidNotSee':questionTrueInputDidNotSee};
  }

  function saveUrlParameters(data) {
    jQuery.each(allUrlParameters, function (index, parameter) {
      if (parameter in data)
        hiddenInputs.append($('<input>')
            .attr('type', 'hidden')
            .attr('value', data[parameter])
            .attr('id', 'url-parameter-' + parameter)
            .attr('name', 'url-parameter-' + parameter)
          );
    });
  }
  
  function makeInputs(data) {
    saveUrlParameters(data);
    
    loadImages(data);
    
    /*jQuery.each(tasks, function (index, task) {
      tasksContainer.append(task['dom-element']);
    });*/
    doneLoading();
  }
  notYetLoaded();
  $(function () {
      $.getJSON("../scripts/python/characters.py", 
        urlParameters.getURLParameters(allUrlParameters),
        makeInputs);
    });
})(jQuery);
