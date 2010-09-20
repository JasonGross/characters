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

var tasks = [];

(function ($) {
  var totalTasks;
  var progressBar;
  var progressMessage;
  $(function () { 
    progressBar = $('#loading_progress');
    var ellipsis = $('<span>').append('..');
    var count = 2;
    var maxCount = 3;
    progressMessage = $('#loading_message')
      .append($('<p>').append('Loading information about what tasks to give you').append(ellipsis));
    ellipsisTime = 1000;
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
        progressBar.progressbar('option', 'value', totalImages - value);
        progressLoaded.html(totalImages - value);
      });
    });
    
    jQuery.each(imagePairs, function (index, imagePair) {
      tasks.push(makeTask(index, imagePair[0], imagePair[1], imagePair[2]));
    });
  }
  
  function makeTask(index, exampleImageUrl, testImageUrl, noiseImageUrl) {
    var task = $('<div>').hide();
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
        .attr('src', exampleImageUrl)
        .attr('alt', 'Example image for task ' + (index + 1) + '.')
        .load(function () { refcounter.decrementCounter('image progress'); });
    var testImage = $('<img>')
        .attr('src', testImageUrl)
        .attr('alt', 'Test image for task ' + (index + 1) + '.')
        .load(function () { refcounter.decrementCounter('image progress'); });
    var noiseImage = $('<img>')
        .attr('src', noiseImageUrl)
        .attr('alt', 'Noise image for task ' + (index + 1) + '.')
        .load(function () { refcounter.decrementCounter('image progress'); });


    return {'dom-element':task};
  }
  
  function makeInputs(data) {
    
    var tasksContainer = $('#all-tasks');
    loadImages(data);
    
    jQuery.each(tasks, function (index, task) {
      tasksContainer.append(task['dom-element']);
    });
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
