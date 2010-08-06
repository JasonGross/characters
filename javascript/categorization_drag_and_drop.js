
function makeTrainingAlphabetDroppable(dropTarget, getAlphabetNumber, setAlphabetChoice) {
  if (getAlphabetNumber === undefined) getAlphabetNumber = _defaultGetAlphabetNumber;
  if (setAlphabetChoice === undefined) setAlphabetChoice = _defaultSetAlphabetChoice;
  if (console && console.log)
    console.log($(dropTarget)[0].childNodes);
  
  $(dropTarget)
    // Highlight on drag entering drop zone.
    .bind('dragenter', function(ev) {
      var dt = ev.originalEvent.dataTransfer;
      //console.log('Drag enter: ' + dt);
      //console.log('this = ' + this);
      //console.log('target = ' + this);
      if (!eval(dt.getData("text/x-function-name"))(this) || !dt.getData("text/x-boolean-droppable"))
        return false;
      if (!this.classCount) this.classCount = {};
      if (!this.classCount['dragover'] || this.classCount['dragover'] < 0 || this == ev.target)
        this.classCount['dragover'] = 0;
      this.classCount['dragover']++;
      $(this).addClass('dragover');
      console.log('dragenter ' + (this != ev.target));
      console.log('ev.target = ' + ev.target.name);
      console.log('dragover count = ' + this.classCount['dragover']);
      console.log('');
      return this != ev.target;
    })
    
    // Un-highlight on drag leaving drop zone.
    .bind('dragleave', function(ev) {
      var dt = ev.originalEvent.dataTransfer;
      //console.log('Drag leave target:' + this);
      if (!eval(dt.getData("text/x-function-name"))(this) || !dt.getData("text/x-boolean-droppable"))
          return false;
      if (!this.classCount) this.classCount = {};
      if (!this.classCount['dragover'] || this.classCount['dragover'] < 1)
        this.classCount['dragover'] = 1;
      this.classCount['dragover']--;
      if (this.classCount['dragover'] == 0)
          $(this).removeClass('dragover');
      console.log('dragleave ' + (this != ev.target));
      console.log('ev.target = ' + ev.target.name);
      console.log('dragover count = ' + this.classCount['dragover']);
      console.log('');
      return this != ev.target;
    })
    
    // Decide whether the thing dragged in is welcome.
    .bind('dragover', function(ev) {
      var dt = ev.originalEvent.dataTransfer;
      if (eval(dt.getData("text/x-function-name"))(this)) {
        this.classCount['dragover'] = 1;
        //$(this).addClass('dragover');
      }
      return !eval(dt.getData("text/x-function-name"))(this);
    })
    
    // Handle the final drop...
    .bind('drop', function(ev) {
      var dt = ev.originalEvent.dataTransfer;
      if (!eval(dt.getData("text/x-function-name"))(this) || !dt.getData("text/x-boolean-droppable")) // ev.target
        return false;
      //console.log(setAlphabetChoice);
      this.classCount['dragover'] = 0;
      $(this).removeClass('dragover');
      setAlphabetChoice(document.getElementById(dt.getData("text/x-object-id")), getAlphabetNumber(this));
      return false;
    });

}

var _categorization_drag_and_drop_validTargetList = [];

function makeTestCharacterDraggable(image, isValidTarget, formSelect) {
  _categorization_drag_and_drop_validTargetList.push(isValidTarget);
  isValidTarget = '_categorization_drag_and_drop_validTargetList[' + 
                    (_categorization_drag_and_drop_validTargetList.length - 1) + ']';
  $(image)
   
    // Set the element as draggable.
    .attr('draggable', 'true')
    
    // Handle the start of dragging to initialize.
    .bind('dragstart', function(ev) {
      var dt = ev.originalEvent.dataTransfer;
      //alert(dt);
      //alert(dt.setData);
      dt.setData("text/x-object-id", $(formSelect).attr('id'));
      //alert(dt.getData("text/x-object-id"));
      //alert(dt);
      //alert(isValidTarget);
      //alert(dt.constructor);
      dt.setData("text/x-function-name", isValidTarget);
      dt.setData("text/x-boolean-droppable", true);
      console.log('Drag started: ' + dt);
      return true;
    })
    
    // Handle the end of dragging.
    .bind('dragend', function(ev) {
      var dt = ev.originalEvent.dataTransfer;
      dt.clearData("text/x-boolean-droppable");
      console.log('Drag ended');
      return false;
    });

}


function _defaultGetAlphabetNumber(target) {
  return parseInt($(target).attr('name').replace('alphabet-', '').replace('-col', ''));
}

function _defaultSetAlphabetChoice(select, number) {
  var len = select.options.length;
  for (var i = 0; i < len; i++) {
    if (select[i].value == number) {
      select.selectedIndex = i;
      $(select).change();
    }
  }
}
  
function makeIsValidTarget(className) {
  return function(target) { return $(target).hasClass(className); };
}
