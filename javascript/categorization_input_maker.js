(function () {
  var alphabetGlobalNum = 0;
    
  function makeBoxForImage(image) {
    var imageBox = $(document.createElement('div'))
      .addClass('image-box image-holder');
    var imageHolder = $(document.createElement('span'))
      .addClass('wraptocenter image-holder');
    imageHolder.append(image);
    imageBox.append(imageHolder);
    return imageBox;
  }
  
  function makeAlphabetQuestions(groupNum, askImages) {
    var questionCount = askImages.length;
    var curAlphabetSetQuestions;
    var curAlphabetSetQuestionSelects;
    for (var questionNum = 0; questionNum < questionCount; questionNum++) {
      var curAlphabetSetQuestion = $(document.createElement('div'))
        .attr('id', 'alphabet-group-' + groupNum + '-question-box-' + questionNum)
        .attr('name', 'alphabet-group-' + groupNum + '-question-box-' + questionNum)
        .addClass('alphabet-set alphabet-question');
      var curAlphabetSetDropDownHolder = $(document.createElement('span'))
        .attr('id', 'alphabet-group-' + groupNum + '-drop-down-holder-' + questionNum)
        .attr('name', 'alphabet-group-' + groupNum + '-drop-down-holder-' + questionNum);
      var curLabel = $(document.createElement('label'));
      var questionImageHolder = $(document.createElement('span'))
        .attr('id', 'alphabet-group-' + groupNum + '-image-holder-' + questionNum)
        .attr('name', 'alphabet-group-' + groupNum + '-image-holder-' + questionNum)
        .addClass('alphabet-group-' + groupNum + '-draggable');
      var questionImage = $(document.createElement('img'))
        .attr('id', 'alphabet-group-' + groupNum + '-image-' + questionNum)
        .attr('name', 'alphabet-group-' + groupNum + '-image-' + questionNum)
        .attr('src', '../' + askImages[questionNum])
        .attr('align', 'absmiddle')
        .attr('alt', 'Test image ' + (questionNum + 1) + ' for alphabet group ' + (groupNum + 1) + '.');
      var questionSelect = $(document.createElement('select'))
        .attr('name', 'alphabet_group_' + groupNum + '_number_test_' + questionNum)
        .attr('id', 'alphabet_group_' + groupNum + '_number_test_' + questionNum);
      var defaultOption = $(document.createElement('option'))
        .attr('id', 'default-option')
        .attr('value', -1)
        .append('(select an alphabet number)')
      var questionTimeInput = $(document.createElement('input'))
        .attr('type', 'hidden')
        .attr('value', '')
        .attr('id', 'alphabet-group-' + groupNum + '-image-' + questionNum + '-time-of-selection')
        .attr('value', '');
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
        curAlphabetSetQuestionSelects.add(questionSelect);
      else
        curAlphabetSetQuestionSelects = questionSelect;
      
      
      questionImageHolder.append(makeBoxForImage(questionImage));
      curLabel.append('I think ').append(questionImageHolder).append(' is most likely to be from alphabet ')
        .append(questionSelect).append('.');
      curAlphabetSetDropDownHolder.append(curLabel).append(questionTimeInput)
        .append($(document.createElement('input'))
            .attr('type', 'hidden')
            .attr('id', 'question_' + questionNum + '-group_' + groupNum +
              '-questionImagePath')
            .attr('value', askImages[questionNum])
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
            'dom-element': curAlphabetSetQuestions
           };
  }
  function makeAlphabetGroupClickable(alphabetNumber, curCol, questionSelects) {
    curCol.click(function () { _defaultSetAlphabetChoice(questionSelects.context, alphabetNumber); });
  }
  
  function makeTrainingTable(groupNum, alphabets, questionSelects) {
    var alphabetTableHolderHolder = $(document.createElement('div'))
      .css('text-align', 'center')
      .css('display', 'block');
    var alphabetTableHolder = $(document.createElement('div'))
      .css('text-align', 'center')
      .css('display', 'inline');
    var alphabetTable = $(document.createElement('div'))
      .attr('id', 'alphabet-table-' + groupNum)
      .attr('name', 'alphabet-table-' + groupNum)
      .addClass('table alphabet-table');
    
    var alphabetIds = alphabets.keys();
    var alphabetGroupLength = alphabetIds.length;
    var alphabet; 
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
        .append('Alphabet ' + alphabetGlobalNum);
      var curCell = $(document.createElement('div'))
        .addClass('table-cell alphabet-table-cell');
      for (var imageNum = 0; imageNum < imagesList.length; imageNum++) {
        var image = $(document.createElement('img'))
          .attr('src', '../' + imagesList[imageNum])
          .attr('alt', 'Training image ' + (imageNum + 1) + ' for alphabet ' + alphabetGlobalNum + ' in group ' + (groupNum + 1) + '.')
          .attr('draggable', 'false')
          .bind('dragstart', function() { return false; });
        curCell.append(makeBoxForImage(image))
          .append($(document.createElement('input'))
            .attr('type', 'hidden')
            .attr('id', 'alphabet_' + imageNum + '-group_' + groupNum + '-alphabetGlobalNum_' + (alphabetGlobalNum - 1) + 
              '-imagePath')
            .attr('value', imagesList[imageNum])
          );
        
      }
      
      if (questionSelects.length == 1)
        makeAlphabetGroupClickable(alphabetGlobalNum - 1, curCol, questionSelects);
      
      curCol.append(curHeader).append(curCell);
      alphabetTable.append(curCol);
      questionSelects.append($(document.createElement('option'))
        .attr('value', (alphabetGlobalNum - 1))
        .append(alphabetGlobalNum)
      );
    }
    alphabetTableHolder.append(alphabetTable);
    alphabetTableHolderHolder.append(alphabetTableHolder)
    
    return alphabetTableHolderHolder;
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
      var trainingTable = makeTrainingTable(groupNum, group['alphabets'], questionSelects);
      
      curAlphabetSetTraining.append(trainingTable);
      curAlphabetSet.append(curAlphabetSetTraining)
        .append($(document.createElement('br')))
        .append(curAlphabetSetQuestions);
      alphabetsContainer.append(curAlphabetSet);
      
      makeTrainingAlphabetDroppable('.alphabet-group-' + groupNum + '-droppable');
      
    });
    
    function fixPadding() {
      if (this.width > this.height) {
        this.width = 75;
        //this.style.paddingBottom = this.style.paddingTop = (this.width - this.height) / 2 + _image_padding + 'px';
        //this.style.paddingRight = this.style.paddingLeft = _image_padding + 'px';
      } else if (this.height > this.width) {
        this.height = 75;
        //this.style.paddingRight = this.style.paddingLeft = (this.height - this.width) / 2 + _image_padding + 'px';
        //this.style.paddingBottom = this.style.paddingTop = _image_padding + 'px';
      } else if (this.height && this.width) {
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
      $.getJSON("../scripts/python/alphabets.py", makeInputs);
    });
})();
