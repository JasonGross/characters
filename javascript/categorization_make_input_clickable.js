var makeAlphabetGroupClickable;
(function () {
  makeAlphabetGroupClickable = function (groupNumber, selectionClickTargets, questionClickTargets, questionSelects, 
					 selectTargetForQuestion, isTargetCurrentlySelectedForQuestion, getQuestionFromSelect) {
    var currentlySelectedQuestionTarget = questionClickTargets.get(0);
    var selectFromTarget = {};
    questionClickTargets.each(function (index) { selectFromTarget[this] = questionSelects.get(index); });
    
    function selectionChoiceChanged() {
      selectionClickTargets.each(function (index) {
        if (isTargetCurrentlySelectedForQuestion(this, selectFromTarget[currentlySelectedQuestionTarget]))
          $(this).addClass('selected');
        else
          $(this).removeClass('selected');
      });
    }

    selectionClickTargets.mouseover(function () { $(this).addClass('mouseover-select'); });
    selectionClickTargets.mouseleave(function () { $(this).removeClass('mouseover-select'); });

    selectionClickTargets.click(function () {
      selectTargetForQuestion(this, selectFromTarget[currentlySelectedQuestionTarget]);
    });
    
    if (questionClickTargets.length > 1) {
      questionClickTargets.slice(0, 1).addClass('selected');
      questionClickTargets.addClass('dragoverable');

      function questionChanged(newQuestion) {
	$(currentlySelectedQuestionTarget).removeClass('selected');
	currentlySelectedQuestionTarget = newQuestion;
	$(currentlySelectedQuestionTarget).addClass('selected');
	selectionChoiceChanged();
      }

      questionSelects.change(function () { questionChanged($(getQuestionFromSelect(this)).get(0)); });
      
      questionClickTargets.click(questionChanged);
      questionClickTargets.mouseover(function () { $(this).addClass('mouseover-select'); });
      questionClickTargets.mouseleave(function () { $(this).removeClass('mouseover-select'); });  
    } else {
      questionSelects.change(selectionChoiceChanged);
    }
  }  
})();
