var TasksBreak;
(function (defaultBreakDivSelector,
           $, jQuery, undefined) {
  TasksBreak = function (progressPause, breakDivSelector,
      canSeeProgress) {

    var breakDiv = $(breakDivSelector || defaultBreakDivSelector).hide();
    var actualAfterBreak = function () {
      var curAfterBreak = afterBreak;
      afterBreak = function () {};
      self.isBreaking = false;
      breakDiv.hide();
      curAfterBreak.apply(this, arguments);
    };
    var afterBreak = function () {};
    var message = 'You have completed a group of tasks.  You may take a short break';
    var messageP = $('<p>');
    var messageButton;
    var waitForClick = (progressPause <= 0);
    var self = this;
    if (canSeeProgress === undefined) canSeeProgress = true;
    if (!waitForClick)
      message += ' of about ' + progressPause / 1000.0 + ' seconds';
    if (canSeeProgress)
      message += ' and see your progress, below';
    message += '.';
    messageP.append($('<span>').append(message));
    if (waitForClick)
      messageP.append($('<span>').append('  When you are ready to move on, click '));
    if (waitForClick)
      messageP.append(messageButton = $('<input>')
          .attr('type', 'submit')
          .attr('name', 'finish_break')
          .attr('id', 'finish_break')
          .attr('value', 'here')
          .click(actualAfterBreak))
        .append($('<span>').append('.'));
    breakDiv.append(messageP);

    this.isBreaking = false;

    this.makeBreak = function (doAfterBreak, newMessageMaker) {
      self.isBreaking = true;
      if (newMessageMaker !== undefined) {
        messageP.children().detach();
        messageP.append(newMessageMaker(messageButton));
      }
      afterBreak = doAfterBreak;
      breakDiv.show();
      if (!waitForClick)
        setTimeout(actualAfterBreak, progressPause);
    };
  };
})('.task-break', jQuery, jQuery);
