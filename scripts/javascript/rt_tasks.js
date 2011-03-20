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
    SequentialTasks.apply(this);
    
    if (totalTasks === undefined) totalTasks = defaultTotalTasks;
    if (delayRange === undefined) delayRange = defaultDelayRange;
    if (displayEvery === undefined) displayEvery = defaultDisplayEvery;
    if (displayDelay === undefined) displayDelay = defaultDisplayDelay;
    if (sameDelay === undefined) sameDelay = -1;
    var showAnswer = sameDelay >= 0;
    var results;
    var taskNumber;
    var taskTotal;
    var tasks;
    var averageSpan, lastSpan, answerSpan;
    var averageP, lastP;
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
    var sameCount = 0;
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
          curTimeInputs[name] = makeInput(tag + 'task-' + self.getCurrentTaskNumber() + '-time-of-' + name);
          results.append(curTimeInputs[name]);
        });

      curKeypress = makeInput(tag + 'task-' + self.getCurrentTaskNumber() + '-keypress');
      curJumpinessInput = makeInput(tag + 'task-' + self.getCurrentTaskNumber() + '-keypress_before_show_prompt_count');

      results.append(curKeypress).append(curJumpinessInput);
    }

    this.beforeEachTask = function (task, callback) { callback(); };

    this.prepTask = function (task, index) {};

    function queueResponse(task, delay) {
      timeoutId = setTimeout(function () { showCharacters(task); }, delay);
      doOnKeypress = function () { badKeypress(task, delay); };
    };

    function doTask(task, delay) {
      doOnKeypress = function () {};
      displayResults.hide();
      self.beforeEachTask(task, function () {
        makeNextTask();
        self.prepTask(task, self.getCurrentTaskNumber());
        if (delay === undefined) delay = getNextDelay();
       
        curTimeInputs['doTask'].attr('value', dateUTC(new Date()));
        queueResponse(task, delay);
      });
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
      doOnKeypress = function () { onkeypress.apply(this, [task].concat(Array.prototype.slice.call(arguments))); };
      if (sameDelay > 0)
        sameTimeoutId = setTimeout(function () {
              sameCount++;
              self.finishTask(task, true); 
            },
            sameDelay);
    }

    function showResults(task, answeredSame, doNext) {
      if (doNext === undefined) doNext = function () { self.doNextTask(); };
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
      setTimeout(doNext, displayDelay);
    }

    this.onDoneTasks = function () {};

    function onkeypress(task, ev) {
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
      self.finishTask(task, false);
    };

    this.onFinishTask = function (task, answeredSame, willShowResults) {};

    this.finishTask = function (task, answeredSame, shouldShowResults) {
      doOnKeypress = function () {};
      if (shouldShowResults === undefined) shouldShowResults = true;
      self.onFinishTask(task, answeredSame, shouldShowResults);
      if (self.doneWithTasks()) { 
        $(document).unbind('keypress', actualDoOnKeypress);
        doOnKeypress = function () { console.log("Detachment of keypress event failed."); alert("Something went wrong.  Why am I here?"); };
        showResults(task, answeredSame,
            function () { tasks.hide();  self.onDoneTasks(); });
      } else {
        if (self.getCurrentTaskNumber() % displayEvery == 0 && shouldShowResults)
          showResults(task, answeredSame);
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

