var ClassificationTasks;
(function (resultsDivSelector,
           taskNumberSelector, taskTotalSelector, tasksDivSelector, 
           tag,
           taskDisplaySelector,
           $, jQuery, undefined) {
  var noiseImageURLs = [];
  for (var i = 0; i < 10; i++) {
    noiseImageURLs.push('https://jgross.scripts.mit.edu/alphabets/images/strokeNoise' + i + '.png');
  }
  var tasksDiv;
  $(function () { tasksDiv = $(tasksDivSelector).hide(); });
  ClassificationTasks = function ClassificationTasks(data, totalTasks, dataLoader, onDoneTasks) {
    SequentialTasks.call(this, undefined, taskNumberSelector, taskTotalSelector, tasksDivSelector, resultsDivSelector,
                         data['tasksPerFeedbackGroup'][0], tag);

    var self = this;
    var onLoadImage = dataLoader.thingDone;
    var progressPause = data['pauseToNextGroup'][0]; // characters.py makes it a list, but I don't care about the random part
    var displayProgressBarDuringTask = data['displayProgressBarDuringTask'];

    var confirmToContinue = data['confirmToContinue'];

    var $anchorsHolder;

    var tasksBreak = new TasksBreak(progressPause);
    var tasksProgress;

    var anchorImageHolders = [];
    var anchorBoxes = [];
    var classImageHolders = [];
    var classBoxes = [];
    var $imageHolders = $();
    var $chosenCharacterDisplay;
    var $characterInput;

    var $continueButton;

    var curTask;

    var jumpToTask = function dontJumpToTask() {};

    this.taskDisplay = undefined;

    HintedTasks.call(this,
                     jQuery.map(['pauseToFirstHint', 'pauseToSecondHint', 'pauseToAnchor', 'pauseToNoise', 'pauseToTest'], function (tag) {
                                  return data[tag][0];
                                }),
                     jQuery.map(['first-hint', 'second-hint', 'show-anchor', 'noise', 'show-classes'], function (keyword) {
                                  return function (index) { return tag + 'task-' + index + '-time-of-' + keyword; };
                                }),
                     [showFirstHint, showSecondHint, showAnchors, showNoise, showClasses],
                     self.recordInfo);



    function makeTask(taskIndex, taskData) {
      var rtn = {
        'anchors':[],
        'anchorURLs':[],
        'noiseImages':[],
        'noiseImageURLs':[],
        'classes':[],
        'classURLs':[],
        'letters':[],
        'letterURLs':[],
        'inputs':{},
        'correctClassIndex':undefined,
        'pauseToHints':undefined
      };

      for (var i = 0; i < taskData['anchors'].length; i++) {
        var src = noiseImageURLs[Math.floor(Math.random() * noiseImageURLs.length)];
        rtn['noiseImages'][i] = $('<img>')
          .attr('src', src)
          .attr('alt', 'Noise image ' + (i + 1) + ' for task ' + (taskIndex + 1) + '.')
          .addClass('noise-image character')
          .hide()
          .load(onLoadImage);
        rtn['noiseImageURLs'][i] = src;

        src = taskData['anchors'][i]['anonymous url'];
        rtn['anchors'][i] = $('<img>')
          .attr('src', src)
          .attr('alt', 'Anchor image ' + (i + 1) + ' for task ' + (taskIndex + 1) + '.')
          .addClass('anchor-image character')
          .hide()
          .load(onLoadImage);
        rtn['anchorURLs'][i] = src;
      }

      for (var i = 0; i < taskData['classes'].length; i++) { // each class
        rtn['classes'][i] = [];
        rtn['classURLs'][i] = [];
        for (var j = 0; j < taskData['classes'][i][0].length; j++) { // each character in the class
          var src = taskData['classes'][i][0][j]['anonymous url'];
          rtn['classes'][i][j] = $('<img>')
            .attr('src', src)
            .attr('alt', 'Character image of class ' + (i + 1) + ' for task ' + (taskIndex + 1) + '.')
            .addClass('class-image character')
            .hide()
            .load(onLoadImage);
          rtn['classURLs'][i][j] = src;
        }
        if (taskData['classes'][i][1])
          rtn['correctClassIndex'] = i;
      }

      if (data['pauseToNoise'][0] > 0) {
        rtn['pauseToHints'] = jQuery.map(['pauseToFirstHint', 'pauseToSecondHint', 'pauseToAnchor', 'pauseToNoise', 'pauseToTest'], function (pause) {
                                            if (data[pause][1])
                                              return data[pause][0] + (2 * Math.random() - 1) * data[pause][1];
                                            else
                                              return data[pause][0];
                                          });
      }
      return rtn;
    }

    this.extraTaskInfo = function defaultExtraTaskInfo(task) { return {}; }

    this.onFinishTask = function (task, answerIndex, willShowResults) {
      var isCorrect = (answerIndex == task['correctClassIndex']);
      self.recordInfo(function (index) { return tag + 'task-' + index + '-is-correct-answer'; }, isCorrect);
      self.recordInfo(function (index) { return tag + 'task-' + index + '-chosen-class'; }, answerIndex);
      self.recordInfo(function (index) { return tag + 'task-' + index + '-correct-class'; }, task['correctClassIndex']);
      jQuery.each(anchorImageHolders, function (index, imageHolder) {
          self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-noise-image-' + index + '-url'; },
                          task['noiseImageURLs'][index]);
          self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-anchor-image-' + index + '-anonymous_url'; },
                          task['anchorURLs'][index]);
        });
      var extraInfo = self.extraTaskInfo(task);
      if (extraInfo)
        jQuery.each(extraInfo, function (key, value) {
            self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-' + key; }, value);
          });
      if (isCorrect)
        tasksProgress.addCorrect();
      else
        tasksProgress.addIncorrect();
    };

    this.prepTask = function (task) {
      curTask = task;
      jQuery.each(anchorImageHolders, function (index, imageHolder) {
          imageHolder.children().remove();
        });

      jQuery.each(classBoxes, function (index, box) {
          box.removeClass('class-selected');
        });

      jQuery.each(classImageHolders, function (index, imageHolderList) {
          jQuery.each(imageHolderList, function (characterIndex, imageHolder) {
            imageHolder.children().remove();
            self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-class-' + index + '-image-' + characterIndex + '-anonymous_url'; },
                            task['classURLs'][index][characterIndex]);
          });
        });

      jQuery.each(task['letterURLs'], function (index, url) {
          self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-character-' + index + '-anonymous_url'; },
                          url);
        });

      jQuery.each(task['inputs'], function (key, input) {
          self.recordInput(input);
        });

      $continueButton.attr('disabled', 'disabled');
      $characterInput.attr('value', '').attr('disabled', 'disabled');
      $chosenCharacterDisplay.children().hide();
      refreshDisplayForTasks();
    };

    this.showResults = function showResults(task, answer, callback) {
      tasksProgress.showProgress();
      tasksDiv.hide();
      if (self.doneWithTasks()) {
        tasksBreak.makeBreak(function () {
            tasksProgress.hideProgress();
            onDoneTasks.apply(this, arguments);
          }, function (button) {
            return $('<span>').append('You have completed all the tasks.  ' + 
              'To answer some final questions and submit your answers, click ')
              .append(button).append('.');
          });
      } else {
        tasksBreak.makeBreak(function () {
            tasksProgress.hideProgress();
            tasksDiv.show();
            callback.apply(this, arguments);
          });
      }
    };

    this.doTask = function doTask(task) {
      jumpToTask();
      jQuery.each(classBoxes, function (index, box) { box.addClass('class-disable-select'); });
      if (data['pauseToNoise'][0] > 0) {
        self.beginPrompting(task, task['pauseToHints']);
      } else {
        showAnchors(task);
        showClasses(task);
      }
    };

    function showFirstHint() {
      $anchorsHolder.removeClass('prompt-holder-done').addClass('prompt-holder-long');
    };

    function showSecondHint() {
      $anchorsHolder.removeClass('prompt-holder-long').addClass('prompt-holder-short');
    };

    function showAnchors(task) {
      $anchorsHolder.removeClass('prompt-holder-short prompt-holder-done').addClass('prompt-holder-doing');
      jQuery.each(anchorImageHolders, function (index, imageHolder) {
          imageHolder.append(task['anchors'][index].show());
        });
    };

    function showNoise(task) {
      $anchorsHolder.removeClass('prompt-holder-doing').addClass('prompt-holder-done');
      jQuery.each(anchorImageHolders, function (index, imageHolder) {
          imageHolder.children().remove();
          imageHolder.append(task['noiseImages'][index].show());
        });
    };

    function showClasses(task) {
      self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-time-of-show-classes'; },
                      dateUTC(new Date()));
      $characterInput.attr('disabled', '');
      jQuery.each(classImageHolders, function (classIndex, imageHolderList) {
          classBoxes[classIndex].removeClass('class-disable-select');
          jQuery.each(imageHolderList, function (characterIndex, imageHolder) {
              imageHolder.children().remove();
              imageHolder.append(task['classes'][classIndex][characterIndex].show());
              // XXX TODO: Fix this so it displays multiples properly.
            });
        });
    }

    function selectAnswer(classIndex, changeFocus) {
      if (changeFocus === undefined) changeFocus = true;
      jQuery.each(classBoxes, function (index, box) { box.removeClass('class-selected'); });
      $chosenCharacterDisplay.children().hide();
      if (classIndex === undefined || classIndex === '') {
        $continueButton.attr('disabled', 'disabled');
        return;
      }
      if (classBoxes[classIndex].hasClass('class-disable-select')) return;
      classBoxes[classIndex].addClass('class-selected');
      if ($characterInput.attr('value') != classIndex) $characterInput.attr('value', classIndex);
      $continueButton.attr('disabled', '');
      var images = curTask['classURLs'][classIndex];
      var image = images[Math.floor(Math.random() * images.length)];
      $chosenCharacterDisplay.children()
        .attr('src', image)
        .attr('alt', 'Character Class ' + (classIndex + 1))
        .show();
      if (changeFocus) {
        if (confirmToContinue)
          $continueButton.focus();
        else
          self.finishTask(curTask, $characterInput.attr('value'));
      }
    }

    function makeImageHolder(pre_tag, img_holder_class_string, post_tag) {
      if (post_tag === undefined) post_tag = '';
      if (img_holder_class_string === undefined) img_holder_class_string = '';
      var imageBox = $('<div>')
        .addClass('image-box')
        .attr('id', pre_tag + 'box' + post_tag);
      var imageHolder = $('<span>')
        .addClass('wraptocenter image-holder ' + img_holder_class_string)
        .css({'width':data['characterSize'], 'height':data['characterSize']})
        .attr('id', pre_tag + 'image-holder' + post_tag);
      $imageHolders = $imageHolders.add(imageHolder);
      imageBox.append(imageHolder);
      return {'box':imageBox, 'image-holder':imageHolder};
    }

    this.resizeImages = function resizeImages(size) {
      $imageHolders.css({'width':size, 'height':size});
    }

    this.resetImageSizes = function resetImageSizes() {
      self.resizeImages(data['characterSize']);
    }

    function makeAnchor(index) {
      var imageHolder = makeImageHolder('anchor-', 'anchor-holder', '-' + index);
      anchorBoxes[index] = imageHolder['box'];
      anchorImageHolders[index] = imageHolder['image-holder'];
      return imageHolder['box'];
    }

    function makeClass(index, imageCount, compressIfSingle) {
      if (compressIfSingle === undefined) compressIfSingle = true;
      var classHolder = $('<fieldset>')
        .addClass('class-holder class-unselected')
        .append($('<legend>').append(index + 1).addClass('class-label'))
        .mouseover(function () { classHolder.addClass('class-hover'); })
        .mouseleave(function () { classHolder.removeClass('class-hover'); })
        .click(function () { selectAnswer(index); });
      classBoxes[index] = classHolder;
      classImageHolders[index] = [];
      var imageHolder;
      for (var i = 0; i < imageCount; i++) {
        imageHolder = makeImageHolder('class-' + index + '-', 'class-character-holder', '-' + i);
        if (compressIfSingle && imageCount == 1)
          classHolder.append(imageHolder['image-holder']);
        else
          classHolder.append(imageHolder['box']);
        classImageHolders[index][i] = imageHolder['image-holder'];
      }
      return classHolder;
    }

    /*************************** kludge ********************************
     * this code is a kludge to get around the fact that chrome fails at
     * {rendering,deleting elements,navigating by url hash}.
     * See http://code.google.com/p/chromium/issues/detail?id=87391
     * for more details
     */
    function refreshDisplayForTasks() {
      var parent = self.tasksDisplay.parent();
      var elements = self.tasksDisplay.detach();
      setTimeout(function () { parent.append(elements); jumpToTask(); }, 1);
    }
    this.onBeginTasksAfterDisplay = refreshDisplayForTasks;
    /*******************************************************************/


    this.onBeginTasks = function onBeginTasks() {
      self.taskDisplay = $(taskDisplaySelector);
      var anchorsDiv = $('<div>')
        .attr('id', 'anchors-holder')
      var classesDiv = $('<div>')
        .attr('id', 'classes-holder');
      var taskHolder = $('<div>')
        .addClass('task-holder');
      $anchorsHolder = $('<div>')
        .addClass('prompt-holder-done inline');
      self.taskDisplay.append(taskHolder);

      $characterInput = $('<select>')
        .attr('id', 'character-input')
        .addClass('character-question');
      var defaultOption = $('<option>')
        .attr('id', 'default-option')
        .attr('value', '')
        .append('(#)');
      $characterInput.append(defaultOption)
        .change(function () { selectAnswer(this.value); })
        .keyup(function () { selectAnswer($characterInput.attr('value'), false); })
        .keydown(function () { selectAnswer($characterInput.attr('value'), false); });
      for (var i = 0; i < data['tasks'][0]['classes'].length; i++) {
        $characterInput.append($('<option>')
                                 .attr('value', i)
                                 .append(i + 1));
      }

      var $prompt = $('<p>')
        .addClass('character-question')
        .append("I think that ")
        .append($anchorsHolder);
      for (var i = 0; i < data['tasks'][0]['anchors'].length; i++) {
        $anchorsHolder.append(makeAnchor(i));
      }
      var chosenImageHolder = makeImageHolder('chosen-');
      $chosenCharacterDisplay = chosenImageHolder['image-holder'].append($('<img>')
                                                                          .css({'width':'100%', 'height':'100%'})); // not sure why I need this
      $prompt
        .append(" is most likely to be the same as character ")
        .append($characterInput)
        .append(": ")
        .append(chosenImageHolder['box']);
      anchorsDiv.append($prompt);

      for (var i = 0; i < data['tasks'][0]['classes'].length; i++) {
        classesDiv.append(makeClass(i, data['tasks'][0]['classes'][0][0].length));
      }
      
      if (data['anchorPosition'] in ['above', 'top']) {
        taskHolder
          .append(anchorsDiv)
          .append(classesDiv);
      } else {
        taskHolder
          .append(classesDiv)
          .append(anchorsDiv);
      }

      var continueDiv = $('<div>')
        .css({'text-align':'center'})
        .append($continueButton = $('<button>')
                  .addClass('character-question')
                  .attr('type', 'button')
                  .attr('disabled', 'disabled')
                  .append('continue to the next task')
                  .click(function () {
                    $continueButton.attr('disabled', 'disabled');
                    if ($characterInput.attr('value') !== '' && $characterInput.attr('value') !== undefined) {
                      self.finishTask(curTask, $characterInput.attr('value'));
                      return true;
                    } else {
                      selectAnswer('');
                      return false;
                    }}));

      if (confirmToContinue) taskHolder.append(continueDiv);

      if (data['pauseToNoise'][0] > 0)
        jumpToTask = function jumpToTask() {
          window.location.hash = '';
          window.location.hash = 'anchors-holder';
        };
      else
        jumpToTask = function jumpToTaskTop() {
          window.location.hash = '';
          window.location.hash = 'task';
          window.location.hash = 'extra-options-form';
        };
    }

    jQuery.each(data['tasks'], function (index, task) {
        self.pushTask(makeTask(index, task));
      });

    tasksProgress = new TasksProgress(this.tasksLeftCount());
  };
})('#task-results', '.task-number',
  '.task-count', '#all-tasks', '',
  '#task',
  jQuery, jQuery);
