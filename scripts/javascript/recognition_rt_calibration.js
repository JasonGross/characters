var calibrationTasks;
(function (calibrationResultsDivSelector, calibrationTaskNumberSelector, 
           calibrationTaskTotalSelector, calibrationLetterDivSelector, 
           calibrationTasksDivSelector, defaultLetter, defaultHider, 
           defaultTotalTasks, defaultDelayRange, $, jQuery, undefined) {
  $(function () { $(calibrationTasksDivSelector).hide(); });
  calibrationTasks = function (onDoneTasks, totalTasks, defaultHiderCharacter,
        delayRange) {
    if (totalTasks === undefined) totalTasks = defaultTotalTasks;
    if (defaultHiderCharacter === undefined) defaultHiderCharacter = defaultHider;
    if (delayRange === undefined) delayRange = defaultDelayRange;
    if (onDoneTasks === undefined) onDoneTasks = function () {};
    var calibrationResults = $(calibrationResultsDivSelector);
    var calibrationTaskNumber = $(calibrationTaskNumberSelector);
    var calibrationTaskTotal = $(calibrationTaskTotalSelector);
    var calibrationLetters = $(calibrationLetterDivSelector);
    var calibrationTasks = $(calibrationTasksDivSelector);
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

    function getNextDelay() {
      return delayRange[0] + Math.random() * delayRange[1];
    }

    this.doneWithTasks = function () { return curTaskNumber >= totalTasks; }

    function makeNextTask() {
      calibrationTaskNumber.html(curTaskNumber + 1);

      jQuery.each(['doTask', 'showCharacters', 'keypress'],
        function (index, name) {
          curTimeInputs[name] = $('<input>')
            .attr('type', 'hidden')
            .attr('value', '')
            .attr('id', 'calibration-' + curTaskNumber + '-time-of-' + name)
            .attr('name','calibration-' + curTaskNumber + '-time-of-' + name);
          calibrationResults.append(curTimeInputs[name]);
        });

      curKeypress = $('<input>')
        .attr('type', 'hidden')
        .attr('value', '')
        .attr('id', 'calibration-' + curTaskNumber + '-keypress')
        .attr('name','calibration-' + curTaskNumber + '-keypress');


    }

    function doNextTask(make, hiderCharacter, delay, character) {
      console.log('doNextTask');
      doOnKeypress = function () {};
      if (hiderCharacter === undefined) hiderCharacter = defaultHiderCharacter;
      if (delay === undefined) delay = getNextDelay();
      if (make === undefined) make = true;
      calibrationLetters.html(hiderCharacter);
      if (make) makeNextTask();

      curTimeInputs['doTask'].attr('value', dateUTC(new Date()));

      timeoutId = setTimeout(function () { showCharacters(character); }, delay);
      //$('body').keypress(badKeypress);
      doOnKeypress = function () { badKeypress(); };
    };

    function badKeypress() {
      clearTimeout(timeoutId);
      doNextTask(false);
      falsePositives++;
    }

    function showCharacters(character) {
      if (character === undefined) character = defaultLetter;
      curTimeInputs['showCharacters'].attr('value', dateUTC(new Date()));
      calibrationLetters.html(character);
      $('body').focus();
      doOnKeypress = function () { onkeypress.apply(this, arguments); };
    }

    function onkeypress(ev) {
      $('body').unbind('keypress', badKeypress);
      curTimeInputs['keypress'].attr('value', dateUTC(new Date()));
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
      $('body').unbind('keypress', onkeypress);
      if (self.doneWithTasks()) { 
         calibrationResults.append($('<input>')
            .attr('type', 'hidden')
            .attr('value', falsePositives)
            .attr('id', 'calibration-false_positives')
            .attr('name','calibration-false_positive'));
         $('body').unbind('keypress', actualDoOnKeypress);
         calibrationTasks.hide();
         onDoneTasks();
      } else {
        doNextTask();
      }
    };

    this.startTasks = function () {
      calibrationTasks.show();
      $('body').bind('keypress', actualDoOnKeypress);
      if (!(self.doneWithTasks())) doNextTask();
      self.startTasks = undefined;
    };
    
  };
})("#calibration-results", "#calibration-task-number", 
  "#calibration-task-total", "#calibration-letter-1,#calibration-letter-2",
  "#calibration-tasks", "B", "#", 25, [600, 1000], jQuery, jQuery);
