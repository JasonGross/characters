function makeBoxForImage(image) {
  var imageBox = $('<div>')
    .addClass('image-box image-holder')
    .attr('id', 'image-box-for-' + image.attr('id'))
    .attr('name', 'image-box-for-' + image.attr('name'));
  var imageHolder = $('<span>')
    .addClass('wraptocenter image-holder')
    .attr('id', 'image-holder-for-' + image.attr('id'))
    .attr('name', 'image-holder-for' + image.attr('name'));
  imageHolder.append(image);
  imageBox.append(imageHolder);
  return imageBox;
}

(function () {
  function makeTraining(trainingImages, groupNum) {
    if (trainingImages.length <= 1) return '';
    var training = $('<div>')
      .addClass('training training_group_' + groupNum)
      
    var examplesHolder = $('<p>')
      .addClass('examples-holder')
      .append('Example' + (trainingImages.length > 1 ? 's' : '') + ' of character ' + (groupNum + 1) + ': ');
    jQuery.each(trainingImages, function (imageNum, imageObject) {
      examplesHolder.append($('<div>')
        .addClass('example-holder')
        
        .append(makeBoxForImage($('<img>')
          .attr('id', 'group_' + groupNum + '-training_image_' + (imageNum))
          .attr('name', 'group_' + groupNum + '-training_image_' + (imageNum))
          .attr('src', imageObject['anonymous url'])
          .attr('alt', 'Training image ' + (imageNum + 1) + ' for group ' + (groupNum + 1) + '.')
          .attr('draggable', 'false')
          .bind('dragstart', function() { return false; })
        ))
        
        .append($('<input>')
          .attr('type', 'hidden')
          .attr('id', 'group_' + groupNum + '-training_image_' + (imageNum) + '-image_hash')
          .attr('name', 'group_' + groupNum + '-training_image_' + (imageNum) + '-image_hash')
          .attr('value', imageObject['hash'])
        )
      );
    });
    training.append(examplesHolder);
    return training;
  }
  
  function makeTest(testImages, groupNum, trainingImages) {
    var test = $('<div>')
      .addClass('test test_group_' + groupNum)
      
      //.append($('<p>').append('Select whether or not each of the following images is an example of character ' + (groupNum + 1) + ' and how confident you are of this judgement.'))
      ;
    var testsHolder = $('<div>').addClass('tests-holder');
    
    var trainingImage = '';
    if (trainingImages.length == 1)
      trainingImage = $('<span>')
        .append(makeBoxForImage($('<img>')
          .attr('id', 'group_' + groupNum + '-training_image')
          .attr('name', 'group_' + groupNum + '-training_image')
          .attr('src', trainingImages[0]['anonymous url'])
          .attr('alt', 'Training image for group ' + (groupNum + 1) + '.')
          .attr('draggable', 'false')
          .bind('dragstart', function() { return false; })
        ))
        .append($('<input>')
          .attr('type', 'hidden')
          .attr('id', 'group_' + groupNum + '-training_image-image_hash')
          .attr('name', 'group_' + groupNum + '-training_image-image_hash')
          .attr('value', trainingImages[0]['hash'])
        );
            
    jQuery.each(testImages, function (imageNum, imageObject) {
      var testHolderHolder = $('<div>').addClass('test');
      var testHolder = $('<fieldset>')
        .append($('<legend>').append('Test image ' + (imageNum + 1) + ' for character ' + (groupNum + 1)));
      var curTest = $('<p>');
      var testImage = makeBoxForImage($('<img>')
        .attr('id', 'group_' + groupNum + '-test_image_' + (imageNum))
        .attr('name', 'group_' + groupNum + '-test_image_' + (imageNum))
        .attr('src', imageObject['anonymous url'])
        .attr('alt', 'Test image ' + (imageNum + 1) + ' for group ' + (groupNum + 1) + '.')
        .attr('draggable', 'false')
        .bind('dragstart', function() { return false; })
      );
      var testHash = $('<input>')
        .attr('type', 'hidden')
        .attr('id', 'group_' + groupNum + '-test_image_' + (imageNum) + '-image_hash')
        .attr('name', 'group_' + groupNum + '-test_image_' + (imageNum) + '-image_hash')
        .attr('value', imageObject['hash']);
      var questionTimeInput = $('<input>')
        .attr('type', 'hidden')
        .attr('value', '')
        .attr('id', 'group-' + groupNum + '-test_image_' + imageNum + '-time_of_selection')
        .attr('name', 'group-' + groupNum + '-test_image_' + imageNum + '-time_of_selection');
      var testSelect = $('<select>')
        .attr('id', 'group_' + groupNum + '-test_image_' + (imageNum) + '-test')
        .attr('name', 'group_' + groupNum + '-test_image_' + (imageNum) + '-test')
        .addClass('character-select')
        .one('change', function () { 
          var len = this.options.length;
          for (var i = 0; i < len; i++) {
            if (this[i].value == '-1') {
              this.remove(i);
              break;
            }
          }
        })
        .change(function () {
          questionTimeInput.attr('value', dateUTC(new Date()));
        });
      if (trainingImages.length == 1) {
        testSelect
          .append($('<option>').attr('value', '-1').append('(select yes/same ("are") or no/different ("are not"))'))
          .append($('<option>').attr('value', 'true').append('are'))
          .append($('<option>').attr('value', 'false').append('are not'));
      } else {
        testSelect
          .append($('<option>').attr('value', '-1').append('(select yes (is) or no (is not))'))
          .append($('<option>').attr('value', 'true').append('is'))
          .append($('<option>').attr('value', 'false').append('is not'));
      }
      var testConfidenceHolder = $('<label>');
      var testConfidence;
      if (Modernizr.inputtypes['range']) {
        var testConfidenceSubHolder = $('<div>').css({'display':'inline', 'textAlign':'center'});
        var testConfidenceSubSubHolder = $('<span>').addClass('bottom');
        testConfidence = $('<input>')
          .attr('id', 'group_' + groupNum + '-test_image_' + (imageNum) + '-confidence')
          .attr('name', 'group_' + groupNum + '-test_image_' + (imageNum) + '-confidence')
          .attr('type', 'range')
          .attr('min', 0)
          .attr('max', 5)
          .attr('value', 0)
          .attr('disabled', 'disabled')
          .one('change', function () { 
            $(this).attr('min', 1);
          })
          .change(function () {
            questionTimeInput.attr('value', dateUTC(new Date()));
          });
        var testConfidenceDescription = $('<span>')
          .append('(select your level of confidence on a scale of 1 to 5, using the above slider)')
          .addClass('top');
        testConfidenceSubSubHolder.append(testConfidence);
        testConfidenceSubHolder.append(testConfidenceDescription).append(testConfidenceSubSubHolder);
        testConfidenceHolder.append(testConfidenceSubHolder);
      } else {
        testConfidence = $('<select>')
          .attr('id', 'group_' + groupNum + '-test_image_' + (imageNum) + '-confidence')
          .attr('name', 'group_' + groupNum + '-test_image_' + (imageNum) + '-confidence')
          .attr('disabled', 'disabled')
          .one('change', function () { 
            var len = this.options.length;
            for (var i = 0; i < len; i++) {
              if (this[i].value == '-1') {
                this.remove(i);
                break;
              }
            }
          })
          .change(function () {
            questionTimeInput.attr('value', dateUTC(new Date()));
          })
          .append($('<option>').attr('value', '-1').append('(select your level of confidence on a scale of 1 to 5)'))
          .append($('<option>').attr('value', '1').append('randomly guessing (1)'))
          .append($('<option>').attr('value', '2').append('slightly confident (2)'))
          .append($('<option>').attr('value', '3').append('confident (3)'))
          .append($('<option>').attr('value', '4').append('very confident (4)'))
          .append($('<option>').attr('value', '5').append('absolutely sure (5)'));
        testConfidenceHolder.append(testConfidence);
      }
       
      curTest
        .append('I think that ')
        .append(testImage)
        .append(testHash);
      if (trainingImages.length == 1) {
        curTest
          .append(' and ')
          .append(trainingImage.clone())
          .append(testSelect)
          .append(' examples of the same character');
      } else {
        curTest
          .append(testSelect)
          .append(' an example of character ' + (groupNum + 1));
      }
      curTest
        .append(', and I am ')
        .append(testConfidenceHolder)
        .append(' that I am right.');
      testHolder.append(curTest);
      testHolderHolder.append(testHolder);
      testsHolder.append(testHolderHolder);
    });
    test.append(testsHolder);
    return test;
  }
  
  function makeTask(trainingImages, testImages, groupNum) {
    return $('<fieldset>')
      .append($('<legend>').append('Character ' + (groupNum + 1)))
      .append(makeTraining(trainingImages, groupNum))
      .append(makeTest(testImages, groupNum, trainingImages));
  }
  
  function makeInputs(data) {
    
    var alphabetsContainer = $('#all-tasks');
    jQuery.each(data, function(groupNum, group) {
      alphabetsContainer.append(makeTask(group['training characters'], group['test characters'], groupNum));
    });
    
    
    function fixPadding() {
      if (this.width > this.height) {
        this.height *= 75.0 / this.width;
        this.width = 75;
        //this.style.paddingBottom = this.style.paddingTop = (this.width - this.height) / 2 + _image_padding + 'px';
        //this.style.paddingRight = this.style.paddingLeft = _image_padding + 'px';
      } else if (this.height > this.width) {
        this.width *= 75.0 / this.height;
        this.height = 75;
        //this.style.paddingRight = this.style.paddingLeft = (this.height - this.width) / 2 + _image_padding + 'px';
        //this.style.paddingBottom = this.style.paddingTop = _image_padding + 'px';
      } else if (this.height && this.width) {
        this.width = 75;
        this.height = 75;
        //this.style.padding = _image_padding + 'px';
      }
      this.style.backgroundColor = 'white';
      //this.style.border = 'thin solid gray';
      doneLoading(this);
    }
    $('img').each(function () {
      //if (this.height <= 26) // Empty text?
      notYetLoaded(this);
      $(this).load(fixPadding);
    });
    doneLoading(this);
  }
  
  notYetLoaded(this);
  $(function () {
      $.getJSON("../scripts/python/characters.py", urlParameters, makeInputs);
    });
})();
