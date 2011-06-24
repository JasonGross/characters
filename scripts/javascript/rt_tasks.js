var RTTasks;
(function (defaultResultsDivSelector, defaultTaskNumberSelector, 
           defaultTaskTotalSelector,
           defaultTasksDivSelector, 
           defaultTotalTasks, defaultDelayRange, defaultDisplaySelector,
           defaultDisplayEvery, defaultDisplayDelay,
           $, jQuery, undefined) {
  RTTasks = function (tag, delayRange, displayEvery, 
      displayDelay, resultsDivSelector, taskNumberSelector, 
      taskTotalSelector, tasksDivSelector, displaySelector, sameDelay) {
    if (displayEvery === undefined) displayEvery = defaultDisplayEvery;
    SequentialTasks.call(this, undefined, (taskNumberSelector || defaultTaskNumberSelector),
                         (taskTotalSelector || defaultTaskTotalSelector),
                         (tasksDivSelector || defaultTasksDivSelector),
                         (resultsDivSelector || defaultResultsDivSelector),
                         displayEvery,
                         tag);
    
    if (delayRange === undefined) delayRange = defaultDelayRange;
    if (displayDelay === undefined) displayDelay = defaultDisplayDelay;
    if (sameDelay === undefined) sameDelay = -1;
    var showAnswer = sameDelay >= 0;
    var averageSpan, lastSpan, answerSpan;
    var averageP, lastP;
    var totalReactionTime = 0;
    var lastReactionTime;
    var lastStartTime;
    var timeoutId;
    var curJumpiness = 0;
    var displayResults;
    var sameTimeoutId = undefined;
    var sameCount = 0;
    var doOnKeypress = function () {};
    var actualDoOnKeypress = function () {
      doOnKeypress.apply(this, arguments);
    };
    var self = this; // so that calling functions from somewhere else doesn't break things

    

    function getNextDelay() {
      return delayRange[0] + Math.random() * delayRange[1];
    }

    this.beforeEachTask = function (task, callback) { callback(); };

    function queueResponse(task, delay) {
      timeoutId = setTimeout(function () { showCharacters(task); }, delay);
      doOnKeypress = function () { badKeypress(task, delay); };
    };

    this.beforeTask = function beforeTask(task, callback) {
      doOnKeypress = function () {};
      displayResults.hide();
      self.beforeEachTask(task, function () {
        queueResponse(task, getNextDelay());
        callback.apply(this, arguments);
      });
    };

    function badKeypress(task, delay) {
      clearTimeout(timeoutId);
      alert("Please wait until after the prompt to press a key.");
      queueResponse(task, delay);
      curJumpiness++;
    }

    this.showPrompt = function (task) {};

    function showCharacters(task) {
      self.recordInfo(function (num) { return tag + 'task-' + num + '-time-of-showCharacters'; }, lastStartTime = dateUTC(new Date()));
      self.showPrompt(task);
      doOnKeypress = function () { onkeypress.apply(this, [task].concat(Array.prototype.slice.call(arguments))); };
      if (sameDelay > 0)
        sameTimeoutId = setTimeout(function () {
              sameCount++;
              self.finishTask(task, true); 
            },
            sameDelay);
    }

    this.showResults = function showResults(task, answeredSame, doNext) {
      //if (doNext === undefined) doNext = function () { self.doNextTask(); };
      if (!answeredSame) {
        /*if (self.getCurrentTaskNumber() + 1 - sameCount != 0)
          averageSpan.html(totalReactionTime / (self.getCurrentTaskNumber() + 1 - sameCount));
        else
          averageSpan.html('Weird error: self.getCurrentTaskNumber() = -1.  totalReactionTime = ' + totalReactionTime);*/
        lastSpan.html(lastReactionTime).show();
        averageP.hide();
        lastP.show();
      } else {
        averageP.hide();
        lastP.hide();
      }
      if (showAnswer) {
        if (answeredSame)
          answerSpan.html('Same');
        else
          answerSpan.html('Different');
      }
      displayResults.show();
      setTimeout(function () { doNext(); }, displayDelay);
    }

    function onkeypress(task, ev) {
      doOnKeypress = function () {};
      if (sameTimeoutId !== undefined) clearTimeout(sameTimeoutId);
      self.recordInfo(function (num) { return tag + 'task-' + num + '-time-of-keypress'; }, lastReactionTime = dateUTC(new Date()));
      lastReactionTime -= lastStartTime;
      totalReactionTime += lastReactionTime;
      self.recordInfo(function (num) { return tag + 'task-' + num + '-keypress_before_show_prompt_count'; }, curJumpiness);
      curJumpiness = 0;
      self.recordInfo(function (num) { return tag + 'task-' + num + '-keypress'; }, JSON.stringify(
        {
          'altKey':ev.altKey,
          'charCode':ev.charCode,
          'ctrlKey':ev.ctrlKey,
          'keyCode':ev.keyCode,
          'metaKey':ev.metaKey,
          'shiftKey':ev.shiftKey,
          'timeStamp':ev.timeStamp,
          'which':ev.which
        }));
      self.finishTask(task, false);
    };

    this.onFinishTask = function (task, answeredSame, willShowResults) {};

    var oldFinishTask = this.finishTask;

    this.finishTask = function finishTask(task, answeredSame, shouldShowResults) {
      doOnKeypress = function () {};
      if (self.doneWithTasks()) { 
        $(document).unbind('keypress', actualDoOnKeypress);
        doOnKeypress = function () { console.log("Detachment of keypress event failed."); alert("Something went wrong.  Why am I here?"); };
      }
      oldFinishTask.apply(this, arguments);
      lastReactionTime = 0;
    };

    this.onBeginTasks = function () {};

    var oldStartTasks = this.startTasks;
    this.startTasks = function startTasks() {
      displayResults = $(displaySelector || defualtDisplaySelector);
      if (sameDelay >= 0)
        displayResults
          .append($('<p>')
            .append('Your Answer: ')
            .append(answerSpan = $('<span>')))
      displayResults
        .append(averageP = $('<p>')
          .append('Average Reaction Time: ')
          .append(averageSpan = $('<span>'))
          .append(' ms'))
        .append(lastP = $('<p>')
          .append('Most Recent Reaction Time: ')
          .append(lastSpan = $('<span>'))
          .append(' ms'));
      oldStartTasks.apply(this, arguments);
      $(document).bind('keypress', actualDoOnKeypress);
    };
    
  };
})("#calibration-results", "#calibration-task-number", 
  "#calibration-task-total", "#calibration-tasks", 25, [600, 1000],
  "#calibration-display",
  1, 1000,
  jQuery, jQuery);

