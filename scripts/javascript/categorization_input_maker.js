function makeBoxForImage(image) {
  var imageBox = $('<div>')
    .addClass('image-box image-holder')
    .attr('id', 'image-box-for-' + image.attr('id'))
    .attr('name', 'image-box-for-' + image.attr('name'));
//  var imageInnerBox = $('<div>')
//    .addClass('image-inner-box image-holder');
  var imageHolder = $('<span>')
    .addClass('wraptocenter image-holder')
    .attr('id', 'image-holder-for-' + image.attr('id'))
    .attr('name', 'image-holder-for' + image.attr('name'));
  imageHolder.append(image);
  imageBox.append(imageHolder);
  //imageOuterBox.append(imageInnerBox);
  return imageBox;
}

(function () {
  var alphabetGlobalNum = 0;
  
  function getQuestionFromSelect(select) {
    var id = $(select).attr('id').replace(/alphabet_group_/, 'alphabet-group-').replace(/_number_test_/, '-question-');
    return $('#' + id);
  }

  function makeAlphabetQuestions(groupNum, askImages) {
    var questionCount = askImages.length;
    var curAlphabetSetQuestions;
    var curAlphabetSetQuestionSelects;
    
    for (var questionNum = 0; questionNum < questionCount; questionNum++) {
      var curAlphabetSetQuestion = $('<div>')
        .attr('id', 'alphabet-group-' + groupNum + '-question-' + questionNum)
        .addClass('alphabet-set alphabet-question');
      var curAlphabetSetDropDownHolder = $('<span>');
      var curLabel = $('<label>');
      var questionImageHolder = $('<span>')
        .addClass('alphabet-group-' + groupNum + '-draggable');
      var questionImage = $('<img>')
        .attr('id', 'alphabet-group-' + groupNum + '-image-' + questionNum)
        .attr('name', 'alphabet-group-' + groupNum + '-image-' + questionNum)
        .attr('src', (isMSIE ? askImages[questionNum]['url'] : askImages[questionNum]['data_uri']))
        .attr('align', 'absmiddle')
        .attr('alt', 'Test image ' + (questionNum + 1) + ' for alphabet group ' + (groupNum + 1) + '.');
      var questionSelect = $('<select>')
        .attr('id', 'alphabet_group_' + groupNum + '_number_test_' + questionNum)
        .attr('name', 'alphabet_group_' + groupNum + '_number_test_' + questionNum)
	      .addClass('alphabet-question');
      var defaultOption = $('<option>')
        .attr('id', 'default-option')
        .attr('value', -1)
        .append('(select an alphabet number)')
      var questionTimeInput = $('<input>')
        .attr('type', 'hidden')
        .attr('value', '')
        .attr('id', 'alphabet-group-' + groupNum + '-image-' + questionNum + '-time-of-selection')
        .attr('name', 'alphabet-group-' + groupNum + '-image-' + questionNum + '-time-of-selection');
      questionSelect.append(defaultOption)
        .one('change', function () { 
          var len = this.options.length;
          for (var i = 0; i < len; i++) {
            if (this[i].value < 0) {
              this.remove(i);
              break;
            }
          }
        })
        .change(function () {
          questionTimeInput.attr('value', dateUTC(new Date()));
        });
      
      if (curAlphabetSetQuestionSelects)
        curAlphabetSetQuestionSelects = curAlphabetSetQuestionSelects.add(questionSelect);
      else
        curAlphabetSetQuestionSelects = questionSelect;
      
      
      questionImageHolder.append(makeBoxForImage(questionImage, true));
      curLabel.append('I think ').append(questionImageHolder).append(' is most likely to be from alphabet ')
        .append(questionSelect).append('.');
      curAlphabetSetDropDownHolder.append(curLabel).append(questionTimeInput)
        .append($(document.createElement('input'))
            .attr('type', 'hidden')
            .attr('id', 'question_' + questionNum + '-group_' + groupNum + '-questionImagePath')
            .attr('name', 'question_' + questionNum + '-group_' + groupNum + '-questionImagePath')
            .attr('value', askImages[questionNum]['url'])
          );
      curAlphabetSetQuestion.append(curAlphabetSetDropDownHolder);
      if (curAlphabetSetQuestions)
        curAlphabetSetQuestions.add(curAlphabetSetQuestion);
      else
        curAlphabetSetQuestions = curAlphabetSetQuestion;
      
      makeTestCharacterDraggable(questionImage, 
        makeIsValidTarget('alphabet-group-' + groupNum + '-droppable'),
        questionSelect);
    }
    return {
            'selects': curAlphabetSetQuestionSelects,
            'dom-element': curAlphabetSetQuestions,
            'getQuestionFromSelect':getQuestionFromSelect
           };
  }
  
  function selectTargetForQuestion(target, questionSelect) {
    var alphabetNum = $(target).attr('id').replace(/alphabet-/, '').replace(/-col/, '');
    _defaultSetAlphabetChoice(questionSelect, alphabetNum);
  }

  function isTargetCurrentlySelectedForQuestion(target, questionSelect) {
    var alphabetNum = $(target).attr('id').replace(/alphabet-/, '').replace(/-col/, '');
    return questionSelect[questionSelect.selectedIndex].value == alphabetNum;
  }

  function makeTrainingTable(groupNum, alphabets, questionSelects) {
    var alphabetTableHolderHolder = $(document.createElement('div'))
      .attr('id', 'alphabet-table-holder-holder-' + groupNum)
      .attr('name', 'alphabet-table-holder-holder-' + groupNum)
      .css('text-align', 'center')
      .css('display', 'block');
    var alphabetTableHolder = $(document.createElement('div'))
      .attr('id', 'alphabet-table-holder-' + groupNum)
      .attr('name', 'alphabet-table-holder-' + groupNum)
      .css('text-align', 'center')
      .css('display', 'inline');
    var alphabetTable = $(document.createElement('div'))
      .attr('id', 'alphabet-table-' + groupNum)
      .attr('name', 'alphabet-table-' + groupNum)
      .addClass('table alphabet-table');
    
    var alphabetIds = keys(alphabets);
    var alphabetGroupLength = alphabetIds.length;
    var alphabet; 
    var cols;
    for (var alphabetNum = 0; alphabetNum < alphabetGroupLength; alphabetNum++) {
      alphabetGlobalNum++;
      alphabetId = alphabetIds[alphabetNum];
      imagesList = alphabets[alphabetId];
      var curCol = $(document.createElement('div'))
        .attr('id', 'alphabet-' + (alphabetGlobalNum - 1) + '-col')
        .attr('name', 'alphabet-' + (alphabetGlobalNum - 1) + '-col')
        .addClass('alphabet-image-holder dragoverable')
        .addClass('alphabet-group-' + groupNum + '-droppable')
        .addClass('table-col alphabet-table-col');
      var curHeader = $(document.createElement('div'))
        .addClass('table-header table-cell alphabet-table-header alphabet-table-cell')
        .attr('id', 'alphabet-header-' + (alphabetGlobalNum - 1))
        .attr('name', 'alphabet-header-' + (alphabetGlobalNum - 1))
        .append('Alphabet ' + alphabetGlobalNum);
      var curCell = $(document.createElement('div'))
        .attr('id', 'alphabet-table-cell-' + (alphabetGlobalNum - 1))
        .attr('name', 'alphabet-table-cell' + (alphabetGlobalNum - 1))
        .addClass('table-cell alphabet-table-cell');
      for (var imageNum = 0; imageNum < imagesList.length; imageNum++) {
        var image = $(document.createElement('img'))
          .attr('id', 'alphabet-' + (alphabetGlobalNum - 1) + '-image-' + imageNum)
          .attr('name', 'alphabet-' + (alphabetGlobalNum - 1) + '-image-' + imageNum)
          .attr('src', (isMSIE ? imagesList[imageNum]['url'] : imagesList[imageNum]['data_uri']))
          .attr('alt', 'Training image ' + (imageNum + 1) + ' for alphabet ' + alphabetGlobalNum + ' in group ' + (groupNum + 1) + '.')
          .attr('draggable', 'false')
          .bind('dragstart', function() { return false; });
        curCell.append(makeBoxForImage(image))
          .append($(document.createElement('input'))
            .attr('type', 'hidden')
            .attr('id', 'alphabet_' + imageNum + '-group_' + groupNum + '-alphabetGlobalNum_' + (alphabetGlobalNum - 1) + 
              '-imagePath')
            .attr('name', 'alphabet_' + imageNum + '-group_' + groupNum + '-alphabetGlobalNum_' + (alphabetGlobalNum - 1) + 
              '-imagePath')
            .attr('value', imagesList[imageNum]['url'])
          );        
      }
	
      if (cols)
        cols = cols.add(curCol);
      else
        cols = curCol;
      
      curCol.append(curHeader).append(curCell);
      alphabetTable.append(curCol);
      questionSelects.append($(document.createElement('option'))
        .attr('value', (alphabetGlobalNum - 1))
        .append(alphabetGlobalNum)
      );
    }
    alphabetTableHolder.append(alphabetTable);
    alphabetTableHolderHolder.append(alphabetTableHolder)
    
    return {
	    'dom-element':alphabetTableHolderHolder,
	    'cols':cols
	   };
  }
  
  function makeInputs(data) {
    
    var alphabetsContainer = $('#all-alphabets');
    jQuery.each(data, function(groupNum, group) {
      var curAlphabetSet = $(document.createElement('fieldset'))
        .attr('id', 'alphabet-set-' + groupNum)
        .attr('name', 'alphabet-set-' + groupNum)
        .addClass('alphabet-set')
        .append($(document.createElement('legend'))
          .append('Alphabet Group ' + (groupNum + 1))
        );
      var curAlphabetSetTraining = $(document.createElement('div'))
        .attr('id', 'alphabet-set-training' + groupNum)
        .attr('name', 'alphabet-set-training' + groupNum)
        .addClass('alphabet-set');
        
      // Making questions
      var alphabetQuestions = makeAlphabetQuestions(groupNum, group['ask_for']);
      var questionSelects = alphabetQuestions['selects'];
      var curAlphabetSetQuestions = alphabetQuestions['dom-element'];
  
      
      // Making training      
      var training = makeTrainingTable(groupNum, group['alphabets'], questionSelects);
      var trainingTable = training['dom-element'];
      var curGroupColumns = training['cols'];
      
      curAlphabetSetTraining.append(trainingTable);
      curAlphabetSet.append(curAlphabetSetTraining)
        .append($(document.createElement('br')))
        .append(curAlphabetSetQuestions);
      alphabetsContainer.append(curAlphabetSet);
      
      makeTrainingAlphabetDroppable('.alphabet-group-' + groupNum + '-droppable');
      makeAlphabetGroupClickable(groupNum, curGroupColumns, curAlphabetSetQuestions, questionSelects,	    
                                 selectTargetForQuestion, isTargetCurrentlySelectedForQuestion, getQuestionFromSelect);
      
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
      $.getJSON("../scripts/python/alphabets.py", 
        {
          'trainingCharactersPerAlphabet':getTrainingCharactersPerAlphabet(),
          'numberOfGroups':getNumberOfGroups(),
          'alphabetsPerGroup':getAlphabetsPerGroup(),
          'questionsPerGroup':getQuestionsPerGroup()
        },
        makeInputs);
    });
})();
