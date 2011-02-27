var SequentialTasks;
(function ($, jQuery, undefined) {
  SequentialTasks = function (taskList) {
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
  };
})(jQuery, jQuery);
