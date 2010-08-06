
function makeInputs(data) {
  var alphabetsContainer = $('#all-alphabets');
  var alphabetGlobalNum = 0;
  jQuery.each(data, function(groupNum, group) {
    var curAlphabetSet = $(document.createElement('div'))
      .attr('id', 'alphabet-set-' + groupNum)
      .attr('name', 'alphabet-set-' + groupNum)
      .addClass('alphabet-set');
    var curAlphabetSetTraining = $(document.createElement('div'))
      .attr('id', 'alphabet-set-training' + groupNum)
      .attr('name', 'alphabet-set-training' + groupNum)
      .addClass('alphabet-set');
      
    // Making questions
    var askImages = group['ask_for'];
    var questionCount = askImages.length;
    var curAlphabetSetQuestions;
    var curAlphabetSetQuestionSelects;
    for (var questionNum = 0; questionNum < questionCount; questionNum++) {
      var curAlphabetSetQuestion = $(document.createElement('div'))
        .attr('id', 'alphabet-group-' + groupNum + '-question-box-' + questionNum)
        .attr('name', 'alphabet-group-' + groupNum + '-question-box-' + questionNum)
        .addClass('alphabet-set alphabet-question');
      var questionCenter = $(document.createElement('center'));
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
        .attr('id', 'alphabet_group_' + groupNum + '_number_test_' + questionNum)
        .append($(document.createElement('option')).attr('value', -1).append('(select an alphabet number)'));
      if (curAlphabetSetQuestionSelects)
        curAlphabetSetQuestionSelects.add(questionSelect);
      else
        curAlphabetSetQuestionSelects = questionSelect;
      
      
      questionImageHolder.append(questionImage);
      curLabel.append('I think ').append(questionImageHolder).append(' is most likely to be from alphabet ')
        .append(questionSelect).append('.');
      curAlphabetSetDropDownHolder.append(curLabel);
      questionCenter.append(curAlphabetSetDropDownHolder);
      curAlphabetSetQuestion.append(questionCenter);
      if (curAlphabetSetQuestions)
        curAlphabetSetQuestions.add(curAlphabetSetQuestion);
      else
        curAlphabetSetQuestions = curAlphabetSetQuestion;
      
      makeTestCharacterDraggable(questionImage, 
        makeIsValidTarget('alphabet-group-' + groupNum + '-droppable'),
        questionSelect);
    }

    
    // Making training      
      
    var centerElement = $(document.createElement('center'));
    var alphabetTable = $(document.createElement('table'))
      .attr('id', 'alphabet-table-' + groupNum)
      .attr('name', 'alphabet-table-' + groupNum)
      .attr('border', 1);
    var tableHead = $(document.createElement('thead'))
    var tableHeadRow = $(document.createElement('tr'));
    var tableBody = $(document.createElement('tbody'));
    var tableMainRow = $(document.createElement('tr'));
    
    var alphabetIds = group['alphabets'].keys();
    var alphabetGroupLength = alphabetIds.length;
    var alphabet; 
    for (var alphabetNum = 0; alphabetNum < alphabetGroupLength; alphabetNum++) {
      alphabetGlobalNum++;
      alphabetId = alphabetIds[alphabetNum];
      imagesList = group['alphabets'][alphabetId];
      tableHeadRow.append($(document.createElement('th')).append('Alphabet ' + alphabetGlobalNum));
      var tableMainCell = $(document.createElement('td'));
      var imageHolder = $(document.createElement('div'))
        .attr('id', 'alphabet-' + (alphabetGlobalNum - 1) + '-col')
        .attr('name', 'alphabet-' + (alphabetGlobalNum - 1) + '-col')
        .addClass('alphabet-image-holder dragoverable')
        .addClass('alphabet-group-' + groupNum + '-droppable');
      for (var imageNum = 0; imageNum < imagesList.length; imageNum++) {
        var image = $(document.createElement('img'))
          .attr('src', '../' + imagesList[imageNum])
          .attr('alt', 'Training image ' + (imageNum + 1) + ' for alphabet ' + alphabetGlobalNum + ' in group ' + (groupNum + 1) + '.');
        imageHolder.append(image);
      }
      tableMainCell.append(imageHolder);
      tableMainRow.append(tableMainCell);
      curAlphabetSetQuestionSelects.append($(document.createElement('option'))
        .attr('value', (alphabetGlobalNum - 1))
        .append(alphabetGlobalNum)
      );
    }
    tableBody.append(tableMainRow);
    tableHead.append(tableHeadRow);
    alphabetTable.append(tableHead).append(tableBody);
    centerElement.append(alphabetTable);
    curAlphabetSetTraining.append(centerElement);
    curAlphabetSet.append(curAlphabetSetTraining)
      .append($(document.createElement('br')))
      .append(curAlphabetSetQuestions)
      .append($(document.createElement('hr')))
      .append($(document.createElement('br')))
      .append($(document.createElement('br')))
      .append($(document.createElement('br')))
      .append($(document.createElement('br')));
    alphabetsContainer.append(curAlphabetSet);
    
    makeTrainingAlphabetDroppable('.alphabet-group-' + groupNum + '-droppable');
  });
}

$(function () {
    $.getJSON("../scripts/python/alphabets.py", makeInputs);
  });
