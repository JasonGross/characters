var CompletionTasks;
(function (resultsDivSelector,
           taskNumberSelector, taskTotalSelector, tasksDivSelector, 
           tag,
           taskDisplaySelector,
           $, jQuery, undefined) {
  var tasksDiv;
  $(function () { tasksDiv = $(tasksDivSelector).hide(); });
  CompletionTasks = function CompletionTasks(data, totalTasks, dataLoader, onDoneTasks) {
    SequentialTasks.call(this, undefined, taskNumberSelector, taskTotalSelector, tasksDivSelector, resultsDivSelector,
                         0, tag);

    var self = this;
    var onLoadImage = dataLoader.thingDone;

    var $canvasHolder;
    var $seenBeforeInputs;
    var $continueButton;
    var updateContinueButton;
    var doFinishTask;

    this.taskDisplay = undefined;

    this.onDoneTasks = onDoneTasks;

    function makeTask(taskIndex, taskData) {
      var rtn = {
        'imageURL':taskData['image']['anonymous url'],
        'canvas':undefined,
        'imageHalf':taskData['imageHalf'],
        'inputs':{}
      };

      var image = $('<img>')
        .load(onLoadImage) // for counting purposes
        .attr('src', rtn['imageURL']);

      rtn['canvas'] = new CompletionCanvas(tag + 'task-' + taskIndex + '-canvas', data['characterSize'], data['characterSize'], image,
                                           rtn['imageHalf']);

      return rtn;
    }

    this.extraTaskInfo = function defaultExtraTaskInfo(task) { return {}; }

    this.onFinishTask = function (task, canvas, willShowResults) {
      self.recordInfo(function (index) { return tag + 'task-' + index + '-strokes'; }, canvas.strokesToString());
      self.recordInfo(function (index) { return tag + 'task-' + index + '-image'; }, canvas.getImage());
      self.recordInfo(function (index) { return tag + 'task-' + index + '-seen-before'; }, getCheckedValue($seenBeforeInputs));
      var extraInfo = self.extraTaskInfo(task);
      if (extraInfo)
        jQuery.each(extraInfo, function (key, value) {
            self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-' + key; }, value);
          });
    };

    this.prepTask = function (task) {
      $canvasHolder.children().remove();

      updateContinueButton = function updateContinueButton() {
        if (task['canvas'].canUndo() && getCheckedValue($seenBeforeInputs) !== '')
          $continueButton.attr('disabled', '');
        else
          $continueButton.attr('disabled', 'disabled');
      };

      doFinishTask = function doFinishTask() {
        if (task['canvas'].canUndo() && getCheckedValue($seenBeforeInputs) !== '') {
          self.finishTask(task, task['canvas']);
          return true;
        } else {
          return false;
        }
      };

      self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-image-anonymous_url'; },
                      task['imageURL']);
      self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-image-show_half'; },
                      task['imageHalf']);

      jQuery.each(task['inputs'], function (key, input) {
          self.recordInput(input);
        });

      $continueButton.attr('disabled', 'disabled');
      setCheckedValue($seenBeforeInputs, '');
      $seenBeforeInputs.change();
    };

    this.doTask = function doTask(task) {
      $canvasHolder.append(task['canvas'].DOMElement);
      task['canvas'].dirty(updateContinueButton);
    };

    this.onBeginTasks = function onBeginTasks() {
      self.taskDisplay = $(taskDisplaySelector);
      $seenBeforeInputs = $('.seen-before')
        .change(function () { updateContinueButton(); });
      $canvasHolder = $('#canvas-holder');
      $continueButton = $('#next-task-button');
      
      $continueButton
        .click(function () {
            $continueButton.attr('disabled', 'disabled');
            return doFinishTask();
          });
    }

    jQuery.each(data['tasks'], function (index, task) {
        self.pushTask(makeTask(index, task));
      });

    return this;
  };
})('#task-results', '.task-number',
  '.task-count', '#all-tasks', '',
  '#task',
  jQuery, jQuery);
