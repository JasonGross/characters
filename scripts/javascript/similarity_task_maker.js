var SimilarityTasks;
(function (resultsDivSelector,
           taskNumberSelector, taskTotalSelector, tasksDivSelector, 
           tag,
           taskDisplaySelector,
           $, jQuery, undefined) {
  var tasksDiv;
  $(function () { tasksDiv = $(tasksDivSelector).hide(); });
  SimilarityTasks = function SimilarityTasks(data, totalTasks, dataLoader, onDoneTasks) {
    SequentialTasks.call(this, undefined, taskNumberSelector, taskTotalSelector, tasksDivSelector, resultsDivSelector,
                         0, tag);

    var self = this;
    var onLoadImage = dataLoader.thingDone;

    var imageHolders = [];
    var $imageHolders = $();
    var similarityInput;
    var $continueButton;

    var sameCount = 0, differentCount = 0, sameSum = 0, differentSum = 0;

    this.taskDisplay = undefined;

    this.onDoneTasks = onDoneTasks;

    function makeTask(taskIndex, taskData) {
      var rtn = {
        'images':[],
        'imageURLs':[],
        'inputs':{},
        'areSame':undefined
      };

      for (var i = 0; i < taskData['images'].length; i++) {
        src = taskData['images'][i]['anonymous url'];
        rtn['images'][i] = $('<img>')
          .attr('src', src)
          .attr('alt', 'Image ' + (i + 1) + ' for task ' + (taskIndex + 1) + '.')
          .addClass('character')
          .hide()
          .load(onLoadImage);
        rtn['imageURLs'][i] = src;
      }
      rtn['areSame'] = taskData['areSame'];

      return rtn;
    }

    this.extraTaskInfo = function defaultExtraTaskInfo(task) { return {}; }

    this.onFinishTask = function (task, answer, willShowResults) {
      if (task['areSame']) {
        sameCount++;
        sameSum += answer;
      } else {
        differentCount++;
        differentSum += answer;
      }
      self.recordInfo(function (index) { return tag + 'task-' + index + '-answer'; }, answer);
      self.recordInfo(function (index) { return tag + 'task-' + index + '-are-same'; }, task['areSame']);
      var extraInfo = self.extraTaskInfo(task);
      if (extraInfo)
        jQuery.each(extraInfo, function (key, value) {
            self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-' + key; }, value);
          });
    };

    this.prepTask = function (task) {
      curTask = task;
      $imageHolders.children().remove();

      jQuery.each(task['imageURLs'], function (index, url) {
          self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-image-' + index + '-anonymous_url'; },
                          url);
        });

      jQuery.each(task['inputs'], function (key, input) {
          self.recordInput(input);
        });

      $continueButton.attr('disabled', 'disabled');
      $similarityInput.attr('value', '').attr('disabled', 'disabled');
    };

    this.doTask = function doTask(task) {
      jQuery.each(task['images'], function (index, image) {
          imageHolders[index].append(image.show());
        });
      $similarityInput.attr('disabled', '');
    };

    function selectAnswer(answer, changeFocus) {
      if (changeFocus === undefined) changeFocus = true;
      if (answer === undefined) answer = '';
      if ($similarityInput.attr('value') != answer)
        $similarityInput.attr('value', answer);
      if (answer === '') {
        $continueButton.attr('disabled', 'disabled');
        return;
      }
      $continueButton.attr('disabled', '');
      if (changeFocus) {
        $continueButton.focus();
      }
    }

    this.resizeImages = function resizeImages(size) {
      $imageHolders.css({'width':size, 'height':size});
    }

    this.resetImageSizes = function resetImageSizes() {
      self.resizeImages(data['characterSize']);
    }

    this.onBeginTasks = function onBeginTasks() {
      self.resetImageSizes();
      self.taskDisplay = $(taskDisplaySelector);
      $similarityInput = $('#similarity-input');
      imageHolders = [$('#image-holder-0'), $('#image-holder-1')];
      $imageHolders = $('#image-holder-0,#image-holder-1');
      $continueButton = $('#next-task-button');
      
      $similarityInput
        .change(function () { selectAnswer(this.value); })
        .keyup(function () { selectAnswer($similarityInput.attr('value'), false); })
        .keydown(function () { selectAnswer($similarityInput.attr('value'), false); });

      $continueButton
        .click(function () { self.finishTask(curTask, $similarityInput.attr('value')); return true; }, false);
    }

    jQuery.each(data['tasks'], function (index, task) {
        self.pushTask(makeTask(index, task));
      });

    tasksProgress = new TasksProgress(this.tasksLeftCount());
  };
})('#task-results', '.task-number',
  '.task-count', '#all-tasks', '',
  '#task',
  jQuery, jQuery);
