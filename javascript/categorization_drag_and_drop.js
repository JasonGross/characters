var a;
var makeTrainingAlphabetDroppable, makeTestCharacterDraggable;
(function () {
  var dragData = {};
  makeTrainingAlphabetDroppable = function (dropTarget, getAlphabetNumber, setAlphabetChoice) {
    if (getAlphabetNumber === undefined) getAlphabetNumber = _defaultGetAlphabetNumber;
    if (setAlphabetChoice === undefined) setAlphabetChoice = _defaultSetAlphabetChoice;

    $(dropTarget)
      // Highlight on drag entering drop zone.
      .bind('dragenter', function(ev) {
        console.log('dragenter');
        if (!(dragData['isValidDropTarget'] && dragData['isValidDropTarget'](this)) || !dragData['isDroppable']) {
	  if (dragData['lastTargetId'])
	    $('#' + dragData['lastTargetId']).removeClass('dragover');
          dragData['lastTargetId'] = undefined;
          return false;
        }
        if (dragData['lastTargetId'] && dragData['lastTargetId'] != this.id)
          $('#' + dragData['lastTargetId']).removeClass('dragover');
        $(this).addClass('dragover');
        console.log('dragenter ' + (this != ev.target));
        console.log('ev.target = ' + ev.target.id + ' (' + ev.target + ')');
        console.log(' last target = ' + dragData['lastTargetId']);
        console.log(' last event = ' + dragData['lastEventName']);
        console.log('');
        dragData['lastTargetId'] = this.id;    
        dragData['lastEventName'] = 'dragenter';
        return this != ev.target;
      })
    
      // Un-highlight on drag leaving drop zone.
      .bind('dragleave', function(ev) {
        if (!dragData['isValidDropTarget'](this) || !dragData['isDroppable']) {
          if (dragData['lastTargetId'])
            $('#' + dragData['lastTargetId']).removeClass('dragover');
	  dragData['lastTargetId'] = undefined;
	  return false;
        }
        if (dragData['lastEventName'] == 'dragleave')
          $(this).removeClass('dragover');
        console.log('dragleave ' + (this != ev.target));
        console.log('ev.target = ' + ev.target.id + ' (' + ev.target + ')');
        console.log(' last target = ' + dragData['lastTargetId']);
	console.log(' last event = ' + dragData['lastEventName']);
        console.log('');
        dragData['lastEventName'] = 'dragleave';
        return false;
      })
    
      // Decide whether the thing dragged in is welcome.
      .bind('dragover', function(ev) {
        console.log('dragover');
        if (dragData['isValidDropTarget'](this)) {
          //dragData['lastTargetId'] = this.id;
	  $(this).addClass('dragover');
        }
        return !dragData['isValidDropTarget'](this);
      })
    
      // Handle the final drop...
      .bind('drop', function(ev) {
        var dt = ev.originalEvent.dataTransfer;
        if (!dragData['isValidDropTarget'](this) || !dragData['isDroppable']) // ev.target
          return false;
        if (dragData['lastTargetId'])
          $('#' + dragData['lastTargetId']).removeClass('dragover');
        $(this).removeClass('dragover');
        setAlphabetChoice(document.getElementById(dt.getData("Text")), getAlphabetNumber(this));
        console.log('Drop');
        return false;
      });
  };

  makeTestCharacterDraggable = function (image, isValidTarget, formSelect) {
    $(image)
   
      // Set the element as draggable.
      .attr('draggable', 'true')
    
      // Handle the start of dragging to initialize.
      .bind('dragstart', function(ev) {
        var dt = ev.originalEvent.dataTransfer;
        dt.effectAllowed = 'copy';
        
        dt.setData("Text", $(formSelect).attr('id'));
        dragData['isValidDropTarget'] = isValidTarget;
        dragData['isDroppable'] = true;
        if (dt.setDragImage)
          dt.setDragImage(this, 0, 0);
        console.log('Drag started: ' + dragData);
	      return true;
      })
    
      // Handle the end of dragging.
      .bind('dragend', function(ev) {
        if (dragData['lastTargetId'])
          $('#' + dragData['lastTargetId']).removeClass('dragover');
        dragData['isDroppable'] = undefined;
        console.log('Drag ended');
        return false;
      });
  };
})();

function _defaultGetAlphabetNumber(target) {
  return parseInt($(target).attr('name').replace('alphabet-', '').replace('-col', ''));
}

function _defaultSetAlphabetChoice(select, number) {
  var len = select.options.length;
  for (var i = 0; i < len; i++) {
    if (select[i].value == number) {
      select.selectedIndex = i;
      $(select).change();
      break;
    }
  }
}
  
function makeIsValidTarget(className) {
  return function(target) { return $(target).hasClass(className); };
}
