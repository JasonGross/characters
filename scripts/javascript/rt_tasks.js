var RTTasks;
(function (defaultResultsDivSelector, defaultTaskNumberSelector, 
           defaultTaskTotalSelector,
           defaultTasksDivSelector, 
           defaultTotalTasks, defaultDelayRange, defaultDisplaySelector,
           defaultDisplayEvery, defaultDisplayDelay,
           $, jQuery, undefined) {
  RTTasks = function (tag, delayRange, displayEvery, 
      displayDelay, resultsDivSelector, taskNumberSelector, taskTotalSelector,
      tasksDivSelector, displaySelector, sameDelay) {
    SequentialTasks.apply(this);
    
    if (totalTasks === undefined) totalTasks = defaultTotalTasks;
    if (delayRange === undefined) delayRange = defaultDelayRange;
    if (displayEvery === undefined) displayEvery = defaultDisplayEvery;
    if (displayDelay === undefined) displayDelay = defaultDisplayDelay;
    if (sameDelay === undefined) sameDelay = -1;
    var results;
    var taskNumber;
    var taskTotal;
    var tasks;
    var averageSpan, lastSpan;
    var totalReactionTime = 0;
    var lastReactionTime;
    var lastStartTime;
    var curTimeInputs = {};
    var curKeypress;
    var timeoutId;
    var curJumpiness = 0;
    var curJumpinessInput;
    var totalTasks;
    var displayResults;
    var sameTimeoutId = undefined;
    var doOnKeypress = function () {};
    var actualDoOnKeypress = function () {
      doOnKeypress.apply(this, arguments);
    };
    var self = this; // so that calling functions from somewhere else doesn't break things

    

    function getNextDelay() {
      return delayRange[0] + Math.random() * delayRange[1];
    }

    function makeNextTask() {
      taskNumber.html(self.getCurrentTaskNumber() + 1);

      jQuery.each(['doTask', 'showCharacters', 'keypress'],
        function (index, name) {
          curTimeInputs[name] = makeInput(tag + '-' + self.getCurrentTaskNumber() + '-time-of-' + name);
          results.append(curTimeInputs[name]);
        });

      curKeypress = makeInput(tag + '-' + self.getCurrentTaskNumber() + '-keypress');
      curJumpinessInput = makeInput(tag + '-' + self.getCurrentTaskNumber() + '-keypress_before_show_prompt_count');

      results.append(curKeypress).append(curJumpinessInput);
    }

    this.beforeEachTask = function () {};

    this.prepTask = function (task, index) {};

    function queueResponse(task, delay) {
      timeoutId = setTimeout(function () { showCharacters(task); }, delay);
      doOnKeypress = function () { badKeypress(task, delay); };
    };

    function doTask(task, delay) {
      doOnKeypress = function () {};
      displayResults.hide();
      self.beforeEachTask();
      makeNextTask();
      self.prepTask(task, self.getCurrentTaskNumber());
      if (delay === undefined) delay = getNextDelay();
     
      curTimeInputs['doTask'].attr('value', dateUTC(new Date()));
      queueResponse(task, delay);
    };

    this.doNextTask = function (delay) {
      if (self.doneWithTasks()) return false;
      return doTask(self.takeNextTask(), delay);
    };

    function badKeypress(task, delay) {
      clearTimeout(timeoutId);
      alert("Please wait until after the prompt to press a key.");
      queueResponse(task, delay);
      curJumpiness++;
    }

    this.showPrompt = function (task) {};

    function showCharacters(task) {
      curTimeInputs['showCharacters'].attr('value', lastStartTime = dateUTC(new Date()));
      self.showPrompt(task);
      doOnKeypress = function () { onkeypress.apply(this, arguments); };
      if (sameDelay > 0)
        sameTimeoutId = setTimeout(self.finishTask, sameDelay);
    }

    function showResults(doNext) {
      if (doNext === undefined) doNext = function () { self.doNextTask(); };
      if (self.getCurrentTaskNumber() + 1 != 0)
        averageSpan.html(totalReactionTime / (self.getCurrentTaskNumber() + 1));
      else
        averageSpan.html('Weird error: self.getCurrentTaskNumber() = -1.  totalReactionTime = ' + totalReactionTime);
      lastSpan.html(lastReactionTime);
      displayResults.show();
      setTimeout(doNext, displayDelay);
    }

    this.onDoneTasks = function () {};

    function onkeypress(ev) {
      doOnKeypress = function () {};
      if (sameTimeoutId !== undefined) clearTimeout(sameTimeoutId);
      curTimeInputs['keypress'].attr('value', lastReactionTime = dateUTC(new Date()));
      lastReactionTime -= lastStartTime;
      totalReactionTime += lastReactionTime;
      curJumpinessInput.attr('value', curJumpiness);
      curJumpiness = 0;
      curKeypress.attr('value', JSON.stringify(
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
      self.finishTask(true);
    };

    this.onFinishTask = function () {};

    this.finishTask = function (shouldShowResults) {
      doOnKeypress = function () {};
      self.onFinishTask();
      if (shouldShowResults === undefined) showResults = false;
      if (self.doneWithTasks()) { 
        $(document).unbind('keypress', actualDoOnKeypress);
        doOnKeypress = function () { console.log("Detachment of keypress event failed."); alert("Something went wrong.  Why am I here?"); };
        showResults(function () { tasks.hide();  self.onDoneTasks(); });
      } else {
        if (self.getCurrentTaskNumber() % displayEvery == 0 && shouldShowResults)
          showResults();
        else
          self.doNextTask();
      }
      lastReactionTime = 0;
    };

    this.onBeginTasks = function () {};

    this.startTasks = function () {
      results = $(resultsDivSelector || defaultResultsDivSelector);
      taskNumber = $(taskNumberSelector || defaultTaskNumberSelector);
      taskTotal = $(taskTotalSelector || defaultTaskTotalSelector);
      tasks = $(tasksDivSelector || defaultTasksDivSelector);
      displayResults = $(displaySelector || defualtDisplaySelector)
        .append($('<p>')
          .append('Average Reaction Time: ')
          .append(averageSpan = $('<span>'))
          .append(' ms'))
        .append($('<p>')
          .append('Most Recent Reaction Time: ')
          .append(lastSpan = $('<span>'))
          .append(' ms'));
      self.onBeginTasks();
      taskTotal.html(totalTasks = self.tasksLeftCount());
      taskNumber.html(1);
      tasks.show();
      $(document).bind('keypress', actualDoOnKeypress);
      if (!(self.doneWithTasks())) self.doNextTask();
      self.startTasks = undefined;
    };
    
  };
})("#calibration-results", "#calibration-task-number", 
  "#calibration-task-total", "#calibration-tasks", 25, [600, 1000],
  "#calibration-display",
  1, 1000,
  jQuery, jQuery);

