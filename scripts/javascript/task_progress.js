var TasksProgress;
(function (defaultTaskProgressSelector, 
           defaultTaskProgressMessageSelector,
           defaultTaskProgressBarHolderSelector,
           defaultTaskActualProgressBarSelector,
           defaultTaskOverlayProgressBarSelector,
           defaultTaskCorrectProgressBarSelector,
           defaultTaskIncorrectProgressBarSelector,
           defaultTaskCorrectTextSelector,
           defaultTaskIncorrectTextSelector, defaultTaskScoredTextSelector,
           $, jQuery, undefined) {
  TasksProgress = function (totalTasks, 
      taskProgressSelector,
      taskProgressMessageSelector, taskProgressBarHolderSelector,
      taskActualProgressBarSelector, taskOverlayProgressBarSelector,
      taskCorrectProgressBarSelector,
      taskIncorrectProgressBarSelector, taskCorrectTextSelector,
      taskIncorrectTextSelector, taskScoredTextSelector) {

    var taskProgress = $(taskProgressSelector || defaultTaskProgressSelector);
    taskProgress.html(taskProgress.html().replace(/>(\s|\n)+</g, '><')); // this must be up here, or we lose the elements the following variables point to
    var taskProgressMessage = $(taskProgressMessageSelector || defaultTaskProgressMessageSelector);
    var taskProgressBarHolder = $(taskProgressBarHolderSelector || defaultTaskProgressBarHolderSelector);
    var taskActualProgressBar = $(taskActualProgressBarSelector || defaultTaskActualProgressBarSelector).progressbar({value:0});
    var taskOverlayProgressBar = $(taskOverlayProgressBarSelector || defaultTaskOverlayProgressBarSelector);
    var taskCorrectProgressBar = $(taskCorrectProgressBarSelector || defaultTaskCorrectProgressBarSelector);
    var taskIncorrectProgressBar = $(taskIncorrectProgressBarSelector || defaultTaskIncorrectProgressBarSelector);
    
    var taskCorrectText = $(taskCorrectTextSelector || defaultTaskCorrectTextSelector);
    var taskIncorrectText = $(taskIncorrectTextSelector || defaultTaskIncorrectTextSelector);
    var taskScoredText = $(taskScoredTextSelector || defaultTaskScoredTextSelector);

    var self = this;

    var numRight = 0, numWrong = 0, numOther = 0;
    

    taskProgress.show();
    taskCorrectProgressBar.height(taskActualProgressBar.height());
    taskIncorrectProgressBar.height(taskActualProgressBar.height());
    taskOverlayProgressBar.height(taskActualProgressBar.height());
    taskProgress.hide();

    this.addCorrect = function (addNumRight) {
      if (addNumRight === undefined) addNumRight = 1;
      numRight += addNumRight;
      self.updateProgress();
    };

    this.addIncorrect = function (addNumWrong) {
      if (addNumWrong === undefined) addNumWrong = 1;
      numWrong += addNumWrong;
      self.updateProgress();
    };

    this.addOther = function (addNumOther) {
      if (addNumOther === undefined) addNumOther = 1;
      numOther += addNumOther;
      self.updateProgress();
    };

    this.updateProgress = function (newNumRight, newNumWrong, newNumOther) {
      if (newNumRight !== undefined) numRight = newNumRight;
      if (newNumWrong !== undefined) numWrong = newNumWrong;
      if (newNumOther !== undefined) numOther = newNumOther;
      taskCorrectProgressBar.width(numRight * 100.0 / totalTasks + '%');
      taskIncorrectProgressBar.width(numWrong * 100.0 / totalTasks + '%');
      taskActualProgressBar.progressbar('option', 'value', (numRight + numWrong + numOther) * 100.0 / totalTasks);
      taskCorrectText.html(numRight);
      taskIncorrectText.html(numWrong);
      taskScoredText.html(numRight + numWrong + numOther);
    };

    this.showProgress = function () { taskProgress.show(); };
    this.hideProgress = function () { taskProgress.hide(); };
  };
})('.task-progress', '.task-message', '.task-progress-bar-holder',
   '.task-actual-progress-bar', '.task-overlay-progress-bar-holder',
   '.task-correct-progress-bar', '.task-incorrect-progress-bar',
   '#task-progress-message-num-tasks-correct',
   '#task-progress-message-num-tasks-incorrect',
   '#task-progress-message-num-tasks-known',
   jQuery, jQuery);
