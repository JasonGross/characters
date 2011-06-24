var SequentialTasks;
(function (defaultDisplayEvery, $, jQuery, undefined) {
  SequentialTasks = function SequentialTasks(taskList, currentTaskNumberSelector, taskCountSelector, allTasksSelector, resultsSelector, displayEvery, tag) {
    if (taskList === undefined) taskList = [];
    var tasksLeft = taskList.slice(0); // copy array of tasks
    var curTaskNumber = -1;
    var self = this;
    this.peekNextTask = function () { return tasksLeft[0]; };
    this.takeNextTask = function () { 
      curTaskNumber++;
      return tasksLeft.shift(); 
    };
    this.pushTask = function () { tasksLeft.push.apply(tasksLeft, arguments); };
    this.insertTask = function (index) {
      if (index === undefined)
        index = Math.floor(Math.random() * (tasksLeft.length + 1));
      tasksLeft.splice.apply(tasksLeft, [index, 0] + arguments.slice(1));
    };
    this.tasksLeftCount = function () { return tasksLeft.length; };
    this.doneWithTasks = function () { return self.tasksLeftCount() <= 0; };
    this.getCurrentTaskNumber = function () { return curTaskNumber; };

    /* methods for display */
    var currentTaskNumberDisplay;
    var taskCountDisplay;
    this.tasksDisplay = undefined;
    var results;
    if (displayEvery === undefined) displayEvery = defaultDisplayEvery;
    if (tag === undefined) tag = 'sequential-';

    this.recordInput = function recordInput(input, value) {
      if (value !== undefined) $(input).attr('value', value);
      results.append(input);
    }

    this.recordInfo = function recordInfo(nameFunc, value) {
      var input = makeInput(nameFunc(self.getCurrentTaskNumber()));
      self.recordInput(input, value);
      return input;
    }

    this.beforeTask = function beforeTask(task, callback) { callback(); };

    this.prepTask = function prepTask(task) {};

    this.doTask = function doTask(task) {};

    this.doNextTask = function doNextTask() {
      if (self.doneWithTasks()) return false;
      var task = self.takeNextTask();
      self.beforeTask(task, function () {
        self.prepTask.apply(self, [task].concat(Array.prototype.slice.call(arguments)));
        currentTaskNumberDisplay.html(self.getCurrentTaskNumber() + 1);
        self.recordInfo(function (num) { return tag + 'task-' + num + '-time-of-do-task'; }, dateUTC(new Date()));
        self.doTask.apply(self, [task].concat(Array.prototype.slice.call(arguments)));
      });
    };


    this.showResults = function showResults(task, answer, doNext) { doNext(); };

    this.onFinishTask = function onFinishTask(task, answer, willShowResults) {};

    this.finishTask = function finishTask(task, answer, shouldShowResults) {
      console.log(displayEvery);
      if (shouldShowResults === undefined) shouldShowResults = true;
      self.onFinishTask(task, answer, shouldShowResults);
      if (self.doneWithTasks()) {
        self.showResults(task, answer, 
                         function () { self.tasksDisplay.hide(); self.onDoneTasks(); });
      } else {
        if (displayEvery > 0 && self.getCurrentTaskNumber() > 0 &&
            (self.getCurrentTaskNumber() % displayEvery) == 0 && shouldShowResults)
          self.showResults(task, answer, self.doNextTask);
        else
          self.doNextTask();
      }
    };

    this.onBeginTasks = function onBeginTasks() {};
    this.onBeginTasksAfterDisplay = function onBeginTasksAfterDisplay() {};

    this.startTasks = function startTasks() {
      self.startTasks = undefined;
      currentTaskNumberDisplay = $(currentTaskNumberSelector);
      taskCountDisplay = $(taskCountSelector);
      self.tasksDisplay = $(allTasksSelector);
      results = $(resultsSelector).hide();
      
      taskCountDisplay.html(self.tasksLeftCount());
      currentTaskNumberDisplay.html(1);
      self.onBeginTasks();
      self.tasksDisplay.show();
      self.onBeginTasksAfterDisplay();
      if (!self.doneWithTasks())
        self.doNextTask();
    };
  }
})(10, jQuery, jQuery);
