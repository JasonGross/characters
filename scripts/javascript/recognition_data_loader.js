function makeBoxForImage(image) {
  var imageBox = $('<div>')
    .addClass('image-box image-holder')
    .attr('id', 'image-box-for-' + image.attr('id'))
    .attr('name', 'image-box-for-' + image.attr('name'));
//  var imageInnerBox = $('<div>')
//    .addClass('image-inner-box image-holder');
  /*var imageHolder = $('<span>')
    .addClass('wraptocenter image-holder')
    .attr('id', 'image-holder-for-' + image.attr('id'))
    .attr('name', 'image-holder-for' + image.attr('name'));*/
  imageBox.append(image);
  //imageBox.append(imageHolder);
  //imageOuterBox.append(imageInnerBox);
  return imageBox;
}

var firstTask = null;

(function ($) {
  var progressHolder;
  var totalTasks;
  var progressBar;
  var progressMessage;
  var acceptButton;
  var removeOnAccept;
  var allTasksDiv;
  $(function () { 
    progressHolder = $('#loading-progress');
    progressBar = $('#loading_progress').progressbar({value:0});
    acceptButton = $('#accept_task-button');
    removeOnAccept = $('.pre-task');
    allTasksDiv = $('#all-tasks');
    var ellipsis = $('<span>').append('..');
    var count = 2;
    var maxCount = 3;
    progressMessage = $('#loading_message')
      .append($('<p>').append('Loading information about what tasks to give you').append(ellipsis));
    ellipsisTime = 500;
    ellipsisFunc = function () {
      if (ellipsis) {
        if (count == maxCount) {
          count = 0;
          ellipsis.html('');
        } else {
          count++;
          ellipsis.append('.');
        }
        setTimeout(ellipsisFunc, ellipsisTime);
      }
    };
    ellipsisFunc();
  });
  
  function loadImages(imagePairs) {
    totalTasks = imagePairs.length;
    var totalImages = totalTasks * 3;
    refcounter.setCounter('image progress', totalImages);
    $(function () {
      progressMessage.children().remove();
      var progressLoaded = $('<span>').append('0')
      progressMessage
        .append('Loading images.  ')
        .append(progressLoaded)
        .append(' of ' + totalImages + ' done.');
      progressBar.progressbar('option', 'value', 0);
      refcounter.handleCounterChange('image progress', function (value) {
        progressBar.progressbar('option', 'value', 100 * (totalImages - value) / totalImages);
        progressLoaded.html(totalImages - value);
      });
      refcounter.handleCounterZero('image progress', function () {
        console.log($('.warning .error'));
        console.log(($('.warning .error') ? true : false));
        if (!$('.warning .error'))
          acceptButton.attr('disabled', '');
        progressHolder.hide();
      });
    });
    
    jQuery.each(imagePairs, function (index, imagePair) {
      firstTask = makeTask(index, imagePair[0], imagePair[1], imagePair[2], firstTask);
    });
    
    acceptButton.submit(function () {
      removeOnAccept.remove();
      allTasksDiv.append(firstTask['dom-element']);
      firstTask['do-task']();
    });
  }
  
  function makeTask(index, exampleImageObject, testImageObject, noiseImageUrl, nextTask) {
    var task = $('<div>');
    var taskFieldSet = $('<fieldset>')
      .append($('<legend>').append('Task ' + (index + 1) + ' of ' + totalTasks))
      .addClass('task-holder');
    var example = $('<div>')
      .addClass('example-holder');
    var test = $('<div>')
      .addClass('test-holder');
    var question = $('<div>')
      .addClass('question-holder')
    
    // Example
    var exampleImage = $('<img>')
        .attr('src', exampleImageObject['anonymous url'])
        .attr('alt', 'Example image for task ' + (index + 1) + '.')
        .addClass('example-image')
        .load(function () { refcounter.decrementCounter('image progress'); });
    var testImage = $('<img>')
        .attr('src', testImageObject['anonymous url'])
        .attr('alt', 'Test image for task ' + (index + 1) + '.')
        .addClass('test-image')
        .load(function () { refcounter.decrementCounter('image progress'); });
    var noiseImage = $('<img>')
        .attr('src', noiseImageUrl)
        .attr('alt', 'Noise image for task ' + (index + 1) + '.')
        .addClass('noise-image')
        .load(function () { refcounter.decrementCounter('image progress'); });
    
    var exampleHeader = $('<div>')
      .addClass('example-header')
      .append('Example Image');
    var testHeader = $('<div>')
      .addClass('example-header')
      .append('Test Image');
    var questionFields = $('<fieldset>');
    var questionLegend = $('<legend>').append('Are these images examples of the same character?');
    var questionInputYes = $('<label>').append(
      $('<input>')
        .attr('type', 'radio')
        .attr('name', 'task-' + index + '_question')
        .attr('id', 'task-' + index + '_question-yes')
        .attr('value', 1)
      ).append(
        'Yes, they are the same.'
      );
    var questionInputNo = $('<label>').append(
      $('<input>')
        .attr('type', 'radio')
        .attr('name', 'task-' + index + '_question')
        .attr('id', 'task-' + index + '_question-no')
        .attr('value', 0)
      ).append(
        'No, they are different.'
      );
      
    var exampleImageHolder = $('<div>')
      .addClass('example-image-holder');
    var testImageHolder = $('<div>')
      .addClass('test-image-holder');
      
    example.append(exampleHeader).append(exampleImageHolder);    
    test.append(testHeader).append(testImageHolder);
   
    questionLegend.append(questionInputYes).append($('<br>')).append(questionInputNo);
    questionFields.append(questionLegend);
    question.append(questionFields);
    taskFieldSet.append(example).append(test).append(question);
    task.append(taskFieldSet);
    
    allTasksDiv.append(task);
    
    var doneTask = function () {
      example.remove();
      test.remove();
      task.hide();
      task.parent().append(nextTask['dom-element']);
      nextTask['do-task']();
    };
    
    var doTask = function () {
      //task.show();
    };

    return {'dom-element':task, 'do-task':doTask};
  }
  
  function makeInputs(data) {
    
    var tasksContainer = $('#all-tasks');
    loadImages(data);
    
    /*jQuery.each(tasks, function (index, task) {
      tasksContainer.append(task['dom-element']);
    });*/
    doneLoading();
  }
  notYetLoaded();
  $(function () {
      $.getJSON("../scripts/python/characters.py", 
        urlParameters.getURLParameters(['numberOfAlphabets', 'exampleCharactersPerAlphabet', 'sameTestCharactersPerAlphabet',
                                        'differentTestCharactersPerAlphabet', 'differentAlphabetTestCharactersPerAlphabet', 'distractWithAll']),
        makeInputs);
    });
})(jQuery);
