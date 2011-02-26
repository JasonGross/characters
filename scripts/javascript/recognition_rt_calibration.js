var calibrationTasks;
(function (calibrationResultsDivSelector, calibrationTaskNumberSelector, 
           calibrationTaskTotalSelector, calibrationLetterDivSelector, 
           calibrationTasksDivSelector, defaultLetter, defaultHider, 
           defaultTotalTasks, defaultDelayRange, calibrationDisplaySelector,
           defaultDisplayEvery, defaultDisplayDelay,
           $, jQuery, undefined) {
  $(function () { $(calibrationTasksDivSelector).hide(); });
  calibrationTasks = function (onDoneTasks, totalTasks, defaultHiderCharacter,
        delayRange, displayEvery, displayDelay) {
    if (totalTasks === undefined) totalTasks = defaultTotalTasks;
    if (defaultHiderCharacter === undefined) defaultHiderCharacter = defaultHider;
    if (delayRange === undefined) delayRange = defaultDelayRange;
    if (onDoneTasks === undefined) onDoneTasks = function () {};
    if (displayEvery === undefined) displayEvery = defaultDisplayEvery;
    if (displayDelay === undefined) displayDelay = defaultDisplayDelay;
    var calibrationResults = $(calibrationResultsDivSelector);
    var calibrationTaskNumber = $(calibrationTaskNumberSelector);
    var calibrationTaskTotal = $(calibrationTaskTotalSelector);
    var calibrationLetters = $(calibrationLetterDivSelector);
    var calibrationTasks = $(calibrationTasksDivSelector);
    var calibrationAverageSpan, calibrationLastSpan;
    var totalReactionTime = 0;
    var lastReactionTime;
    var lastStartTime;
    var curTaskNumber = 0;
    var curTimeInputs = {};
    var curKeypress;
    var timeoutId;
    var falsePositives = 0;
    var doOnKeypress = function () {};
    var actualDoOnKeypress = function () {
      doOnKeypress.apply(this, arguments);
    };
    var self = this; // so that calling functions from somewhere else doesn't break things
    calibrationTaskTotal.html(totalTasks);
    calibrationTaskNumber.html(1);
    var calibrationDisplayResults = $(calibrationDisplaySelector).append($('<p>')
        .append('Average Reaction Time: ')
        .append(calibrationAverageSpan = $('<span>'))
        .append(' ms'))
      .append($('<p>')
        .append('Most Recent Reaction Time: ')
        .append(calibrationLastSpan = $('<span>'))
        .append(' ms'));


    function getNextDelay() {
      return delayRange[0] + Math.random() * delayRange[1];
    }

    this.doneWithTasks = function () { return curTaskNumber >= totalTasks; }

    function makeNextTask() {
      calibrationTaskNumber.html(curTaskNumber + 1);

      jQuery.each(['doTask', 'showCharacters', 'keypress'],
        function (index, name) {
          curTimeInputs[name] = makeInput('calibration-' + curTaskNumber + '-time-of-' + name);
          calibrationResults.append(curTimeInputs[name]);
        });

      curKeypress = makeInput('calibration-' + curTaskNumber + '-keypress');

    }

    function doNextTask(make, hiderCharacter, delay, character) {
      console.log('doNextTask');
      doOnKeypress = function () {};
      if (hiderCharacter === undefined) hiderCharacter = defaultHiderCharacter;
      if (delay === undefined) delay = getNextDelay();
      if (make === undefined) make = true;
      calibrationLetters.html(hiderCharacter);
      calibrationDisplayResults.hide();
      if (make) makeNextTask();

      curTimeInputs['doTask'].attr('value', dateUTC(new Date()));

      timeoutId = setTimeout(function () { showCharacters(character); }, delay);
      doOnKeypress = function () { badKeypress(); };
    };

    function badKeypress() {
      clearTimeout(timeoutId);
      alert("Please wait until after the prompt to press a key");
      doNextTask(false);
      falsePositives++;
    }

    function showCharacters(character) {
      if (character === undefined) character = defaultLetter;
      curTimeInputs['showCharacters'].attr('value', lastStartTime = dateUTC(new Date()));
      calibrationLetters.html(character);
      $('body').focus();
      doOnKeypress = function () { onkeypress.apply(this, arguments); };
    }

    function showResults(doNext) {
      if (doNext === undefined) doNext = doNextTask;
      if (curTaskNumber != 0)
        calibrationAverageSpan.html(totalReactionTime / curTaskNumber);
      else
        calibrationAverageSpan.html('Weird error: curTaskNumber = 0.  totalReactionTime = ' + totalReactionTime);
      calibrationLastSpan.html(lastReactionTime);
      calibrationDisplayResults.show();
      setTimeout(doNext, displayDelay);
    }

    function onkeypress(ev) {
      doOnKeypress = function () {};
      curTimeInputs['keypress'].attr('value', lastReactionTime = dateUTC(new Date()));
      lastReactionTime -= lastStartTime;
      totalReactionTime += lastReactionTime;
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
      curTaskNumber++;
      if (self.doneWithTasks()) { 
         calibrationResults.append(makeInput('calibration-false_positives', falsePositives));
         $(document).unbind('keypress', actualDoOnKeypress);
         doOnKeypress = function () { console.log("Detachment of keypress event failed."); alert("Something went wrong.  Why am I here?"); };
         showResults(function () { calibrationTasks.hide();  onDoneTasks(); });
      } else {
        if (curTaskNumber % displayEvery == 0)
          showResults();
        else
          doNextTask();
      }
    };

    this.startTasks = function () {
      calibrationTasks.show();
      $(document).bind('keypress', actualDoOnKeypress);
      if (!(self.doneWithTasks())) doNextTask();
      self.startTasks = undefined;
    };
    
  };
})("#calibration-results", "#calibration-task-number", 
  "#calibration-task-total", "#calibration-letter-1,#calibration-letter-2",
  "#calibration-tasks", "B", "#", 25, [600, 1000], "#calibration-display",
  1, 1000,
  jQuery, jQuery);
