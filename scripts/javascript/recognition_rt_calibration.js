var CalibrationTasks;
(function (calibrationResultsDivSelector, calibrationTaskNumberSelector, 
           calibrationTaskTotalSelector, calibrationLetterDivSelectors, 
           calibrationTasksDivSelector, defaultLetters, defaultHiders, 
           defaultTotalTasks, defaultDelayRange, calibrationDisplaySelector,
           defaultDisplayEvery, defaultDisplayDelay,
           $, jQuery, undefined) {
  $(function () { $(calibrationTasksDivSelector).hide(); });
  CalibrationTasks = function (onDoneTasks, totalTasks, 
      defaultCharacters, defaultHiderCharacters) {
    RTTasks.apply(this, ['calibration_',
      defaultDelayRange, defaultDisplayEvery, defaultDisplayDelay, 
      calibrationResultsDivSelector, calibrationTaskNumberSelector,
      calibrationTaskTotalSelector, calibrationTasksDivSelector, "#calibration-display"]);

    if (defaultHiderCharacters === undefined) defaultHiderCharacters = defaultHiders;
    if (totalTasks === undefined) totalTasks = defaultTotalTasks;
    var calibrationLetters = jQuery.map(calibrationLetterDivSelectors, 
      function (selector) { return $(selector); });
    var self = this; // so that calling functions from somewhere else doesn't break things

    this.prepTask = function (task) {
      var hiderCharacters = task['hiderCharacters'] || defaultHiderCharacters;
      jQuery.each(calibrationLetters, function (index, elem) {
          if (hiderCharacters[index])
            elem.html(hiderCharacters[index]);
          else
            elem.html(hiderCharacters);
        });
    };

   
    this.showPrompt = function (task) {
      var characters = task['characters'] || defaultLetters;
      jQuery.each(calibrationLetters, function (index, elem) {
          if (characters[index])
            elem.html(characters[index]);
          else
            elem.html(characters);
        });
    }

    for (var i = 0; i < totalTasks; i++) {
      this.pushTask({'characters':(defaultCharacters || defaultLetters),
          'hiderCharacters':(defaultHiderCharacters || defaultHider)});
    }

    this.onDoneTasks = onDoneTasks;
  };
})("#calibration-results", "#calibration-task-number", 
  "#calibration-task-total",
  ["#calibration-letter-1", "#calibration-letter-2"],
  "#calibration-tasks", ["B", "D"], "#", 25, [600, 1000],
  "#calibration-display",
  1, 1000,
  jQuery, jQuery);
