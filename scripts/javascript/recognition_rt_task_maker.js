var RecognitionRTTasks;
(function (delayRange, displayEvery, displayDelay, resultsDivSelector,
           taskNumberSelector, taskTotalSelector, tasksDivSelector, 
           displaySelector, tag, defaultSameDelay,
           taskProgressSelector, taskProgressMessageSelector,
           taskProgressBarHolderSelector, 
           taskActualProgressBarSelector, 
           taskOverlayProgressBarSelector,
           taskCorrectProgressBarSelector,
           taskIncorrectProgressBarSelector,
           taskCorrectTextSelector, taskIncorrectTextSelector,
           taskScoredTextSelector, breakDivSelector,
           $, jQuery, undefined) {
  var noiseImageURLs = [];
  for (var i = 0; i < 10; i++) {
    noiseImageURLs.push('http://jgross.scripts.mit.edu/alphabets/images/strokeNoise' + i + '.png');
  }
  var tasksDiv;
  $(function () { tasksDiv = $(tasksDivSelector).hide(); });
  RecognitionRTTasks = function (data, totalTasks, dataLoader, 
      onDoneTasks, sameDelay) {
    if (sameDelay === undefined) sameDelay = defaultSameDelay;
    RTTasks.apply(this, [tag,
      delayRange, displayEvery, displayDelay,
      resultsDivSelector, taskNumberSelector, taskTotalSelector,
      tasksDivSelector, displaySelector, sameDelay]);

    var self = this;
    var onLoadImage = dataLoader.thingDone;
    var $results = $(resultsDivSelector);
    var tasksPerGroup = data['tasksPerFeedbackGroup'][0]; // characters.py makes it a list, but I don't care about the random part
    var progressPause = data['pauseToGroup'][0]; // characters.py makes it a list, but I don't care about the random part
    var displayProgressBarDuringTask = data['displayProgressBarDuringTask'];

    var tasksBreak = new TasksBreak(progressPause);
    var tasksProgress;


    function makeTask(taskIndex, imagePair) {
      var rtn = {
        'noiseImages':[],
        'noiseImageURLs':[],
        'letters':[],
        'letterURLs':[],
        'inputs':{},
        'are-same':imagePair[3]
      };
      for (var i = 0; i < 5; i++) {
        var src = noiseImageURLs[Math.floor(Math.random() * noiseImageURLs.length)];
        rtn['noiseImages'][i] = $('<img>')
          .attr('src', src)
          .attr('alt', 'Noise image for task ' + (taskIndex + 1) + '.')
          .addClass('noise-image')
          .hide()
          .load(onLoadImage);
        rtn['noiseImageURLs'][i] = src;
      }
      for (var i = 0; i < 2; i++) {
        var src = imagePair[i]['anonymous url'];
        rtn['letters'][i] = $('<img>')
          .attr('src', src)
          .attr('alt', 'Image ' + (i + 1) + ' for task ' + (taskIndex + 1) + '.')
          .addClass('rt-symbol')
          .hide()
          .load(onLoadImage);
        rtn['letterURLs'][i] = src;
      }
      rtn['inputs']['is-correct-answer'] = makeInput(tag + 'task-' + taskIndex + '-is-correct-answer');
      return rtn;
    }

    this.onFinishTask = function (task, answeredSame, willShowResults) {
      task['inputs']['is-correct-answer'].attr('value',
          answeredSame == task['are-same']); // TODO: should I coerce these to booleans?
      if (answeredSame == task['are-same'])
        tasksProgress.addCorrect();
      else
        tasksProgress.addIncorrect();
    };

    this.prepTask = function (task, taskIndex) {
      $('.rt-symbol-holder').each(function (index) {
          var $this = $(this);
          $this.children().remove();
          $this.append(task['noiseImages'][index].show());
          $results.append(makeInput(tag + 'task-' + taskIndex + '-noise-image-' + index + '-url')
            .attr('value', task['noiseImageURLs'][index]));
        });

      jQuery.each(task['letterURLs'], function (index, url) {
          $results.append(makeInput(tag + 'task-' + taskIndex + '-character-' + index + '-anonymous_url')
            .attr('value', url));
        });

      jQuery.each(task['inputs'], function (key, input) {
          $results.append(input);
        });

      $results.append(makeInput(tag + 'task-' + taskIndex + '-are-same')
          .attr('value', task['are-same']));
    };

    this.beforeEachTask = function (task, callback) {
      if (tasksPerGroup > 0 && self.getCurrentTaskNumber() > 0 &&
          (self.getCurrentTaskNumber() % tasksPerGroup) == 0) {
        tasksProgress.showProgress();
        tasksDiv.hide();
        tasksBreak.makeBreak(function () {
            tasksProgress.hideProgress();
            tasksDiv.show();
            callback.apply(this, arguments);
          });
      } else
        callback();

    };

    this.onDoneTasks = function () {
      tasksProgress.showProgress();
      tasksBreak.makeBreak(function () {
          tasksProgress.hideProgress();
          onDoneTasks.apply(this, arguments);
        }, function (button) {
          return $('<span>').append('You have completed all the tasks.  ' + 
            'To answer some final questions and submit your answers, click ')
            .append(button).append('.');
        });
    }
    
    this.showPrompt = function (task) {
      $('.rt-character-holder').each(function (index) {
          var $this = $(this);
          $this.children().remove();
          $this.append(task['letters'][index].show());
      });
    };



    jQuery.each(data['tasks'], function (index, imagePair) {
        self.pushTask(makeTask(index, imagePair));
      });

    tasksProgress = new TasksProgress(this.tasksLeftCount());
  };
})([600, 1000], 1, 1000, '#rt-results', '#task-number',
  '#task-total', '#all-tasks', "#rt-display", 
  '', 4000,
  '.task-progress', '.task-message', '.task-progress-bar-holder',
  '.task-actual-progress-bar', '.task-overlay-progress-bar-holder',
  '.task-correct-progress-bar', '.task-incorrect-progress-bar',
  '#task-progress-message-num-tasks-correct', 
  '#task-progress-message-num-tasks-incorrect', 
  '#task-progress-message-num-tasks-known', '.task-break',
  jQuery, jQuery);
