var RecognitionRTTasks;
(function (delayRange, displayEvery, displayDelay, resultsDivSelector,
           taskNumberSelector, taskTotalSelector, tasksDivSelector, 
           displaySelector, tag, defaultSameDelay, 
           $, jQuery, undefined) {
  var noiseImageURLs = [];
  for (var i = 0; i < 10; i++) {
    noiseImageURLs.push('http://jgross.scripts.mit.edu/alphabets/images/strokeNoise' + i + '.png');
  }
  $(function () { $(tasksDivSelector).hide(); });
  RecognitionRTTasks = function (data, totalTasks, dataLoader, onDoneTasks, 
      sameDelay) {
    RTTasks.apply(this, [tag,
      delayRange, displayEvery, displayDelay,
      resultsDivSelector, taskNumberSelector, taskTotalSelector,
      tasksDivSelector, displaySelector, sameDelay]);

    var self = this;
    var onLoadImage = dataLoader.thingDone;
    var $results = $(resultsDivSelector);
    if (sameDelay === undefined) sameDelay = defaultSameDelay;


    function makeTask(taskIndex, imagePair) {
      var rtn = {
        'noiseImages':[],
        'noiseImageURLs':[],
        'letters':[],
        'letterURLs':[],
        'inputs':{},
        'are-same':imagePair[3]
      };
      for (var i = 0; i < 5; i++) {
        var src = noiseImageURLs[Math.floor(Math.random() * noiseImageURLs.length)];
        rtn['noiseImages'][i] = $('<img>')
          .attr('src', src)
          .attr('alt', 'Noise image for task ' + (taskIndex + 1) + '.')
          .addClass('noise-image')
          .hide()
          .load(onLoadImage);
        rtn['noiseImageURLs'][i] = src;
      }
      for (var i = 0; i < 2; i++) {
        var src = imagePair[i]['anonymous url'];
        rtn['letters'][i] = $('<img>')
          .attr('src', src)
          .attr('alt', 'Image ' + (i + 1) + ' for task ' + (taskIndex + 1) + '.')
          .addClass('rt-symbol')
          .hide()
          .load(onLoadImage);
        rtn['letterURLs'][i] = src;
      }
      return rtn;
    }

    this.prepTask = function (task, taskIndex) {
      $('.rt-symbol-holder').each(function (index) {
          var $this = $(this);
          $this.children().remove();
          $this.append(task['noiseImages'][index].show());
          $results.append(makeInput(tag + '-' + taskIndex + '-noise-image-' + index + '-url')
            .attr('value', task['noiseImageURLs'][index]));
        });

      jQuery.each(task['letterURLs'], function (index, url) {
          $results.append(makeInput(tag + '-' + taskIndex + '-character-' + index + '-url')
            .attr('value', url));
        });

      $results.append(makeInput(tag + '-' + taskIndex + '-are-same')
          .attr('value', task['are-same']));
    };
    
    this.showPrompt = function (task) {
      $('.rt-character-holder').each(function (index) {
          var $this = $(this);
          $this.children().remove();
          $this.append(task['letters'][index].show());
      });
      sameTimeoutId = setTimeout(self.finishTask, sameDelay);
    };

    this.onFinishTask = function () {
      clearTimeout(sameTimeoutId);
    }



    jQuery.each(data['tasks'], function (index, imagePair) {
        self.pushTask(makeTask(index, imagePair));
      });
  };
})([600, 1000], 1, 1000, '#rt-results', '#task-number',
  '#task-total', '#all-tasks', "#rt-display", 
  'recognition-rt-task', 4000, jQuery, jQuery);
