var CalibrationTasks;
(function (calibrationResultsDivSelector, calibrationTaskNumberSelector, 
           calibrationTaskTotalSelector, calibrationLetterDivSelector, 
           calibrationTasksDivSelector, defaultLetter, defaultHider, 
           defaultTotalTasks, defaultDelayRange, calibrationDisplaySelector,
           defaultDisplayEvery, defaultDisplayDelay,
           $, jQuery, undefined) {
  $(function () { $(calibrationTasksDivSelector).hide(); });
  CalibrationTasks = function (onDoneTasks, totalTasks, 
      defaultCharacter, defaultHiderCharacter) {
    RTTasks.apply(this, ['calibration',
      defaultDelayRange, defaultDisplayEvery, defaultDisplayDelay, 
      calibrationResultsDivSelector, calibrationTaskNumberSelector,
      calibrationTaskTotalSelector, calibrationTasksDivSelector, "#calibration-display"]);

    if (defaultHiderCharacter === undefined) defaultHiderCharacter = defaultHider;
    if (totalTasks === undefined) totalTasks = defaultTotalTasks;
    var calibrationLetters = $(calibrationLetterDivSelector);
    var self = this; // so that calling functions from somewhere else doesn't break things

    this.prepTask = function (task) {
      var hiderCharacter = task['hiderCharacter'] || defaultHiderCharacter;
      calibrationLetters.html(hiderCharacter);
    };

   
    this.showPrompt = function (task) {
      var character = task['character'] || defaultLetter;
      calibrationLetters.html(character);
    }

    for (var i = 0; i < totalTasks; i++) {
      this.pushTask({'character':(defaultCharacter || defaultLetter),
          'hiderCharacter':(defaultHiderCharacter || defaultHider)});
    }

    this.onDoneTasks = onDoneTasks;
  };
})("#calibration-results", "#calibration-task-number", 
  "#calibration-task-total", "#calibration-letter-1,#calibration-letter-2",
  "#calibration-tasks", "B", "#", 25, [600, 1000], "#calibration-display",
  1, 1000,
  jQuery, jQuery);
