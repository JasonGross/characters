var DuplicationCompletionTasks;
(function (resultsDivSelector,
           taskNumberSelector, taskTotalSelector, tasksDivSelector, 
           tag,
           taskDisplaySelector,
           $, jQuery, undefined) {
  var noiseImageURLs = [];
  for (var i = 0; i < 10; i++) {
    noiseImageURLs.push('//jgross.scripts.mit.edu/alphabets/images/strokeNoise' + i + '.png');
  }
  DuplicationCompletionTasks = function DuplicationCompletionTasks(data, totalTasks, dataLoader, onDoneTasks) {
    SequentialTasks.call(this, undefined, taskNumberSelector, taskTotalSelector, tasksDivSelector, resultsDivSelector,
                         0, tag);

    var self = this;
    var onLoadImage = dataLoader.thingDone;

    var $canvasHolder;
    var $continueButton;
    var updateContinueButton;
    var exampleHolder;
    var exampleBox;
    var exampleImageHolder;
    var doFinishTask;
    var timed = true; // might customize later

    var curTask;

    this.taskDisplay = undefined;

    HintedTasks.call(this,
                     jQuery.map(['pauseToFirstHint', 'pauseToSecondHint', 'pauseToExample', 'pauseToNoise'], function (tag) {
                                  return data[tag][0];
                                }),
                     jQuery.map(['first-hint', 'second-hint', 'show-examples', 'noise'], function (keyword) {
                                  return function (index) { return tag + 'task-' + index + '-time-of-' + keyword; };
                                }),
                     [showFirstHint, showSecondHint, showExamples, showNoise],
                     self.recordInfo);

    this.onDoneTasks = onDoneTasks;

    function makeTask(taskIndex, taskData) {
      var rtn = {
        'completionImage':undefined,
        'completionImageURL':taskData['completionImage']['anonymous url'],
        'duplicationImage':undefined,
        'duplicationImageURL':taskData['duplicationImage']['anonymous url'],
        'noiseImage':undefined,
        'noiseImageURL':noiseImageURLs[Math.floor(Math.random() * noiseImageURLs.length)],
        'canvas':undefined,
        'imageHalf':taskData['imageHalf'],
        'pauseToHints':undefined,
        'timed':timed,
        'inputs':{}
      };

      jQuery.each(['completion', 'duplication', 'noise'], function (i, tag) {
        rtn[tag + 'Image'] = $('<img>')
          .attr('src', rtn[tag + 'ImageURL'])
          .attr('alt', tag + ' image for task ' + (taskIndex + 1) + '.')
          .addClass(tag + '-image character')
          .hide()
          .load(onLoadImage);
      });

      rtn['canvas'] = new CompletionCanvas(tag + 'task-' + taskIndex + '-canvas', data['canvasSize'], data['canvasSize'], rtn['completionImage'],
                                           rtn['imageHalf']);

      if (timed) {
        rtn['pauseToHints'] = jQuery.map(['pauseToFirstHint', 'pauseToSecondHint', 'pauseToExample', 'pauseToNoise'], function (pause) {
                                            if (data[pause][1])
                                              return data[pause][0] + (2 * Math.random() - 1) * data[pause][1];
                                            else
                                              return data[pause][0];
                                          });
      }
      return rtn;
    }

    this.extraTaskInfo = function defaultExtraTaskInfo(task) { return {}; }

    this.onFinishTask = function (task, canvas, willShowResults) {
      self.recordInfo(function (index) { return tag + 'task-' + index + '-strokes'; }, canvas.strokesToString());
      self.recordInfo(function (index) { return tag + 'task-' + index + '-image'; }, canvas.getImage());
      
      var extraInfo = self.extraTaskInfo(task);
      if (extraInfo)
        jQuery.each(extraInfo, function (key, value) {
            self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-' + key; }, value);
          });
    };

    doFinishTask = function doFinishTask() {
      if (canvas.canUndo()) {
        self.finishTask(curTask, canvas);
        return true;
      } else {
        return false;
      }
    };

    this.prepTask = function (task) {
      curTask = task;

      $canvasHolder.children().remove();

      updateContinueButton = function updateContinueButton() {
        if (task['canvas'].canUndo())
          $continueButton.attr('disabled', '');
        else
          $continueButton.attr('disabled', 'disabled');
      };

      doFinishTask = function doFinishTask() {
        if (task['canvas'].canUndo()) {
          self.finishTask(task, task['canvas']);
          return true;
        } else {
          return false;
        }
      };

      self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-image-show_half'; },
                      task['imageHalf']);

      self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-duplication-image-anonymous_url'; },
                      task['duplicationImageURL']);
      self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-completion-image-anonymous_url'; },
                      task['completionImageURL']);


      exampleImageHolder.children().remove();

      jQuery.each(task['inputs'], function (key, input) {
          self.recordInput(input);
        });

      $continueButton.attr('disabled', 'disabled');
    };

    function updateContinueButton() {
      if (canvas.canUndo())
        $continueButton.attr('disabled', '');
      else
        $continueButton.attr('disabled', 'disabled');
    }

    this.doTask = function doTask(task) {
      if (timed) {
        self.beginPrompting(task, task['pauseToHints']);
      } else {
        showExamples(task);
        exampleHolder.removeClass('prompt-holder-doing');
      }
    };

    function showFirstHint() {
      exampleHolder.removeClass('prompt-holder-done').addClass('prompt-holder-long');
    };

    function showSecondHint() {
      exampleHolder.removeClass('prompt-holder-long').addClass('prompt-holder-short');
    };

    function showExamples(task) {
      exampleHolder.removeClass('prompt-holder-short prompt-holder-done').addClass('prompt-holder-doing');
      exampleImageHolder.append(task['duplicationImage'].show());
    }

    function showNoise(task) {
      exampleHolder.removeClass('prompt-holder-doing').addClass('prompt-holder-done');
      exampleImageHolder.children().remove();
      exampleImageHolder.append(task['noiseImage'].show());

      $canvasHolder.append(task['canvas'].DOMElement);
      task['canvas'].dirty(updateContinueButton);
    }

    this.onBeginTasks = function onBeginTasks() {
      self.taskDisplay = $(taskDisplaySelector);
      $canvasHolder = $('#canvas-holder');

      $continueButton = $('#next-task-button')
        .click(function () {
            $continueButton.attr('disabled', 'disabled');
            return doFinishTask();
          });

      exampleHolder = $('#examples-holder')
      exampleBox = $('#example-box');
      exampleImageHolder = $('#example-image-holder')
        .css({'width':data['characterSize'], 'height':data['characterSize']});
    }

    jQuery.each(data['tasks'], function (index, task) {
        self.pushTask(makeTask(index, task));
      });

    return this;
  };
})('#task-results', '.task-number',
  '.task-count', '#all-tasks', '',
  '#task',
  jQuery, jQuery);
