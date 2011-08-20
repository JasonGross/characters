var DuplicationTasks;
(function (resultsDivSelector,
           taskNumberSelector, taskTotalSelector, tasksDivSelector, 
           tag,
           taskDisplaySelector,
           $, jQuery, undefined) {
  var noiseImageURLs = [];
  for (var i = 0; i < 10; i++) {
    noiseImageURLs.push('//jgross.scripts.mit.edu/alphabets/images/strokeNoise' + i + '.png');
  }
  DuplicationTasks = function DuplicationTasks(data, totalTasks, dataLoader, onDoneTasks) {
    SequentialTasks.call(this, undefined, taskNumberSelector, taskTotalSelector, tasksDivSelector, resultsDivSelector,
                         0, tag);

    var self = this;
    var onLoadImage = dataLoader.thingDone;

    var canvas;
    var $continueButton;
    var $didNotSeeButton;
    var exampleImageHolders;
    var $examplesHolder = $();
    var $imageHolders = $();
    var doFinishTask;
    var deferTask;
    var timed = (data['exampleClassCount'] <= 1 && data['examplePerClassCount'] <= 1);

    var curTask;

    this.taskDisplay = undefined;

    if (!timed)
      data['pauseToNoise'] = [0];

    HintedTasks.call(this,
                     jQuery.map(['pauseToFirstHint', 'pauseToSecondHint', 'pauseToExample', 'pauseToNoise'], function (tag) {
                                  return data[tag][0];
                                }),
                     jQuery.map(['first-hint', 'second-hint', 'show-examples', 'noise'], function (keyword) {
                                  return function (index) { return tag + 'task-' + index + '-time-of-' + keyword; };
                                }),
                     [showFirstHint, showSecondHint, showExamples, showNoise],
                     self.recordInfo);

    this.onDoneTasks = onDoneTasks;

    function makeTask(taskIndex, taskData) {
      var rtn = {
        'noiseImages':[],
        'noiseImageURLs':[],
        'exampleImages':[],
        'exampleImageURLs':[],
        'inputs':{},
        'pauseToHints':undefined,
        'timed':timed
      };

      for (var i = 0; i < taskData['images'].length; i++) {
        rtn['noiseImages'][i] = [];
        rtn['noiseImageURLs'][i] = [];
        rtn['exampleImages'][i] = [];
        rtn['exampleImageURLs'][i] = [];
        for (var j = 0; j < taskData['images'][i].length; j++) {
          var src = noiseImageURLs[Math.floor(Math.random() * noiseImageURLs.length)];
          rtn['noiseImages'][i][j] = $('<img>')
            .attr('src', src)
            .attr('alt', 'Noise image ' + (i + 1) + ' for class ' + (j + 1) + ' for task ' + (taskIndex + 1) + '.')
            .addClass('noise-image character')
            .hide()
            .load(onLoadImage);
          rtn['noiseImageURLs'][i][j] = src;

          src = taskData['images'][i][j]['anonymous url'];
          rtn['exampleImages'][i][j] = $('<img>')
            .attr('src', src)
            .attr('alt', 'Example image ' + (i + 1) + ' for class ' + (j + 1) + ' for task ' + (taskIndex + 1) + '.')
            .addClass('example-image character')
            .hide()
            .load(onLoadImage);
          rtn['exampleImageURLs'][i][j] = src;
        }
      }

      if (timed) {
        rtn['pauseToHints'] = jQuery.map(['pauseToFirstHint', 'pauseToSecondHint', 'pauseToExample', 'pauseToNoise'], function (pause) {
                                            if (data[pause][1])
                                              return data[pause][0] + (2 * Math.random() - 1) * data[pause][1];
                                            else
                                              return data[pause][0];
                                          });
      }
      return rtn;
    }

    this.extraTaskInfo = function defaultExtraTaskInfo(task) { return {}; }

    this.onFinishTask = function (task, canvas, willShowResults) {
      self.recordInfo(function (index) { console.log(index); return tag + 'task-' + index + '-strokes'; }, canvas.strokesToString());
      self.recordInfo(function (index) { return tag + 'task-' + index + '-image'; }, canvas.getImage());
      
      jQuery.each(exampleImageHolders, function (classIndex, classHolders) {
        jQuery.each(classHolders, function (exampleIndex, exampleImageHolder) {
          self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-class-' + classIndex + '-noise-image-' + exampleIndex + '-url'; },
                          task['noiseImageURLs'][classIndex][exampleIndex]);
          self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-class-' + classIndex + '-example-image-' + exampleIndex + '-anonymous_url'; },
                          task['exampleImageURLs'][classIndex][exampleIndex]);
        });
      });

      var extraInfo = self.extraTaskInfo(task);
      if (extraInfo)
        jQuery.each(extraInfo, function (key, value) {
            self.recordInfo(function (taskIndex) { return tag + 'task-' + taskIndex + '-' + key; }, value);
          });
    };

    doFinishTask = function doFinishTask() {
      if (canvas.canUndo()) {
        self.finishTask(curTask, canvas);
        return true;
      } else {
        return false;
      }
    };

    this.prepTask = function (task) {
      curTask = task;
      canvas.clear();

      jQuery.each(exampleImageHolders, function (classIndex, classHolders) {
        jQuery.each(classHolders, function (exampleIndex, exampleImageHolder) {
          exampleImageHolder.children().detach();
        });
      });

      $continueButton.attr('disabled', 'disabled');
      $didNotSeeButton.attr('disabled', 'disabled');

      jQuery.each(task['inputs'], function (key, input) {
          self.recordInput(input);
        });

      deferTask = function deferTask() { self.deferTask(task); };
    };

    function updateContinueButton() {
      if (canvas.canUndo())
        $continueButton.attr('disabled', '');
      else
        $continueButton.attr('disabled', 'disabled');
    }

    function jumpToTask() {
      window.location.hash = '';
      window.location.hash = 'task';
      window.location.hash = 'extra-options-form';
    }

    this.doTask = function doTask(task) {
      jumpToTask();
      if (timed) {
        self.beginPrompting(task, task['pauseToHints']);
      } else {
        showExamples(task);
        $examplesHolder.removeClass('prompt-holder-doing');
      }
    };

    function showFirstHint() {
      $examplesHolder.removeClass('prompt-holder-done').addClass('prompt-holder-long');
    };

    function showSecondHint() {
      $examplesHolder.removeClass('prompt-holder-long').addClass('prompt-holder-short');
    };

    function showExamples(task) {
      $examplesHolder.removeClass('prompt-holder-short prompt-holder-done').addClass('prompt-holder-doing');
      jQuery.each(exampleImageHolders, function (classIndex, classHolders) {
        jQuery.each(classHolders, function (exampleIndex, exampleImageHolder) {
          exampleImageHolder.append(task['exampleImages'][classIndex][exampleIndex].show());
        });
      });
      $didNotSeeButton.attr('disabled', '');
    }

    function showNoise(task) {
      $examplesHolder.removeClass('prompt-holder-doing').addClass('prompt-holder-done');
      jQuery.each(exampleImageHolders, function (classIndex, classHolders) {
        jQuery.each(classHolders, function (exampleIndex, exampleImageHolder) {
          exampleImageHolder.children().detach();
          exampleImageHolder.append(task['noiseImages'][classIndex][exampleIndex].show());
        });
      });
    }

    function makeClassHolder(pre_tag, class_holder_class_string, post_tag) {
      if (pre_tag === undefined) pre_tag = '';
      if (post_tag === undefined) post_tag = '';
      if (class_holder_class_string === undefined) class_holder_class_string = '';
      var classBox = $('<div>')
        .addClass('class-box class-box-' + (timed ? 'timed ' : 'untimed ')  + class_holder_class_string)
        .attr('id', pre_tag + 'class-box' + post_tag);
      $examplesHolder = $examplesHolder.add(classBox);
      return classBox;
    }

    function makeImageHolder(pre_tag, img_holder_class_string, post_tag) {
      if (pre_tag === undefined) pre_tag = '';
      if (post_tag === undefined) post_tag = '';
      if (img_holder_class_string === undefined) img_holder_class_string = '';
      var imageBox = $('<div>')
        .addClass('image-box')
        .attr('id', pre_tag + 'box' + post_tag);
      var imageHolder = $('<span>')
        .addClass('wraptocenter image-holder ' + img_holder_class_string)
        .css({'width':data['characterSize'], 'height':data['characterSize']})
        .attr('id', pre_tag + 'image-holder' + post_tag);
      $imageHolders = $imageHolders.add(imageHolder);
      imageBox.append(imageHolder);
      return {'box':imageBox, 'image-holder':imageHolder};
    }

    this.resizeImages = function resizeImages(size) {
      $imageHolders.css({'width':size, 'height':size});
    }

    this.resetImageSizes = function resetImageSizes() {
      self.resizeImages(data['characterSize']);
    }

    this.onBeginTasks = function onBeginTasks() {
      self.taskDisplay = $(taskDisplaySelector);
      canvas = new DrawingCanvas(tag + 'canvas', data['canvasSize'], data['canvasSize']);
      $canvasHolder = $('#canvas-holder')
        .append(canvas.DOMElement);
      canvas.dirty(updateContinueButton);

      $continueButton = $('#next-task-button')
        .click(function () {
            $continueButton.attr('disabled', 'disabled');
            return doFinishTask();
          });

      exampleImageHolders = [];
      var $allExamplesHolder = $('#examples-holder');
      for (var i = 0; i < data['exampleClassCount']; i++) {
        exampleImageHolders[i] = [];
        var classHolder = makeClassHolder();
        $allExamplesHolder.append(classHolder);
        for (var j = 0; j < data['examplePerClassCount']; j++) {
          var example = makeImageHolder();
          classHolder.append(example['box']);
          exampleImageHolders[i][j] = example['image-holder'];
        }
      }

      $didNotSeeButton = $('#did-not-see-button');
      if (timed)
        $didNotSeeButton.click(function () { deferTask(); });
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
